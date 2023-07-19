from django.db import models
from django.contrib.auth.models import User

class Finca(models.Model):
    nombre_finca = models.CharField(max_length=150)
    ubicacion = models.CharField(max_length=150,  null=True)
    telefono = models.CharField(max_length=150,  null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.nombre_finca} - {self.usuario.username}"