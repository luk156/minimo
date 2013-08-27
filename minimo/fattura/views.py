# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext, Context
from minimo.fattura.models import *
from minimo.fattura.forms import *
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

from minimo.fattura.utils import *

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

def export_csv(request, queryset, export_data, filter_by=None, file_name='exported_data.csv',
        object_id=None, not_available='n.a.', require_permission=None):
    '''
    Export objects from a queryset
    
    @param queryset: the queryset containing a list of objects
    @param export_data: a dictionary of the form 'path.to.data': 'Column Title'
    @param filter_by: filter the queryset by this column__condition and object_id
    @param file_name: the file name offered in the browser or a callable
    @param object_id: if file_name is callable and object_id is given, then the 
        file_name is determined by calling file_name(object_id)
    @param not_available: the default data if a given object in export_data 
        is not available
    @param require_permission: only user's havig the required permission can 
        access this view
        
    Example usage:
    'queryset': User.objects.all(),
    'filter_by': 'is_active',
    'object_id': 1,
    'export_data':  [
        ('username', 'User name'),
        ('get_full_name', 'Full name'),
        ('get_profile.some_profile_var', 'Some data'),
        ]
    '''
    if require_permission and not (request.user.is_authenticated() and 
                       request.user.has_perm(require_permission)):
        return redirect_to_login(request.path)
    queryset = queryset._clone()
    if filter_by and object_id:
        queryset = queryset.filter(**{'%s' % filter_by: object_id})
    
    def get_attr(object, attrs=None):
        if attrs == None or attrs == []:
            return object
        current = attrs.pop(0)
        try:
            return get_attr(callable(getattr(object, current)) and 
                        getattr(object, current)() or 
                        getattr(object, current), attrs)
        except (ObjectDoesNotExist, AttributeError):
            return not_available
    
    def stream_csv(data):
        sio = StringIO()
        writer = csv.writer(sio)
        writer.writerow(data)
        return sio.getvalue()
    
    def streaming_response_generator():
        yield codecs.BOM_UTF8
        yield stream_csv(zip(*export_data)[0])
        import django.db.models.query
        for item in queryset.iterator():
            
            row = []
            for attr in zip(*export_data)[1]:
                obj = get_attr(item, attr.split('.'))
                #pdb.set_trace()
                if callable(obj):
                    res = obj()
                else:
                    res = obj
                if isinstance(res, unicode) is True:
                    res = res.encode('utf-8')
                elif isinstance(res, dt.date) or isinstance(res, dt.datetime):
                    res=res.__str__()
                elif isinstance(res, django.db.models.query.QuerySet) is True:
                    elenco=''
                    for i in res:
                        elenco+=i.__unicode__()+", "
                    res=elenco
                elif isinstance(res, str) is False:
                    res = str(res)
                row.append(res)
            yield stream_csv(row)
    
    rsp = HttpResponse(streaming_response_generator(), 
                        mimetype='text/csv', 
                        content_type='text/csv; charset=utf-8')
    filename = object_id and callable(file_name) and file_name(object_id) or file_name
    rsp['Content-Disposition'] = 'attachment; filename=%s' % filename.encode('utf-8')
    return rsp


corrente = dt.datetime.today().year
precedente = corrente -1
anni=(precedente,corrente)


def home(request):
    return True

@login_required
def nuovaprestazione(request,f_id):
    azione = 'nuovo'
    f=Fattura.objects.get(id=f_id)
    if request.method == 'POST':
        form = PrestazioneForm(request.POST)
        form.helper.form_action = '/prestazioni/nuova/'+str(f.id)
        if form.is_valid():
            data = form.cleaned_data
            p=Prestazione(descrizione=data['descrizione'],importo_unitario=data['importo_unitario'], quantita=data['quantita'],fattura=f, descrizione_iva=data['descrizione_iva'])
            p.save()
            return HttpResponseRedirect('/fatture/dettagli/'+str(f.id)) 
    else:
        form = PrestazioneForm()
        form.helper.form_action = '/prestazioni/nuova/'+str(f.id)
    return render_to_response('form_prestazione.html',{'request':request, 'form': form,'azione': azione, 'f': f_id}, RequestContext(request))
 

