from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError
from Fincas.models import Finca, Lotes, Bodegas

UserModel = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserModel
		fields = (
			'email',
			'password',
			'groups',
		)
	def create(self, clean_data):
		user_obj = UserModel.objects.create_user(email=clean_data['email'], password=clean_data['password'],username = clean_data['email'])
		user_obj.groups.set(clean_data['groups'])
		user_obj.save()
		return user_obj

class UserLoginSerializer(serializers.Serializer):
	email = serializers.CharField()
	password = serializers.CharField()
	##
	def check_user(self, clean_data):
		user = authenticate(username=clean_data['email'], password=clean_data['password'])
		if not user:
			raise ValidationError('user not foundd')
		return user

class UserSerializerLogout(serializers.ModelSerializer):
	class Meta:
		model = UserModel
		fields = ['email']

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserModel
		fields = ('__all__')

class FincaSerializer(serializers.ModelSerializer):
	class Meta:
		model = Finca
		fields = ('__all__')

class LotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lotes
        fields = ['id','nombre_lote']

class BodegasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bodegas
        fields = ['id','nombre_bodega']
	
class FincaBodegaLoteSerializer(serializers.ModelSerializer):
    lotes_finca = serializers.SerializerMethodField()
    bodegas_finca = serializers.SerializerMethodField()

    class Meta:
        model = Finca
        fields = ['id','nombre_finca','lotes_finca','bodegas_finca']

    def get_lotes_finca(self, obj):
        # Filtra los lotes asociados a la finca y al usuario actual
        user = self.context['request'].user
        return LotesSerializer(obj.lotes.filter(usuario=user), many=True).data

    def get_bodegas_finca(self, obj):
        # Filtra las bodegas asociadas a la finca y al usuario actual
        user = self.context['request'].user
        return BodegasSerializer(obj.bodegas.filter(usuario=user), many=True).data