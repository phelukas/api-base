import uuid
from django.db import models
from django.forms.models import model_to_dict

ESTADOS_BRASIL = (
    ('AC', 'Acre'),
    ('AL', 'Alagoas'),
    ('AP', 'Amapá'),
    ('AM', 'Amazonas'),
    ('BA', 'Bahia'),
    ('CE', 'Ceará'),
    ('DF', 'Distrito Federal'),
    ('ES', 'Espírito Santo'),
    ('GO', 'Goiás'),
    ('MA', 'Maranhão'),
    ('MT', 'Mato Grosso'),
    ('MS', 'Mato Grosso do Sul'),
    ('MG', 'Minas Gerais'),
    ('PA', 'Pará'),
    ('PB', 'Paraíba'),
    ('PR', 'Paraná'),
    ('PE', 'Pernambuco'),
    ('PI', 'Piauí'),
    ('RJ', 'Rio de Janeiro'),
    ('RN', 'Rio Grande do Norte'),
    ('RS', 'Rio Grande do Sul'),
    ('RO', 'Rondônia'),
    ('RR', 'Roraima'),
    ('SC', 'Santa Catarina'),
    ('SP', 'São Paulo'),
    ('SE', 'Sergipe'),
    ('TO', 'Tocantins'),
)



class TimeStampedModel(models.Model):
    created = models.DateTimeField(db_index=True, auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDModel(models.Model):
    uuid = models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Telefone(models.Model):
    telefone = models.CharField(verbose_name="Telefone", max_length=100, blank=True, null=True)

    def __str__(self) -> str:
        return self.telefone
    
    @property
    def get_telefone(self):
        return model_to_dict(self)


class Endereco(models.Model):
    rua = models.CharField(verbose_name="Endereço", max_length=100, null=False, blank=False)
    estados = models.CharField(verbose_name="Estados", max_length=2, choices=ESTADOS_BRASIL, blank=False, null=False)
    cidade = models.CharField(verbose_name="Cidade", max_length=50, blank=False, null=False)
   
    def __str__(self) -> str:
        return f'Rua:{self.rua} - Cidade:{self.cidade} - Estado:{self.estados}'
    
    @property
    def get_endereco(self):
        return model_to_dict(self)
