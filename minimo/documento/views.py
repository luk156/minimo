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
from minimo.tassa.models import *
from minimo.movimento.models import *

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

@login_required
def home(request):
    documenti = Documento.objects.all()
    imposte = Imposta.objects.all()
    ritenute = Ritenuta.objects.all()
    pagamenti = Pagamento.objects.all()
    print 'home'
    Documenti=[]
    f=[]
    Documenti.append(anni)
    for anno in anni:
        f.append(documenti.filter(data__year=anno))
    Documenti.append(f)
    Documenti=zip(*Documenti)
    return render_to_response( 'documento/documenti.html', {'request':request, 'pagamenti': pagamenti, 'ritenute': ritenute ,'documenti': Documenti, 'anni': anni, 'imposte':imposte}, RequestContext(request))


@login_required
def nuovariga(request,f_id):
    azione = 'nuovo'
    f=Documento.objects.get(id=f_id)
    if request.method == 'POST':
        form = RigaForm(request.POST)
        form.helper.form_action = reverse('minimo.documento.views.nuovariga', args=(str(f.id),),)
        if form.is_valid():
            data = form.cleaned_data
            print '--', data['descrizione_imposta']
            r=Riga(descrizione=data['descrizione'],importo_unitario=data['importo_unitario'], quantita=data['quantita'],documento=f, descrizione_imposta=data['descrizione_imposta'])
            r.save()
            return HttpResponseRedirect(reverse('minimo.documento.views.dettagli_documento', args=(str(f.id),))) 
    else:
        form = RigaForm()
        form.helper.form_action = reverse('minimo.documento.views.nuovariga', args=(str(f.id),))
    return render_to_response('documento/form_riga.html',{'request':request, 'form': form,'azione': azione, 'f': f_id}, RequestContext(request))
 

@login_required
def modificariga(request,p_id):
    azione = 'Modifica'
    riga = Riga.objects.get(id=p_id)
    f=riga.documento
    if request.method == 'POST': 
        form = RigaForm(request.POST, instance=riga,)
        form.helper.form_action = reverse('minimo.documento.views.modificariga', args=(str(riga.id),),)
        if form.is_valid():
            data = form.cleaned_data             
            form.save()
            return HttpResponseRedirect(reverse('minimo.documento.views.dettagli_documento', args=(str(f.id),))) 
    else:
        form = RigaForm(instance=riga)
        form.helper.form_action = reverse('minimo.documento.views.modificariga', args=(str(riga.id),))
    return render_to_response('documento/form_riga.html',{'request':request, 'form': form,'azione': azione, 'p': riga,}, RequestContext(request))


@login_required
def eliminariga(request,p_id):
    riga = Riga.objects.get(id=p_id)
    d=riga.documento.id
   
    riga.delete()
    return HttpResponseRedirect(reverse('minimo.documento.views.dettagli_documento', args=(d,)))


@login_required
def righe(request):
    righe=Riga.objects.all()
    return render_to_response( 'righe.html', {'request':request, 'righe': righe}, RequestContext(request))

#TODO: passare come parametro il tipo di documento da creare
@login_required
def nuovodocumento(request):
    azione = 'Nuovo'
    if request.method == 'POST':
        form = DocumentoForm(request.POST)
        form.helper.form_action = reverse('minimo.documento.views.nuovodocumento')
        if form.is_valid():
            cliente = Cliente.objects.get(ragione_sociale=form.cleaned_data['ragione_sociale'])
            f=form.save(commit=False)
            try:
                f.descrizione_ritenuta = form.cleaned_data['descrizione_ritenuta']
                f.ritenuta = Ritenuta.objects.get(nome=form.cleaned_data['descrizione_ritenuta']).aliquota
            except Exception:
                pass
            f.user=request.user
            f.save()
            print f
            copia_dati_fiscali(f, cliente)
            return HttpResponseRedirect(reverse('minimo.documento.views.dettagli_documento', args=(str(f.id),),))
    else:
        form = DocumentoForm()
        form.helper.form_action = reverse('minimo.documento.views.nuovodocumento')
    return render_to_response('documento/form_documento.html',{'request':request,'form': form,'azione': azione,}, RequestContext(request))


