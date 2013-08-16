from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax
from minimo.fattura.models import *
from minimo.fattura.views import *
from dajaxice.utils import deserialize_form
from django.template.loader import render_to_string
from django.template import Context, Template
import datetime as dt


@dajaxice_register
def aggiorna_bilancio(request,inizio,fine):
	dajax=Dajax()
	if (inizio=="0"):
	 	anno=dt.datetime.today().year
	 	fatturato=bilancio_intervallo(request,dt.date(anno,1,1),dt.datetime.now().date())
	 	html_fatturato = render_to_string( 'bilancio/fatturato.html', {'request':request, 'fatturato': fatturato, }, RequestContext(request))
	 	dajax.assign('div #fatturato', 'innerHTML', html_fatturato)
	elif (inizio!="" and fine!=""):
	 	data_inizio=dt.datetime.strptime(inizio, "%d/%m/%Y").date()
	 	data_fine=dt.datetime.strptime(fine, "%d/%m/%Y").date()
	 	fatturato=bilancio_intervallo(request,data_inizio,data_fine)
	 	html_fatturato = render_to_string( 'bilancio/fatturato.html', {'request':request, 'fatturato': fatturato, }, RequestContext(request))
	 	dajax.assign('div #fatturato', 'innerHTML', html_fatturato)
	return dajax.json()
