from rest_framework import serializers
from .models import Salida
from Insumo.serializers import InsumoSerializer
from Entrada.models import Entrada

class SalidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salida
        fields = ('fecha_salida','insumo','cantidad','valor_total_salida')
        extra_kwargs = {
            'entradas': {'required': False}
        }

class SalidaAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = Salida
        fields = ('id','fecha_salida','insumo','cantidad','valor_total_salida')
        extra_kwargs = {
            'entradas': {'required': False}
        }


class SalidaCreateSerializer(serializers.ModelSerializer):
    codigo_contable = serializers.CharField(source='insumo__codigo_contable', required=False)  # Haciendo el campo opcional

    class Meta:
        model = Salida
        fields = ('id','fecha_salida', 'codigo_contable', 'cantidad','valor_total_salida')