from django.conf.urls.defaults import *
from django.contrib import admin

from django.views.generic.simple import direct_to_template
from django.conf.urls.defaults import *

from myproject.feeds import FeedUsu
admin.autodiscover()


urlpatterns = patterns('',
           (r'^admin/',include(admin.site.urls)),
           (r'^login', 'django.contrib.auth.views.login'),
           (r'^logout','django.contrib.auth.views.logout'),
           (r'^accounts/profile/','myproject.MiResumen.views.autenticado',),
           

           # parsea el rss del micronotero que le hemos pedido
           (r'^inicio/(?P<notero>[\S]+)','myproject.MiResumen.views.inicio',),
           # recurso que me devuelve las ultimas 50 micronoticias del micronotero 
           (r'^noteros/(?P<micronotero>[\S]+)','myproject.MiResumen.views.noticiasMicronotero',),
           # devuelve la lista de micronoteros de la aplicacion
           (r'^noteros','myproject.MiResumen.views.micros',),
           # recurso que devuelve los canales de las ultimas 50 noticias
           (r'^usuarios/(?P<usuario_id>.*)/feed', FeedUsu()),
           # recurso que me devuelve las ultimas 50 micronoticias de los micronoteros que sigue el usuario
           (r'^usuarios/(?P<user>[\S]+)','myproject.MiResumen.views.noticiasUsuario',),
           # devuelve una lista de todos los usuarios
           (r'^usuarios','myproject.MiResumen.views.usus',),
           # configuracion del estilo
           (r'^conf/skin','myproject.MiResumen.views.confEstilo',),
           # configuracion del usuario
           (r'^conf','myproject.MiResumen.views.confUsuario',),
           # lista de los micronoteros seleccionados
           (r'^micronoteros','myproject.MiResumen.views.micronoterosUsuario',),
           # actualiza las micronotas
           (r'^update','myproject.MiResumen.views.actualiza',),
           # recurso que me devuelve las ultimas 50 micronoticias
           (r'^$', 'myproject.MiResumen.views.main',),
           (r'^mcss','myproject.MiResumen.views.mcss',),
           (r'^css/(?P<path>.*)$', 'django.views.static.serve',{'document_root': './css'}), 
           (r'^imagenes/(?P<path>.*)$', 'django.views.static.serve',{'document_root': './imagenes'}), 

)
