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
        "pessoa": {
            "primeiro_nome": "",
            "sobre_nome": "",
            "cpf": "",
            "telefone": "",
            "endereco": "",
        },
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


def comparar_chaves(dicionario1, dicionario2):
    chaves_diferentes = []

    if sorted(dicionario1.keys()) != sorted(dicionario2.keys()):
        return list(set(dicionario1.keys()) ^ set(dicionario2.keys()))

    for chave in dicionario1.keys():
        valor1 = dicionario1[chave]
        valor2 = dicionario2[chave]

        if isinstance(valor1, dict) and isinstance(valor2, dict):
            chaves_sub_diferentes = comparar_chaves(valor1, valor2)
            if chaves_sub_diferentes:
                chaves_diferentes.extend(
                    [f"{chave}.{sub_chave}" for sub_chave in chaves_sub_diferentes]
                )
        elif valor1 != valor2:
            chaves_diferentes.append(chave)

    print("TTTTT")
    print(chaves_diferentes)

    return chaves_diferentes


# def comparar_chaves(dicionario1, dicionario2):
#     if sorted(dicionario1.keys()) != sorted(dicionario2.keys()):
#         return False

#     for chave in dicionario1.keys():
#         valor1 = dicionario1[chave]
#         valor2 = dicionario2[chave]

#         if isinstance(valor1, dict) and isinstance(valor2, dict):
#             if not comparar_chaves(valor1, valor2):
#                 return False

#     return True


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
