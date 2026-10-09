from http import HTTPStatus
from pathlib import Path

from saudemaisapi.routers import usuarios_institucionais


def dados_institucional():
    return {
        'email': 'instituicao@saudemais.com',
        'nome': 'Instituição Saúde Mais',
        'senha': 'segredo',
        'cnpj': '12345678000199',
        'vinculo_instituicao': 'Unidade de saúde',
        'razao_social': 'Instituição Saúde Mais LTDA',
        'nome_responsavel': 'Maria da Silva',
        'cargo_responsavel': 'Diretora',
        'site': 'https://saudemais.com',
        'telefone': '2133334444',
        'descricao': 'Atendimento à comunidade',
        'endereco': 'Rua da Saúde, 10',
    }


def test_crud_usuario_institucional(client, tmp_path, monkeypatch):
    monkeypatch.setattr(usuarios_institucionais, 'PASTA_DOCUMENTOS', tmp_path)
    dados = dados_institucional()

    resposta = client.post(
        '/usuarios/institucional/criar_usuario/', json=dados
    )
    assert resposta.status_code == HTTPStatus.CREATED
    usuario = resposta.json()
    assert usuario['cnpj'] == dados['cnpj']
    assert usuario['razao_social'] == dados['razao_social']
    assert usuario['status'] == 'Pendente'
    assert 'senha' not in usuario

    id_usuario = usuario['id']
    resposta = client.post(
        f'/usuarios/institucional/{id_usuario}/documentos',
        files={
            'docCnpj': ('cnpj.pdf', b'comprovante cnpj', 'application/pdf'),
            'docResponsavel': (
                'responsavel.png',
                b'documento responsavel',
                'image/png',
            ),
            'docVinculo': (
                'vinculo.jpg',
                b'comprovante vinculo',
                'image/jpeg',
            ),
        },
    )
    assert resposta.status_code == HTTPStatus.OK
    caminhos = [
        resposta.json()['documento_cnpj'],
        resposta.json()['documento_responsavel'],
        resposta.json()['documento_vinculo'],
    ]
    assert all(Path(caminho).is_file() for caminho in caminhos)

    resposta = client.get(f'/usuarios/institucional/{id_usuario}')
    assert resposta.status_code == HTTPStatus.OK

    resposta = client.get('/usuarios/institucional/')
    assert resposta.status_code == HTTPStatus.OK
    assert len(resposta.json()) == 1

    dados['descricao'] = 'Descrição atualizada'
    resposta = client.put(
        f'/usuarios/institucional/atualizar_usuario/{id_usuario}', json=dados
    )
    assert resposta.status_code == HTTPStatus.OK
    assert resposta.json()['descricao'] == dados['descricao']

    resposta = client.delete(
        f'/usuarios/institucional/deletar_usuario/{id_usuario}'
    )
    assert resposta.status_code == HTTPStatus.OK
    assert resposta.json() == {'mensagem': 'Usuário removido com sucesso!'}
    assert all(not Path(caminho).exists() for caminho in caminhos)


def test_nao_cria_institucional_com_dados_repetidos(client):
    dados = dados_institucional()
    client.post('/usuarios/institucional/criar_usuario/', json=dados)

    resposta = client.post(
        '/usuarios/institucional/criar_usuario/', json=dados
    )
    assert resposta.status_code == HTTPStatus.CONFLICT


def test_rejeita_documento_institucional_invalido(client):
    resposta = client.post(
        '/usuarios/institucional/criar_usuario/',
        json=dados_institucional(),
    )
    id_usuario = resposta.json()['id']

    resposta = client.post(
        f'/usuarios/institucional/{id_usuario}/documentos',
        files={
            'docCnpj': ('cnpj.txt', b'arquivo', 'text/plain'),
            'docResponsavel': (
                'responsavel.pdf',
                b'documento',
                'application/pdf',
            ),
        },
    )
    assert resposta.status_code == HTTPStatus.UNSUPPORTED_MEDIA_TYPE
