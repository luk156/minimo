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


urlpatterns = patterns('minimo',
    # Examples:
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('minimo.fattura.urls')),
    url(r'^clienti/', include('minimo.cliente.urls')),
    url(r'^template/', include('minimo.template.urls')),
    url(r'^tasse/', include('minimo.tassa.urls'))
    
) #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

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



