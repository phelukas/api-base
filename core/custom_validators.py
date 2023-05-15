from rest_framework.serializers import Serializer
from rest_framework.exceptions import ValidationError

def validar_serializacoes(serializacoes):
    for serializacao in serializacoes:
        serializer = Serializer(data=serializacao)
        if not serializer.is_valid():
            nome_serializer = serializer.__class__.__name__
            mensagem_erro = f'A serialização é inválida para o serializer {nome_serializer}.'
            raise ValidationError(mensagem_erro)
    return True
