from rest_framework import viewsets
from .models import Endereco, Telefone
from .serializers import EnderecoSerializer, TelefoneSerializer


class EnderecoViewSet(viewsets.ModelViewSet):
    queryset = Endereco.objects.all()
    serializer_class = EnderecoSerializer

class TelefoneViewSet(viewsets.ModelViewSet):
    queryset = Telefone.objects.all()
    serializer_class = TelefoneSerializer