@login_required
def modificaprestazione(request,p_id):
    azione = 'Modifica'
    prestazione = Prestazione.objects.get(id=p_id)
    f=prestazione.fattura
    if request.method == 'POST': 
        form = PrestazioneForm(request.POST, instance=prestazione,)
        form.helper.form_action = '/prestazioni/modifica/'+str(prestazione.id)+'/'
        if form.is_valid():
            data = form.cleaned_data             
            form.save()
            return HttpResponseRedirect('/fatture/dettagli/'+str(f.id)) 
    else:
        form = PrestazioneForm(instance=prestazione)
        form.helper.form_action = '/prestazioni/modifica/'+str(prestazione.id)+'/'
    return render_to_response('form_prestazione.html',{'request':request, 'form': form,'azione': azione, 'p': prestazione,}, RequestContext(request))


@login_required
def eliminaprestazione(request,p_id):
    prestazione = Prestazione.objects.get(id=p_id)
    f=prestazione.fattura
    prestazione.delete()
    return HttpResponseRedirect('/fatture/dettagli/'+str(f.id))


@login_required
def prestazioni(request):
    if request.user.is_superuser:
        prestazioni=Prestazione.objects.all()
    else:
        prestazioni=Prestazione.objects.filter(fattura_user=request.user)
    return render_to_response( 'prestazioni.html', {'request':request, 'prestazioni': prestazioni}, RequestContext(request))

@login_required
def nuovafattura(request):
    azione = 'Nuova'
    #pdb.set_trace()
    if request.method == 'POST':
        form = FatturaForm(request.POST,user_rid=request.user.id)
        form.helper.form_action = '/fatture/nuovo/'
        if form.is_valid():
            cliente = Cliente.objects.get(ragione_sociale=form.cleaned_data['ragione_sociale'])
            f=form.save(commit=False)
            f.descrizione_ritenuta = form.cleaned_data['descrizione_ritenuta']
            f.ritenuta = Ritenuta.objects.get(nome=form.cleaned_data['descrizione_ritenuta']).aliquota
            f.user=request.user
            f.save()
            form.save_m2m()
            copia_dati_fiscali(f, cliente)
            return HttpResponseRedirect('/fatture/dettagli/'+str(f.id))
    else:
        form = FatturaForm(user_rid=request.user.id)
        form.helper.form_action = '/fatture/nuovo/'
    return render_to_response('form_fattura.html',{'request':request,'form': form,'azione': azione,}, RequestContext(request))

@login_required
def modificafattura(request,f_id):
    azione = 'Modifica'
    f = Fattura.objects.get(id=f_id)
    if request.method == 'POST':  # If the form has been submitted...
        form = FatturaForm(request.POST, instance=f)  # necessario per modificare la riga preesistente
        form.helper.form_action = '/fatture/modifica/'+str(f.id)+'/'
        if form.is_valid():
            cliente = Cliente.objects.get(ragione_sociale=form.cleaned_data['ragione_sociale'])
            f=form.save(commit=False)
            
            f.descrizione_ritenuta = form.cleaned_data['descrizione_ritenuta']
            try:
                f.ritenuta = Ritenuta.objects.get(nome=form.cleaned_data['descrizione_ritenuta']).aliquota
            except DoesNotExist:
                pass
            #f.ritenuta = Ritenuta.objects.get(nome=form.cleaned_data['descrizione_ritenuta']).aliquota
            f.save()
            form.save_m2m()
            copia_dati_fiscali(f, cliente)
            return HttpResponseRedirect('/fatture/dettagli/'+str(f.id)) # Redirect after POST
    else:
        form = FatturaForm(instance=f)
        form.helper.form_action = '/fatture/modifica/'+str(f.id)+'/'
    return render_to_response('form_fattura.html',{'request': request, 'form': form,'azione': azione, 'f': f}, RequestContext(request))
   

