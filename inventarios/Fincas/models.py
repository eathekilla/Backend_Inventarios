from django.db import models
from django.contrib.auth.models import User

class Lotes(models.Model):
    nombre_lote = models.CharField(max_length=150)
    ubicacion = models.CharField(max_length=150,  null=True, default="")
    hectareas = models.FloatField(default=0)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.nombre_lote}"

class Bodegas(models.Model):
    nombre_bodega = models.CharField(max_length=150)
    ubicacion = models.CharField(max_length=150,  null=True , default="")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.nombre_bodega}"

class Finca(models.Model):
    nombre_finca = models.CharField(max_length=150)
    ubicacion = models.CharField(max_length=150,  null=True)
    telefono = models.CharField(max_length=150,  null=True)
    usuario = models.ManyToManyField(User, null=True,related_name='usuarios_finca')
    bodegas = models.ManyToManyField(Bodegas, null=True,related_name='bodegas_finca')
    lotes = models.ManyToManyField(Lotes, null=True,related_name='lotes_finca')
    def __str__(self):
        return f"{self.nombre_finca} - {self.usuario.username}"

