
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext, Context
from fattura.models import *
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



anni=(2012,2013)


def home(request):
	return True

@login_required
def nuovocliente(request):
	azione = 'nuovo';
	if request.method == 'POST':
		form = ClienteForm(request.POST)
		if form.is_valid():
			c=form.save(commit=False)
			c.user=request.user
			c.save()
			return HttpResponseRedirect('/clienti') 
	else:
		form = ClienteForm()
	return render_to_response('form_cliente.html',{'request':request, 'form': form,'azione': azione}, RequestContext(request))

@login_required
def modificacliente(request,c_id):
	azione = 'modifica'
	cliente = Cliente.objects.get(id=c_id)
	if cliente.user == request.user or request.user.is_superuser:
		if request.method == 'POST': 
			form = ClienteForm(request.POST, instance=cliente,)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/clienti') 
		else:
			form = ClienteForm(instance=cliente)
		return render_to_response('form_cliente.html',{'request':request, 'form': form,'azione': azione, 'c': cliente,}, RequestContext(request))
	else:
		raise PermissionDenied

@login_required
def clienti(request):
	if request.user.is_superuser:
		clienti=Cliente.objects.all()
	else:
		clienti=Cliente.objects.filter(user=request.user)
	return render_to_response( 'clienti.html', {'request':request, 'clienti': clienti}, RequestContext(request))

@login_required
def export_clienti(request):
	if request.user.is_superuser:
		clienti=Cliente.objects.all()
	else:
		clienti=Cliente.objects.filter(user=request.user)	
    # Create the HttpResponse object with the appropriate CSV header
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
	if c.user == request.user or request.user.is_superuser:
		return render_to_response( 'cliente.html', {'request':request, 'c':c , 'f': Fattura.objects.filter(cliente=c)}, RequestContext(request))
	else:
		raise PermissionDenied

@login_required
def eliminacliente(request,c_id):
	cliente = Cliente.objects.get(id=c_id)
	if cliente.user == request.user or request.user.is_superuser:
		cliente.delete()
		return HttpResponseRedirect('/clienti')
	else:
		raise PermissionDenied

@login_required
def nuovaprestazione(request,f_id):
	azione = 'nuovo'
	f=Fattura.objects.get(id=f_id)
	if f.user == request.user or request.user.is_superuser:
		if request.method == 'POST':
			form = PrestazioneForm(request.POST)
			form.helper.form_action = '/prestazioni/nuova/'+str(f.id)
			if form.is_valid():
				data = form.cleaned_data
				p=Prestazione(descrizione=data['descrizione'],importo=data['importo'],fattura=f)
				p.save()
				return HttpResponseRedirect('/fatture/dettagli/'+str(f.id)) 
		else:
			form = PrestazioneForm()
			form.helper.form_action = '/prestazioni/nuova/'+str(f.id)
		return render_to_response('form_prestazione.html',{'request':request, 'form': form,'azione': azione, 'f': f_id}, RequestContext(request))
	else:
		raise PermissionDenied

@login_required
def modificaprestazione(request,p_id):
	azione = 'Modifica'
	prestazione = Prestazione.objects.get(id=p_id)
	f=prestazione.fattura
	if f.user == request.user or request.user.is_superuser:
		if request.method == 'POST': 
			form = PrestazioneForm(request.POST, instance=prestazione,)
			form.helper.form_action = '/prestazioni/modifica/'+str(prestazione.id)+'/'
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/fatture/dettagli/'+str(f.id)) 
		else:
			form = PrestazioneForm(instance=prestazione)
			form.helper.form_action = '/prestazioni/modifica/'+str(prestazione.id)+'/'
		return render_to_response('form_prestazione.html',{'request':request, 'form': form,'azione': azione, 'p': prestazione,}, RequestContext(request))
	else:
		raise PermissionDenied

