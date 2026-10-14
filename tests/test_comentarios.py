from http import HTTPStatus

import pytest


def dados_comentario(evento=1, usuario=1):
    return {
        'titulo': 'Evento muito bom',
        'conteudo': 'Gostei bastante do evento.',
        'usuario': usuario,
        'evento': evento,
        'nota': 5,
        'comentario_pai': None,
    }


def criar_segundo_evento(client):
    resposta = client.post(
        '/eventos/criar_evento/',
        json={
            'titulo': 'Segundo evento',
            'descricao': 'Outro evento',
            'data_hora_evento': '2026-12-10T10:00:00',
            'data_hora_fim': '2026-12-10T12:00:00',
            'publico_alvo': 'Todos',
            'categoria': 1,
            'foto_evento': 1,
            'criador_institucional': 1,
            'capacidade_maxima': 20,
            'endereco': 'Outro local',
        },
    )
    assert resposta.status_code == HTTPStatus.CREATED
    return resposta.json()['id']


def test_crud_comentario(client, evento, usuario_comum):
    dados = dados_comentario()
    resposta = client.post('/comentarios/', json=dados)
    assert resposta.status_code == HTTPStatus.CREATED
    comentario = resposta.json()
    assert comentario['titulo'] == dados['titulo']
    assert comentario['nota'] == dados['nota']
    assert comentario['nome_usuario'] == usuario_comum.nome
    assert comentario['data_hora_feito']
    assert comentario['respostas'] == []
    id_comentario = comentario['id']

    resposta = client.get(f'/comentarios/{id_comentario}')
    assert resposta.status_code == HTTPStatus.OK
    assert resposta.json()['conteudo'] == dados['conteudo']

    resposta = client.get('/comentarios/evento/1')
    assert resposta.status_code == HTTPStatus.OK
    assert [item['id'] for item in resposta.json()] == [id_comentario]

    resposta = client.get('/comentarios/?limit=1&offset=0')
    assert resposta.status_code == HTTPStatus.OK
    assert len(resposta.json()) == 1

    dados['titulo'] = 'Título atualizado'
    dados['nota'] = 4
    resposta = client.put(f'/comentarios/{id_comentario}', json=dados)
    assert resposta.status_code == HTTPStatus.OK
    assert resposta.json()['titulo'] == dados['titulo']
    assert resposta.json()['nota'] == dados['nota']

    resposta = client.get('/eventos/1')
    assert resposta.status_code == HTTPStatus.OK
    assert resposta.json()['comentarios'][0]['id'] == id_comentario

    resposta = client.delete(f'/comentarios/{id_comentario}')
    assert resposta.status_code == HTTPStatus.OK
    assert resposta.json() == {'mensagem': 'Comentário removido com sucesso!'}

    resposta = client.get(f'/comentarios/{id_comentario}')
    assert resposta.status_code == HTTPStatus.NOT_FOUND


def test_comentario_fica_no_evento_correto(client, evento, usuario_comum):
    id_evento_2 = criar_segundo_evento(client)
    comentario_1 = client.post(
        '/comentarios/', json=dados_comentario(evento=evento.id)
    ).json()
    comentario_2 = client.post(
        '/comentarios/', json=dados_comentario(evento=id_evento_2)
    ).json()

    resposta_1 = client.get(f'/comentarios/evento/{evento.id}').json()
    resposta_2 = client.get(f'/comentarios/evento/{id_evento_2}').json()
    assert [item['id'] for item in resposta_1] == [comentario_1['id']]
    assert [item['id'] for item in resposta_2] == [comentario_2['id']]

    evento_1 = client.get(f'/eventos/{evento.id}').json()
    evento_2 = client.get(f'/eventos/{id_evento_2}').json()
    assert [item['id'] for item in evento_1['comentarios']] == [
        comentario_1['id']
    ]
    assert [item['id'] for item in evento_2['comentarios']] == [
        comentario_2['id']
    ]


def test_resposta_ao_comentario(client, evento, usuario_comum):
    comentario = client.post('/comentarios/', json=dados_comentario()).json()
    dados_resposta = {
        **dados_comentario(),
        'titulo': 'Resposta',
        'conteudo': 'Também gostei.',
        'comentario_pai': comentario['id'],
    }
    resposta = client.post('/comentarios/', json=dados_resposta)
    assert resposta.status_code == HTTPStatus.CREATED
    id_resposta = resposta.json()['id']

    comentario_atualizado = client.get(
        f'/comentarios/{comentario["id"]}'
    ).json()
    assert len(comentario_atualizado['respostas']) == 1
    assert comentario_atualizado['respostas'][0]['id'] == id_resposta
    assert comentario_atualizado['respostas'][0]['nome_usuario'] == (
        usuario_comum.nome
    )
    assert comentario_atualizado['respostas'][0]['data_hora_feito']

    evento_atualizado = client.get('/eventos/1').json()
    assert evento_atualizado['comentarios'][0]['respostas'][0]['id'] == (
        id_resposta
    )

    resposta = client.delete(f'/comentarios/{comentario["id"]}')
    assert resposta.status_code == HTTPStatus.OK
    assert client.get(f'/comentarios/{id_resposta}').status_code == (
        HTTPStatus.NOT_FOUND
    )


