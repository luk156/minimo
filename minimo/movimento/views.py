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
from minimo.documento.forms import *
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
    print movimenti
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
def documenti(request, d_tipo):
    documenti = Documento.objects.filter(tipo=d_tipo)
    print documenti
    Documenti=[]
    f=[]
    Documenti.append(anni)
    for anno in anni:
        f.append(documenti.filter(data__year=anno))
    Documenti.append(f)
    Documenti=zip(*Documenti)
    context = {
        'request':request,
        'documenti': Documenti,
        'anni': anni,
        
        }
    return render_to_response( 'movimento/documenti.html', context, RequestContext(request))


@login_required
def nuovopagamento(request):
    azione = 'Nuovo'
    if request.method == 'POST':
        form = PagamentoaForm(request.POST)
        form.helper.form_action = reverse('minimo.documento.views.nuovopagamento')
        if form.is_valid():
            t=form.save(commit=False)
            t.user=request.user
            t.save()
            return HttpResponseRedirect(reverse('minimo.documento.views.home'))
    else:
        form = PagamentoaForm()
        form.helper.form_action = reverse('minimo.documento.views.nuovopagamento')
    return render_to_response('documento/form_pagamento.html',{'request':request,'form': form,'azione': azione,}, RequestContext(request))

@login_required
def modificapagamento(request,i_id):
    azione = 'Modifica'
    i = Pagamento.objects.get(id=i_id)
    #if i.user == request.user or request.user.is_superuser:
    if request.method == 'POST':  # If the form has been submitted...
        form = PagamentoaForm(request.POST, instance=i)  # necessario per modificare la riga preesistente
        form.helper.form_action = reverse('minimo.documento.views.modificapagamento', args=(str(i.id)))
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('minimo.documento.views.home')) # Redirect after POST
    else:
        form = PagamentoaForm(instance=i)
        form.helper.form_action = reverse('minimo.documento.views.modificapagamento', args=(str(i.id)))
    return render_to_response('documento/form_pagamento.html',{'request': request, 'form': form,'azione': azione, 'i': i}, RequestContext(request))
    #else:
    #    raise PermissionDenied

@login_required
def eliminapagamento(request,i_id):
    r = Pagamento.objects.get(id=i_id)
    r.delete()
    return HttpResponseRedirect(reverse('minimo.documento.views.home'))

    