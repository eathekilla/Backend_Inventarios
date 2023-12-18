from django.db import models
from Insumo.models import Insumo
from Entrada.models import Entrada
from datetime import datetime
from django.core.exceptions import ValidationError
from django.db.models import Sum


class Salida(models.Model):
    fecha_salida = models.DateTimeField(default=datetime.now)
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE)
    cantidad = models.FloatField(default=0)
    valor_total_salida = models.FloatField(default=0)
    entradas = models.ManyToManyField(Entrada, related_name='salidas_entradas')
    movimientos=models.TextField(default='', null=True)
    

    def __str__(self):
        return f"Salida - {self.fecha_salida} - {self.insumo.nombre}"
    
    def save(self, *args, **kwargs):
        es_nueva_instancia = not self.pk
        suma_movimientos = ""
        entradas_rel = []

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
                    str_entrada = f"- Cant {cantidad_pendiente_str} * Vrl/u {formatear_como_divisa(valor_unitario_entrada_a_str)} = {formatear_como_divisa(valor)} ({entrada.pk})\n"
                    suma_movimientos += str_entrada
                    entradas_rel.append(entrada)
                    entrada.cantidad -= cantidad_pendiente
                    entrada.save()
                    break
                else:
                    valor_total += entrada.cantidad * entrada.valor_unitario_entrada_a
                    valor = str(entrada.cantidad * entrada.valor_unitario_entrada_a)
                    valor_unitario_entrada_a_str=str(entrada.valor_unitario_entrada_a)
                    cantidad_pendiente_str = str(entrada.cantidad)
                    if entrada.cantidad > 0:
                        str_entrada = f"- Cant {cantidad_pendiente_str} * Vrl/u {formatear_como_divisa(valor_unitario_entrada_a_str)} = {formatear_como_divisa(valor)} ({entrada.pk})\n"
                        suma_movimientos += str_entrada
                    cantidad_pendiente -= entrada.cantidad
                    entrada.cantidad = 0
                    entradas_rel.append(entrada)
                    entrada.save()

            self.valor_total_salida = valor_total 
            self.movimientos = suma_movimientos  

        super(Salida, self).save(*args, **kwargs)
        # Añadir las entradas a la salida después de que se haya guardado la salida
        for entrada in entradas:
            self.entradas.add(entrada)
        
    def save_with_selected_entrada(self, selected_entrada, *args, **kwargs):
        # Verificar que la entrada seleccionada pertenezca al mismo insumo
        if selected_entrada.insumo != self.insumo:
            raise ValidationError("La entrada seleccionada no corresponde al mismo insumo.")

        # Verificar que la cantidad de la entrada seleccionada sea suficiente
        if selected_entrada.cantidad < self.cantidad:
            raise ValidationError("La cantidad de la entrada seleccionada no es suficiente.")

        # Realizar el descuento directamente de la entrada seleccionada
        valor_total = self.cantidad * selected_entrada.valor_unitario_entrada_a
        valor_unitario_entrada_a_str = str(selected_entrada.valor_unitario_entrada_a)
        cantidad_str = str(self.cantidad)
        str_entrada = f"- Cant {cantidad_str} * Vrl/u {formatear_como_divisa(valor_unitario_entrada_a_str)} = {formatear_como_divisa(valor_total)} ({selected_entrada.pk})\n"

        # Actualizar la entrada seleccionada y la salida
        selected_entrada.cantidad -= self.cantidad
        selected_entrada.save()

        self.valor_total_salida = valor_total
        self.movimientos = str_entrada

        # Limpiar las otras entradas relacionadas
        self.entradas.clear()

        # Añadir la entrada seleccionada a la salida
        self.entradas.add(selected_entrada)

        super(Salida, self).save(*args, **kwargs)

    
    def reverse(self):
        # Asumiendo que tienes un campo en el modelo Salida que almacena las entradas relacionadas
        for entrada in self.entradas.all():
            # Devuelve la cantidad de la salida a la entrada correspondiente
            entrada.cantidad += self.cantidad
            entrada.save()

        # Elimina la salida
        self.delete()






import locale

def formatear_como_divisa(numero):
    locale.setlocale(locale.LC_ALL, 'es_CO.utf-8')

    # Asegurarse de que el número sea de tipo float
    numero = float(numero)

    # Formatear el número como divisa colombiana
    return locale.currency(numero, grouping=True)