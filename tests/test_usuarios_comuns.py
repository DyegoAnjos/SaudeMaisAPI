from http import HTTPStatus


def test_listar_usuarios_comum(client, usuario_comum):

    resposta = client.get('usuarios/comum/')

    assert resposta.status_code == HTTPStatus.OK
    assert resposta.data == [usuario_comum]
