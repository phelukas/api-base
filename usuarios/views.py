from usuarios.models import Usuario
from usuarios.serializers import AddUsuarioSerializer
from rest_framework.viewsets import ModelViewSet


class UsuarioCreateView(ModelViewSet):
    serializer_class = AddUsuarioSerializer
    queryset = Usuario.objects.all()
