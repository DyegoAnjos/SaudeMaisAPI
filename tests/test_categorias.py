from http import HTTPStatus


def test_listar_categorias_vazio(client):
    resposta = client.get('/categorias/')
    assert resposta.status_code == HTTPStatus.OK
    assert resposta.json() == {'categorias': []}


def test_crud_categoria(client):
    criacao = client.post(
        '/categorias/',
        json={'nome': 'Atividade física', 'descricao': 'Exercícios'},
    )
    assert criacao.status_code == HTTPStatus.CREATED
    assert criacao.json() == {
        'id': 1,
        'nome': 'Atividade física',
        'descricao': 'Exercícios',
    }

    busca = client.get('/categorias/1')
    assert busca.status_code == HTTPStatus.OK
    assert busca.json() == criacao.json()

    atualizacao = client.put(
        '/categorias/1',
        json={'nome': 'Vacinação', 'descricao': 'Campanhas de vacinação'},
    )
    assert atualizacao.status_code == HTTPStatus.OK
    assert atualizacao.json()['nome'] == 'Vacinação'

    remocao = client.delete('/categorias/1')
    assert remocao.status_code == HTTPStatus.OK
    assert remocao.json() == {'mensagem': 'Categoria removida com sucesso!'}

    assert client.get('/categorias/1').status_code == HTTPStatus.NOT_FOUND


def test_categoria_duplicada(client, categoria):
    resposta = client.post(
        '/categorias/',
        json={'nome': categoria.nome, 'descricao': 'Outra descrição'},
    )
    assert resposta.status_code == HTTPStatus.CONFLICT
    assert resposta.json() == {'detail': 'Categoria já existe'}


def test_categoria_invalida(client):
    resposta = client.post('/categorias/', json={'nome': '', 'descricao': ''})
    assert resposta.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_categoria_nao_encontrada(client):
    assert client.get('/categorias/999').status_code == HTTPStatus.NOT_FOUND
    assert (
        client.put(
            '/categorias/999',
            json={'nome': 'Teste', 'descricao': 'Teste'},
        ).status_code
        == HTTPStatus.NOT_FOUND
    )
    assert client.delete('/categorias/999').status_code == HTTPStatus.NOT_FOUND
