from http import HTTPStatus
from pathlib import Path

TAMANHO_FOTO_USUARIO = len(b'foto_usuario')


def test_listar_fotografias(client, fotografia_de_usuario):
    resposta = client.get('/fotografias/')

    assert resposta.status_code == HTTPStatus.OK
    assert resposta.json()['fotografias'][0]['nome'] == 'usuario.png'
    assert resposta.json()['fotografias'][0]['tipo'] == 'image/png'
    assert resposta.json()['fotografias'][0]['tamanho'] == TAMANHO_FOTO_USUARIO


def test_listar_fotografias_vazio(client):
    resposta = client.get('/fotografias/')
    assert resposta.status_code == HTTPStatus.OK
    assert resposta.json() == {'fotografias': []}


def test_buscar_fotografia(client, fotografia_de_evento):
    resposta = client.get('/fotografias/1')

    assert resposta.status_code == HTTPStatus.OK
    assert resposta.json()['nome'] == 'evento.jpg'
    assert resposta.json()['foto_de_evento'] is True


def test_fotografia_nao_encontrada(client):
    resposta = client.get('/fotografias/999')
    assert resposta.status_code == HTTPStatus.NOT_FOUND


def test_criar_fotografia(client, mock_db_time):
    resposta = client.post(
        '/fotografias/criar_fotografia',
        files={'arquivo': ('perfil.png', b'conteudo_png', 'image/png')},
        data={'foto_de_evento': 'false'},
    )

    assert resposta.status_code == HTTPStatus.CREATED
    assert resposta.json() == {
        'id': 1,
        'nome': 'perfil.png',
        'tipo': 'image/png',
        'tamanho': 12,
        'foto_de_evento': False,
        'data_hora_envio': mock_db_time.isoformat(),
    }


def test_criar_fotografia_com_formato_invalido(client):
    resposta = client.post(
        '/fotografias/criar_fotografia',
        files={'arquivo': ('texto.txt', b'conteudo', 'text/plain')},
    )
    assert resposta.status_code == HTTPStatus.UNSUPPORTED_MEDIA_TYPE
    assert resposta.json() == {'detail': 'Formato de imagem não permitido'}


def test_criar_fotografia_vazia(client):
    resposta = client.post(
        '/fotografias/criar_fotografia',
        files={'arquivo': ('vazia.png', b'', 'image/png')},
    )
    assert resposta.status_code == HTTPStatus.BAD_REQUEST


def test_criar_fotografia_grande_demais(client):
    resposta = client.post(
        '/fotografias/criar_fotografia',
        files={
            'arquivo': (
                'grande.jpg',
                b'x' * (5 * 1024 * 1024 + 1),
                'image/jpeg',
            )
        },
    )
    assert resposta.status_code == HTTPStatus.REQUEST_ENTITY_TOO_LARGE


def test_obter_arquivo(client, fotografia_de_usuario):
    resposta = client.get('/fotografias/1/arquivo')

    assert resposta.status_code == HTTPStatus.OK
    assert resposta.content == b'foto_usuario'
    assert resposta.headers['content-type'] == 'image/png'


def test_atualizar_fotografia(client, fotografia_de_usuario):
    caminho_antigo = Path(fotografia_de_usuario.caminho)
    resposta = client.put(
        '/fotografias/atualizar_fotografia/1',
        files={'arquivo': ('nova.webp', b'nova_foto', 'image/webp')},
        data={'foto_de_evento': 'true'},
    )

    assert resposta.status_code == HTTPStatus.OK
    assert resposta.json()['nome'] == 'nova.webp'
    assert resposta.json()['tipo'] == 'image/webp'
    assert resposta.json()['foto_de_evento'] is True
    assert not caminho_antigo.exists()


def test_atualizar_fotografia_inexistente(client):
    resposta = client.put(
        '/fotografias/atualizar_fotografia/999',
        files={'arquivo': ('nova.png', b'nova', 'image/png')},
    )
    assert resposta.status_code == HTTPStatus.NOT_FOUND


def test_remover_fotografia(client, fotografia_de_usuario):
    caminho = Path(fotografia_de_usuario.caminho)
    resposta = client.delete('/fotografias/remover_fotografia/1')

    assert resposta.status_code == HTTPStatus.OK
    assert resposta.json() == {'mensagem': 'Fotografia removida com sucesso!'}
    assert not caminho.exists()