@login_required    
def sblocca_fattura(request, f_id):
    azione = 'i'
    f = Fattura.objects.get(id=f_id)
    f.stato = False
    f.save()
    return HttpResponseRedirect('/fatture/dettagli/'+str(f.id))



@login_required    
def incassa_fattura(request, f_id):
    azione = 'i'
    f = Fattura.objects.get(id=f_id)
    f.stato = True
    f.save()
    return HttpResponseRedirect('/fatture/dettagli/'+str(f.id))


    
@login_required
def eliminafattura(request,f_id):
    fattura = Fattura.objects.get(id=f_id)
    fattura.delete()
    return HttpResponseRedirect('/fatture')


@login_required
def fatture(request):
    fatture = Fattura.objects.all()
    imposte = Imposta.objects.all()
    ritenute = Ritenuta.objects.all()
    pagamenti = Pagamento.objects.all()
    
    Fatture=[]
    f=[]
    Fatture.append(anni)
    for anno in anni:
        f.append(fatture.filter(data__year=anno))
    Fatture.append(f)
    Fatture=zip(*Fatture)
    return render_to_response( 'fatture.html', {'request':request, 'pagamenti': pagamenti, 'ritenute': ritenute ,'fatture': Fatture, 'anni': anni, 'imposte':imposte}, RequestContext(request))


@login_required
def export_fatture(request):
    #if request.user.is_superuser:
     #   fatture=Fattura.objects.all()
    #else:
     #   fatture=Fattura.objects.filter(fattura_user=request.user)
    fatture=Fattura.objects.all()
    # Create the HttpResponse object with the appropriate CSV header
    if settings.TIPO_FATTURA=="standard":
        return export_csv(request, fatture, [('Data','data'),
        ('Cliente','ragione_sociale'),
        ('Via', 'via'),
        ('Cap', 'cap'),
        ('Città', 'citta'),
        ('Provincia', 'provincia'),
        ('Aliquota IVA','IVA'),
        ('Pagata','stato_pagamento'),
        ('Prestazioni','prestazione_fattura.all'),
        ('Imponibile','imponibile'),
        ('IVA','iva'),
        ('Totale','totale'),
        ])
    elif settings.TIPO_FATTURA=="minimo":
        return export_csv(request, fatture, [('Data','data'),
        ('Cliente','cliente'),
        ('Stato','stato'),
        ('ID Bollo','bollo'),
        ('Valore Bollo','valore_bollo'),
        ('Imponibile','imponibile'),
        ('Rivalsa INPS','rivalsa'),
        ('Totale','totale'),
        ])

@login_required
def fattura(request, f_id):
    f=Fattura.objects.get(id=f_id)
    form_prestazione = PrestazioneForm()
    if f.user == request.user or request.user.is_superuser:
        return render_to_response( 'fattura.html', {'request':request, 'f': f,'form':form_prestazione }, RequestContext(request))
    else:
        raise PermissionDenied      

@login_required
def stampa_fattura(request,f_id):
    f=Fattura.objects.get(id=f_id)
    #if f.user == request.user or request.user.is_superuser:
    #pdb.set_trace()
    #f.template
    template = webodt.ODFTemplate(f.template.template.name)
    context = dict(
        data=str(f.data),
        fattura=f,
        )

    document = template.render(Context(context))
    conv = converter()
    pdf = conv.convert(document, format='pdf')
    #return render_to_response( 'modello_fattura.html', {'request':request, 'f': f})
    response = HttpResponse(pdf, mimetype='application/pdf')
    if f.tipo == 'RA':
        response['Content-Disposition'] = 'attachment; filename=RitenutaAcconto-%s-%s.pdf' % (f.progressivo(),f.data.year)
    if f.tipo == 'FA':
        response['Content-Disposition'] = 'attachment; filename=Fattura-%s-%s.pdf' % (f.progressivo(),f.data.year)
    return response
    #else:
    #    raise PermissionDenied      

