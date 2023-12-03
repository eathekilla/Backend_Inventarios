from rest_framework import serializers
from .models import Proveedor

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = ('nit_cedula','tipo_documento','razon_social')
        extra_kwargs = {
            'representante_legal': {'required': False},
            'direccion': {'required': False},
            'telefono': {'required': False},
            'vereda': {'required': False},
            'email': {'required': False},
            'departamento': {'required': False},
            'municipio': {'required': False},
            'barrio': {'required': False},

        }

