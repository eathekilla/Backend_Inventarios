from django.db import models



class IngredienteActivo(models.Model):
    nombre = models.CharField(max_length=100,  null=True)
    def __str__(self):
        return self.nombre


class Certificacion(models.Model):
    ingrediente_activo = models.ForeignKey(IngredienteActivo, on_delete=models.CASCADE, null=True)
    periodo_carencia = models.DateTimeField()
    periodo_reingreso = models.DateTimeField()
    registro_ica = models.CharField(max_length=50,  null=True)
    fecha_registro = models.DateField()

    def __str__(self):
        return f"Certificación - {self.registro_ica}"
    
class UnidadMedida(models.Model):
    nombre = models.CharField(max_length=50,  null=True)
    def __str__(self):
        return self.nombre


class Insumo(models.Model):
    nombre = models.CharField(max_length=100,  null=True)
    unidad_medida = models.ForeignKey(UnidadMedida, on_delete=models.CASCADE, null=True)
    codigo_contable = models.CharField(max_length=20)
    certificacion = models.ForeignKey(Certificacion, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.nombre
    

class Grupo(models.Model):
    nombre = models.CharField(max_length=100,  null=True)
    inicial = models.CharField(max_length=5, null=True)
    insumos = models.ManyToManyField(Insumo, null=True,related_name='grupos')
    def __str__(self):
        return self.nombre

    