@login_required
def invio_fattura(request,f_id):
    f=Fattura.objects.get(id=f_id)
    azione = 'Invio'
    data = {
        'mittente' : f.user.email,
        'destinatario' : f.cliente.mail,
    }
   
    if request.method == 'POST': 
        form = FatturaInvioForm(request.POST, data,)
        #form.helper.form_action = 'fatture/invio/'+ str(f.id)+'/'
        if form.is_valid():
            oggetto = form.cleaned_data['oggetto']
            corpo = form.cleaned_data['messaggio']
            cc = [form.cleaned_data['cc_destinatario']]
            to = [form.cleaned_data['destinatario']]
            print to, cc
            email = EmailMessage(oggetto, corpo, form.cleaned_data['mittente'],
                to,cc,
                headers = {'Reply-To': form.cleaned_data['mittente']})
            template = webodt.ODFTemplate(f.template.template.name)
            context = dict(
                data=str(f.data),
                fattura=f,
                )
    
            document = template.render(Context(context))
            conv = converter()
            pdf = conv.convert(document, format='pdf')
            email.attach_file(pdf.name)
            return HttpResponseRedirect('/fatture/dettagli/'+str(f.id)) 
    else:
        form = FatturaInvioForm(data)
        #form.helper.form_action = '/'
    return render_to_response('InvioFattura.html',{'request':request, 'form':form, }, RequestContext(request))
    

@login_required
def bilancio(request):

    form=IntervalloForm()
    if request.method == 'POST':  # If the form has been submitted...
        form = IntervalloForm(request.POST) 
    anno=dt.datetime.today().year
    fatturato=bilancio_intervallo(request,dt.date(anno,1,1),dt.datetime.now().date())
    
    return render_to_response( 'bilancio.html', {'request':request, 'fatturato': fatturato,'form':form, }, RequestContext(request))

@login_required
def bilancio_intervallo(request, inizio, fine):
    #if request.user.is_superuser:
    #    fatture=Fattura.objects.filter(data__gte=inizio,data__lte=fine)
    #else:
    #    fatture=Fattura.objects.filter(data__gte=inizio,data__lte=fine,user=request.user)
    fatture=Fattura.objects.filter(data__gte=inizio,data__lte=fine)
    f_data=[]
    f_tot=[]
    fatturato=[]
    data_precedente=dt.date(1,1,1)

    for f in fatture:
        if f.data == data_precedente:
            f_tot[-1]+=f.totale()
        else:
            f_data.append(f.data)
            f_tot.append(f.totale())
        data_precedente = f.data
    
    fatturato.append(f_data)
    fatturato.append(f_tot)
    fatturato=zip(*fatturato)

    return fatturato



@login_required
def nuovopagamento(request):
    azione = 'Nuovo'
    if request.method == 'POST':
        form = PagamentoaForm(request.POST)
        form.helper.form_action = '/pagamenti/nuovo/'
        if form.is_valid():
            t=form.save(commit=False)
            t.user=request.user
            t.save()
            return HttpResponseRedirect('/fatture')
    else:
        form = PagamentoaForm()
        form.helper.form_action = '/pagamenti/nuovo/'
    return render_to_response('form_pagamento.html',{'request':request,'form': form,'azione': azione,}, RequestContext(request))

@login_required
def modificapagamento(request,i_id):
    azione = 'Modifica'
    i = Pagamento.objects.get(id=i_id)
    #if i.user == request.user or request.user.is_superuser:
    if request.method == 'POST':  # If the form has been submitted...
        form = PagamentoaForm(request.POST, instance=i)  # necessario per modificare la riga preesistente
        form.helper.form_action = '/pagamenti/modifica/'+str(i.id)+'/'
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/fatture') # Redirect after POST
    else:
        form = PagamentoaForm(instance=i)
        form.helper.form_action = '/pagamenti/modifica/'+str(i.id)+'/'
    return render_to_response('form_pagamento.html',{'request': request, 'form': form,'azione': azione, 'i': i}, RequestContext(request))
    #else:
    #    raise PermissionDenied

@login_required
def eliminapagamento(request,i_id):
    r = Pagamento.objects.get(id=i_id)
    #if r.user == request.user or request.user.is_superuser: 
    r.delete()
    return HttpResponseRedirect('/fatture')
    #else:
    #    raise PermissionDenied
    