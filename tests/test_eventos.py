from http import HTTPStatus

from saudemaisapi.schemas import Evento_retorno_Schema


def teste_criar_evento(client, mock_db_time, evento):
    resposta = client.post(
        '/eventos/criar_evento/',
        json={
            'titulo': 'Vem Zumbar 2',
            'descricao': 'Evento de zumba',
            'data_hora_evento': mock_db_time.isoformat(),
            'data_hora_fim': mock_db_time.isoformat(),
            'publico_alvo': 'Idosos',
            'categoria': 1,
            'foto_evento': 1,
            'criador_institucional': 1,
            'capacidade_maxima': 10,
            'unidade_associada': 1,
            'endereco': 'Arena Jovelina',
            'pagina_evento': 'www.VemZumbar.com',
        },
    )
    assert resposta.status_code == HTTPStatus.CREATED
    assert resposta.json() == {
        'id': 2,
        'titulo': 'Vem Zumbar 2',
        'descricao': 'Evento de zumba',
        'data_hora_evento': mock_db_time.isoformat(),
        'data_hora_fim': mock_db_time.isoformat(),
        'publico_alvo': 'Idosos',
        'categoria': 1,
        'foto_evento': 1,
        'criador_institucional': 1,
        'capacidade_maxima': 10,
        'inscricoes_atuais': 0,
        'unidade_associada': 1,
        'endereco': 'Arena Jovelina',
        'status': 'Pendente',
        'pagina_evento': 'www.VemZumbar.com',
        'data_hora_criacao': mock_db_time.isoformat(),
        'data_hora_cancelamento': None,
        'data_hora_ultima_atualizacao': None,
        'comentarios': [],
    }


def test_criar_evento_existente(client, mock_db_time, evento):
    resposta = client.post(
        '/eventos/criar_evento/',
        json={
            'titulo': 'Vem Zumbar',
            'descricao': 'Evento de zumba',
            'data_hora_evento': mock_db_time.isoformat(),
            'data_hora_fim': mock_db_time.isoformat(),
            'publico_alvo': 'Idosos',
            'categoria': 1,
            'foto_evento': 1,
            'criador_institucional': 1,
            'capacidade_maxima': 10,
            'unidade_associada': 1,
            'endereco': 'Arena Jovelina',
            'pagina_evento': 'www.VemZumbar.com',
        },
    )
    assert resposta.status_code == HTTPStatus.CONFLICT
    assert resposta.json() == {'detail': 'Evento já existe!'}


def teste_listar_eventos(client, evento, mock_db_time):
    evento_schema = Evento_retorno_Schema.model_validate(evento).model_dump()

    evento_schema['data_hora_criacao'] = mock_db_time.isoformat()
    evento_schema['data_hora_evento'] = mock_db_time.isoformat()
    evento_schema['data_hora_fim'] = mock_db_time.isoformat()

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
    evento_schema = Evento_retorno_Schema.model_validate(evento).model_dump()

    evento_schema['data_hora_criacao'] = mock_db_time.isoformat()
    evento_schema['data_hora_fim'] = mock_db_time.isoformat()
    evento_schema['data_hora_evento'] = mock_db_time.isoformat()

    resposta = client.get('/eventos/1')

    assert resposta.status_code == HTTPStatus.OK

    assert resposta.json() == evento_schema


def teste_atualizar_evento_not_found(client, mock_db_time, evento):
    resposta = client.put(
        '/eventos/atualizar_evento/-1',
        json={
            'titulo': 'Vem Zumbar atualizado',
            'descricao': 'Evento de zumba',
            'data_hora_evento': mock_db_time.isoformat(),
            'data_hora_fim': mock_db_time.isoformat(),
            'publico_alvo': 'Idosos',
            'categoria': 1,
            'foto_evento': 1,
            'criador_institucional': 1,
            'capacidade_maxima': 10,
            'unidade_associada': 1,
            'endereco': 'Arena Jovelina',
            'pagina_evento': 'www.VemZumbar.com',
        },
    )

    assert resposta.status_code == HTTPStatus.NOT_FOUND

    assert resposta.json() == {'detail': 'Evento não encontrado'}


