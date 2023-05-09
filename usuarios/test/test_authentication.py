import pytest
from  rest_framework.test import APIClient
from rest_framework.reverse import reverse
from usuarios.models import Usuario, Pessoa
from core.models import Telefone, Endereco


@pytest.mark.django_db
def test_telefone_create():
    Telefone.objects.create(
        telefone="84999566143"
    )
    assert Telefone.objects.count() == 1

@pytest.mark.django_db
def test_endereco_create():
    Endereco.objects.create(
        rua="Rua Cruz de Malta",
        estados="RN",
        cidade="Natal"
    )
    assert Endereco.objects.count() == 1



@pytest.mark.django_db
def test_pessoa_create():
    endereco = Endereco.objects.create(
        rua="Rua Cruz de Malta",
        estados="RN",
        cidade="Natal"
    )
    telefone = Telefone.objects.create(
        telefone="84999566143"
    )
    Pessoa.objects.create(
        primeiro_nome="Pedro",
        sobre_nome="Lucas",
        cpf="09009289486",
        
        telefone=telefone,
        endereco=endereco
    )

    assert Pessoa.objects.count() == 1

@pytest.mark.django_db
def test_usuario_create():
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

    Usuario.objects.create(
        email="pedrolukas@gmail.com",
        pessoa=pessoa
    )
    assert Usuario.objects.count() == 1

# @pytest.mark.django_db
# def test_view(client):
#     url = reverse('usuarios')