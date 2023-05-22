import pytest
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from usuarios.models import Usuario, Pessoa
from core.models import Endereco, Telefone


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_telefone():
    telefone = Telefone.objects.create(
        telefone="84999566143"
    )
    return telefone

@pytest.fixture
def create_endereco():
    endereco = Endereco.objects.create(
        rua="Rua Cruz de Malta",
        estados="RN",
        cidade="Natal"
    )
    return endereco    

@pytest.fixture
def create_pessoa():
    endereco = Endereco.objects.create(
        rua="Rua Cruz de Malta",
        estados="RN",
        cidade="Natal"
    )
    telefone = Telefone.objects.create(
        telefone="84999566143"
    )
    pessoa = Pessoa.objects.create(
        primeiro_nome="Pedro",
        sobre_nome="Lucas",
        cpf="09009289480",
        
        telefone=telefone,
        endereco=endereco
    )
    return pessoa


@pytest.fixture
def create_usuario():
    endereco = Endereco.objects.create(
        rua="Rua Cruz de Malta",
        estados="RN",
        cidade="Natal"
    )
    telefone = Telefone.objects.create(
        telefone="84999566143"
    )
    pessoa = Pessoa.objects.create(
        primeiro_nome="Pedro",
        sobre_nome="Lucas",
        cpf="09009289486",
        
        telefone=telefone,
        endereco=endereco
    )
    usuario = Usuario.objects.create(
        email="test@test.com",
        password="Senha123!",
        pessoa=pessoa
    )
    return usuario


@pytest.fixture
def payload_modelo():
    payload_modelo = {
        "usuario": {
            "id": "",
            "email": "",
            "pessoa": ""
        },
        "pessoa": {
            "primeiro_nome": "",
            "sobre_nome": "",
            "cpf": "",
            "telefone": "",
            "endereco": ""
        },
        "endereco": {
            "id": "",
            "rua": "",
            "estados": "",
            "cidade": ""
        },
        "telefone": {
            "id": "",
            "telefone": ""
        }
    }
    return payload_modelo


def comparar_chaves(dicionario1, dicionario2):
    if sorted(dicionario1.keys()) != sorted(dicionario2.keys()):
        return False

    for chave in dicionario1.keys():
        valor1 = dicionario1[chave]
        valor2 = dicionario2[chave]

        if isinstance(valor1, dict) and isinstance(valor2, dict):
            if not comparar_chaves(valor1, valor2):
                return False

    return True