@login_required
def eliminaprestazione(request,p_id):
	prestazione = Prestazione.objects.get(id=p_id)
	f=prestazione.fattura
	if f.user == request.user or request.user.is_superuser:
		prestazione.delete()
		return HttpResponseRedirect('/fatture/dettagli/'+str(f.id))
	else:
		raise PermissionDenied

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
			f=form.save(commit=False)
			f.user=request.user
			f.save()
			return HttpResponseRedirect('/fatture/dettagli/'+str(f.id))
	else:
		form = FatturaForm(user_rid=request.user.id)
		form.helper.form_action = '/fatture/nuovo/'
	return render_to_response('form_fattura.html',{'request':request,'form': form,'azione': azione,}, RequestContext(request))

@login_required
def modificafattura(request,f_id):
	azione = 'Modifica'
	f = Fattura.objects.get(id=f_id)
	if f.user == request.user or request.user.is_superuser:
		if request.method == 'POST':  # If the form has been submitted...
			form = FatturaForm(request.POST, instance=f, user_rid=request.user.id)  # necessario per modificare la riga preesistente
			form.helper.form_action = '/fatture/modifica/'+str(f.id)+'/'
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/fatture/dettagli/'+str(f.id)) # Redirect after POST
		else:
			form = FatturaForm(instance=f,user_rid=request.user.id)
			form.helper.form_action = '/fatture/modifica/'+str(f.id)+'/'
		return render_to_response('form_fattura.html',{'request': request, 'form': form,'azione': azione, 'f': f}, RequestContext(request))
	else:
		raise PermissionDenied

@login_required
def eliminafattura(request,f_id):
	fattura = Fattura.objects.get(id=f_id)
	if fattura.user == request.user or request.user.is_superuser:
		fattura.delete()
		return HttpResponseRedirect('/fatture')
	else:
		raise PermissionDenied

@login_required
def fatture(request):
	if request.user.is_superuser:
		fatture=Fattura.objects.all()
		imposte=Imposta.objects.all()
	else:
		fatture=Fattura.objects.filter(user=request.user)
		imposte=Imposta.objects.filter(user=request.user)
	Fatture=[]
	f=[]
	Fatture.append(anni)
	for anno in anni:
		f.append(fatture.filter(data__year=anno))
	Fatture.append(f)
	Fatture=zip(*Fatture)
	return render_to_response( 'fatture.html', {'request':request, 'fatture': Fatture, 'anni': anni, 'imposte':imposte}, RequestContext(request))


