from django.db import models
from Fincas.models import Finca
from Insumo.models import Insumo
from simple_history.models import HistoricalRecords
import uuid

class Entrada(models.Model):
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    desde = models.DateField()
    hasta = models.DateField()
    de_finca = models.ForeignKey(Finca,related_name='entradas_de_finca', on_delete=models.CASCADE)
    a_finca = models.ForeignKey(Finca,related_name='entradas_a_finca', on_delete=models.CASCADE)
    insumo = models.ForeignKey(Insumo,related_name='entrada_insumo', on_delete=models.CASCADE, null=True)
    cantidad = models.FloatField()
    valor_unitario_entrada_a = models.FloatField()
    total_entra_a_la_finca = models.FloatField()
    identificador = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = True, unique=True)

    history = HistoricalRecords()

    def __str__(self):
        return f"Entrada - desde {self.desde}"