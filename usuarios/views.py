from rest_framework.exceptions import ValidationError
from usuarios.models import Usuario
from usuarios.serializers import AddUsuarioSerializer, PessoaSerializer, UsuarioSerializer
from core.serializers import EnderecoSerializer, TelefoneSerializer
from rest_framework.viewsets import ModelViewSet
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status
import json
from rest_framework.serializers import Serializer
from rest_framework.exceptions import ValidationError

 

class UsuarioCreateView(ModelViewSet):
    serializer_class = AddUsuarioSerializer
    queryset = Usuario.objects.all()


    def create(self, request, *args, **kwargs):
        usuario_data = request.data['usuario']
        pessoa_data = request.data['pessoa']
        endereco_data = request.data['endereco']
        telefone_data = request.data['telefone']

        try:
            with transaction.atomic():
                endereco = EnderecoSerializer(data=endereco_data)
                telefone = TelefoneSerializer(data=telefone_data)
                endereco.is_valid(raise_exception=True)
                telefone.is_valid(raise_exception=True)
                endereco_obj = endereco.save()
                telefone_obj = telefone.save()
                pessoa_data['telefone'] = telefone_obj.pk
                pessoa_data['endereco'] = endereco_obj.pk
                pessoa = PessoaSerializer(data=pessoa_data)
                pessoa.is_valid(raise_exception=True)
                pessoa_obj = pessoa.save()
                usuario_data['pessoa'] = pessoa_obj.pk
                usuario = UsuarioSerializer(data=usuario_data)
                usuario.is_valid(raise_exception=True)
                usuario.save()

            return Response({"status": "sucesso"}, status=status.HTTP_201_CREATED)
        
        except ValidationError as e:
            error_serializer = None
            for serializer in [endereco, telefone, pessoa]:
                if serializer.errors:
                    error_serializer = serializer
                    break
            
            if error_serializer is not None:
                serializer_name = error_serializer.__class__.custom_name()
                serializer_errors = error_serializer.errors
            
            return Response({serializer_name: serializer_errors}, status=status.HTTP_400_BAD_REQUEST)
