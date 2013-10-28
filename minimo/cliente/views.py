# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext, Context

import webodt
import cStringIO as StringIO
from django.template.loader import render_to_string
import pdb
import os
from django.conf import settings
from django.db.models import Sum
from webodt.converters import converter
import datetime as dt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
import csv, codecs
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail, EmailMessage
from django.core import serializers
from django.utils import simplejson

from minimo.cliente.models import *
from minimo.cliente.forms import *
from minimo.documento.models import *
from minimo.utils import *

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

@login_required
def nuovocliente(request):
    azione = 'nuovo';
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            c=form.save(commit=False)
            c.user=request.user
            c.save()
            return HttpResponseRedirect(reverse('minimo.cliente.views.clienti', )) 
    else:
        form = ClienteForm()
    return render_to_response('cliente/form_cliente.html',{'request':request, 'form': form,'azione': azione}, RequestContext(request))

@login_required
def nuovoatom(request,c_id):
    azione = 'nuovo'
    c = Cliente.objects.get(id=c_id)
    if request.method == 'POST':
        form = AtomForm(request.POST)
        form.helper.form_action = reverse('minimo.cliente.views.nuovoatom', args=(str(c.id),),)
        if form.is_valid():
            data = form.cleaned_data
            a = Atom(cliente=c, riferimento=data['riferimento'], tipo=data['tipo'], valore=data['valore'], principale=False)
            a.save()
            return HttpResponseRedirect(reverse('minimo.cliente.views.cliente', args=(str(c.id),))) 
    else:
        form = AtomForm()
        form.helper.form_action = reverse('minimo.cliente.views.nuovoatom', args=(str(c.id),))
    return render_to_response('cliente/form_atom.html',{'request':request, 'form': form,'azione': azione}, RequestContext(request))


@login_required
def eliminaatom(request,a_id):
    atom = Atom.objects.get(id=a_id)
    c = atom.cliente
    atom.delete()
    return HttpResponseRedirect(reverse('minimo.cliente.views.cliente', args=(str(c.id),)))


@login_required
def modificaatom(request,a_id):
    azione = 'modifica'
    a = Atom.objects.get(id=a_id)
    c = a.cliente
    if request.method == 'POST':
        form = AtomForm(request.POST, instance=a)
        form.helper.form_action = reverse('minimo.cliente.views.modificaatom', args=(str(a.id),),)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('minimo.cliente.views.cliente', args=(str(c.id),))) 
    else:
        form = AtomForm(instance=a)
        form.helper.form_action = reverse('minimo.cliente.views.modificaatom', args=(str(a.id),))
    return render_to_response('cliente/form_atom.html',{'request':request, 'form': form,'azione': azione}, RequestContext(request))

    
@login_required
def modificacliente(request,c_id):
    azione = 'modifica'
    cliente = Cliente.objects.get(id=c_id)
    if request.method == 'POST': 
        form = ClienteForm(request.POST, instance=cliente,)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('minimo.cliente.views.clienti', )) 
    else:
        form = ClienteForm(instance=cliente)
    return render_to_response('cliente/form_cliente.html',{'request':request, 'form': form,'azione': azione, 'c': cliente,}, RequestContext(request))
    #else:
    #    raise PermissionDenied
    
@login_required
def clienti(request):
    clienti=Cliente.objects.all()
    
    return render_to_response( 'cliente/clienti.html', {'request':request, 'clienti': clienti}, RequestContext(request))

@login_required
def export_clienti(request):
    clienti=Cliente.objects.all()
    
    return export_csv(request, clienti, [('Ragione Sociale','ragione_sociale'),
        ('Indirizzo','indirizzo'),
        ('Codice Fiscale','codice_fiscale'),
        ('Partita IVA','p_iva'),
        ('Telefono','telefono'),
        ('E-Mail','mail'),
        ])

@login_required
def cliente(request,c_id):
    c= Cliente.objects.get(id=c_id)
    documenti = Documento.objects.filter(ragione_sociale=c.ragione_sociale)
    form = AtomForm()
    context = {
        'request':request,
        'form': form,
        'c': c ,
        'fa': documenti.filter(tipo='FA'),
        'pr': documenti.filter(tipo='PR'),
        'ra': documenti.filter(tipo='RA'),
        'or': documenti.filter(tipo='OR'),
        }
    return render_to_response( 'cliente/cliente.html', context, RequestContext(request))


@login_required
def eliminacliente(request,c_id):
    cliente = Cliente.objects.get(id=c_id)
    cliente.delete()
    return HttpResponseRedirect(reverse('minimo.cliente.views.clienti', ))



def get_clienti(request):
    results = []
    if request.method == "GET":
        if request.GET.has_key(u'q'):
            value = request.GET[u'q']
            if len(value) >= 1:
                model_results = Cliente.objects.filter(ragione_sociale__icontains=value)[:request.GET[u'limit']]
                for x in model_results:
                    results.append("%s" %(x.ragione_sociale))
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

