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
        'email': usuario_comum.email,
        'nome': usuario_comum.nome,
        'senha': usuario_comum.senha,
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
        'email': usuario_institucional.email,
        'nome': usuario_institucional.nome,
        'senha': usuario_institucional.senha,
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
        'email': usuario_administrador.email,
        'nome': usuario_administrador.nome,
        'senha': usuario_administrador.senha,
    }
