from rest_framework import serializers
from .models import Salida
from Insumo.serializers import InsumoSerializer
from Entrada.models import Entrada

class SalidaSerializer(serializers.ModelSerializer):
    #insumo = InsumoSerializer()
    class Meta:
        model = Salida
        fields = '__all__'
