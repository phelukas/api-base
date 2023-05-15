from rest_framework import serializers
from .models import Usuario, Pessoa
from core.serializers import EnderecoSerializer, TelefoneSerializer
from rest_framework.exceptions import ValidationError

from rest_framework.validators import UniqueValidator

from rest_framework.validators import UniqueValidator

class CustomUniqueValidator:
    def __init__(self, queryset, message=None, lookup=None):
        self.queryset = queryset
        self.message = message or 'This field must be unique.'
        self.lookup = lookup or 'exact'

    def __call__(self, value):
        filter_kwargs = {self.field_name: value}

        if self.queryset.filter(**filter_kwargs).exists():
            raise serializers.ValidationError(self.message)

# Uso do CustomUniqueValidator no 
class PessoaSerializer(serializers.ModelSerializer):
    # cpf = serializers.CharField(validators=[CustomUniqueValidator(queryset=Pessoa.objects.all())])

    
    class Meta:
        
        model = Pessoa
        fields = ('primeiro_nome', 'sobre_nome', 'cpf')

    def custom_name():
        return "gabriel"

    def create(self, validated_data):
        telefone = self.initial_data['telefone']
        endereco = self.initial_data['endereco']
        validated_data['telefone_id'] = telefone
        validated_data['endereco_id'] = endereco
        print("validação de pessoa")
        return super().create(validated_data)

class UsuarioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Usuario
        fields = ('password','email')

    def create(self, validated_data, instance=None):
        pessoa = self.initial_data['pessoa']
        validated_data['pessoa_id'] = pessoa
        usuario = Usuario.objects.create(**validated_data)
        usuario.set_password(validated_data['password'])
        usuario.save()
        return usuario

class AddUsuarioSerializer(serializers.Serializer):
    usuario = UsuarioSerializer()
    pessoa = PessoaSerializer()
    endereco = EnderecoSerializer() 
    telefone = TelefoneSerializer()

    def validate(self, attrs):
        print("estou aqui na validações")
        return super().validate(attrs)
    
