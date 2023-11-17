from django.contrib import admin
from .models import Salida

admin.site.site_header = "Administración de Salidas"
admin.site.register(Salida)
