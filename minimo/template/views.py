# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext, Context
from minimo.template.models import *
from minimo.template.forms import *
import cStringIO as StringIO
from django.template.loader import render_to_string

import os
from django.conf import settings
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail, EmailMessage


try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


@login_required
def nuovotemplate(request):
    azione = 'Nuovo'
    if request.method == 'POST':
        form = TemplateDocumentoForm(request.POST, request.FILES)
        form.helper.form_action = '/template/nuovo/'
        if form.is_valid():
            t=form.save(commit=False)
            t.user=request.user
            t.save()
            return HttpResponseRedirect('/template')
    else:
        form = TemplateDocumentoForm()
        form.helper.form_action = '/template/nuovo/'
    return render_to_response('template/form_template.html',{'request':request,'form': form,'azione': azione,}, RequestContext(request))

@login_required
def modificatemplate(request,t_id):
    azione = 'Modifica'
    f = TemplateDocumento.objects.get(id=t_id)
    #if f.user == request.user or request.user.is_superuser:
    if request.method == 'POST':  # If the form has been submitted...
        form = TemplateDocumentoForm(request.POST, request.FILES, instance=f)  # necessario per modificare la riga preesistente
        form.helper.form_action = '/template/modifica/'+str(f.id)+'/'
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/template/') # Redirect after POST
    else:
        form = TemplateDocumentoForm(instance=f)
        form.helper.form_action = '/template/modifica/'+str(f.id)+'/'
    return render_to_response('template/form_template.html',{'request': request, 'form': form,'azione': azione, 'f': f}, RequestContext(request))
    #else:
    #    raise PermissionDenied

@login_required
def eliminatemplate(request,t_id):
    template = TemplateDocumento.objects.get(id=t_id)
    #if template.user == request.user or request.user.is_superuser:  
    template.delete()
    return HttpResponseRedirect('/template')
    #else:
    #    raise PermissionDenied      

@login_required
def template(request):
    #if request.user.is_superuser:
    template=TemplateDocumento.objects.all()
    #else:
    #    template=TemplateDocumento.objects.filter(user=request.user)
    return render_to_response( 'template/template.html', {'request':request, 'templates': template, 'template_esempio':'template_standard.odt'}, RequestContext(request))

