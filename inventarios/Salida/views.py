from rest_framework import generics
from .models import Salida
from .serializers import SalidaSerializer
from rest_framework.authentication import SessionAuthentication
from rest_framework import status,permissions
from rest_framework.response import Response
from Insumo.models import Insumo
from Entrada.models import Entrada

class SalidaListCreateView(generics.ListCreateAPIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (SessionAuthentication,)
    serializer_class = SalidaSerializer
    def get(self, request):
        salidas = Salida.objects.all()
        serializer = SalidaSerializer(salidas, many=True)
        return Response({'fincas': serializer.data}, status=status.HTTP_200_OK)
    
class SalidaCreateView(generics.CreateAPIView):
    serializer_class = SalidaSerializer

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
        entradas = Entrada.objects.filter(insumo=insumo).order_by('desde')
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
