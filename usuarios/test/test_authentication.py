import pytest
from  rest_framework.test import APIClient
from usuarios.models import Usuario
from rest_framework.reverse import reverse



class TestAutentificacao:
    def test_add_user_not_pessoa(self, api_client: APIClient, usuario_data):
        url = reverse("usuario")

        response = api_client.post(
            path=url,
            data=usuario_data,
            
        )

