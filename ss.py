from usuarios.models import Usuario
from usuarios.serializers import AddUsuarioSerializer, PessoaSerializer, UsuarioSerializer
from core.serializers import EnderecoSerializer, TelefoneSerializer
from rest_framework.viewsets import ModelViewSet
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status
import json

 

class UsuarioCreateView(ModelViewSet):
    serializer_class = AddUsuarioSerializer
    queryset = Usuario.objects.all()

    def create(self, request, *args, **kwargs): 
        super().create
        usuario_data = request.data['usuario']
        pessoa_data = request.data['pessoa']
        endereco_data = request.data['endereco']
        telefone_data = request.data['telefone']
    
        try:
            endereco = EnderecoSerializer(data=endereco_data)
            endereco.is_valid(raise_exception=True)
            endereco_obj = endereco.save()
        except:
            ...
        try:
            telefone = TelefoneSerializer(data=telefone_data)
            telefone.is_valid(raise_exception=True)
            telefone_obj = telefone.save()
        except:
            ...
        try:
                pessoa = PessoaSerializer(data=pessoa_data)
                pessoa.is_valid(raise_exception=True)
                pessoa_obj = pessoa.save()
        except:
             ...
        
        try:
                usuario = UsuarioSerializer(data=usuario_data)
                usuario.is_valid(raise_exception=True)
                usuario.save()
        except:
             ...

        try:
            with transaction.atomic():
                pessoa_data['telefone'] = telefone_obj.pk
                pessoa_data['endereco'] = endereco_obj.pk
                usuario_data['pessoa'] = pessoa_obj.pk
                return Response({"status": "sucesso"}, status=status.HTTP_201_CREATED)
            
        except Exception as E:
            print("erro qui")
            print(E.detail)
            print(type(E))
            return Response(E.detail, status=status.HTTP_409_CONFLICT)








def x():
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
            
        except Exception as E:
            print("erro qui")
            print(E.detail)
            print(type(E))
            return Response(E.detail, status=status.HTTP_409_CONFLICT)

