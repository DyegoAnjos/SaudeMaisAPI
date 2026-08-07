from http import HTTPStatus

from saudemaisapi.schemas import Fotografia_retorno_Schema


def teste_listar_fotografias(
    client,
    mock_db_time,
    fotografia_de_usuario,
    fotografia_de_evento,
):
    fotografias_schema = []
    for foto in (fotografia_de_usuario, fotografia_de_evento):
        dados = Fotografia_retorno_Schema.model_validate(foto).model_dump(
            mode='json'
        )
        fotografias_schema.append(dados)

    resposta = client.get('/fotografias/')

    assert resposta.status_code == HTTPStatus.OK
    assert resposta.json() == {'fotografias': fotografias_schema}


def teste_listar_fotografias_null(client):
    resposta = client.get('/fotografias/')

    assert resposta.status_code == HTTPStatus.OK
    assert resposta.json() == {'fotografias': []}


def teste_listar_fotografia_de_usuario_por_id(
    client,
    mock_db_time,
    fotografia_de_usuario,
):
    resposta = client.get('/fotografias/1/')

    assert resposta.status_code == HTTPStatus.OK
    assert resposta.json() == {
        'id': 1,
        'nome': 'Usuario',
        'arquivo': 'arquivo_binario',
        'foto_de_evento': False,
        'data_hora_envio': mock_db_time.isoformat(),
    }


def teste_listar_fotografia_de_evento_por_id(
    client,
    mock_db_time,
    fotografia_de_evento,
):
    resposta = client.get('/fotografias/1/')

    assert resposta.status_code == HTTPStatus.OK
    assert resposta.json() == {
        'id': 1,
        'nome': 'Foto Vem Zumbar',
        'arquivo': 'arquivo_binario',
        'foto_de_evento': True,
        'data_hora_envio': mock_db_time.isoformat(),
    }


def teste_listar_fotografia_not_found(client):
    resposta = client.get('/fotografias/-1')

    assert resposta.status_code == HTTPStatus.NOT_FOUND
    assert resposta.json() == {'detail': 'Fotografia não encontrada'}


def criar_fotografia_usuario(
    client,
    fotografia_de_usuario,
    mock_db_time,
):
    resposta = client.post(
        '/fotografias/criar_fotografia',
        json={
            'nome': 'Usuario novo',
            'arquivo': 'arquivo_binario',
            'foto_de_evento': False,
        },
    )

    assert resposta.status_code == HTTPStatus.CREATED
    assert resposta.json() == {
        'id': 2,
        'nome': 'Usuario novo',
        'arquivo': 'arquivo_binario',
        'foto_de_evento': False,
        'data_hora_envio': mock_db_time.isoformat(),
    }


def teste_atualizar_fotografia_de_usuario(
    client,
    fotografia_de_usuario,
    mock_db_time,
):
    resposta = client.put(
        '/fotografias/atualizar_fotografia/1',
        json={
            'nome': 'Usuario atualizado',
            'arquivo': 'arquivo_binario',
            'foto_de_evento': False,
        },
    )

    assert resposta.status_code == HTTPStatus.OK
    assert resposta.json() == {
        'id': 1,
        'nome': 'Usuario atualizado',
        'arquivo': 'arquivo_binario',
        'foto_de_evento': False,
        'data_hora_envio': mock_db_time.isoformat(),
    }

def teste_atualizar_fotografia_de_evento(
    client,
    fotografia_de_evento,
    mock_db_time,
):
    resposta = client.put(
        '/fotografias/atualizar_fotografia/1',
        json={
            'nome': 'Evento atualizado',
            'arquivo': 'arquivo_binario',
            'foto_de_evento': False,
        },
    )

    assert resposta.status_code == HTTPStatus.OK
    assert resposta.json() == {
        'id': 1,
        'nome': 'Evento atualizado',
        'arquivo': 'arquivo_binario',
        'foto_de_evento': True,
        'data_hora_envio': mock_db_time.isoformat(),
    }

def atualizar_fotografia_not_found(
        client,
        fotografia_de_evento,
):
    resposta = client.put(
        '/fotografias/atualizar_fotografia/-1',
    )

    assert resposta.status_code == HTTPStatus.NOT_FOUND
    assert resposta.json() == {
        'detail': 'Fotografia não encontrada'
    }

