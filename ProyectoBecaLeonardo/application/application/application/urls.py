from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',

    # Aplication URLS
	url(r'^$', 'vocabulary.views.index'),
    url(r'^loadVocabulary/$', 'vocabulary.views.loadVocabulary'),
	url(r'^vocabulary/', include('vocabulary.urls')),

    # Admin URLS
	url(r'^admin/', include(admin.site.urls)),
)
