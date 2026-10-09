from http import HTTPStatus


def test_inscricao(client, evento, usuario_comum):
    resposta = client.post(
        '/inscricao/inscrever', json={'evento': 1, 'usuario': 1}
    )

    assert resposta.status_code == HTTPStatus.OK
    assert resposta.json() == {'id': 1, 'evento': 1, 'usuario': 1}


def test_inscricao_usuario_errado(client, evento, usuario_comum):
    resposta = client.post(
        '/inscricao/inscrever', json={'evento': 1, 'usuario': 2}
    )

    assert resposta.status_code == HTTPStatus.CONFLICT
    assert resposta.json() == {'detail': 'Usuário não encontrado!'}


def test_inscricao_evento_errado(client, evento, usuario_comum):
    resposta = client.post(
        '/inscricao/inscrever', json={'evento': 12, 'usuario': 1}
    )

    assert resposta.status_code == HTTPStatus.CONFLICT
    assert resposta.json() == {'detail': 'Evento não encontrado!'}


def test_inscricao_usuario_ja_inscrito(
    client, evento, usuario_comum, inscricao_evento1
):
    resposta = client.post(
        '/inscricao/inscrever', json={'evento': 1, 'usuario': 1}
    )

    assert resposta.status_code == HTTPStatus.CONFLICT
    assert resposta.json() == {'detail': 'Usuário já inscrito!'}


def test_cancelar_inscricao(client, evento, usuario_comum, inscricao_evento1):
    resposta = client.delete('/inscricao/cancelar_inscricao/1')

    assert resposta.status_code == HTTPStatus.OK
    assert resposta.json() == {'mensagem': 'Inscrição cancelada no evento!'}


def test_cancelar_inscricao_errado(
    client, evento, usuario_comum, inscricao_evento1
):
    resposta = client.delete('/inscricao/cancelar_inscricao/2')

    assert resposta.status_code == HTTPStatus.CONFLICT
    assert resposta.json() == {'detail': 'Usuário não inscrito no evento!'}


def test_listar_inscricao(client, evento, usuario_comum, inscricao_evento1):
    resposta = client.get('/inscricao/1')

    assert resposta.status_code == HTTPStatus.OK
    assert resposta.json() == [{'id': 1, 'evento': 1, 'usuario': 1}]


def test_listar_inscricao_errado(
    client, evento, usuario_comum, inscricao_evento1
):
    resposta = client.get('/inscricao/2')

    assert resposta.status_code == HTTPStatus.NOT_FOUND
    assert resposta.json() == {'detail': 'Usuário sem inscrição!'}
