from django.db import models
from Fincas.models import Finca
from Insumo.models import Insumo
from simple_history.models import HistoricalRecords
from datetime import datetime
import uuid

class Entrada(models.Model):
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_ingreso = models.DateTimeField(default=datetime.now())
    de_finca = models.ForeignKey(Finca,related_name='entradas_de_finca', on_delete=models.CASCADE)
    a_finca = models.ForeignKey(Finca,related_name='entradas_a_finca', on_delete=models.CASCADE)
    insumo = models.ForeignKey(Insumo,related_name='entrada_insumo', on_delete=models.CASCADE, null=True)
    cantidad = models.FloatField()
    valor_unitario_entrada_a = models.FloatField()
    total_entra_a_la_finca = models.FloatField()
    id = models.IntegerField(primary_key=True, unique=True,default=132321321312)

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.fecha_ingreso} - {self.insumo}"