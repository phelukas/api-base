from usuarios.models import Usuario
from usuarios.serializers import AddUsuarioSerializer, PessoaSerializer, UsuarioSerializer
from rest_framework.viewsets import ModelViewSet
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status
import json
from rest_framework.serializers import Serializer
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView

 

class UsuarioCreateView(ModelViewSet):
    serializer_class = AddUsuarioSerializer
    queryset = Usuario.objects.all()
