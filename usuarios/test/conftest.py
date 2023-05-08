import pytest
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import Group


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def usuario_data():
    payload = {
        "rua": "Rua cruz de malta",
        "estados": "RN",
        "cidade": "Natal",
        "telefone": "84999566143",
        "primeiro_nome": "Pedro",
        "sobre_nome": "Silva", 
        "cpf": "09009289486",
        "password": "Nohaxe100!",
        "password2": "Nohaxe100!",
        "email": "pedrolukas@gmail.com"
    }
    return payload
