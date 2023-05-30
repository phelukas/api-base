from rest_framework import serializers
from .models import Usuario, Pessoa
from core.serializers import EnderecoSerializer, TelefoneSerializer


class PessoaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pessoa
        fields = ("primeiro_nome", "sobre_nome", "cpf")

    def create(self, validated_data):
        telefone = self.initial_data["telefone"]
        endereco = self.initial_data["endereco"]
        validated_data["telefone_id"] = telefone
        validated_data["endereco_id"] = endereco
        return super().create(validated_data)


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ("password", "email")

    def create(self, validated_data, instance=None):
        pessoa = self.initial_data["pessoa"]
        validated_data["pessoa_id"] = pessoa
        usuario = Usuario.objects.create(**validated_data)
        usuario.set_password(validated_data["password"])
        usuario.save()
        return usuario


class AddUsuarioSerializer(serializers.Serializer):
    usuario = UsuarioSerializer()
    pessoa = PessoaSerializer()
    endereco = EnderecoSerializer()
    telefone = TelefoneSerializer()

    def to_representation(self, instance):
        print("aqui viu")
        print(instance)
        pessoa_obj = instance.pessoa
        resp = {
            "usuario": instance.get_usuario,
            "pessoa": pessoa_obj.get_pessoa,
            "endereco": pessoa_obj.endereco.get_endereco,
            "telefone": pessoa_obj.telefone.get_telefone,
        }

        return resp

    def create(self, validated_data):
        usuario_data = validated_data["usuario"]
        pessoa_data = validated_data["pessoa"]
        endereco_data = validated_data["endereco"]
        telefone_data = validated_data["telefone"]

        endereco_serializer = EnderecoSerializer(data=endereco_data)
        telefone_serializer = TelefoneSerializer(data=telefone_data)
        pessoa_serializer = PessoaSerializer(data=pessoa_data)
        usuario_serializer = UsuarioSerializer(data=usuario_data)

        if (
            endereco_serializer.is_valid()
            and telefone_serializer.is_valid()
            and pessoa_serializer.is_valid()
            and usuario_serializer.is_valid()
        ):
            endereco_obj = endereco_serializer.save()
            telefone_obj = telefone_serializer.save()
            pessoa_data["endereco"] = endereco_obj.pk
            pessoa_data["telefone"] = telefone_obj.pk
            pessoa_obj = pessoa_serializer.save()
            usuario_data["pessoa"] = pessoa_obj.pk
            obj = usuario_serializer.save()

            return obj

        raise serializers.ValidationError(
            {
                "error": "Erros de validação",
                "endereco_errors": endereco_serializer.errors,
                "telefone_errors": telefone_serializer.errors,
                "pessoa_errors": pessoa_serializer.errors,
                "usuario_errors": usuario_serializer.errors,
            }
        )

    def update(self, instance, validated_data):
        usuario_data = validated_data.get("usuario", instance)
        pessoa_data = validated_data.get("pessoa", instance.pessoa)
        endereco_data = validated_data.get("endereco", instance.pessoa.endereco)
        telefone_data = validated_data.get("telefone", instance.pessoa.telefone)

        print(usuario_data)
        print(pessoa_data)
        print(endereco_data)
        print(type(telefone_data))

        endereco_serializer = EnderecoSerializer(
            instance.pessoa.endereco, data=endereco_data, partial=True
        )
        telefone_serializer = TelefoneSerializer(
            instance.pessoa.telefone, data=telefone_data, partial=True
        )
        pessoa_serializer = PessoaSerializer(
            instance.pessoa, data=pessoa_data, partial=True
        )
        usuario_serializer = UsuarioSerializer(
            instance, data=usuario_data, partial=True
        )

        is_endereco_valid = endereco_serializer.is_valid()
        is_telefone_valid = telefone_serializer.is_valid()
        is_pessoa_valid = pessoa_serializer.is_valid()
        is_usuario_valid = usuario_serializer.is_valid()

        if (
            is_endereco_valid
            and is_telefone_valid
            and is_pessoa_valid
            and is_usuario_valid
        ):
            endereco_obj = endereco_serializer.save()
            telefone_obj = telefone_serializer.save()
            pessoa_data["endereco"] = endereco_obj.pk
            pessoa_data["telefone"] = telefone_obj.pk
            pessoa_obj = pessoa_serializer.save()
            usuario_data["pessoa"] = pessoa_obj.pk
            obj = usuario_serializer.save()

            return obj
        raise serializers.ValidationError(
            {
                "error": "Erros de validação",
                "endereco_errors": endereco_serializer.errors
                if not is_endereco_valid
                else None,
                "telefone_errors": telefone_serializer.errors
                if not is_telefone_valid
                else None,
                "pessoa_errors": pessoa_serializer.errors
                if not is_pessoa_valid
                else None,
                "usuario_errors": usuario_serializer.errors
                if not is_usuario_valid
                else None,
            }
        )
