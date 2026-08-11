from http import HTTPStatus

UNIDADE = {
    'nome': 'Clínica da Família Centro',
    'endereco': 'Rua Principal, 10',
    'latitude': -22.9,
    'longitude': -43.2,
    'lotacao': 20,
    'tempo_medio_atendimento': 30,
    'especialidade': 'Clínica geral',
}


def test_listar_unidades_vazio(client):
    resposta = client.get('/unidades-saude/')
    assert resposta.status_code == HTTPStatus.OK
    assert resposta.json() == {'unidades': []}


def test_crud_unidade(client):
    criacao = client.post('/unidades-saude/', json=UNIDADE)
    assert criacao.status_code == HTTPStatus.CREATED
    assert criacao.json() == {'id': 1, **UNIDADE}

    busca = client.get('/unidades-saude/1')
    assert busca.status_code == HTTPStatus.OK
    assert busca.json() == criacao.json()

    novos_dados = {**UNIDADE, 'nome': 'Clínica Atualizada', 'lotacao': 35}
    atualizacao = client.put('/unidades-saude/1', json=novos_dados)
    assert atualizacao.status_code == HTTPStatus.OK
    assert atualizacao.json() == {'id': 1, **novos_dados}

    remocao = client.delete('/unidades-saude/1')
    assert remocao.status_code == HTTPStatus.OK
    assert remocao.json() == {
        'mensagem': 'Unidade de saúde removida com sucesso!'
    }

    assert client.get('/unidades-saude/1').status_code == HTTPStatus.NOT_FOUND


def test_unidade_duplicada(client, unidade_saude):
    resposta = client.post(
        '/unidades-saude/',
        json={**UNIDADE, 'nome': unidade_saude.nome},
    )
    assert resposta.status_code == HTTPStatus.CONFLICT
    assert resposta.json() == {'detail': 'Unidade de saúde já existe'}


def test_unidade_invalida(client):
    resposta = client.post(
        '/unidades-saude/',
        json={**UNIDADE, 'latitude': -100, 'lotacao': -1},
    )
    assert resposta.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_unidade_nao_encontrada(client):
    assert (
        client.get('/unidades-saude/999').status_code == HTTPStatus.NOT_FOUND
    )
    assert (
        client.put('/unidades-saude/999', json=UNIDADE).status_code
        == HTTPStatus.NOT_FOUND
    )
    assert (
        client.delete('/unidades-saude/999').status_code
        == HTTPStatus.NOT_FOUND
    )
