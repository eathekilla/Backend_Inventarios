from django.db import models
from Insumo.models import Insumo
from Entrada.models import Entrada
from datetime import datetime
from django.core.exceptions import ValidationError
from django.db.models import Sum

class SalidaEntradaRelacion(models.Model):
    salida = models.ForeignKey('Salida', on_delete=models.CASCADE)
    entrada = models.ForeignKey(Entrada, on_delete=models.CASCADE)
    cantidad_usada = models.FloatField(default=0)
    precio_unitario = models.FloatField(default=0)
    

    def __str__(self):
        return f"Relacion - {self.salida} - {self.entrada}"

class Salida(models.Model):
    fecha_salida = models.DateTimeField(default=datetime.now)
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE)
    cantidad = models.FloatField(default=0)
    valor_total_salida = models.FloatField(default=0)
    movimientos = models.TextField(default="",null=True)
    

    def __str__(self):
        return f"Salida - {self.fecha_salida} - {self.insumo.nombre}"
    
    def save(self, *args, **kwargs):
        es_nueva_instancia = not self.pk
        suma_movimientos = ""

        if es_nueva_instancia:
            cantidad_pendiente = self.cantidad
            

            entradas = Entrada.objects.filter(insumo=self.insumo).order_by('fecha_creacion')
            suma_total = entradas.aggregate(total_unidades=Sum('cantidad'))
            total_unidades = suma_total['total_unidades'] or 0

            if cantidad_pendiente > total_unidades:
                raise ValidationError(f"No hay suficientes unidades para el insumo {self.insumo}. Faltan: {cantidad_pendiente} unidades.")

            valor_total = 0
            for entrada in entradas:
                if entrada.cantidad >= cantidad_pendiente:
                    valor_total += cantidad_pendiente * entrada.valor_unitario_entrada_a
                    valor = str(cantidad_pendiente * entrada.valor_unitario_entrada_a)
                    valor_unitario_entrada_a_str=str(entrada.valor_unitario_entrada_a)
                    cantidad_pendiente_str = str(cantidad_pendiente)
                    str_entrada = f"- Cant {cantidad_pendiente_str} * Vrl/u ${valor_unitario_entrada_a_str} = ${str(valor)}\n"
                    suma_movimientos += str_entrada
                    relacion = SalidaEntradaRelacion(salida=self, entrada=entrada, cantidad_usada=cantidad_pendiente, precio_unitario=entrada.valor_unitario_entrada_a)
                    entrada.cantidad -= cantidad_pendiente
                    entrada.save()
                    break
                else:
                    valor_total += entrada.cantidad * entrada.valor_unitario_entrada_a
                    valor = str(cantidad_pendiente * entrada.valor_unitario_entrada_a)
                    valor_unitario_entrada_a_str=str(entrada.valor_unitario_entrada_a)
                    cantidad_pendiente_str = str(cantidad_pendiente)
                    str_entrada = f"- Cant {cantidad_pendiente_str} * Vrl/u {valor_unitario_entrada_a_str} = {str(valor)}\n"
                    suma_movimientos += str_entrada
                    relacion = SalidaEntradaRelacion(salida=self, entrada=entrada, cantidad_usada=entrada.cantidad, precio_unitario=entrada.valor_unitario_entrada_a)
                    cantidad_pendiente -= entrada.cantidad
                    entrada.cantidad = 0
                    entrada.save()
                #relacion.save()

            self.valor_total_salida = valor_total 
            self.movimientos = suma_movimientos
            

        super(Salida, self).save(*args, **kwargs)





class SalidaEntradaRelacion(models.Model):
    salida = models.ForeignKey(Salida, on_delete=models.CASCADE, related_name='relaciones_salida')
    entrada = models.ForeignKey(Entrada, on_delete=models.CASCADE, related_name='relaciones_entrada')
    cantidad_usada = models.FloatField()
    precio_unitario = models.FloatField()

    def __str__(self):
        return f"Salida {self.salida.id} - Entrada {self.entrada.id}"

