from django.apps import AppConfig


class SalidaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Salida'

class SalidaEntradaRelacionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'SalidaEntradaRelacion'
