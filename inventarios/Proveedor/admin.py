from django.contrib import admin
from .models import Proveedor

# Register your models here.
admin.site.site_header = "Administración de Proveedor"
admin.site.register(Proveedor)