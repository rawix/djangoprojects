from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('vocabulary.views',

    # Aplication URLS
    url(r'^$', 'index'),
    url(r'^index/$', 'index'),
    url(r'^word/','word'),
    url(r'^unit/(?P<unit_id>\d+)','unit'),
    
    # Admin URLS
    url(r'^admin/', include(admin.site.urls)),
)
