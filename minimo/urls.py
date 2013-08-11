from django.conf.urls import patterns, include, url
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()
from django.conf import settings
from django.conf.urls.static import static
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()



urlpatterns = patterns('',
    # Examples:
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('fattura.urls')),
) #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




