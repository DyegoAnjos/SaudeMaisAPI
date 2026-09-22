from encodings import normalize_encoding
from http import HTTPStatus
from multiprocessing.reduction import send_handle

from saudemaisapi.schemas import Usuario_retorno_Schema

def teste_validar_usuario_comum(cliente, usuario_comum):
    id(
        email
        nome(senha())
    )

    usuario_schema = Usuario_retorno_Schema.model_validate(usuario_comum).model_dump()

    resposta = cliente.get(
        '/usuarios/validar',
        json={
            'email': usuario_comum.email,
            'senha': usuario_comum.senha,
        }
        )

    assert resposta.status_code == HTTPStatus.OK
    assert resposta.json() == Usuario_retorno_Schema.dict()