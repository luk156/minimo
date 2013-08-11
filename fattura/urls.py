from django.conf.urls import patterns, include, url
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()
from django.conf import settings
from django.conf.urls.static import static
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from fattura.models import *
from fattura.forms import *

urlpatterns = patterns('fattura.views',
    # Examples:
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    url(r'^$', 'fatture'),
    # url(r'^minimo/', include('minimo.foo.urls')),
    # clienti
    (r'^clienti/$', 'clienti'),
    (r'^clienti/export/$', 'export_clienti'),
    (r'^clienti/nuovo/$', 'nuovocliente'),
    (r'^clienti/(?P<c_id>\w+)/$', 'cliente'),
    (r'^clienti/modifica/(?P<c_id>\w+)/$', 'modificacliente'),
    (r'^clienti/elimina/(?P<c_id>\w+)/$', 'eliminacliente'),
    # prestazioni
    (r'^prestazioni/$', 'prestazioni'),
    (r'^prestazioni/nuova/(?P<f_id>\w+)$', 'nuovaprestazione'),
    #(r'^prestazioni/(?P<p_id>\w+)/$', 'fattura.views.prestazione'),
    (r'^prestazioni/modifica/(?P<p_id>\w+)/$', 'modificaprestazione'),
    (r'^prestazioni/elimina/(?P<p_id>\w+)/$', 'eliminaprestazione'),
    # fatture
    (r'^fatture/$', 'fatture'),
    (r'^fatture/export/$', 'export_fatture'),
    (r'^fatture/nuovo/$', 'nuovafattura'),
    #(r'^fatture/(?P<f_id>\w+)/$', 'fattura.views.fattura'),
    (r'^fatture/dettagli/(?P<f_id>\w+)/$', 'fattura'),
    (r'^fatture/stampa/(?P<f_id>\w+)/$', 'stampa_fattura'),
    (r'^fatture/invio/(?P<f_id>\w+)/$', 'invio_fattura'),
    (r'^fatture/modifica/(?P<f_id>\w+)/$', 'modificafattura'),
    (r'^fatture/elimina/(?P<f_id>\w+)/$', 'eliminafattura'),
    #template
    (r'^template/$', 'template'),
    (r'^template/nuovo/$', 'nuovotemplate'),
    (r'^template/modifica/(?P<t_id>\w+)/$', 'modificatemplate'),
    (r'^template/elimina/(?P<t_id>\w+)/$', 'eliminatemplate'),
    #imposte
    (r'^imposte/nuovo/$', 'nuovoimposta'),
    (r'^imposte/modifica/(?P<i_id>\w+)/$', 'modificaimposta'),
    (r'^imposte/elimina/(?P<i_id>\w+)/$', 'eliminaimposta'),
    #ritenute
    (r'^ritenute/nuovo/$', 'nuovoritenuta'),
    (r'^ritenute/modifica/(?P<i_id>\w+)/$', 'modificaritenuta'),
    (r'^ritenute/elimina/(?P<i_id>\w+)/$', 'eliminaritenuta'),
    # bilancio
    (r'^bilancio/$', 'bilancio'),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += patterns('django.contrib.auth.views',
    #utente
    #(r'^utente/nuovo/$', 'turni.views.nuovoutente'),
    (r'^utenti/modifica_password/$', 'password_change', {'password_change_form': PasswordForm}),
    (r'^utenti/modifica_password/ok/$', 'password_change_done'),
    (r'^utenti/reset/$', 'password_reset'),
    (r'^utenti/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'password_reset_confirm'),
    (r'^utenti/reset/completa/$', 'password_reset_complete'),
    (r'^utenti/reset/ok/$', 'password_reset_done'),
    )

urlpatterns += patterns('',
    (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name':'login.html', 'authentication_form': LoginForm} ),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    )
