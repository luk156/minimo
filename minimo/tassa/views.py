# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext, Context
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail, EmailMessage
from django.core import serializers
from django.utils import simplejson
from django.core.urlresolvers import reverse

import datetime as dt
from minimo.tassa.models import *
from minimo.tassa.forms import *

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

#TODO: usare url dinamici

@login_required
def nuovoimposta(request):
    azione = 'Nuovo'
    if request.method == 'POST':
        form = ImpostaForm(request.POST)
        form.helper.form_action = reverse('minimo.tassa.views.nuovoimposta') #'/tasse/imposte/nuovo/'
        if form.is_valid():
            t=form.save(commit=False)
            t.user=request.user
            t.save()
            return HttpResponseRedirect(reverse('minimo.documento.views.home'))
    else:
        form = ImpostaForm()
        form.helper.form_action = reverse('minimo.tassa.views.nuovoimposta')
    return render_to_response('tassa/form_imposta.html',{'request':request,'form': form,'azione': azione,}, RequestContext(request))

@login_required
def modificaimposta(request,i_id):
    azione = 'Modifica'
    i = Imposta.objects.get(id=i_id)
    #if i.user == request.user or request.user.is_superuser:
    if request.method == 'POST':  # If the form has been submitted...
        form = ImpostaForm(request.POST, instance=i)  # necessario per modificare la riga preesistente
        form.helper.form_action = reverse('minimo.tassa.views.modificaimposta', args=(str(i.id),)) #'/tasse/imposta/modifica/'+str(i.id)+'/'
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('minimo.documento.views.home')) # Redirect after POST
    else:
        form = ImpostaForm(instance=i)
        form.helper.form_action = reverse('minimo.tassa.views.modificaimposta', args=(str(i.id),)) #'/tasse/imposte/modifica/'+str(i.id)+'/'
    return render_to_response('tassa/form_imposta.html',{'request': request, 'form': form,'azione': azione, 'i': i}, RequestContext(request))
    #else:
    #    raise PermissionDenied

@login_required
def eliminaimposta(request,i_id):
    imposta = Imposta.objects.get(id=i_id)
    #if imposta.user == request.user or request.user.is_superuser:   
    imposta.delete()
    return HttpResponseRedirect(reverse('minimo.fattura.views.fatture'))
    #else:
    #    raise PermissionDenied  

@login_required
def nuovoritenuta(request):
    azione = 'Nuovo'
    if request.method == 'POST':
        form = RitenutaForm(request.POST)
        form.helper.form_action = reverse('minimo.tassa.views.nuovoritenuta')
        if form.is_valid():
            t=form.save(commit=False)
            t.user=request.user
            t.save()
            return HttpResponseRedirect(reverse('minimo.documento.views.home'))
    else:
        form = RitenutaForm()
        form.helper.form_action = reverse('minimo.tassa.views.nuovoritenuta')
    return render_to_response('tassa/form_ritenuta.html',{'request':request,'form': form,'azione': azione,}, RequestContext(request))

@login_required
def modificaritenuta(request,i_id):
    azione = 'Modifica'
    i = Ritenuta.objects.get(id=i_id)
    #if i.user == request.user or request.user.is_superuser:
    if request.method == 'POST':  # If the form has been submitted...
        form = RitenutaForm(request.POST, instance=i)  # necessario per modificare la riga preesistente
        form.helper.form_action = reverse('minimo.tassa.views.modificaritenuta', args=(str(i.id),))
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('minimo.documento.views.home')) # Redirect after POST
    else:
        form = RitenutaForm(instance=i)
        form.helper.form_action = reverse('minimo.tassa.views.modificaritenuta', args=(str(i.id),))
    return render_to_response('tassa/form_ritenuta.html',{'request': request, 'form': form,'azione': azione, 'i': i}, RequestContext(request))
    #else:
    #    raise PermissionDenied

@login_required
def eliminaritenuta(request,i_id):
    r = Ritenuta.objects.get(id=i_id)
    #if r.user == request.user or request.user.is_superuser: 
    r.delete()
    return HttpResponseRedirect(reverse('minimo.documento.views.home'))
    #else:
    #    raise PermissionDenied


def get_imposta(request):
    results = {}
    if request.method == "GET":       
        model_results = Imposta.objects.all()
        for x in model_results:
            results[x.nome] = x.aliquota
    json = simplejson.dumps(results)

    return HttpResponse(json, mimetype='application/json')

def get_ritenuta(request):
    results = {}
    if request.method == "GET":       
        model_results = Ritenuta.objects.all()
        for x in model_results:
            results[x.nome] = x.aliquota
    json = simplejson.dumps(results)

    return HttpResponse(json, mimetype='application/json')