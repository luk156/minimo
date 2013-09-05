from django.conf.urls import patterns, include, url
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()
from django.conf import settings
from django.conf.urls.static import static
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from minimo.documento.models import *
from minimo.documento.forms import *

urlpatterns = patterns('minimo.documento.views',
    # Examples:
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    

    # prestazioni
    (r'^documenti/riga/$', 'righe'),
    (r'^documenti/riga/nuova/(?P<f_id>\w+)$', 'nuovariga'),
    (r'^documenti/riga/modifica/(?P<p_id>\w+)/$', 'modificariga'),
    (r'^documenti/riga/elimina/(?P<p_id>\w+)/$', 'eliminariga'),
    # fatture
    
    (r'^documenti/export/(?P<d_tipo>\w+)/$', 'export_documenti'),
    (r'^documenti/nuovo/$', 'nuovodocumento'),
    (r'^documenti/dettagli/(?P<d_num>\w+)/$', 'dettagli_documento'),
    (r'^documenti/stampa/(?P<f_id>\w+)/$', 'stampa_documento'),
    (r'^documenti/invio/(?P<f_id>\w+)/$', 'invio_documento'),
    (r'^documenti/incassa/(?P<d_id>\w+)/$', 'incassa_documento'),
    (r'^documenti/sblocca/(?P<d_id>\w+)/$', 'sblocca_documento'),
    (r'^documenti/modifica/(?P<f_id>\w+)/$', 'modificadocumento'),
    (r'^documenti/elimina/(?P<d_id>\w+)/$', 'eliminadocumento'),
    (r'^documenti/creafattura/(?P<d_id>\w+)/$', 'fattura_documento'),
    (r'^documenti/(?P<d_tipo>\w+)/$', 'documenti'),
    (r'^$', 'home'),
    #pagamenti
    (r'^pagamenti/nuovo/$', 'nuovopagamento'),
    (r'^pagamenti/modifica/(?P<i_id>\w+)/$', 'modificapagamento'),
    (r'^pagamenti/elimina/(?P<i_id>\w+)/$', 'eliminapagamento'),
    # bilancio
    (r'^bilancio/$', 'bilancio'),

)

