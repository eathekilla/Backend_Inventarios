from rest_framework import serializers
from .models import Salida
from Insumo.serializers import Insumo

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
    # Asegúrate de que 'insumo' esté configurado correctamente en tu serializer
    insumo = serializers.PrimaryKeyRelatedField(queryset=Insumo.objects.all())

    class Meta:
        model = Salida
        fields = ['fecha_salida', 'insumo', 'cantidad', 'valor_total_salida', 'entradas']