def test_rejeita_resposta_em_outro_evento(client, evento, usuario_comum):
    id_evento_2 = criar_segundo_evento(client)
    comentario = client.post(
        '/comentarios/', json=dados_comentario(evento=evento.id)
    ).json()
    dados = {
        **dados_comentario(evento=id_evento_2),
        'comentario_pai': comentario['id'],
    }
    resposta = client.post('/comentarios/', json=dados)
    assert resposta.status_code == HTTPStatus.BAD_REQUEST
    assert resposta.json() == {
        'detail': 'A resposta deve pertencer ao mesmo evento'
    }


def test_rejeita_resposta_de_outra_resposta(client, evento, usuario_comum):
    comentario = client.post('/comentarios/', json=dados_comentario()).json()
    primeira_resposta = client.post(
        '/comentarios/',
        json={
            **dados_comentario(),
            'comentario_pai': comentario['id'],
        },
    ).json()
    resposta = client.post(
        '/comentarios/',
        json={
            **dados_comentario(),
            'comentario_pai': primeira_resposta['id'],
        },
    )
    assert resposta.status_code == HTTPStatus.BAD_REQUEST
    assert resposta.json() == {
        'detail': 'Não é possível responder a outra resposta'
    }


def test_rejeita_comentario_original_inexistente(
    client, evento, usuario_comum
):
    dados = {**dados_comentario(), 'comentario_pai': 999}
    resposta = client.post('/comentarios/', json=dados)
    assert resposta.status_code == HTTPStatus.NOT_FOUND
    assert resposta.json() == {'detail': 'Comentário original não encontrado'}


def test_rejeita_alteracao_do_comentario_original(
    client, evento, usuario_comum
):
    comentario = client.post('/comentarios/', json=dados_comentario()).json()
    dados = {**dados_comentario(), 'comentario_pai': 999}
    resposta = client.put(f'/comentarios/{comentario["id"]}', json=dados)
    assert resposta.status_code == HTTPStatus.BAD_REQUEST
    assert resposta.json() == {
        'detail': 'Não é possível alterar o comentário original'
    }


def test_aceita_limites_de_caracteres(client, evento, usuario_comum):
    dados = {
        **dados_comentario(),
        'titulo': 'a' * 100,
        'conteudo': 'b' * 1000,
    }
    resposta = client.post('/comentarios/', json=dados)
    assert resposta.status_code == HTTPStatus.CREATED


@pytest.mark.parametrize(
    ('campo', 'valor'),
    [
        ('titulo', ''),
        ('titulo', 'a' * 101),
        ('conteudo', ''),
        ('conteudo', 'a' * 1001),
        ('nota', -1),
        ('nota', 6),
    ],
)
def test_rejeita_campos_invalidos(client, evento, usuario_comum, campo, valor):
    dados = {**dados_comentario(), campo: valor}
    resposta = client.post('/comentarios/', json=dados)
    assert resposta.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_rejeita_comentario_sem_usuario(client, evento):
    dados = dados_comentario(usuario=999)
    resposta = client.post('/comentarios/', json=dados)
    assert resposta.status_code == HTTPStatus.NOT_FOUND
    assert resposta.json() == {'detail': 'Usuário não encontrado'}


def test_rejeita_comentario_sem_evento(client, usuario_comum):
    dados = dados_comentario(evento=999)
    resposta = client.post('/comentarios/', json=dados)
    assert resposta.status_code == HTTPStatus.NOT_FOUND
    assert resposta.json() == {'detail': 'Evento não encontrado'}


@pytest.mark.parametrize('metodo', ['get', 'put', 'delete'])
def test_comentario_inexistente(client, metodo):
    chamada = getattr(client, metodo)
    if metodo == 'put':
        resposta = chamada('/comentarios/999', json=dados_comentario())
    else:
        resposta = chamada('/comentarios/999')
    assert resposta.status_code == HTTPStatus.NOT_FOUND


def test_evento_inexistente_na_listagem(client):
    resposta = client.get('/comentarios/evento/999')
    assert resposta.status_code == HTTPStatus.NOT_FOUND
