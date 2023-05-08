from rest_framework import serializers
from .models import Usuario, Pessoa
from core.serializers import EnderecoSerializer, TelefoneSerializer

class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField()

    class Meta:
        model = Usuario
        fields = ('email','password',)

    def validate(self, attrs):

        if Usuario.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError(
                {"username": "username existente"})

        return attrs

    def create(self, validated_data, instance=None):
        usuario = Usuario.objects.create(**validated_data)
        usuario.set_password(validated_data['password'])
        usuario.save()
        return usuario

class PessoaSerializer(serializers.ModelSerializer):
    endereco = EnderecoSerializer() 
    telefone = TelefoneSerializer() 

    class Meta:
        model = Pessoa
        fields = '__all__'

class UsuarioAddSerializer(serializers.ModelSerializer):

    pessoa = PessoaSerializer()

    class Meta:
        model = Usuario
        fields = '__all__'
        extra_kwargs = {
            'last_login': {'read_only': True},
            'is_superuser': {'read_only': True},
            'username': {'read_only': True},
            'is_superuser': {'read_only': True},
            'is_staff': {'read_only': True},
            'is_active': {'read_only': True},
            'date_joined': {'read_only': True},
            'user_permissions': {'read_only': True}
        }


    




