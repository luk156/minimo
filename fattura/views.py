
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

anni=(2012,2013)

if settings.TIPO_FATTURA=="standard":
	FatturaForm = FatturaStandardForm
	F = FatturaStandard
	template_fattura='fattura_standard.html'
	template_bilancio='bilancio_standard.html'
	template_esempio='template_standard.odt'
elif settings.TIPO_FATTURA=="minimo":
	FatturaForm = FatturaMinimoForm
	F = FatturaMinimo
	template_fattura='fattura_minimo.html'
	template_bilancio='bilancio_minimo.html'
	template_esempio='template_minimo.odt'

def home(request):
	return True

def nuovocliente(request):
	azione = 'nuovo';
	if request.method == 'POST':
		form = ClienteForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/clienti') 
	else:
		form = ClienteForm()
	return render_to_response('form_cliente.html',{'request':request, 'form': form,'azione': azione}, RequestContext(request))

def modificacliente(request,c_id):
	azione = 'modifica'
	cliente = Cliente.objects.get(id=c_id)
	if request.method == 'POST': 
		form = ClienteForm(request.POST, instance=cliente,)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/clienti') 
	else:
		form = ClienteForm(instance=cliente)
	return render_to_response('form_cliente.html',{'request':request, 'form': form,'azione': azione, 'c': cliente,}, RequestContext(request))

def clienti(request):
	return render_to_response( 'clienti.html', {'request':request, 'clienti': Cliente.objects.all()})

def cliente(request,c_id):
	c= Cliente.objects.get(id=c_id)
	return render_to_response( 'cliente.html', {'request':request, 'c':c , 'f': F.objects.filter(cliente=c)})


def eliminacliente(request,c_id):
	cliente = Cliente.objects.get(id=c_id)
	cliente.delete()
	return HttpResponseRedirect('/clienti')

def nuovaprestazione(request,f_id):
	azione = 'nuovo';
	f=Fattura(id=f_id)
	if request.method == 'POST':
		form = PrestazioneForm(request.POST)
		form.helper.form_action = '/prestazioni/nuova/'+str(f.id)
		if form.is_valid():
			data = form.cleaned_data
			p=Prestazione(descrizione=data['descrizione'],importo=data['importo'],fattura=f)
			p.save()
			return HttpResponseRedirect('/fatture') 
	else:
		form = PrestazioneForm()
		form.helper.form_action = '/prestazioni/nuova/'+str(f.id)
	return render_to_response('form_prestazione.html',{'request':request, 'form': form,'azione': azione, 'f': f_id}, RequestContext(request))

def modificaprestazione(request,p_id):
	azione = 'Modifica'
	prestazione = Prestazione.objects.get(id=p_id)
	if request.method == 'POST': 
		form = PrestazioneForm(request.POST, instance=prestazione,)
		form.helper.form_action = '/prestazioni/modifica/'+str(prestazione.id)+'/'
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/fatture') 
	else:
		form = PrestazioneForm(instance=prestazione)
		form.helper.form_action = '/prestazioni/modifica/'+str(prestazione.id)+'/'
	return render_to_response('form_prestazione.html',{'request':request, 'form': form,'azione': azione, 'p': prestazione,}, RequestContext(request))

def eliminaprestazione(request,p_id):
	prestazione = Prestazione.objects.get(id=p_id)
	prestazione.delete()
	return HttpResponseRedirect('/fatture')

def prestazioni(request):
	return render_to_response( 'prestazioni.html', {'request':request, 'prestazioni': Prestazione.objects.all()})

def nuovafattura(request):
	azione = 'Nuova'
	#pdb.set_trace()
	if request.method == 'POST':
		form = FatturaForm(request.POST)
		form.helper.form_action = '/fatture/nuovo/'
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/fatture')
	else:
		form = FatturaForm()
		form.helper.form_action = '/fatture/nuovo/'
	return render_to_response('form_fattura.html',{'request':request,'form': form,'azione': azione,}, RequestContext(request))


def modificafattura(request,f_id):
	azione = 'Modifica'
	f = Fattura.objects.get(id=f_id)
	if request.method == 'POST':  # If the form has been submitted...
		form = FatturaForm(request.POST, instance=f)  # necessario per modificare la riga preesistente
		form.helper.form_action = '/fatture/modifica/'+str(f.id)+'/'
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/fatture/') # Redirect after POST
	else:
		form = FatturaForm(instance=f)
		form.helper.form_action = '/fatture/modifica/'+str(f.id)+'/'
	return render_to_response('form_fattura.html',{'request': request, 'form': form,'azione': azione, 'f': f}, RequestContext(request))

def eliminafattura(request,f_id):
	fattura = F.objects.get(id=f_id)
	fattura.delete()
	return HttpResponseRedirect('/fatture')

def fatture(request):
	Fatture=[]
	f=[]
	Fatture.append(anni)
	for anno in anni:
		f.append(F.objects.filter(data__year=anno))
	Fatture.append(f)
	Fatture=zip(*Fatture)
	return render_to_response( 'fatture.html', {'request':request, 'fatture': Fatture, 'anni': anni})

def fattura(request, f_id):
	f=F.objects.get(id=f_id)
	return render_to_response( template_fattura, {'request':request, 'f': f,})

def stampa_fattura(request,f_id):
	f=F.objects.get(id=f_id)
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
	response['Content-Disposition'] = 'attachment; filename=Fattura-%s.pdf' % (f)
	return response

def bilancio(request):

	form=IntervalloForm()
	if request.method == 'POST':  # If the form has been submitted...
		form = IntervalloForm(request.POST) 
		if form.is_valid():
			print "ciao"
	anno=dt.datetime.today().year
	fatturato=bilancio_intervallo(request,dt.date(anno,1,1),dt.datetime.now().date())
	
	return render_to_response( 'bilancio.html', {'request':request, 'fatturato': fatturato,'form':form, }, RequestContext(request))


def bilancio_intervallo(request, inizio, fine):

	fatture=F.objects.filter(data__gte=inizio,data__lte=fine)
	f_data=[]
	f_tot=[]
	fatturato=[]
	data_precedente=dt.date.today()
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

def nuovotemplate(request):
	azione = 'Nuovo'
	if request.method == 'POST':
		form = TemplateFatturaForm(request.POST, request.FILES)
		form.helper.form_action = '/template/nuovo/'
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/template')
	else:
		form = TemplateFatturaForm()
		form.helper.form_action = '/template/nuovo/'
	return render_to_response('form_template.html',{'request':request,'form': form,'azione': azione,}, RequestContext(request))


def modificatemplate(request,t_id):
	azione = 'Modifica'
	f = TemplateFattura.objects.get(id=t_id)
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

def eliminatemplate(request,t_id):
	template = TemplateFattura.objects.get(id=t_id)
	template.delete()
	return HttpResponseRedirect('/template')

def template(request):
	return render_to_response( 'template.html', {'request':request, 'templates': TemplateFattura.objects.all(), 'template_esempio':template_esempio})