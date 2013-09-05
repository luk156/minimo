from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax
from minimo.documento.models import *
from minimo.documento.views import *
from dajaxice.utils import deserialize_form
from django.template.loader import render_to_string
from django.template import Context, Template
import datetime as dt


@dajaxice_register
def aggiorna_bilancio(request,inizio,fine):
	dajax=Dajax()
	if (inizio=="0"):
	 	anno=dt.datetime.today().year
	 	documentoto=bilancio_intervallo(request,dt.date(anno,1,1),dt.datetime.now().date())
	 	html_documentoto = render_to_string( 'bilancio/documentoto.html', {'request':request, 'documentoto': documentoto, }, RequestContext(request))
	 	dajax.assign('div #documentoto', 'innerHTML', html_documentoto)
	elif (inizio!="" and fine!=""):
	 	data_inizio=dt.datetime.strptime(inizio, "%d/%m/%Y").date()
	 	data_fine=dt.datetime.strptime(fine, "%d/%m/%Y").date()
	 	documentoto=bilancio_intervallo(request,data_inizio,data_fine)
	 	html_documentoto = render_to_string( 'bilancio/documentoto.html', {'request':request, 'documentoto': documentoto, }, RequestContext(request))
	 	dajax.assign('div #documentoto', 'innerHTML', html_documentoto)
	return dajax.json()
