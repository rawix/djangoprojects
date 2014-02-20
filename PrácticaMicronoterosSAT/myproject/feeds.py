from django.contrib.syndication.views import FeedDoesNotExist, Feed
from django.shortcuts import get_object_or_404

from MiResumen.models import micronotas, microusuarios
from django.contrib.auth.models import User

class FeedUsu(Feed):
	def get_object(self, request, usuario_id):		
		return get_object_or_404(User, username=usuario_id)

	def title(self, obj):
		print obj.username
		return "Micronotas de los micronoteros que sique %s" % obj.username

	def link(self, obj):		
		return obj.get_absolute_url()

	def description(self, obj):		
		return "Micronotas de %s" % obj.username

	def items(self, obj):		
		n=microusuarios.objects.extra(where=['usuario=%s'], params=[obj.username])
		x= micronotas.objects.extra(where=['notero=%s'], params=[n[0].micronotero])
		for i in n:
			x=x|(micronotas.objects.extra(where=['notero=%s'], params=[i.micronotero])).order_by('-pubdate')[:50]
		return x

	def item_title(self,item):
		return item.title
	def item_description(self,item):
		return item.notero
	def item_link(self,item):
		return item.link
	def item_pubdate(self,item):
		return item.pubdate

