from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.contrib import admin
from django.urls import path
from django.urls import include, path, re_path
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from usuarios.views import  UsuarioCreateView
from core.views import EnderecoViewSet, TelefoneViewSet
from django.urls import reverse


router = DefaultRouter()
router.register(r'usuarios', UsuarioCreateView, basename='usuario')
# router.register(r'pessoas', PessoaViewSet, basename='pessoa')
router.register(r'enderecos', EnderecoViewSet, basename='endereco')
router.register(r'telefones', TelefoneViewSet, basename='telefone')
urlpatterns = router.urls



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    # path('api/usuarios/', UsuarioModelView.as_view(), name="usuarios")
    # YOUR PATTERNS
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