def teste_atualizar_evento(client, evento, mock_db_time):
    resposta = client.put(
        '/eventos/atualizar_evento/1',
        json={
            'titulo': 'Vem Zumbar atualizado',
            'descricao': 'Evento de zumba',
            'data_hora_evento': mock_db_time.isoformat(),
            'data_hora_fim': mock_db_time.isoformat(),
            'publico_alvo': 'Idosos',
            'categoria': 1,
            'foto_evento': 1,
            'criador_institucional': 1,
            'capacidade_maxima': 10,
            'unidade_associada': 1,
            'endereco': 'Arena Jovelina',
            'pagina_evento': 'www.VemZumbar.com',
        },
    )

    assert resposta.status_code == HTTPStatus.OK

    resposta = resposta.json()

    resposta['data_hora_ultima_atualizacao'] = mock_db_time.isoformat()

    assert resposta == {
        'id': 1,
        'titulo': 'Vem Zumbar atualizado',
        'descricao': 'Evento de zumba',
        'data_hora_evento': mock_db_time.isoformat(),
        'data_hora_fim': mock_db_time.isoformat(),
        'publico_alvo': 'Idosos',
        'categoria': 1,
        'status': 'Pendente',
        'foto_evento': 1,
        'criador_institucional': 1,
        'inscricoes_atuais': 0,
        'capacidade_maxima': 10,
        'unidade_associada': 1,
        'endereco': 'Arena Jovelina',
        'pagina_evento': 'www.VemZumbar.com',
        'data_hora_criacao': mock_db_time.isoformat(),
        'data_hora_cancelamento': None,
        'data_hora_ultima_atualizacao': mock_db_time.isoformat(),
        'comentarios': [],
    }


def teste_atualizar_evento_integridade(client, evento, mock_db_time):
    client.post(
        '/eventos/criar_evento/',
        json={
            'titulo': 'Vem Zumbar 60+',
            'descricao': 'Evento de zumba',
            'data_hora_evento': mock_db_time.isoformat(),
            'data_hora_fim': mock_db_time.isoformat(),
            'publico_alvo': 'Idosos',
            'categoria': 1,
            'foto_evento': 1,
            'criador_institucional': 1,
            'capacidade_maxima': 10,
            'unidade_associada': 1,
            'endereco': 'Arena Jovelina',
            'pagina_evento': 'www.VemZumbar.com',
        },
    )

    resposta = client.put(
        f'/eventos/atualizar_evento/{evento.id}',
        json={
            'titulo': 'Vem Zumbar 60+',
            'descricao': 'Evento de zumba',
            'data_hora_evento': mock_db_time.isoformat(),
            'data_hora_fim': mock_db_time.isoformat(),
            'publico_alvo': 'Idosos',
            'categoria': 1,
            'foto_evento': 1,
            'criador_institucional': 1,
            'capacidade_maxima': 10,
            'unidade_associada': 1,
            'endereco': 'Arena Jovelina',
            'pagina_evento': 'www.VemZumbar.com',
        },
    )

    assert resposta.status_code == HTTPStatus.CONFLICT
    assert resposta.json() == {'detail': 'Evento já existe!'}


def teste_remover_evento_not_found(client):

    resposta = client.delete('eventos/remover_evento/-1')

    assert resposta.status_code == HTTPStatus.NOT_FOUND

    assert resposta.json() == {'detail': 'Evento não encontrado'}


def teste_remover_evento(client, evento):
    resposta = client.delete('eventos/remover_evento/1')

    assert resposta.status_code == HTTPStatus.OK

    assert resposta.json() == {'mensagem': 'Evento removido com sucesso!'}
