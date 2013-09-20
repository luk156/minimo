from django.conf.urls import patterns, include, url
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()
from django.conf import settings
from django.conf.urls.static import static
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from minimo.tassa.models import *


urlpatterns = patterns('minimo.tassa.views',
    # Examples:
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    #imposte
    (r'^imposte/nuovo/$', 'nuovoimposta'),
    (r'^imposte/modifica/(?P<i_id>\w+)/$', 'modificaimposta'),
    (r'^imposte/elimina/(?P<i_id>\w+)/$', 'eliminaimposta'),
    (r'^imposte/get_imposta$', 'get_imposta'),
    #ritenute
    (r'^ritenute/nuovo/$', 'nuovoritenuta'),
    (r'^ritenute/modifica/(?P<i_id>\w+)/$', 'modificaritenuta'),
    (r'^ritenute/elimina/(?P<i_id>\w+)/$', 'eliminaritenuta'),
    (r'^ritenute/get_ritenuta$', 'get_ritenuta'),

)
