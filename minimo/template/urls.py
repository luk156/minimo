from django.conf.urls import patterns, include, url
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()
from django.conf import settings
from django.conf.urls.static import static
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from minimo.template.models import *
from minimo.template.forms import *

urlpatterns = patterns('minimo.template.views',
    # Examples:
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),


    #template
    (r'^$', 'template'),
    (r'^nuovo/$', 'nuovotemplate'),
    (r'^modifica/(?P<t_id>\w+)/$', 'modificatemplate'),
    (r'^elimina/(?P<t_id>\w+)/$', 'eliminatemplate'),
    
    )