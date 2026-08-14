from datetime import datetime, timedelta
from http import HTTPStatus

import pytest
from pydantic import ValidationError

from saudemaisapi.schemas import Comentario_Schema

EVENTO_VALIDO = {
    'titulo': 'Campanha de saúde',
    'descricao': 'Atendimento à população',
    'data_hora_evento': datetime(2026, 9, 10, 9).isoformat(),
    'data_hora_fim': datetime(2026, 9, 10, 17).isoformat(),
    'publico_alvo': 'Todos',
    'categoria': 1,
    'foto_evento': 1,
    'criador_institucional': 1,
    'capacidade_maxima': 50,
}


def test_evento_rejeita_capacidade_zero(client):
    resposta = client.post(
        '/eventos/criar_evento/',
        json={**EVENTO_VALIDO, 'capacidade_maxima': 0},
    )
    assert resposta.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_evento_rejeita_data_final_anterior(client):
    inicio = datetime(2026, 9, 10, 9)
    resposta = client.post(
        '/eventos/criar_evento/',
        json={
            **EVENTO_VALIDO,
            'data_hora_evento': inicio.isoformat(),
            'data_hora_fim': (inicio - timedelta(hours=1)).isoformat(),
        },
    )
    assert resposta.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    ('nota', 'valida'),
    [(-1, False), (0, True), (5, True), (6, False)],
)
def test_nota_de_comentario_entre_zero_e_cinco(nota, valida):
    dados = {
        'nota': nota,
        'titulo': 'Avaliação',
        'conteudo': 'Comentário sobre o evento',
        'usuario': 1,
        'evento': 1,
    }
    if valida:
        assert Comentario_Schema(**dados).nota == nota
    else:
        with pytest.raises(ValidationError):
            Comentario_Schema(**dados)


@pytest.mark.parametrize('consulta', ['limit=0', 'limit=101', 'offset=-1'])
def test_paginacao_rejeita_valores_invalidos(client, consulta):
    resposta = client.get(f'/eventos/?{consulta}')
    assert resposta.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
