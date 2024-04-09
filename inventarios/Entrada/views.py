from django.shortcuts import get_object_or_404, redirect
from rest_framework import generics
from .models import Entrada
from Insumo.models import Insumo
from Salida.models import Salida
from .serializers import EntradaSerializer,EntradaSerializerHistorico
from rest_framework.authentication import SessionAuthentication
from rest_framework import status,permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import models
from itertools import groupby
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse
from rest_framework.parsers import MultiPartParser
import boto3
from django.conf import settings
from botocore.exceptions import ClientError
AWS_STORAGE_BUCKET_NAME = settings.AWS_STORAGE_BUCKET_NAME

class EntradaListCreateView(generics.ListCreateAPIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (SessionAuthentication,)
    serializer_class = EntradaSerializer
    parser_classes = (MultiPartParser,) 

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os

class EntradaRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EntradaSerializer
    def get_queryset(self):
        return Entrada.objects.all()  # Sobrescribe el método get_queryset

    def put(self, request, *args, **kwargs):
        instance = self.get_object()

        # Verifica si la casilla de verificación está marcada
        mantener_archivo = request.data.get('mantener_archivo', False)

        if not mantener_archivo:
            # El usuario ha subido un nuevo archivo, maneja lógica de archivo aquí
            nuevo_archivo = request.FILES.get('factura')
            if nuevo_archivo:
                # Sube el nuevo archivo a AWS y actualiza la referencia en el modelo
                archivo_nombre = f"comprobantes_inventarios/{instance.identificador}/{nuevo_archivo.name}"
                default_storage.save(archivo_nombre, ContentFile(nuevo_archivo.read()))
                instance.factura.name = archivo_nombre

        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class InventarioHistoricoView(generics.ListAPIView):
    serializer_class = EntradaSerializer

    def get_queryset(self):
        insumo_id = self.kwargs['insumo_id']
        return Entrada.objects.filter(insumo_id=insumo_id).order_by('desde')

class InventarioEstadoActualView(APIView):
    def get(self, request, format=None):
        insumos = Insumo.objects.all()
        estado_actual = []

        for insumo in insumos:
            entradas = Entrada.objects.filter(insumo=insumo)

            cantidad_disponible = sum(entrada.cantidad for entrada in entradas)

            if cantidad_disponible > 0:
                insumo_data = {
                    'id': insumo.id,
                    'nombre': insumo.nombre,
                    'cantidad_disponible': cantidad_disponible
                }
                estado_actual.append(insumo_data)

        return Response(estado_actual)


class InventarioExistenciaView(APIView):
    def get(self, request, format=None):
        entradas = Entrada.objects.all()
        entradas_con_existencia = []

        for entrada in entradas:
            total_salidas = Salida.objects.filter(insumo=entrada.insumo).aggregate(total_salidas=models.Sum('cantidad'))['total_salidas']
            cantidad_disponible = entrada.cantidad - (total_salidas or 0)

            entrada_data = {
                'id': entrada.id,
                'insumo': {
                    'id': entrada.insumo.id,
                    'nombre': entrada.insumo.nombre,
                    'codigo_contable': entrada.insumo.codigo_contable,
                },
                'cantidad_disponible': cantidad_disponible,
                'valor': entrada.valor_unitario_entrada_a,
                'fecha': entrada.fecha_ingreso,
            }
            entradas_con_existencia.append(entrada_data)

        return Response(entradas_con_existencia)

class EntradaHistoricoView(generics.ListAPIView):
    serializer_class = EntradaSerializer

    def get_queryset(self):
        historial = Entrada.history.all().order_by('history_date')

        # Crear un diccionario para agrupar las instancias históricas por el campo identificador (ID)
        grupos = {}
        for entrada in historial:
            identificador = entrada.identificador
            if identificador not in grupos:
                grupos[identificador] = [entrada]
            else:
                grupos[identificador].append(entrada)

        # Ordenar los grupos por fecha de historial en orden ascendente
        historial_ordenado = []
        for identificador, grupo in sorted(grupos.items(), key=lambda item: item[1][0].history_date):
            historial_ordenado.extend(grupo)

        return historial_ordenado


class EntradaHistoricoView(generics.ListAPIView):
    serializer_class = EntradaSerializer

    def get_queryset(self):
        historial = Entrada.history.all().order_by('history_date')

        # Crear un diccionario para agrupar las instancias históricas por el campo identificador (ID)
        grupos = {}
        for entrada in historial:
            identificador = entrada.identificador
            if identificador not in grupos:
                grupos[identificador] = [entrada]
            else:
                grupos[identificador].append(entrada)

        # Ordenar los grupos por fecha de historial en orden ascendente
        historial_ordenado = []
        for identificador, grupo in sorted(grupos.items(), key=lambda item: item[1][0].history_date):
            historial_ordenado.extend(grupo)

        return historial_ordenado

class EntradaPrimerHistoricoView(generics.ListAPIView):
    serializer_class = EntradaSerializer

    def get_queryset(self):
        historial = Entrada.history.all().order_by('history_date')

        # Crear un diccionario para almacenar el primer registro de cada grupo por el campo identificador (ID)
        primeros_registros = {}
        for entrada in historial:
            identificador = entrada.identificador
            if identificador not in primeros_registros:
                primeros_registros[identificador] = entrada

        # Ordenar los registros por fecha de historial en orden ascendente
        historial_ordenado = sorted(primeros_registros.values(), key=lambda entrada: entrada.history_date)

        return historial_ordenado
    
def entradas_proximas_a_vencer(request):
    hoy = timezone.now()
    limite = hoy + timedelta(days=10)
    entradas = Entrada.objects.filter(fecha_vencimiento__range=(hoy, limite))
    data = [{"fecha_creacion": e.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S'),
             "fecha_vencimiento": e.fecha_vencimiento.strftime('%Y-%m-%d %H:%M:%S'),
             "insumo": e.insumo.nombre,  # Asumiendo que el modelo Insumo tiene un campo llamado 'nombre'
             "identificador": e.identificador} for e in entradas]
    return JsonResponse(data, safe=False)

def comprobante(request,pk):
    entrada = get_object_or_404(Entrada,pk=pk)
    s3_client = boto3.client(
    's3',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

    try:
        response = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': AWS_STORAGE_BUCKET_NAME,
                'Key': entrada.factura.name
            },
            ExpiresIn=360
        )
        return redirect(f'{response}')
    except ClientError as e:
        # Manejar cualquier error de generación de URL firmada

        return redirect('/')
    


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from .models import Entrada

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework.views import APIView
from django.db.models import Sum
from .models import Entrada
from rest_framework.permissions import IsAuthenticated
@method_decorator(csrf_exempt, name='dispatch')  # Añade este decorador si necesitas desactivar la protección CSRF
class EntradasListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        if request.user.username != 'simpleagriuser@a.com' and not request.user.is_superuser:
            return Response({'detail': 'No tienes permiso para acceder a esta vista.'}, status=403)
        # Agrupa y suma las entradas por insumo y bodega
        entradas_agrupadas = Entrada.objects.values(
            'insumo__codigo_contable',
            'bodega__codigo'
        ).annotate(
            cantidad_total=Sum('cantidad')
        )

        entradas_list = []

        for entrada_agrupada in entradas_agrupadas:
            insumo_codigo = entrada_agrupada['insumo__codigo_contable']
            bodega_codigo = entrada_agrupada['bodega__codigo']
            cantidad_total = entrada_agrupada['cantidad_total']

            entrada_data = {
                'codigo_insumo': insumo_codigo,
                'codigo_bodega': bodega_codigo,
                'cantidad_total': cantidad_total,
            }

            entradas_list.append(entrada_data)

        return JsonResponse({'entradas_agrupadas': entradas_list}, safe=False)


@method_decorator(csrf_exempt, name='dispatch')  # Añade este decorador si necesitas desactivar la protección CSRF
class EntradasPorInsumoView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, codigo_insumo, *args, **kwargs):
        # Filtra las entradas por el código de insumo
        if request.user.username != 'simpleagriuser@a.com' and not request.user.is_superuser:
            return Response({'detail': 'No tienes permiso para acceder a esta vista.'}, status=403)
        entradas = Entrada.objects.filter(insumo__codigo_contable=codigo_insumo)

        entradas_list = []

        for entrada in entradas:
            bodega_codigo = entrada.bodega.id if entrada.bodega else None
            cantidad = entrada.cantidad
            precio_entrada = entrada.valor_unitario_entrada_a

            entrada_data = {
                'codigo_bodega': bodega_codigo,
                'cantidad': cantidad,
                'precio_entrada': precio_entrada,
            }

            entradas_list.append(entrada_data)

        return JsonResponse({'entradas_por_insumo': entradas_list}, safe=False)
