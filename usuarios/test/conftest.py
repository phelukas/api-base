import random
import pytest
from collections import namedtuple
from rest_framework.test import APIClient
from usuarios.models import Usuario, Pessoa
from core.models import Endereco, Telefone


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_telefone():
    telefone = Telefone.objects.create(telefone="84999566143")
    return telefone


@pytest.fixture
def create_endereco():
    endereco = Endereco.objects.create(
        rua="Rua Cruz de Malta", estados="RN", cidade="Natal"
    )
    return endereco


@pytest.fixture
def create_pessoa():
    endereco = Endereco.objects.create(
        rua="Rua Cruz de Malta", estados="RN", cidade="Natal"
    )
    telefone = Telefone.objects.create(telefone="84999566143")
    pessoa = Pessoa.objects.create(
        primeiro_nome="Pedro",
        sobre_nome="Lucas",
        cpf="09009289480",
        telefone=telefone,
        endereco=endereco,
    )
    return pessoa


@pytest.fixture
def create_usuario():
    endereco = Endereco.objects.create(
        rua="Rua Cruz de Malta", estados="RN", cidade="Natal"
    )
    telefone = Telefone.objects.create(telefone="84999566143")
    pessoa = Pessoa.objects.create(
        primeiro_nome="Pedro",
        sobre_nome="Lucas",
        cpf="09009289486",
        telefone=telefone,
        endereco=endereco,
    )
    usuario = Usuario.objects.create(
        email="test@test.com", password="Senha123!", pessoa=pessoa
    )
    return usuario


@pytest.fixture
def payload_modelo():
    payload_modelo = {
        "usuario": {"id": "", "email": "", "pessoa": ""},
        "pessoa": {"id": "", "primeiro_nome": "", "sobre_nome": "", "cpf": ""},
        "endereco": {"id": "", "rua": "", "estados": "", "cidade": ""},
        "telefone": {"id": "", "telefone": ""},
    }
    return payload_modelo


@pytest.fixture
def payload_modelo_preenchido():
    payload_modelo_preenchido = {
        "usuario": {"password": "Senha@123", "email": "amanda@example.com"},
        "pessoa": {
            "primeiro_nome": "Amanda",
            "sobre_nome": "Salles",
            "cpf": "123456789",
        },
        "endereco": {"rua": "Rua cruz de malta", "estados": "RN", "cidade": "Natal"},
        "telefone": {"telefone": "84999599473"},
    }
    return payload_modelo_preenchido


def comparar_chaves(dicionario1, dicionario2, caminho=""):
    chaves_diferentes = []

    for chave in dicionario1:
        novo_caminho = caminho + "." + chave if caminho else chave
        if chave not in dicionario2:
            chaves_diferentes.append(novo_caminho)
        elif isinstance(dicionario1[chave], dict) and isinstance(
            dicionario2[chave], dict
        ):
            chaves_diferentes.extend(
                comparar_chaves(
                    dicionario1[chave], dicionario2[chave], caminho=novo_caminho
                )
            )

    for chave in dicionario2:
        novo_caminho = caminho + "." + chave if caminho else chave
        if chave not in dicionario1:
            chaves_diferentes.append(novo_caminho)

    return chaves_diferentes


def comparar_dicionarios(dicionario1, dicionario2, caminho=""):
    campos_diferentes = []

    for chave in dicionario1:
        novo_caminho = caminho + "." + chave if caminho else chave
        if chave not in dicionario2:
            campos_diferentes.append((novo_caminho, dicionario1[chave], None))
        elif isinstance(dicionario1[chave], dict) and isinstance(
            dicionario2[chave], dict
        ):
            campos_diferentes.extend(
                comparar_dicionarios(
                    dicionario1[chave], dicionario2[chave], caminho=novo_caminho
                )
            )
        elif dicionario1[chave] != dicionario2[chave]:
            campos_diferentes.append(
                (novo_caminho, dicionario1[chave], dicionario2[chave])
            )

    for chave in dicionario2:
        novo_caminho = caminho + "." + chave if caminho else chave
        if chave not in dicionario1:
            campos_diferentes.append((novo_caminho, None, dicionario2[chave]))

    if campos_diferentes:
        Erro = namedtuple("Erro", ["campo", "valor_1", "valor_2"])
        campos_diferentes = [Erro(*tupla) for tupla in campos_diferentes]

    return campos_diferentes


def gerar_cpf():
    cpf = [random.randint(0, 9) for _ in range(9)]

    # Calcula o primeiro dígito verificador
    soma = sum((valor * (i + 1)) for i, valor in enumerate(cpf))
    digito1 = (soma % 11) % 10
    cpf.append(digito1)

    # Calcula o segundo dígito verificador
    soma = sum((valor * i) for i, valor in enumerate(cpf[::-1])) + (digito1 * 9)
    digito2 = (soma % 11) % 10
    cpf.append(digito2)

    return "".join(str(d) for d in cpf)
