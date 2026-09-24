from http import HTTPStatus


def teste_validar_usuario_comum(client, usuario_comum):

    resposta = client.post(
        '/usuarios/validar',
        json={
            'email': usuario_comum.email,
            'senha': usuario_comum.senha,
        },
    )

    assert resposta.status_code == HTTPStatus.OK
    assert resposta.json() == {
        'id': usuario_comum.id,
        'tipo': 'Usuario_comum',
    }


def teste_validar_usuario_institucional(client, usuario_institucional):

    resposta = client.post(
        '/usuarios/validar',
        json={
            'email': usuario_institucional.email,
            'senha': usuario_institucional.senha,
        },
    )

    assert resposta.status_code == HTTPStatus.OK
    assert resposta.json() == {
        'id': usuario_institucional.id,
        'tipo': 'Usuario_institucional',
    }


def teste_validar_usuario_administrador(client, usuario_administrador):

    resposta = client.post(
        '/usuarios/validar',
        json={
            'email': usuario_administrador.email,
            'senha': usuario_administrador.senha,
        },
    )

    assert resposta.status_code == HTTPStatus.OK
    assert resposta.json() == {
        'id': usuario_administrador.id,
        'tipo': 'Usuario_administrador',
    }
