from django.db import models

class Entrada(models.Model):
    semana = models.CharField(max_length=10)
    desde = models.DateField()
    hasta = models.DateField()
    de_finca = models.CharField(max_length=100,  null=True)
    a_finca = models.CharField(max_length=100,  null=True)
    insumo = models.CharField(max_length=100,  null=True)
    grupo = models.CharField(max_length=100,  null=True)
    medida = models.CharField(max_length=50,  null=True)
    existencia = models.FloatField()
    cantidad = models.FloatField()
    valor_unitario_salida = models.FloatField()
    valor_unitario_entrada_a = models.FloatField()
    total_entra_a_la_finca = models.FloatField()

    def __str__(self):
        return f"Entrada - Semana {self.semana}"
