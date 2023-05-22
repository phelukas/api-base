import pytest
from  rest_framework.test import APIClient
from rest_framework.reverse import reverse
from usuarios.models import Usuario, Pessoa
from core.models import Telefone, Endereco
from django.db.utils import IntegrityError


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

# criar um teste para verificar se pode cadastrar um:
# cadastrar um usuario sem ter um pessoa
@pytest.mark.django_db
def test_create_user_without_person():
    with pytest.raises(IntegrityError):
        Usuario.objects.create(email="test@test.com",password="Senha123!")

# cadastrar um usuario sem telefone
@pytest.mark.django_db
def test_create_person_without_phone(create_endereco):
    with pytest.raises(IntegrityError):
        Pessoa.objects.create(
            primeiro_nome="Pedro",
            sobre_nome="Lucas",
            cpf="09009289486",
            endereco=create_endereco
        )

# cadastrar um usuario sem endereço
@pytest.mark.django_db
def test_create_person_without_address(create_telefone):
    with pytest.raises(IntegrityError):
        Pessoa.objects.create(
            primeiro_nome="Pedro",
            sobre_nome="Lucas",
            cpf="09009289486",
            telefone=create_telefone
        )

@pytest.mark.django_db
def test_create_person_without_cpf(create_telefone, create_endereco):
    with pytest.raises(IntegrityError):
        Pessoa.objects.create(
            primeiro_nome="Pedro",
            sobre_nome="Lucas",
            telefone=create_telefone,
            endereco=create_endereco
        )

# cadastrar um usuario sem email
@pytest.mark.django_db
def test_create_user_without_email(create_pessoa):
    with pytest.raises(IntegrityError):
        Usuario.objects.create(
            pessoa=create_pessoa
        )

# cadastrar um usuario com email existente
@pytest.mark.django_db
def test_create_user_with_existing_email(create_usuario, create_pessoa):
    email = create_usuario.email
    with pytest.raises(IntegrityError):
        Usuario.objects.create(
            email=email,
            password="Senha123!",
            pessoa=create_pessoa
        )

# cadastrar um usuario com cpf existente
@pytest.mark.django_db
def test_create_person_with_existing_cpf(create_pessoa, create_endereco, create_telefone):
    cpf = create_pessoa.cpf
    with pytest.raises(IntegrityError):
        Pessoa.objects.create(
            primeiro_nome="Pedro",
            sobre_nome="Lucas",
            cpf=cpf,
            
            telefone=create_telefone,
            endereco=create_endereco
        )

@pytest.mark.django_db
def test_get_user_status_code_200(api_client, create_usuario):
    response = api_client.get('/api/usuarios/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_user_payload(api_client, payload_modelo, create_usuario):
    response = api_client.get('/api/usuarios/')
    print("*"*89)
    print(Usuario.objects.all())
    print("*"*89)
    print(response.json())
    assert 1 == 0



