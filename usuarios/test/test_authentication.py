import pytest
from usuarios.test.conftest import comparar_chaves, comparar_dicionarios, gerar_cpf
from usuarios.models import Usuario, Pessoa
from core.models import Telefone, Endereco
from django.db.utils import IntegrityError
from django.contrib.auth.hashers import check_password
from faker import Faker
from core.models import ESTADOS_BRASIL
import random
import string


@pytest.mark.django_db
def test_telefone_create():
    Telefone.objects.create(telefone="84999566143")
    assert Telefone.objects.count() == 1


@pytest.mark.django_db
def test_endereco_create():
    Endereco.objects.create(rua="Rua Cruz de Malta", estados="RN", cidade="Natal")
    assert Endereco.objects.count() == 1


@pytest.mark.django_db
def test_pessoa_create():
    endereco = Endereco.objects.create(
        rua="Rua Cruz de Malta", estados="RN", cidade="Natal"
    )
    telefone = Telefone.objects.create(telefone="84999566143")
    Pessoa.objects.create(
        primeiro_nome="Pedro",
        sobre_nome="Lucas",
        cpf="09009289486",
        telefone=telefone,
        endereco=endereco,
    )

    assert Pessoa.objects.count() == 1


# criar um teste para verificar se pode cadastrar um:
# cadastrar um usuario sem ter um pessoa
@pytest.mark.django_db
def test_create_user_without_person():
    with pytest.raises(IntegrityError):
        Usuario.objects.create(email="test@test.com", password="Senha123!")


# cadastrar um usuario sem telefone
@pytest.mark.django_db
def test_create_person_without_phone(create_endereco):
    with pytest.raises(IntegrityError):
        Pessoa.objects.create(
            primeiro_nome="Pedro",
            sobre_nome="Lucas",
            cpf="09009289486",
            endereco=create_endereco,
        )


# cadastrar um usuario sem endereço
@pytest.mark.django_db
def test_create_person_without_address(create_telefone):
    with pytest.raises(IntegrityError):
        Pessoa.objects.create(
            primeiro_nome="Pedro",
            sobre_nome="Lucas",
            cpf="09009289486",
            telefone=create_telefone,
        )


@pytest.mark.django_db
def test_create_person_without_cpf(create_telefone, create_endereco):
    with pytest.raises(IntegrityError):
        Pessoa.objects.create(
            primeiro_nome="Pedro",
            sobre_nome="Lucas",
            telefone=create_telefone,
            endereco=create_endereco,
        )


# cadastrar um usuario sem email
@pytest.mark.django_db
def test_create_user_without_email(create_pessoa):
    with pytest.raises(IntegrityError):
        Usuario.objects.create(pessoa=create_pessoa)


# cadastrar um usuario com email existente
@pytest.mark.django_db
def test_create_user_with_existing_email(create_usuario, create_pessoa):
    email = create_usuario.email
    with pytest.raises(IntegrityError):
        Usuario.objects.create(email=email, password="Senha123!", pessoa=create_pessoa)


# cadastrar um usuario com cpf existente
@pytest.mark.django_db
def test_create_person_with_existing_cpf(
    create_pessoa, create_endereco, create_telefone
):
    cpf = create_pessoa.cpf
    with pytest.raises(IntegrityError):
        Pessoa.objects.create(
            primeiro_nome="Pedro",
            sobre_nome="Lucas",
            cpf=cpf,
            telefone=create_telefone,
            endereco=create_endereco,
        )


# verificar se retorna status code 200
@pytest.mark.django_db
def test_get_user_status_code_200(api_client, create_usuario):
    response = api_client.get("/api/usuarios/")
    assert response.status_code == 200


# verficar se o payload do get retorna os campos
@pytest.mark.django_db
def test_get_user_payload(api_client, payload_modelo, create_usuario):
    payload_get = api_client.get("/api/usuarios/").json()[0]
    comparacao = comparar_chaves(payload_modelo, payload_get)
    assert comparacao == [], comparacao


# verificar se o POST salvou a senha correta
@pytest.mark.django_db
def test_post_save_user_right_password(api_client, payload_modelo_preenchido):
    api_client.post("/api/usuarios/", data=payload_modelo_preenchido, format="json")
    user = Usuario.objects.get(id=1)
    assert (
        check_password(payload_modelo_preenchido["usuario"]["password"], user.password)
        == True
    )


# verificar se o POST salvou campos certos
@pytest.mark.django_db
def test_post_save_user_right_fields(api_client, payload_modelo_preenchido):
    api_client.post("/api/usuarios/", data=payload_modelo_preenchido, format="json")
    user = Usuario.objects.get(id=1)

    del payload_modelo_preenchido["usuario"]["password"]

    dict_user = {
        "usuario": {"email": user.email},
        "pessoa": {
            "primeiro_nome": user.pessoa.primeiro_nome,
            "sobre_nome": user.pessoa.sobre_nome,
            "cpf": user.pessoa.cpf,
        },
        "endereco": {
            "rua": user.pessoa.endereco.rua,
            "estados": user.pessoa.endereco.estados,
            "cidade": user.pessoa.endereco.cidade,
        },
        "telefone": {"telefone": user.pessoa.telefone.telefone},
    }

    comparacao = comparar_dicionarios(dict_user, payload_modelo_preenchido)

    assert comparacao == [], comparacao


# verficar se o PUT retorna status code 200
fake = Faker()


@pytest.mark.django_db
def test_check_if_put_returns_status_code_200(api_client, create_usuario):
    caracteres = string.ascii_letters + string.digits
    senha = "".join(random.choice(caracteres) for _ in range(10))
    payload = {
        "usuario": {"email": fake.email(), "password": senha},
        "pessoa": {
            "primeiro_nome": fake.name(),
            "sobre_nome": fake.name(),
            "cpf": gerar_cpf(),
        },
        "endereco": {
            "rua": fake.address(),
            "estados": random.choice(ESTADOS_BRASIL),
            "cidade": fake.city(),
        },
        "telefone": {"telefone": fake.phone_number()},
    }
    response = api_client.put(
        f"/api/usuarios/{create_usuario.id}/", data=payload, format="json"
    )

    assert response.status_code == 200, response.json()


# verficar se o PUT alterou so os campos passados
# @pytest.mark.django_db
# def check_if_the_put_changed_only_the_fields_passed(api_client, create_usuario):
#     user = Usuario.objects.get(id=1)
#     response = api_client.put("/api/usuarios/", data=)
