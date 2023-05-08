from django.contrib import admin
from django.urls import path
from django.urls import include, path, re_path
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from usuarios.views import UsuarioViewSet
from core.views import EnderecoViewSet, TelefoneViewSet

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuario')
# router.register(r'pessoas', PessoaViewSet, basename='pessoa')
router.register(r'endereco', EnderecoViewSet, basename='endereco')
router.register(r'telefone', TelefoneViewSet, basename='telefone')
urlpatterns = router.urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
