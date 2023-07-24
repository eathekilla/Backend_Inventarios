from rest_framework import generics
from .models import IngredienteActivo, Certificacion, UnidadMedida, Insumo, Grupo
from .serializers import IngredienteActivoSerializer, CertificacionSerializer, UnidadMedidaSerializer, InsumoSerializer, GrupoSerializer

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
