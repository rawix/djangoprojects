from django.contrib import admin
from myproject.MiResumen.models import usuarios,microusuarios,micronotas,micronoteros

admin.site.register(usuarios)
admin.site.register(microusuarios)
admin.site.register(micronotas)
admin.site.register(micronoteros)


