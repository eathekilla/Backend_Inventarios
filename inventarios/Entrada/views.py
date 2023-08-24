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

class EntradaListCreateView(generics.ListCreateAPIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (SessionAuthentication,)
    serializer_class = EntradaSerializer
    def get(self, request):
        entradas = Entrada.objects.all()
        serializer = EntradaSerializer(entradas, many=True)
        return Response({'entradas': serializer.data}, status=status.HTTP_200_OK)

class EntradaRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (SessionAuthentication,)
    queryset = Entrada.objects.all()
    serializer_class = EntradaSerializer

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