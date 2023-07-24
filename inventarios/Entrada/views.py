from rest_framework import generics
from .models import Entrada
from .serializers import EntradaSerializer
from rest_framework.authentication import SessionAuthentication
from rest_framework import status,permissions
from rest_framework.response import Response

class EntradaListCreateView(generics.ListCreateAPIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (SessionAuthentication,)
    serializer_class = EntradaSerializer
    def get(self, request):
        entradas = Entrada.objects.all()
        serializer = EntradaSerializer(entradas, many=True)
        return Response({'fincas': serializer.data}, status=status.HTTP_200_OK)

class EntradaRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (SessionAuthentication,)
    queryset = Entrada.objects.all()
    serializer_class = EntradaSerializer
