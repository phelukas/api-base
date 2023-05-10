from rest_framework import serializers
from .models import Usuario, Pessoa
from core.serializers import EnderecoSerializer, TelefoneSerializer

class PessoaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pessoa
        fields = ('primeiro_nome', 'sobre_nome', 'cpf')

    def create(self, validated_data):
        telefone = self.initial_data['telefone']
        endereco = self.initial_data['endereco']
        validated_data['telefone_id'] = telefone
        validated_data['endereco_id'] = endereco
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


