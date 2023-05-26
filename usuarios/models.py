import re
from core.utils import make_change_dict
from django.contrib.auth.models import AbstractUser
from core.models import Telefone, Endereco
from django.db import models
from django.db import IntegrityError


class Pessoa(models.Model):
    primeiro_nome = models.CharField(
        verbose_name="Primeiro nome", max_length=100, blank=False, null=False
    )
    sobre_nome = models.CharField(
        verbose_name="Segundo nome", max_length=20, blank=False, null=False
    )
    cpf = models.CharField(
        verbose_name="cpf", max_length=15, unique=True, blank=False, null=False
    )

    telefone = models.ForeignKey(
        Telefone, related_name="pessoa_telefone", on_delete=models.CASCADE
    )
    endereco = models.OneToOneField(
        Endereco, related_name="endereco_pessoa", on_delete=models.CASCADE
    )

    @property
    def get_pessoa(self):
        fields = ["id", "primeiro_nome", "sobre_nome", "cpf"]

        return make_change_dict(self, fields)

    def __str__(self):
        return self.cpf

    def get_full_name(self):
        """Nome complete do usuario"""
        return f"{self.primeiro_nome} {self.sobre_nome}"

    def save(self, *args, **kwargs):
        if len(self.cpf) == 0:
            raise IntegrityError("CPF é obrigatorio")
        super(Pessoa, self).save(*args, **kwargs)


class Usuario(AbstractUser):
    email = models.EmailField(
        verbose_name="E-mail", unique=True, blank=False, null=False
    )
    pessoa = models.OneToOneField(
        Pessoa, related_name="usuario_pessoa", on_delete=models.CASCADE, null=False
    )

    username = None
    first_name = None
    last_name = None
    groups = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ("-id",)

    def __str__(self):
        return self.email

    @property
    def get_usuario(self):
        fields = ["id", "email", "pessoa"]

        return make_change_dict(self, fields)

    def save(self, *args, **kwargs):
        if len(self.email) == 0:
            raise IntegrityError("E-mail é obrigatorio")

        regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        if not re.match(regex, self.email) is not None:
            raise IntegrityError("E-mail invalido")

        super(Usuario, self).save(*args, **kwargs)
