from django.contrib import admin
from .models import Finca


admin.site.site_header = "Administración de Fincas"
admin.site.register(Finca)