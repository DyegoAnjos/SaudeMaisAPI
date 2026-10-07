from http import HTTPStatus


def dados_administrador():
    return {
        'email': 'admin@saudemais.com',
        'nome': 'Administrador',
        'senha': 'segredo',
        'telefone': '21999999999',
    }


def test_crud_usuario_administrador(client):
    dados = dados_administrador()

    resposta = client.post(
        '/usuarios/administrador/criar_usuario/', json=dados
    )
    assert resposta.status_code == HTTPStatus.CREATED
    usuario = resposta.json()
    assert usuario['email'] == dados['email']
    assert 'senha' not in usuario

    id_usuario = usuario['id']
    resposta = client.get(f'/usuarios/administrador/{id_usuario}')
    assert resposta.status_code == HTTPStatus.OK

    resposta = client.get('/usuarios/administrador/')
    assert resposta.status_code == HTTPStatus.OK
    assert len(resposta.json()) == 1

    dados['nome'] = 'Administrador atualizado'
    resposta = client.put(
        f'/usuarios/administrador/atualizar_usuario/{id_usuario}', json=dados
    )
    assert resposta.status_code == HTTPStatus.OK
    assert resposta.json()['nome'] == dados['nome']

    resposta = client.delete(
        f'/usuarios/administrador/deletar_usuario/{id_usuario}'
    )
    assert resposta.status_code == HTTPStatus.OK
    assert resposta.json() == {'mensagem': 'Usuário removido com sucesso!'}


def test_nao_cria_administrador_com_email_repetido(client):
    dados = dados_administrador()
    client.post('/usuarios/administrador/criar_usuario/', json=dados)

    resposta = client.post(
        '/usuarios/administrador/criar_usuario/', json=dados
    )
    assert resposta.status_code == HTTPStatus.CONFLICT
