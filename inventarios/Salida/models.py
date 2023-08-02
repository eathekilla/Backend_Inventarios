from django.db import models
from Fincas.models import Finca
from Insumo.models import Insumo
from Entrada.models import Entrada
class Salida(models.Model):
    semana = models.IntegerField(default=0)
    de_finca = models.ForeignKey(Finca,related_name='salidas_de_finca', on_delete=models.CASCADE,null=True)
    a_finca = models.ForeignKey(Finca,related_name='salidas_a_finca', on_delete=models.CASCADE,null=True)
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE)
    cantidad = models.FloatField(default=0)
    valor_unitario_salida = models.FloatField(default=0)
    total_entra_a_la_finca = models.FloatField(default=0)

    def __str__(self):
        return f"Salida - Semana {self.semana}"
    
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
                entrada_copy.fecha_creacion = entrada.fecha_creacion
                entrada_copy.save()
            else:
                entrada.cantidad = cantidad_disponible - cantidad_salida
                entrada.save()
                break

        super().save(*args, **kwargs)
