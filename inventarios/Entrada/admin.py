from django.contrib import admin
from .models import Entrada


admin.site.site_header = "Administración de Entradas"
admin.site.register(Entrada)