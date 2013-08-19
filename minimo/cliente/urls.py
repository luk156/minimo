from django.conf.urls import patterns, include, url
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()
from django.conf import settings
from django.conf.urls.static import static
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from minimo.cliente.models import *
from minimo.cliente.forms import *

urlpatterns = patterns('minimo.cliente.views',


    # url(r'^minimo/', include('minimo.foo.urls')),
    # clienti
    (r'^$', 'clienti'),
    (r'^export/$', 'export_clienti'),
    (r'^nuovo/$', 'nuovocliente'),
    (r'^(?P<c_id>\w+)/$', 'cliente'),
    (r'^modifica/(?P<c_id>\w+)/$', 'modificacliente'),
    (r'^elimina/(?P<c_id>\w+)/$', 'eliminacliente'),
    (r'^get_clienti', 'get_clienti'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
