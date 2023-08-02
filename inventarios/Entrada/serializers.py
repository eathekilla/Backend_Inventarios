from rest_framework import serializers
from .models import Entrada
from Insumo.serializers import InsumoSerializer

class EntradaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entrada
        fields = '__all__'

class EntradaSerializerHistorico(serializers.ModelSerializer):
    insumo = InsumoSerializer()
    class Meta:
        model = Entrada
        fields = '__all__'
