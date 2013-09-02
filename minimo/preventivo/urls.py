from django.conf.urls import patterns, include, url
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()
from django.conf import settings
from django.conf.urls.static import static
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from minimo.fattura.models import *
from minimo.fattura.forms import *

urlpatterns = patterns('minimo.preventivo.views',
    # Examples:
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    url(r'^$', 'fatture'),


    (r'^preventivi/prestazioni/$', 'prestazioni'),
    (r'^preventivi/prestazioni/nuova/(?P<f_id>\w+)$', 'nuovaprestazione'),
    (r'^preventivi/prestazioni/modifica/(?P<p_id>\w+)/$', 'modificaprestazione'),
    (r'^preventivi/prestazioni/elimina/(?P<p_id>\w+)/$', 'eliminaprestazione'),

    (r'^preventivi/$', 'fatture'),
    (r'^preventivi/export/$', 'export_fatture'),
    (r'^preventivi/nuovo/$', 'nuovafattura'),
    (r'^preventivi/dettagli/(?P<f_id>\w+)/$', 'fattura'),
    (r'^preventivi/stampa/(?P<f_id>\w+)/$', 'stampa_fattura'),
    (r'^preventivi/invio/(?P<f_id>\w+)/$', 'invio_fattura'),
    (r'^preventivi/modifica/(?P<f_id>\w+)/$', 'modificafattura'),
    (r'^preventivi/elimina/(?P<f_id>\w+)/$', 'eliminafattura'),



)
