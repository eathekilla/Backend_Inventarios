from rest_framework import serializers
from .models import Entrada
from Insumo.models import Insumo
from Insumo.serializers import InsumoSerializer

class EntradaSerializer(serializers.ModelSerializer):
    insumo_id = serializers.PrimaryKeyRelatedField(source='insumo', queryset=Insumo.objects.all(), write_only=True)

    class Meta:
        model = Entrada
        fields = ['fecha_creacion', 'fecha_ingreso', 'de_finca', 'a_finca', 'cantidad', 'valor_unitario_entrada_a', 'total_entra_a_la_finca', 'identificador', 'insumo']

    def create(self, validated_data):
        insumo_id = validated_data.pop('insumo_id')
        entrada = Entrada.objects.create(insumo_id=insumo_id, **validated_data)
        return entrada

class EntradaSerializerHistorico(serializers.ModelSerializer):
    insumo = InsumoSerializer()
    class Meta:
        model = Entrada
        fields = '__all__'
