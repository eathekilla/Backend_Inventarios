from django.db import models

class Proveedor(models.Model):
    nit_cedula = models.CharField(max_length=20)
    tipo_documento = models.CharField(max_length=20,null=True)
    razon_social = models.CharField(max_length=100,  null=True)
    representante_legal = models.CharField(max_length=100,  null=True,blank=True)
    direccion = models.CharField(max_length=200,blank=True)
    telefono = models.CharField(max_length=20,blank=True)
    email = models.EmailField(null=True, blank=True)
    vereda = models.CharField(max_length=100,  null=True)
    departamento = models.CharField(max_length=100,  null=True)
    municipio = models.CharField(max_length=100,  null=True)
    barrio = models.CharField(max_length=100,  null=True)

    def __str__(self):
        return self.razon_social