@login_required
def modificadocumento(request,f_id):
    azione = 'Modifica'
    f = Documento.objects.get(id=f_id)
    if request.method == 'POST':  # If the form has been submitted...
        form = DocumentoForm(request.POST, instance=f)  # necessario per modificare la riga preesistente
        form.helper.form_action = reverse('minimo.documento.views.modificadocumento', args=(str(f.id),))
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
            copia_dati_fiscali(f, cliente)
            return HttpResponseRedirect(reverse('minimo.documento.views.dettagli_documento', args=(str(f.id),))) # Redirect after POST
    else:
        form = DocumentoForm(instance=f)
        form.helper.form_action = reverse('minimo.documento.views.modificadocumento', args=(str(f.id),))
    return render_to_response('documento/form_documento.html',{'request': request, 'form': form,'azione': azione, 'f': f}, RequestContext(request))
   

@login_required    
def sblocca_documento(request, d_id):
    azione = 'sblocca'
    d = Documento.objects.get(id=d_id)
    d.stato = False
    d.save()
    movimento = Movimento(data_movimento=dt.datetime.today(), user=request.user, tipo='U')
    movimento.importo = d.totale
    if d.importo_residuo:
        movimento.importo = d.totale - d.importo_residuo
        movimento.descrizione = "Storno incasso parziale fattura %s del %s cliente %s per errato incasso" %(d, d.data, d.cliente)
    else:
        movimento.importo = d.totale
        movimento.descrizione = "Storno fattura %s del %s cliente %s per errato incasso" %(d, d.data, d.cliente)
    movimento.documento = d
    movimento.data_movimento = dt.datetime.today()
    d.importo_residuo = 0
    d.save()
    movimento.save()
    return HttpResponseRedirect(reverse('minimo.documento.views.dettagli_documento', args=(str(d.id),)))



@login_required    
def incassa_documento(request, d_id):
    azione = 'incassa'
    d = Documento.objects.get(id=d_id)
    d.stato = True
    d.save()
    movimento = Movimento(data_movimento=dt.datetime.today(), user=request.user, tipo='E')
    if d.importo_residuo:
        movimento.importo = d.importo_residuo
        movimento.descrizione = "Incasso residuo fattura %s del %s cliente %s" %(d, d.data, d.cliente)
    else:
        movimento.importo = d.totale
        movimento.descrizione = "Incasso fattura %s del %s cliente %s" %(d, d.data, d.cliente)
    movimento.documento = d
    movimento.data_movimento = dt.datetime.today()
    d.importo_residuo = 0
    d.save()
    movimento.save()
    return HttpResponseRedirect(reverse('minimo.documento.views.dettagli_documento', args=(str(d.id),)))

#TODO: controllare se l'importo incassato è minore del residuo e ritornare 
def incassa_parziale_documento(request, d_id):

    d = Documento.objects.get(id=d_id)
    azione = 'Incassa parzialmente doumento %s' %d
    residuo = 0.0
    if d.importo_residuo:
        residuo = d.residuo
    else:
        residuo = d.totale
    if request.method == 'POST':  # If the form has been submitted...
        form = IncassaForm(request.POST)  # necessario per modificare la riga preesistente
        form.helper.form_action = reverse('minimo.documento.views.incassa_parziale_documento', args=(str(d.id)))
        if form.is_valid():
            movimento = Movimento(data_movimento=dt.datetime.today(), user=request.user, tipo='E')
            movimento.importo = form.cleaned_data['importo']
            movimento.documento = d
            movimento.descrizione = "Incasso parziale fattura %s del %s cliente %s" %(d, d.data, d.cliente)
            movimento.data_movimento = dt.datetime.today()
            if d.importo_residuo:
                d.importo_residuo -= form.cleaned_data['importo']
            else:
                d.importo_residuo = d.totale - form.cleaned_data['importo']
            d.save()
            movimento.save()
            return HttpResponseRedirect(reverse('minimo.documento.views.dettagli_documento', args=(str(d.id),))) # Redirect after POST
    else:
        form = IncassaForm()
        form.helper.form_action = reverse('minimo.documento.views.incassa_parziale_documento', args=(str(d.id)))
    return render_to_response('documento/form_incassa.html',{'request': request, 'form': form,'azione': azione, 'residuo': residuo}, RequestContext(request))

    
