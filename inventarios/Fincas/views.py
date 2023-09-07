from django.contrib.auth import get_user_model, authenticate, login, logout
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer,UserSerializerLogout,FincaSerializer,FincaBodegaLoteSerializer
from .serializers import LotesSerializer, BodegasSerializer, FincaSerializer,FincaSerializerRel
from .models import Finca
from rest_framework import status,permissions,generics
from rest_framework import serializers
from .models import Lotes, Bodegas, Finca




UserModel = get_user_model()

class UserRegister(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegisterSerializer
    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user_obj = serializer.save()
            return Response({'message': 'User created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogin(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserLoginSerializer
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.check_user(serializer.validated_data)
            login(request, user)
            return Response({'message': 'User logged in'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogout(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({'message': 'User logged out'}, status=status.HTTP_200_OK)
    
class UserView(APIView):
	permission_classes = (permissions.IsAuthenticated,)

	##
	def get(self, request):
		serializer = UserSerializer(request.user)
		return Response({'user': serializer.data}, status=status.HTTP_200_OK)

class FincaView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        fincas = Finca.objects.all()
        serializer = FincaSerializer(fincas, many=True)
        return Response({'fincas': serializer.data}, status=status.HTTP_200_OK)

class FincaList(generics.ListCreateAPIView):
    serializer_class = FincaBodegaLoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filtrar las fincas por el usuario autenticado
        user = self.request.user
        return Finca.objects.filter(usuario=user)
    


class LotesListCreateView(generics.ListCreateAPIView):
    queryset = Lotes.objects.all()
    serializer_class = LotesSerializer

class LotesRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lotes.objects.all()
    serializer_class = LotesSerializer

class BodegasListCreateView(generics.ListCreateAPIView):
    queryset = Bodegas.objects.all()
    serializer_class = BodegasSerializer

class BodegasRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bodegas.objects.all()
    serializer_class = BodegasSerializer

class FincaListCreateView(generics.ListCreateAPIView):
    queryset = Finca.objects.all()
    serializer_class = FincaSerializer

class FincaRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Finca.objects.all()
    serializer_class = FincaSerializer


class FincaRelListCreateView(generics.ListCreateAPIView):
    queryset = Finca.objects.all()
    serializer_class = FincaSerializerRel 
