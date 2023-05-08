
from django.contrib.auth.models import AbstractUser
from core.models import TimeStampedModel, Telefone, Endereco
from django.db import models


class Pessoa(TimeStampedModel):
    primeiro_nome = models.CharField(verbose_name="Primeiro nome", max_length=100, blank=False, null=False)
    sobre_nome = models.CharField(verbose_name="Segundo nome", max_length=20, blank=False, null=False)
    cpf = models.CharField(verbose_name="CPF", max_length=15, null=False, blank=False, unique=True)
    
    telefone = models.ForeignKey(Telefone, related_name="pessoa_telefone", on_delete=models.CASCADE)
    endereco = models.OneToOneField(Endereco, related_name='endereco_pessoa', on_delete=models.CASCADE)


    def get_full_name(self):
        """Nome complete do usuario"""
        return f'{self.primeiro_nome} {self.sobre_nome}'

class Usuario(AbstractUser):
    email = models.EmailField(verbose_name="E-mail", unique=True, blank=False, null=False)
    pessoa = models.OneToOneField(Pessoa, related_name="usuario_pessoa", on_delete=models.CASCADE, null=True)
    
    username = None
    first_name = None
    last_name = None
    groups = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.email

    