@login_required
def eliminadocumento(request,d_id):
    documento = Documento.objects.get(id=d_id)
    tipo = documento.tipo
    documento.delete()
    return HttpResponseRedirect(reverse('minimo.documento.views.home'))

@login_required
def dettagli_documento(request, d_num):
    d = Documento.objects.get(id=d_num)
    form_riga = RigaForm()
    return render_to_response( 'documento/documento.html', {'request':request, 'f': d,'form':form_riga }, RequestContext(request))
     


@login_required
def documenti(request, d_tipo):
    documenti = Documento.objects.filter(tipo=d_tipo)
    imposte = Imposta.objects.all()
    ritenute = Ritenuta.objects.all()
    pagamenti = Pagamento.objects.all()
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
        'pagamenti': pagamenti,
        'ritenute': ritenute ,
        'documenti': Documenti,
        'anni': anni,
        'imposte':imposte,
        'filtro': d_tipo
        }
    return render_to_response( 'documento/documenti.html', context, RequestContext(request))


@login_required
def esportadocumenti(request, d_tipo):
    if d_tipo != 'ALL':
        documenti=Documento.objects.filter(tipo=d_tipo)
    else:
        documenti=Documento.objects.all()
    return export_csv(request, documenti, [
    ('Tipo documento', 'tipo_documento'),
    ('Data','data'),
    ('Data consegna', 'data_consegna'),
    ('Cliente','ragione_sociale'),
    ('Via', 'via'),
    ('Cap', 'cap'),
    ('Città', 'citta'),
    ('Provincia', 'provincia'),
    ('Pagata','stato_pagamento'),
    ('Metodo pagamento','pagamento'),
    ('Prestazioni','righe'),
    ('Imponibile','imponibile'),
    ('IVA','imposta_totale'),
    ('Desc ritenuta','descrizione_ritenuta'),
    ('Aliquota ritenuta','ritenuta'),
    ('Ritenuta totale','tot_ritenute'),
    ('Totale','totale'),
    ('Sconto', 'sconto'),
    ('Note', 'note'),
    ('Documento di riferimento', 'riferimento'),
    
    ])


@login_required
def fattura_documento(request,d_id):
    preventivo = Documento.objects.get(id=d_id)
    fattura = Documento.objects.get(id=d_id)
    fattura.id = None
    fattura.save()
    if fattura.ritenuta:
        fattura.tipo = 'RA'
    else:
        fattura.tipo = 'FA'
    fattura.riferimento = preventivo
    fattura.data = dt.datetime.today()
    fattura.numero = 0
    fattura.save()
    for riga in preventivo.righe:
        riga.id = None
        riga.documento = fattura
        riga.save()
    preventivo.riferimento = fattura
    preventivo.save()
    return HttpResponseRedirect(reverse('minimo.documento.views.dettagli_documento', args=(str(fattura.id),))) 
    
@login_required
def stampa_documento(request,f_id):
    f = Documento.objects.get(id=f_id)

    template = webodt.ODFTemplate(f.template.template.name)
    context = dict(
        data=str(f.data),
        fattura=f,
        )

    document = template.render(Context(context))
    conv = converter()
    pdf = conv.convert(document, format='pdf')
    #return render_to_response( 'modello_documento.html', {'request':request, 'f': f})
    response = HttpResponse(pdf, mimetype='application/pdf')
    if f.tipo == 'RA':
        response['Content-Disposition'] = 'attachment; filename=RitenutaAcconto-%s-%s.pdf' % (f.progressivo(),f.data.year)
    if f.tipo == 'FA':
        response['Content-Disposition'] = 'attachment; filename=Fattura-%s-%s.pdf' % (f.progressivo(),f.data.year)
    if f.tipo == 'PR':
        response['Content-Disposition'] = 'attachment; filename=Offerta-%s-%s.pdf' % (f.progressivo(),f.data.year)
    if f.tipo == 'OR':
        response['Content-Disposition'] = 'attachment; filename=Ordine-%s-%s.pdf' % (f.progressivo(),f.data.year)
    return response


