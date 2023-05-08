from rest_framework import viewsets
from .models import Usuario, Pessoa
from .serializers import UsuarioAddSerializer
from rest_framework import generics, status, views
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


class UsuarioViewSet(viewsets.ViewSet):
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return UsuarioAddSerializer
        else:
            return UsuarioAddSerializer

    def get_queryset(self):
        queryset = Usuario.objects.all()
        return queryset

    def get_object(self):
        queryset = self.get_queryset()
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(queryset, pk=pk)
        return obj        

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        return serializer_class(*args, **kwargs)            

    def list(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

