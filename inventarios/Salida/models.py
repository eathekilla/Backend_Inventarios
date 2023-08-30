from django.db import models
from Fincas.models import Finca
from Insumo.models import Insumo, Grupo
from Entrada.models import Entrada
from datetime import datetime
class Salida(models.Model):
    fecha_ingreso = models.DateTimeField(default=datetime.now())
    de_bodega = models.ForeignKey(Finca,related_name='salidas_de_bodega', on_delete=models.CASCADE,null=True)
    a_bodega = models.ForeignKey(Finca,related_name='entrada_a_bodega', on_delete=models.CASCADE,null=True)
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE)
    cantidad = models.FloatField(default=0)
    valor_unitario_salida = models.FloatField(default=0)
    valor_unitario_entrada = models.FloatField(default=0)
    grupo = models.ForeignKey(Grupo,related_name='grupo_insumo_salida', on_delete=models.CASCADE,null=True )

    def __str__(self):
        return f"Salida - {self.fecha_ingreso} - {self.insumo.nombre}"
    
    def save(self, *args, **kwargs):
        insumo_filter = self.insumo
        cantidad_salida = self.cantidad
        total_entradas = Entrada.objects.all()

        entradas = Entrada.objects.filter(insumo=insumo_filter).order_by('fecha_creacion')

        cantidad_disponible_total = sum(entrada.cantidad for entrada in entradas)

        if cantidad_salida > cantidad_disponible_total:
            raise ValueError("La cantidad de salida es mayor a la cantidad disponible.")

        for entrada in entradas:
            cantidad_disponible = entrada.cantidad
            if cantidad_salida >= cantidad_disponible:
                cantidad_salida -= cantidad_disponible
                entrada_copy = entrada  # Hacer una copia de la entrada antes de modificarla
                entrada_copy.id = None  # Crear una nueva entrada con la copia
                entrada_copy.cantidad = 0  # Establecer la cantidad en cero en la copia
                entrada_copy.fecha_ingreso = entrada.fecha_ingreso
                entrada_copy.save()
            else:
                entrada.cantidad = cantidad_disponible - cantidad_salida
                entrada.save()
                break

        super().save(*args, **kwargs)
