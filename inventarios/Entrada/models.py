from django.db import models
from Fincas.models import Finca
from Insumo.models import Insumo

class Entrada(models.Model):
    semana = models.CharField(max_length=10)
    desde = models.DateField()
    hasta = models.DateField()
    de_finca = models.ForeignKey(Finca,related_name='entradas_de_finca', on_delete=models.CASCADE)
    a_finca = models.ForeignKey(Finca,related_name='entradas_a_finca', on_delete=models.CASCADE)
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE)
    grupo = models.CharField(max_length=100,  null=True)
    medida = models.CharField(max_length=50,  null=True)
    existencia = models.FloatField()
    cantidad = models.FloatField()
    valor_unitario_salida = models.FloatField()
    valor_unitario_entrada_a = models.FloatField()
    total_entra_a_la_finca = models.FloatField()

    def __str__(self):
        return f"Entrada - Semana {self.semana}"
