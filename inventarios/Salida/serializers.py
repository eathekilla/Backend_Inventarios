from rest_framework import serializers
from .models import Salida
from Insumo.serializers import InsumoSerializer
from Entrada.models import Entrada

class SalidaSerializer(serializers.ModelSerializer):
    #insumo = InsumoSerializer()
    class Meta:
        model = Salida
        fields = '__all__'
    def validate(self, data):
        insumo = data['insumo']
        cantidad_salida = data['cantidad']

        entradas = Entrada.objects.filter(insumo=insumo).order_by('fecha_ingreso')
        cantidad_disponible_total = sum(entrada.cantidad for entrada in entradas)

        if cantidad_salida > cantidad_disponible_total:
            raise serializers.ValidationError("La cantidad de salida es mayor a la cantidad disponible.")

        return data
