from django.db import models

class usuarios (models.Model):
	usuario = models.TextField(primary_key=True)
	css = models.TextField()
	idioma = models.TextField()
	nombrePublico = models.TextField()

class microusuarios (models.Model):
	usuario = models.TextField()
	micronotero = models.TextField()
	
class micronoteros (models.Model):
	micronotero = models.TextField()
	numeroID = models.TextField(primary_key=True)

class micronotas (models.Model):
	title = models.TextField()
	notero = models.TextField()
	link = models.TextField()
	guid = models.TextField(primary_key=True)
	pubdate = models.DateTimeField()


