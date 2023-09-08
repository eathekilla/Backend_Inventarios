from django.contrib import admin
from .models import Finca,Lotes,Bodegas, InfoUser


admin.site.site_header = "Administración de Fincas"
admin.site.register(Finca)
admin.site.register(Lotes)
admin.site.register(Bodegas)
admin.site.register(InfoUser)