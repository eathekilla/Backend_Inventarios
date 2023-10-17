from django.db import models
from Fincas.models import Finca
from Insumo.models import Insumo, Grupo
from Entrada.models import Entrada
from datetime import datetime
from django.core.exceptions import ValidationError
from django.db.models import Sum

class Salida(models.Model):
    fecha_salida = models.DateTimeField(default=datetime.now())
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE)
    cantidad = models.FloatField(default=0)
    valor_total_salida = models.FloatField(default=0)
    #grupo = models.ForeignKey(Grupo,related_name='grupo_insumo_salida', on_delete=models.CASCADE,null=True )

    def __str__(self):
        return f"Salida - {self.fecha_salida} - {self.insumo.nombre}"
    
    def save(self, *args, **kwargs):
        # Creamos una variable para determinar si es una nueva instancia
        es_nueva_instancia = not self.pk

        # Guardar primero la instancia para tener un ID (si es una nueva instancia)
        super(Salida, self).save(*args, **kwargs)

        if es_nueva_instancia:  # Estamos creando una nueva salida
            cantidad_pendiente = self.cantidad

            # Consulta las entradas más antiguas de este insumo
            entradas = Entrada.objects.filter(insumo=self.insumo).order_by('fecha_creacion')
            suma_total = entradas.aggregate(total_unidades=Sum('cantidad'))
            total_unidades = suma_total['total_unidades'] 
            if entradas.count()==0:
                total_unidades = 0
            # Si aún queda cantidad pendiente después de considerar todas las entradas
            if cantidad_pendiente > total_unidades:
                raise ValidationError(f"No hay suficiente stock para el insumo {self.insumo}. Falta: {cantidad_pendiente} unidades.")
            
            valor_total = 0
            for entrada in entradas:
                if entrada.cantidad >= cantidad_pendiente:  # La entrada cubre la cantidad pendiente
                    valor_total += cantidad_pendiente * entrada.valor_unitario_entrada_a
                    relacion = SalidaEntradaRelacion(salida=self, entrada=entrada, cantidad_usada=cantidad_pendiente, precio_unitario=entrada.valor_unitario_entrada_a)
                    relacion.save()
                    entrada.cantidad -= cantidad_pendiente
                    entrada.save()
                    break  # Hemos cubierto la cantidad necesaria con las entradas
                else:  # La entrada no cubre toda la cantidad pendiente
                    valor_total += entrada.cantidad * entrada.valor_unitario_entrada_a
                    relacion = SalidaEntradaRelacion(salida=self, entrada=entrada, cantidad_usada=entrada.cantidad, precio_unitario=entrada.valor_unitario_entrada_a)
                    relacion.save()
                    cantidad_pendiente -= entrada.cantidad
                    entrada.cantidad = 0
                    entrada.save()

           

            self.valor_total_salida = valor_total
            super(Salida, self).save(update_fields=['valor_total_salida'])  # Actualizar solo el campo valor_total_salida


class SalidaEntradaRelacion(models.Model):
    salida = models.ForeignKey(Salida, on_delete=models.CASCADE)
    entrada = models.ForeignKey(Entrada, on_delete=models.CASCADE)
    cantidad_usada = models.FloatField()
    precio_unitario = models.FloatField()

    def __str__(self):
        return f"Salida {self.salida.id} - Entrada {self.entrada.id}"
