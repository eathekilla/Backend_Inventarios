from rest_framework import serializers
from .models import IngredienteActivo, Certificacion, UnidadMedida, Insumo, Grupo

class IngredienteActivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngredienteActivo
        fields = '__all__'

class CertificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificacion
        fields = '__all__'

class UnidadMedidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadMedida
        fields = '__all__'

class InsumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insumo
        fields = '__all__'

class GrupoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grupo
        fields = '__all__'
