from http import HTTPStatus

from saudemaisapi.schemas import EventoGet


def teste_criar_evento(client, mock_db_time):
    resposta = client.post(
        '/criar_evento/',
        json={
            'usuario_criador': 1,
            'unidade_associada': 2,
            'titulo': 'Vem Zumbar 2',
            'descricao': 'Evento de zumba',
            'endereco': 'Pérola Negra',
            'foto_evento': 1,
            'link_externo': 'www.linkExterno.com',
            'tipo_evento': 1,
            'capacidade_maxima': 20,
            'data': '2026-07-10',
        },
    )
    assert resposta.status_code == HTTPStatus.CREATED
    assert resposta.json() == {
        'id': 1,
        'usuario_criador': 1,
        'unidade_associada': 2,
        'titulo': 'Vem Zumbar 2',
        'descricao': 'Evento de zumba',
        'endereco': 'Pérola Negra',
        'foto_evento': 1,
        'link_externo': 'www.linkExterno.com',
        'tipo_evento': 1,
        'status': 'Pendente',
        'qtd_inscricoes': 0,
        'capacidade_maxima': 20,
        'data': '2026-07-10',
        'data_criacao': mock_db_time.isoformat(),
        'data_cancelamento': None,
        'data_ultima_atualizacao': None,
        'comentarios': [],
    }


def test_criar_evento_existente(client, mock_db_time, evento):
    resposta = client.post(
        '/criar_evento/',
        json={
            'usuario_criador': 1,
            'unidade_associada': 2,
            'titulo': 'Vem Zumbar',
            'descricao': 'Evento de zumba',
            'endereco': 'Pérola Negra',
            'foto_evento': 1,
            'link_externo': 'www.linkExterno.com',
            'tipo_evento': 1,
            'capacidade_maxima': 20,
            'data': '2026-07-10',
        },
    )
    assert resposta.status_code == HTTPStatus.CONFLICT
    assert resposta.json() == {'detail': 'Evento já existe!'}


def teste_listar_eventos(client, evento, mock_db_time):
    evento_schema = EventoGet.model_validate(evento).model_dump()

    evento_schema['data_criacao'] = mock_db_time.isoformat()
    evento_schema['data'] = mock_db_time.date().isoformat()

    resposta = client.get('/eventos/')

    assert resposta.status_code == HTTPStatus.OK
    assert resposta.json() == {'eventos': [evento_schema]}


def teste_lista_eventos_null(client):
    resposta = client.get('/eventos/')
    assert resposta.status_code == HTTPStatus.OK
    assert resposta.json() == {'eventos': []}


def teste_listar_eventos_por_id_not_found(client):
    resposta = client.get('/eventos/-1')
    assert resposta.status_code == HTTPStatus.NOT_FOUND
    assert resposta.json() == {'detail': 'Evento não encontrado'}


def teste_listar_evento_por_id(client, evento, mock_db_time):
    evento_schema = EventoGet.model_validate(evento).model_dump()

    evento_schema['data_criacao'] = mock_db_time.isoformat()
    evento_schema['data'] = mock_db_time.date().isoformat()

    resposta = client.get('/eventos/1')

    assert resposta.status_code == HTTPStatus.OK

    assert resposta.json() == evento_schema


def teste_atualizar_evento_not_found(client):
    resposta = client.put(
        '/atualizar_evento/-1',
        json={
            'usuario_criador': 1,
            'unidade_associada': 2,
            'titulo': 'Vem Zumbar 60+',
            'descricao': 'Evento de zumba',
            'endereco': 'Pérola Negra',
            'foto_evento': 1,
            'link_externo': 'www.linkExterno.com',
            'tipo_evento': 1,
            'capacidade_maxima': 20,
            'data': '2026-07-10',
        },
    )

    assert resposta.status_code == HTTPStatus.NOT_FOUND

    assert resposta.json() == {'detail': 'Evento não encontrado'}


def teste_atualizar_evento(client, evento, mock_db_time):
    resposta = client.put(
        '/atualizar_evento/1',
        json={
            'usuario_criador': 1,
            'unidade_associada': 2,
            'titulo': 'Vem Zumbar 60+',
            'descricao': 'Evento de zumba',
            'endereco': 'Pérola Negra',
            'foto_evento': 1,
            'link_externo': 'www.linkExterno.com',
            'tipo_evento': 1,
            'capacidade_maxima': 20,
            'data': '2026-07-10',
        },
    )

    assert resposta.status_code == HTTPStatus.OK

    dados_resposta = resposta.json()

    assert dados_resposta['data_ultima_atualizacao'] is not None
    assert 'T' in dados_resposta['data_ultima_atualizacao']

    assert dados_resposta == {
        'id': 1,
        'usuario_criador': 1,
        'unidade_associada': 2,
        'titulo': 'Vem Zumbar 60+',
        'descricao': 'Evento de zumba',
        'endereco': 'Pérola Negra',
        'foto_evento': 1,
        'link_externo': 'www.linkExterno.com',
        'tipo_evento': 1,
        'status': 'Pendente',
        'qtd_inscricoes': 0,
        'capacidade_maxima': 20,
        'data': '2026-07-10',
        'data_criacao': mock_db_time.isoformat(),
        'data_cancelamento': None,
        'data_ultima_atualizacao': dados_resposta['data_ultima_atualizacao'],
        'comentarios': [],
    }


def teste_atualizar_evento_integridade(client, evento):
    client.post(
        '/criar_evento/',
        json={
            'usuario_criador': 1,
            'unidade_associada': 2,
            'titulo': 'Vem Zumbar 2',
            'descricao': 'Evento de zumba',
            'endereco': 'Pérola Negra',
            'foto_evento': 1,
            'link_externo': 'www.linkExterno.com',
            'tipo_evento': 1,
            'capacidade_maxima': 20,
            'data': '2026-07-10',
        },
    )

    resposta = client.put(
        f'/atualizar_evento/{evento.id}',
        json={
            'usuario_criador': 1,
            'unidade_associada': 2,
            'titulo': 'Vem Zumbar 2',
            'descricao': 'Evento de zumba',
            'endereco': 'Pérola Negra',
            'foto_evento': 1,
            'link_externo': 'www.linkExterno.com',
            'tipo_evento': 1,
            'capacidade_maxima': 20,
            'data': '2026-07-10',
        },
    )

    assert resposta.status_code == HTTPStatus.CONFLICT
    assert resposta.json() == {'detail': 'Evento já existe!'}


def teste_remover_evento_not_found(client):

    resposta = client.delete('/remover_evento/-1')

    assert resposta.status_code == HTTPStatus.NOT_FOUND

    assert resposta.json() == {'detail': 'Evento não encontrado'}


def teste_remover_evento(client, evento):
    resposta = client.delete('/remover_evento/1')

    assert resposta.status_code == HTTPStatus.OK

    assert resposta.json() == {'mensagem': 'Evento removido com sucesso!'}
