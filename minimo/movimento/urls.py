from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('minimo.movimento.views',
                       
    (r'^elencomovimenti/$', 'movimenti'),
    (r'^elencodocumenti/$', 'documenti'),
    (r'^nuovomovimento/$', 'nuovomovimento'),
    (r'^modificamovimento/(?P<i_id>\w+)/$', 'modificamovimento'),
    (r'^nuovodocumento/$', 'nuovodocumento'),
    (r'^modificadocumento/(?P<t_id>\w+)/$', 'modificadocumento'),
    (r'^eliminadocumento/(?P<i_id>\w+)/$', 'eliminadocumento'),
    (r'^pagadocumento/(?P<i_id>\w+)/$', 'pagadocumento',),
    (r'^esportalistamovimenti/$', 'esportamovimenti',),
    #(r'^$', 'movimenti'),
)