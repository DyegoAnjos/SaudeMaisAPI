from http import HTTPStatus


def test_verificar_api(client):
    resposta = client.get('/')

    assert resposta.status_code == HTTPStatus.OK
    assert resposta.json() == {'mensagem': 'API Saude+ funcionando'}


def test_cors_permite_front_local(client):
    resposta = client.options(
        '/',
        headers={
            'Origin': 'http://localhost:5173',
            'Access-Control-Request-Method': 'GET',
        },
    )

    assert resposta.status_code == HTTPStatus.OK
    assert (
        resposta.headers['access-control-allow-origin']
        == 'http://localhost:5173'
    )
