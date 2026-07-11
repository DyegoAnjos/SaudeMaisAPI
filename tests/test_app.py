from datetime import date
from http import HTTPStatus


def teste_lista_eventos_null(client):
    resposta = client.get('/eventos/')
    assert resposta.status_code == HTTPStatus.OK
    assert resposta.json() == {'eventos': []}


def teste_criar_evento(client):
    resposta = client.post(
        '/criar_evento/',
        json={
            'id_usuario_criador': 1,
            'id_unidade_associada': 2,
            'titulo': 'Vem Zumbar',
            'descricao': 'Evento de zumba',
            'endereco': 'Pérola Negra',
            'foto': 'aquivoFoto.png',
            'link_externo': 'www.linkExterno.com',
            'categoria': 'Esporte',
            'qtd_inscricoes_maxima': 20,
            'data_evento': '2026-07-10',
        },
    )
    assert resposta.status_code == HTTPStatus.CREATED
    assert resposta.json() == {
        'id': 1,
        'id_usuario_criador': 1,
        'id_unidade_associada': 2,
        'titulo': 'Vem Zumbar',
        'descricao': 'Evento de zumba',
        'endereco': 'Pérola Negra',
        'foto': 'aquivoFoto.png',
        'link_externo': 'www.linkExterno.com',
        'categoria': 'Esporte',
        'status': 'Pendente',
        'qtd_inscricoes': 0,
        'qtd_inscricoes_maxima': 20,
        'data_evento': '2026-07-10',
        'data_criacao': date.today().isoformat(),
        'data_cancelamento': None,
        'data_atualizacao': None,
        'comentarios': [],
    }


def teste_listar_eventos(client):
    resposta = client.get('/eventos/')

    assert resposta.status_code == HTTPStatus.OK
    assert resposta.json() == {
        'eventos': [
            {
                'id': 1,
                'id_usuario_criador': 1,
                'id_unidade_associada': 2,
                'titulo': 'Vem Zumbar',
                'descricao': 'Evento de zumba',
                'endereco': 'Pérola Negra',
                'foto': 'aquivoFoto.png',
                'link_externo': 'www.linkExterno.com',
                'categoria': 'Esporte',
                'status': 'Pendente',
                'qtd_inscricoes': 0,
                'qtd_inscricoes_maxima': 20,
                'data_evento': '2026-07-10',
                'data_criacao': date.today().isoformat(),
                'data_cancelamento': None,
                'data_atualizacao': None,
                'comentarios': [],
            }
        ]
    }


def teste_listar_eventos_por_id_not_found(client):
    resposta = client.get('/eventos/-1')
    assert resposta.status_code == HTTPStatus.NOT_FOUND
    assert resposta.json() == {'detail': 'Evento não encontrado'}


def teste_listar_evento_por_id(client):
    resposta = client.get('/eventos/1')

    assert resposta.status_code == HTTPStatus.OK
    assert resposta.json() == {
        'id': 1,
        'id_usuario_criador': 1,
        'id_unidade_associada': 2,
        'titulo': 'Vem Zumbar',
        'descricao': 'Evento de zumba',
        'endereco': 'Pérola Negra',
        'foto': 'aquivoFoto.png',
        'link_externo': 'www.linkExterno.com',
        'categoria': 'Esporte',
        'status': 'Pendente',
        'qtd_inscricoes': 0,
        'qtd_inscricoes_maxima': 20,
        'data_evento': '2026-07-10',
        'data_criacao': date.today().isoformat(),
        'data_cancelamento': None,
        'data_atualizacao': None,
        'comentarios': [],
    }


def teste_atualizar_evento_not_found(client):
    resposta = client.put(
        '/atualizar_evento/-1',
        json={
            'id_usuario_criador': 1,
            'id_unidade_associada': 2,
            'titulo': 'Vem Zumbar 60+',
            'descricao': 'Evento de zumba',
            'endereco': 'Pérola Negra',
            'foto': 'aquivoFoto.png',
            'link_externo': 'www.linkExterno.com',
            'categoria': 'Esporte',
            'qtd_inscricoes_maxima': 20,
            'data_evento': '2026-07-10',
        },
    )
    assert resposta.status_code == HTTPStatus.NOT_FOUND
    assert resposta.json() == {'detail': 'Evento não encontrado'}


def teste_atualizar_evento(client):
    resposta = client.put(
        '/atualizar_evento/1',
        json={
            'id_usuario_criador': 1,
            'id_unidade_associada': 2,
            'titulo': 'Vem Zumbar 60+',
            'descricao': 'Evento de zumba',
            'endereco': 'Pérola Negra',
            'foto': 'aquivoFoto.png',
            'link_externo': 'www.linkExterno.com',
            'categoria': 'Esporte',
            'qtd_inscricoes_maxima': 20,
            'data_evento': '2026-07-10',
        },
    )

    assert resposta.status_code == HTTPStatus.OK
    assert resposta.json() == {
        'id': 1,
        'id_usuario_criador': 1,
        'id_unidade_associada': 2,
        'titulo': 'Vem Zumbar 60+',
        'descricao': 'Evento de zumba',
        'endereco': 'Pérola Negra',
        'foto': 'aquivoFoto.png',
        'link_externo': 'www.linkExterno.com',
        'categoria': 'Esporte',
        'status': 'Pendente',
        'qtd_inscricoes': 0,
        'qtd_inscricoes_maxima': 20,
        'data_evento': '2026-07-10',
        'data_criacao': date.today().isoformat(),
        'data_cancelamento': None,
        'data_atualizacao': None,
        'comentarios': [],
    }


def teste_remover_evento_not_found(client):
    resposta = client.delete('/remover_evento/-1')
    assert resposta.status_code == HTTPStatus.NOT_FOUND
    assert resposta.json() == {'detail': 'Evento não encontrado'}


def teste_remover_evento(client):
    resposta = client.delete('/remover_evento/1')

    assert resposta.status_code == HTTPStatus.OK
    assert resposta.json() == {'mensagem': 'Evento removido com sucesso!'}