@login_required
def invio_documento(request,f_id):
    f = Documento.objects.get(id=f_id)
    azione = 'Invio'
    data = {
        'mittente' : f.user.email,
        'destinatario' : f.cliente.mail,
    }
   
    if request.method == 'POST': 
        form = FatturaInvioForm(request.POST, data,)
        #form.helper.form_action = 'documenti/invio/'+ str(f.id)+'/'
        if form.is_valid():
            oggetto = form.cleaned_data['oggetto']
            corpo = form.cleaned_data['messaggio']
            cc = [form.cleaned_data['cc_destinatario']]
            to = [form.cleaned_data['destinatario']]
            email = EmailMessage(oggetto, corpo, form.cleaned_data['mittente'],
                to,cc,
                headers = {'Reply-To': form.cleaned_data['mittente']})
            template = webodt.ODFTemplate(f.template.template.name)
            context = dict(
                data=str(f.data),
                documento=f,
                )
    
            document = template.render(Context(context))
            conv = converter()
            pdf = conv.convert(document, format='pdf')
            email.attach_file(pdf.name)
            return HttpResponseRedirect(reverse('minimo.documento.views.documento', args=(str(f.id)))) 
    else:
        form = FatturaInvioForm(data)
        #form.helper.form_action = '/'
    return render_to_response('documento/InvioDocumento.html',{'request':request, 'form':form, }, RequestContext(request))
    

@login_required
def bilancio(request):

    form=IntervalloForm()
    if request.method == 'POST':  # If the form has been submitted...
        form = IntervalloForm(request.POST) 
    anno = dt.datetime.today().year
    fatt = bilancio_intervallo(request,dt.date(anno,1,1),dt.datetime.now().date())
    doc = fatturato(request,dt.date(anno,1,1),dt.date(anno,12,31))
    prev = preventivato(request,dt.date(anno,1,1),dt.date(anno,12,31))
    return render_to_response( 'documento/bilancio.html', {'request':request, 'documenti': fatt,'form':form, 'dati': doc, 'prev': prev, 'anno': anno}, RequestContext(request))

class fatturato():
    
    def __init__(self,request, inizio, fine):
        self.documenti=Documento.objects.filter(data__gte=inizio,data__lte=fine, tipo__in=['RA', 'FA'],)
    
    def iva(self):
        totale = 0
        for f in self.documenti:
            if f.tipo == 'FA' and f.stato:
                totale += f.imposta_totale
        return totale
    
    def ritenute(self):    
        totale = 0
        for f in self.documenti:
            if f.tipo == 'RA' and f.stato:
                totale += f.tot_ritenute
        return totale
    
    def totale(self):
        totale = 0
        for f in self.documenti:
            totale += f.totale
        return totale
    
    def incassato(self):
        totale = 0
        for f in self.documenti:
            if f.stato:
                totale += f.totale
        return totale
    
    def incassare(self):
        totale = 0
        for f in self.documenti:
            if not f.stato:
                totale += f.totale
        return totale
    
    def scadute(self):
        totale = 0
        for f in self.documenti:
            if f.scaduto:
                totale += f.totale
        return totale

    def sbilancio(self):
        return self.totale() - self.incassare()
    
class preventivato():
    def __init__(self,request, inizio, fine):
        self.documenti=Documento.objects.filter(data__gte=inizio,data__lte=fine, tipo__in=['PR', 'OR'],)
        
    def tot_preventivi(self):
        totale = 0
        for f in self.documenti.filter(tipo='PR'):
            totale += f.totale
        return totale
    
    def tot_ordino(self):
        totale = 0
        for f in self.documenti.filter(tipo='OR'):
            totale += f.totale
        return totale
    
    def num_preventivi(self):
        return self.documenti.filter(tipo='PR').count()
    
    def num_ordini(self):
        return self.documenti.filter(tipo='OR').count()
    
    def doc_fatturati(self):
        return self.documenti.filter(riferimento__isnull=False).count()
    

    def sbilancio(self):
        return self.totale() - self.incassare()
    


@login_required
def bilancio_intervallo(request, inizio, fine):
    docs=Documento.objects.filter(data__gte=inizio,data__lte=fine, tipo__in=['RA', 'FA'],)
    f_data=[]
    f_tot=[]
    documenti=[]
    data_precedente=dt.date(1,1,1)

    for f in docs:
        if f.data == data_precedente:
            f_tot[-1]+=f.totale
        else:
            f_data.append(f.data)
            f_tot.append(f.totale)
        data_precedente = f.data
    
    documenti.append(f_data)
    documenti.append(f_tot)
    documenti=zip(*documenti)

    return documenti



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

    