@login_required
def export_fatture(request):
	if request.user.is_superuser:
		fatture=Fattura.objects.all()
	else:
		fatture=Fattura.objects.filter(fattura_user=request.user)
    # Create the HttpResponse object with the appropriate CSV header
	if settings.TIPO_FATTURA=="standard":
		return export_csv(request, fatture, [('Data','data'),
		('Cliente','cliente'),
		('Aliquota IVA','IVA'),
		('Stato','stato'),
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
	if f.user == request.user or request.user.is_superuser:
		#pdb.set_trace()
		#f.template
		template = webodt.ODFTemplate(f.template.template.name)
		context = dict(
			data=str(f.data),
			fattura=f,
			cliente=f.cliente,
			prestazioni=f.prestazione_fattura.all(),
			)

		document = template.render(Context(context))
		conv = converter()
		pdf = conv.convert(document, format='pdf')
		#return render_to_response( 'modello_fattura.html', {'request':request, 'f': f})
		response = HttpResponse(pdf, mimetype='application/pdf')
		response['Content-Disposition'] = 'attachment; filename=Fattura-%s-%s.pdf' % (f.progressivo(),f.data.year)
		return response
	else:
		raise PermissionDenied		

@login_required
def bilancio(request):

	form=IntervalloForm()
	if request.method == 'POST':  # If the form has been submitted...
		form = IntervalloForm(request.POST) 
		if form.is_valid():
			print "ciao"
	anno=dt.datetime.today().year
	fatturato=bilancio_intervallo(request,dt.date(anno,1,1),dt.datetime.now().date())
	
	return render_to_response( 'bilancio.html', {'request':request, 'fatturato': fatturato,'form':form, }, RequestContext(request))

@login_required
def bilancio_intervallo(request, inizio, fine):
	if request.user.is_superuser:
		fatture=Fattura.objects.filter(data__gte=inizio,data__lte=fine)
	else:
		fatture=Fattura.objects.filter(data__gte=inizio,data__lte=fine,user=request.user)
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
def nuovotemplate(request):
	azione = 'Nuovo'
	if request.method == 'POST':
		form = TemplateFatturaForm(request.POST, request.FILES)
		form.helper.form_action = '/template/nuovo/'
		if form.is_valid():
			t=form.save(commit=False)
			t.user=request.user
			t.save()
			return HttpResponseRedirect('/template')
	else:
		form = TemplateFatturaForm()
		form.helper.form_action = '/template/nuovo/'
	return render_to_response('form_template.html',{'request':request,'form': form,'azione': azione,}, RequestContext(request))

@login_required
def modificatemplate(request,t_id):
	azione = 'Modifica'
	f = TemplateFattura.objects.get(id=t_id)
	if f.user == request.user or request.user.is_superuser:
		if request.method == 'POST':  # If the form has been submitted...
			form = TemplateFatturaForm(request.POST, request.FILES, instance=f)  # necessario per modificare la riga preesistente
			form.helper.form_action = '/template/modifica/'+str(f.id)+'/'
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/template/') # Redirect after POST
		else:
			form = TemplateFatturaForm(instance=f)
			form.helper.form_action = '/template/modifica/'+str(f.id)+'/'
		return render_to_response('form_template.html',{'request': request, 'form': form,'azione': azione, 'f': f}, RequestContext(request))
	else:
		raise PermissionDenied

@login_required
def eliminatemplate(request,t_id):
	template = TemplateFattura.objects.get(id=t_id)
	if template.user == request.user or request.user.is_superuser:	
		template.delete()
		return HttpResponseRedirect('/template')
	else:
		raise PermissionDenied		

@login_required
def template(request):
	if request.user.is_superuser:
		template=TemplateFattura.objects.all()
	else:
		template=TemplateFattura.objects.filter(user=request.user)
	return render_to_response( 'template.html', {'request':request, 'templates': template, 'template_esempio':'template_standard.odt'}, RequestContext(request))

@login_required
def nuovoimposta(request):
	azione = 'Nuovo'
	if request.method == 'POST':
		form = ImpostaForm(request.POST)
		form.helper.form_action = '/imposte/nuovo/'
		if form.is_valid():
			t=form.save(commit=False)
			t.user=request.user
			t.save()
			return HttpResponseRedirect('/fatture')
	else:
		form = ImpostaForm()
		form.helper.form_action = '/imposte/nuovo/'
	return render_to_response('form_imposta.html',{'request':request,'form': form,'azione': azione,}, RequestContext(request))

@login_required
def modificaimposta(request,i_id):
	azione = 'Modifica'
	i = Imposta.objects.get(id=i_id)
	if i.user == request.user or request.user.is_superuser:
		if request.method == 'POST':  # If the form has been submitted...
			form = ImpostaForm(request.POST, instance=i)  # necessario per modificare la riga preesistente
			form.helper.form_action = '/imposta/modifica/'+str(i.id)+'/'
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/fatture') # Redirect after POST
		else:
			form = ImpostaForm(instance=i)
			form.helper.form_action = '/imposte/modifica/'+str(i.id)+'/'
		return render_to_response('form_imposta.html',{'request': request, 'form': form,'azione': azione, 'i': i}, RequestContext(request))
	else:
		raise PermissionDenied

@login_required
def eliminaimposta(request,i_id):
	imposta = Imposta.objects.get(id=i_id)
	if imposta.user == request.user or request.user.is_superuser:	
		imposta.delete()
		return HttpResponseRedirect('/fatture')
	else:
		raise PermissionDenied		