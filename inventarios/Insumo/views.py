from rest_framework import generics
from .models import IngredienteActivo, Certificacion, UnidadMedida, Insumo, Grupo
from .serializers import IngredienteActivoSerializer, CertificacionSerializer, UnidadMedidaSerializer, InsumoSerializer, GrupoSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status,generics
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.db.models import Sum
from Entrada.models import Entrada
from Insumo.models import Insumo
import json

class IngredienteActivoListCreateView(generics.ListCreateAPIView):
    queryset = IngredienteActivo.objects.all()
    serializer_class = IngredienteActivoSerializer

class IngredienteActivoRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = IngredienteActivo.objects.all()
    serializer_class = IngredienteActivoSerializer

class CertificacionListCreateView(generics.ListCreateAPIView):
    queryset = Certificacion.objects.all()
    serializer_class = CertificacionSerializer

class CertificacionRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Certificacion.objects.all()
    serializer_class = CertificacionSerializer

class UnidadMedidaListCreateView(generics.ListCreateAPIView):
    queryset = UnidadMedida.objects.all()
    serializer_class = UnidadMedidaSerializer

class UnidadMedidaRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UnidadMedida.objects.all()
    serializer_class = UnidadMedidaSerializer

class InsumoListCreateView(generics.ListCreateAPIView):
    queryset = Insumo.objects.all()
    serializer_class = InsumoSerializer

class InsumoRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Insumo.objects.all()
    serializer_class = InsumoSerializer

class GrupoListCreateView(generics.ListCreateAPIView):
    queryset = Grupo.objects.all()
    serializer_class = GrupoSerializer

class GrupoRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Grupo.objects.all()
    serializer_class = GrupoSerializer

@api_view(['GET'])
def consultar_insumos_grupo(request, grupo_id):
    try:
        grupo = Grupo.objects.get(pk=grupo_id)
        insumos = grupo.insumos.all()
        
        insumos_data = [{"id": insumo.id, "nombre": insumo.nombre} for insumo in insumos]
        
        return JsonResponse({"success": True, "insumos": insumos_data})
    except Grupo.DoesNotExist:
        return JsonResponse({"success": False, "message": "Grupo no encontrado"})

@api_view(['GET','PUT'])
def edit_info_proveedor(request, pk):
    try:
        insumo =  get_object_or_404(Insumo,pk=pk)
    except Insumo.DoesNotExist:
        return Response({"message": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    
    '''if request.method == 'PUT':
        serializer = EditeUserWithInfoUserSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.update()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)'''
    
    if request.method == 'GET':
        insumo =  get_object_or_404(Insumo,pk=pk)  # Obtén los grupos a los que pertenece el usuario
        proveedor_data = {
                    "id": insumo.pk,
                    "nombre": insumo.nombre,
                    "codigo_contable": insumo.codigo_contable,
                    "unidad_medida": insumo.unidad_medida.pk,
                    "certificacion": insumo.certificacion.pk,
                    }
    
        return Response(proveedor_data, status=status.HTTP_200_OK)
    return Response({"message": "Proveedor no encontrado"}, status=status.HTTP_404_NOT_FOUND)




@api_view(['GET','PUT'])
def edit_ingrediente(request, pk):
    try:
        ingrediente =  get_object_or_404(IngredienteActivo,pk=pk)
    except Insumo.DoesNotExist:
        return Response({"message": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'PUT':
        serializer = IngredienteActivoSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.update()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'GET':
        ingrediente =  get_object_or_404(IngredienteActivo,pk=pk)  # Obtén los grupos a los que pertenece el usuario
        ingrediente_data = {
                    "id": ingrediente.pk,
                    "nombre": ingrediente.nombre,
                    }
        return Response(ingrediente_data, content_type='application/json', status=status.HTTP_200_OK)
    return Response({"message": "Ingrediente no encontrado"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET','PUT'])
def edit_certificacion(request, pk):
    try:
        certificacion =  get_object_or_404(Certificacion,pk=pk)
    except Insumo.DoesNotExist:
        return Response({"message": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'PUT':
        serializer = CertificacionSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.update()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'GET':
        certificacion =  get_object_or_404(Certificacion,pk=pk)  # Obtén los grupos a los que pertenece el usuario
        certificacion_data={    "periodo_carencia": certificacion.periodo_carencia,
                                "periodo_reingreso": certificacion.periodo_reingreso,
                                "registro_ica": certificacion.registro_ica,
                                "fecha_registro": certificacion.fecha_registro,
                                "ingrediente_activo": certificacion.ingrediente_activo_id  }
        return Response(certificacion_data, content_type='application/json', status=status.HTTP_200_OK)
    return Response({"message": "Certificacion no encontrada"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET','PUT'])
def edit_unidad(request, pk):
    try:
        unidad =  get_object_or_404(UnidadMedida,pk=pk)
    except Insumo.DoesNotExist:
        return Response({"message": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'PUT':
        serializer = UnidadMedidaSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.update()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'GET':
        unidad =  get_object_or_404(UnidadMedida,pk=pk)  # Obtén los grupos a los que pertenece el usuario
        unidad_data = {
                    "id": unidad.pk,
                    "nombre": unidad.nombre,
                    }
        return Response(unidad_data, content_type='application/json', status=status.HTTP_200_OK)
    return Response({"message": "Ingrediente no encontrado"}, status=status.HTTP_404_NOT_FOUND)




def cantidad_total_insumo(request, id_insumo):
    insumo = get_object_or_404(Insumo,id=id_insumo)
    unidad_medida = insumo.unidad_medida
    return JsonResponse({'unidad_medida': unidad_medida.nombre})
