from rest_framework import generics
from .models import Salida
from .serializers import SalidaSerializer
from rest_framework.authentication import SessionAuthentication
from rest_framework import status,permissions
from rest_framework.response import Response
from Insumo.models import Insumo
from Entrada.models import Entrada
from django.core.exceptions import ValidationError

class SalidaListCreateView(generics.ListCreateAPIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (SessionAuthentication,)
    serializer_class = SalidaSerializer
    def get(self, request):
        salidas = Salida.objects.all()
        serializer = SalidaSerializer(salidas, many=True)
        return Response({'salidas': serializer.data}, status=status.HTTP_200_OK)
    
class SalidaCreateView(generics.CreateAPIView):
    serializer_class = SalidaSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        insumo_id = serializer.validated_data['insumo']
        cantidad_salida = serializer.validated_data['cantidad']

        try:
            insumo = Insumo.objects.get(pk=insumo_id.id)
        except Insumo.DoesNotExist:
            return Response({'error': 'El insumo especificado no existe.'}, status=status.HTTP_400_BAD_REQUEST)

        # Obtener las entradas ordenadas por fecha ascendente
        entradas = Entrada.objects.filter(insumo=insumo).order_by('fecha_creacion')
        cantidad_disponible_total = sum(entrada.cantidad for entrada in entradas)

        if cantidad_salida > cantidad_disponible_total:
            return Response({'error': 'La cantidad de salida es mayor a la cantidad disponible.'}, status=status.HTTP_400_BAD_REQUEST)

        Salida.objects.create(insumo_id=insumo_id.id, cantidad=serializer.validated_data['cantidad'])

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class SalidaRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (SessionAuthentication,)
    queryset = Salida.objects.all()
    serializer_class = SalidaSerializer


class SalidaCreateAPIView(generics.CreateAPIView):
    queryset = Salida.objects.all()
    serializer_class = SalidaSerializer

    def create(self, request, *args, **kwargs):
        try:
            return super(SalidaCreateAPIView, self).create(request, *args, **kwargs)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SalidaListAPIView(generics.ListAPIView):
    queryset = Salida.objects.all()
    serializer_class = SalidaSerializer


class SalidaEntradaAPIView(generics.CreateAPIView):
    queryset = Salida.objects.all()
    serializer_class = SalidaSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        try:

            # Obtener los datos del request
            data = request.data
            if request.user.username != 'simpleagriuser@a.com' and not request.user.is_superuser:
                return Response({'detail': 'No tienes permiso para acceder a esta vista.'}, status=403)

            # Verificar si se proporciona una entrada manualmente
            entrada_id = data.get('entrada_id')
            if entrada_id:
                selected_entrada = Entrada.objects.get(pk=entrada_id)
                # Crear la salida con la entrada seleccionada
                salida_serializer = self.get_serializer(data=data)
                salida_serializer.is_valid(raise_exception=True)
                self.perform_create_with_selected_entrada(salida_serializer, selected_entrada)
                headers = self.get_success_headers(salida_serializer.data)
                return Response(salida_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            else:
                # Crear la salida de manera normal
                return super(SalidaCreateAPIView, self).create(request, *args, **kwargs)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def perform_create_with_selected_entrada(self, serializer, selected_entrada):
        serializer.save()
        # Llamar al nuevo método en el modelo para manejar la entrada seleccionada
        serializer.instance.save_with_selected_entrada(selected_entrada)


class SalidaReverseAPIView(generics.DestroyAPIView):
    queryset = Salida.objects.all()
    serializer_class = SalidaSerializer
    permission_classes = (permissions.AllowAny,)

    def destroy(self, request, *args, **kwargs):
        try:
            if request.user.username != 'simpleagriuser@a.com' and not request.user.is_superuser:
                return Response({'detail': 'No tienes permiso para acceder a esta vista.'}, status=403)
            instance = self.get_object()
            instance.reverse()
            
            return Response({'detail': 'Reversa exitosa'}, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

