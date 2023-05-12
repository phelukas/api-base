from rest_framework.exceptions import ValidationError

class CustomValidationError(ValidationError):
    print("ffffffffffffffffffffffffffffffff")

    def __init__(self, detail=None, code=None, params=None):
        print("yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy")
        if detail is None:
            detail = {'error': 'Something went wrong.'}
        super().__init__(detail=detail, code=code, params=params)

    def custom_exception_handler(exc, context):
        print("ddddddddddddd")
        if isinstance(exc, ValidationError):
            # Se o erro for uma instancia de ValidationError, use a nova classe CustomValidationError
            exc = CustomValidationError(detail=exc.detail, code=exc.code)
        return super().custom_exception_handler(exc, context)

