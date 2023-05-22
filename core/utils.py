from django.forms.models import model_to_dict


def make_change_dict(model, fields):
    dicionario = model_to_dict(model)
    list_fields = fields
    chaves_para_remover = []
    for chave in dicionario:
        if chave not in list_fields:
            chaves_para_remover.append(chave)

    for chave in chaves_para_remover:
        dicionario.pop(chave)

    return dicionario
