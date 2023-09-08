from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError
from Fincas.models import Finca, Lotes, Bodegas
from django.contrib.auth.models import User

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


class LotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lotes
        fields = '__all__'

class BodegasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bodegas
        fields = '__all__'

class FincaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Finca
        fields = '__all__'
        


class BodegaSerializerRel(serializers.ModelSerializer):
    class Meta:
        model = Bodegas
        fields = '__all__'

class LoteSerializerRel(serializers.ModelSerializer):
    bodegas = BodegaSerializerRel(many=True, read_only=True)

    class Meta:
        model = Lotes
        fields = '__all__'

class FincaSerializerRel(serializers.ModelSerializer):
    lotes = LoteSerializerRel(many=True, read_only=True)

    class Meta:
        model = Finca
        fields = '__all__'


from .models import InfoUser

class InfoUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfoUser
        fields = ('telefono', 'direccion', 'tipo_documento', 'numero_documento')


class EditInfoUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfoUser
        fields = ('telefono', 'direccion', 'tipo_documento', 'numero_documento')

class CreateUserWithInfoUserSerializer(serializers.ModelSerializer):
    info_user = InfoUserSerializer()  # Serializador de InfoUser
    
    class Meta:
        model = User
        fields = ('email','password','groups','info_user')
        extra_kwargs = {
            'password': {'write_only': True},
        }

        

    def create(self, validated_data):
        # Extrae los datos de info_user del validated_data
        info_user_data = validated_data.pop('info_user')
        user_obj = UserModel.objects.create_user(email=validated_data['email'], password=validated_data['password'],username = validated_data['email'])
        user_obj.groups.set(validated_data['groups'])
        user_obj.save()
        
        info_usuario = self.data['info_user']
        # Crea un InfoUser relacionado con el usuario
        InfoUser.objects.create(usuario=user_obj, telefono=info_usuario['telefono'],direccion=info_usuario['direccion'],tipo_documento=info_usuario['tipo_documento'],numero_documento=info_usuario['numero_documento'])
        
        return user_obj
    

class InfoUserSerializerDetail(serializers.ModelSerializer):
    class Meta:
        model = InfoUser
        fields = ('telefono', 'direccion', 'tipo_documento', 'numero_documento')

class UserDetailSerializer(serializers.ModelSerializer):
    info_user = InfoUserSerializerDetail()  # Serializador de InfoUser
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'info_user', 'groups')