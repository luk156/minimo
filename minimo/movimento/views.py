# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext, Context
from django.template.loader import render_to_string
from django.conf import settings
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail, EmailMessage
from django.core import serializers
from django.utils import simplejson

import webodt
import pdb
import os
from webodt.converters import converter
import datetime as dt
import csv, codecs

from minimo.documento.utils import *
from minimo.documento.models import *
from minimo.movimento.forms import *
from minimo.movimento.models import *

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


corrente = dt.datetime.today().year
precedente = corrente -1
anni=(precedente,corrente)

@login_required
def movimenti(request):
    movimenti = Movimento.objects.all()
    conto = Conto.objects.all()[0]
    Movimenti=[]
    m=[]
    Movimenti.append(anni)
    for anno in anni:
        m.append(movimenti.filter(data_movimento__year=anno))
    Movimenti.append(m)
    Movimenti=zip(*Movimenti)
    context = {
        'request':request,
        'movimenti': Movimenti,
        'anni': anni,
        'saldo': conto.saldo,
        }
    return render_to_response( 'movimento/movimenti.html', context, RequestContext(request))

@login_required
def documenti(request):
    documenti = FattureFornitore.objects.all()
    Documenti=[]
    f=[]
    Documenti.append(anni)
    for anno in anni:
        f.append(documenti.filter(data_documento__year=anno))
    Documenti.append(f)
    Documenti=zip(*Documenti)
    context = {
        'request':request,
        'documenti': Documenti,
        'anni': anni,
        }
    return render_to_response( 'movimento/documenti.html', context, RequestContext(request))


@login_required
def nuovomovimento(request):
    azione = 'Nuovo'
    conto = Conto.objects.all()[0]
    if request.method == 'POST':
        form = MovimentoForm(request.POST)
        form.helper.form_action = reverse('minimo.movimento.views.nuovomovimento')
        if form.is_valid():
            t=form.save(commit=False)
            t.conto = conto
            t.user=request.user
            t.save()
            return HttpResponseRedirect(reverse('minimo.movimento.views.movimenti'))
    else:
        form = MovimentoForm()
        form.helper.form_action = reverse('minimo.movimento.views.nuovomovimento')
    return render_to_response('movimento/form_movimento.html',{'request':request,'form': form,'azione': azione,}, RequestContext(request))


@login_required
def modificamovimento(request,i_id):
    azione = 'Modifica'
    i = Movimento.objects.get(id=i_id)
    importo_old = i.importo
    tipo_old = i.tipo
    if request.method == 'POST':  # If the form has been submitted...
        form = MovimentoForm(request.POST, instance=i)  # necessario per modificare la riga preesistente
        form.helper.form_action = reverse('minimo.movimento.views.modificamovimento', args=(str(i.id),))
        if form.is_valid():
            #riporto il saldo alla situazione precedente
            if tipo_old == 'U':
                i.conto.saldo += importo_old
            if tipo_old == 'E':
                i.conto.saldo -= importo_old
            i.conto.save()
            #salvo le modifche
            form.save()
             
            return HttpResponseRedirect(reverse('minimo.movimento.views.movimenti')) # Redirect after POST
    else:
        form = MovimentoForm(instance=i)
        form.helper.form_action = reverse('minimo.movimento.views.modificamovimento', args=(str(i.id),))
    return render_to_response('movimento/form_movimento.html',{'request': request, 'form': form,'azione': azione, 'i': i}, RequestContext(request))


@login_required
def eliminamovimento(request,i_id):
    r = Movimento.objects.get(id=i_id)
    r.delete()
    return HttpResponseRedirect(reverse('minimo.movimento.views.movimenti'))


@login_required
def nuovodocumento(request):
    azione = 'Nuovo'
    if request.method == 'POST':
        form = RegistraDocumentoForm(request.POST)
        form.helper.form_action = reverse('minimo.movimento.views.nuovodocumento')
        if form.is_valid():
            t=form.save(commit=False)
            t.user=request.user
            t.save()
            return HttpResponseRedirect(reverse('minimo.movimento.views.modificadocumento', args=(str(t.id),)))
    else:
        form = RegistraDocumentoForm()
        form.helper.form_action = reverse('minimo.movimento.views.nuovodocumento')
    return render_to_response('movimento/form_registrazione.html',{'request':request,'form': form,'azione': azione,}, RequestContext(request))


@login_required
def modificadocumento(request,t_id):
    azione = 'Modifica'
    i = FattureFornitore.objects.get(id=t_id)
    if request.method == 'POST':  # If the form has been submitted...
        form = RegistraDocumentoForm(request.POST, instance=i)  # necessario per modificare la riga preesistente
        form.helper.form_action = reverse('minimo.movimento.views.modificadocumento', args=(str(i.id),))
        if form.is_valid():
            t=form.save(commit=False)
            t.user=request.user
            t.save()
             
            return HttpResponseRedirect(reverse('minimo.movimento.views.documenti')) # Redirect after POST
    else:
        form = RegistraDocumentoForm(instance=i)
        form.helper.form_action = reverse('minimo.movimento.views.modificadocumento', args=(str(i.id),))
    return render_to_response('movimento/form_registrazione.html',{'request': request, 'form': form,'azione': azione, 'i': i}, RequestContext(request))


@login_required
def eliminadocumento(request,i_id):
    f = FattureFornitore.objects.get(id=i_id)
    try:
        m = Movimento.objects.get(documento=f)
        if tipo_old == 'U':
            m.conto.saldo += f.importo
        if tipo_old == 'E':
            m.conto.saldo -= f.importo
        i.conto.save()
        f.delete()
    except:
        f.delete()
    return HttpResponseRedirect(reverse('minimo.movimento.views.documenti'))


@login_required
def pagadocumento(request,i_id):
    f = FattureFornitore.objects.get(id=i_id)
    conto = Conto.objects.all()[0]
    movimento = Movimento(data_movimento=dt.datetime.today(), user=request.user, tipo='U')
    movimento.importo = f.importo
    movimento.descrizione = "Pagamento fattura %s del %s %s" %(f.numero, f.data_documento, f.descrizione)
    movimento.documento = f
    movimento.data_movimento = dt.datetime.today()
    movimento.save()
    f.stato = True
    f.save()
    return HttpResponseRedirect(reverse('minimo.movimento.views.documenti'))