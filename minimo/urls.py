from django.conf.urls import patterns, include, url
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()
from fattura.models import *


urlpatterns = patterns('',
	# Examples:
	url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
	url(r'^$', 'fattura.views.fatture'),
	# url(r'^minimo/', include('minimo.foo.urls')),
	# clienti
	(r'^clienti/$', 'fattura.views.clienti'),
	(r'^clienti/export/$', 'fattura.views.export_clienti'),
	(r'^clienti/nuovo/$', 'fattura.views.nuovocliente'),
	(r'^clienti/(?P<c_id>\w+)/$', 'fattura.views.cliente'),
	(r'^clienti/modifica/(?P<c_id>\w+)/$', 'fattura.views.modificacliente'),
	(r'^clienti/elimina/(?P<c_id>\w+)/$', 'fattura.views.eliminacliente'),
	# prestazioni
	(r'^prestazioni/$', 'fattura.views.prestazioni'),
	(r'^prestazioni/nuova/(?P<f_id>\w+)$', 'fattura.views.nuovaprestazione'),
	#(r'^prestazioni/(?P<p_id>\w+)/$', 'fattura.views.prestazione'),
	(r'^prestazioni/modifica/(?P<p_id>\w+)/$', 'fattura.views.modificaprestazione'),
	(r'^prestazioni/elimina/(?P<p_id>\w+)/$', 'fattura.views.eliminaprestazione'),
	# fatture
	(r'^fatture/$', 'fattura.views.fatture'),
	(r'^fatture/export/$', 'fattura.views.export_fatture'),
	(r'^fatture/nuovo/$', 'fattura.views.nuovafattura'),
	#(r'^fatture/(?P<f_id>\w+)/$', 'fattura.views.fattura'),
	(r'^fatture/dettagli/(?P<f_id>\w+)/$', 'fattura.views.fattura'),
	(r'^fatture/stampa/(?P<f_id>\w+)/$', 'fattura.views.stampa_fattura'),
	(r'^fatture/modifica/(?P<f_id>\w+)/$', 'fattura.views.modificafattura'),
	(r'^fatture/elimina/(?P<f_id>\w+)/$', 'fattura.views.eliminafattura'),
	#template
	(r'^template/$', 'fattura.views.template'),
	(r'^template/nuovo/$', 'fattura.views.nuovotemplate'),
	(r'^template/modifica/(?P<t_id>\w+)/$', 'fattura.views.modificatemplate'),
	(r'^template/elimina/(?P<t_id>\w+)/$', 'fattura.views.eliminatemplate'),
	# bilancio
	(r'^bilancio/$', 'fattura.views.bilancio'),
	# Uncomment the admin/doc line below to enable admin documentation:
	# url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	# Uncomment the next line to enable the admin:
	#url(r'^admin/', include(admin.site.urls)),
)

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
