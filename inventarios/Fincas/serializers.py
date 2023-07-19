from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError
from Fincas.models import Finca

UserModel = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserModel
		fields = (
			'email',
			'password',
		)
	def create(self, clean_data):
		user_obj = UserModel.objects.create_user(email=clean_data['email'], password=clean_data['password'],username = clean_data['email'])
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