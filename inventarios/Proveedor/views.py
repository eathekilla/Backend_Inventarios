from rest_framework import generics
from .models import Proveedor
from .serializers import ProveedorSerializer
from rest_framework.response import Response
from rest_framework import status,generics
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404

class ProveedorListCreateView(generics.ListCreateAPIView):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer

class ProveedorRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer


@api_view(['GET','PUT'])
def edit_info_proveedor(request, pk):
    try:
        proveedor =  get_object_or_404(Proveedor,pk=pk)
    except Proveedor.DoesNotExist:
        return Response({"message": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    
    '''if request.method == 'PUT':
        serializer = EditeUserWithInfoUserSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.update()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)'''
    
    if request.method == 'GET':
        proveedor =  get_object_or_404(Proveedor,pk=pk)  # Obtén los grupos a los que pertenece el usuario

        proveedor_data = {
                    "id": proveedor.pk,
                    "nit_cedula": proveedor.nit_cedula,
                    "razon_social": proveedor.razon_social,
                    "representante_legal": proveedor.representante_legal,
                    "direccion": proveedor.direccion,
                    "telefono": proveedor.telefono,
                    "email": proveedor.email,
                    "vereda": proveedor.vereda,
                    "departamento": proveedor.departamento,
                    "municipio": proveedor.municipio,
                    "barrio": proveedor.barrio
                    }
    
        return Response(proveedor_data, content_type='application/json', status=status.HTTP_200_OK)
    return Response({"message": "Proveedor no encontrado"}, status=status.HTTP_404_NOT_FOUND)
