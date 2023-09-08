from django.db import models
from django.contrib.auth.models import User

class Bodegas(models.Model):
    nombre_bodega = models.CharField(max_length=150)
    ubicacion = models.CharField(max_length=150,  null=True , default="")
    usuario = models.ManyToManyField(User, null=True,related_name='bodegas_finca_usuario')
    def __str__(self):
        return f"{self.nombre_bodega}"

class Lotes(models.Model):
    nombre_lote = models.CharField(max_length=150)
    ubicacion = models.CharField(max_length=150,  null=True, default="")
    hectareas = models.FloatField(default=0)
    bodegas = models.ManyToManyField(Bodegas, null=True,related_name='bodegas_finca')
    def __str__(self):
        return f"{self.nombre_lote}"

class Finca(models.Model):
    nombre_finca = models.CharField(max_length=150)
    ubicacion = models.CharField(max_length=150,  null=True)
    telefono = models.CharField(max_length=150,  null=True)
    lotes = models.ManyToManyField(Lotes, null=True,related_name='lotes_finca')
    def __str__(self):
        return f"{self.nombre_finca}"

class InfoUser(models.Model):
    telefono = models.CharField(max_length=12)
    direccion = models.CharField(max_length=150)
    tipo_documento = models.CharField(max_length=20)
    numero_documento = models.CharField(max_length=20)
    usuario = models.ForeignKey(User,related_name="info_user",on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.usuario}"

