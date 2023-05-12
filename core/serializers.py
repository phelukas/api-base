from rest_framework import serializers
from .models import Endereco, Telefone
from rest_framework.exceptions import ValidationError

class CustomValidationError(ValidationError):
    print("aquiiii")
    def __init__(self, detail=None, code=None, params=None):
        if detail is None:
            detail = {'error': 'Something went wrong.'}
        super().__init__(detail=detail, code=code, params=params)


class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = '__all__' 

class TelefoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Telefone
        fields = '__all__' 

