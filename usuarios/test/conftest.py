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

