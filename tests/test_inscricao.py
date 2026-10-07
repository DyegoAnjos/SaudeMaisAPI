from http import HTTPStatus


def test_inscricao(client, evento, usuario_comum):
    resposta = client.post(
        '/inscricao/inscrever', json={'id_evento': 1, 'id_usuario': 1}
    )

    assert resposta.status_code == HTTPStatus.OK
    assert resposta.json() == {'id': 0, 'id_evento': 1, 'id_usuario': 1}
