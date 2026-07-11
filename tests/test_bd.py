from dataclasses import asdict
from datetime import date

from sqlalchemy import select

from saudemaisapi.models import Evento


def test_criar_evento(session, mock_db_time):
    with mock_db_time(model=Evento) as time:
        novo_evento = Evento(
            titulo='Vem Zumbar',
            data=date(2026, 7, 10),
            usuario_criador=1,
            tipo_evento=1,
            foto_evento=1,
            capacidade_maxima=10,
        )

        session.add(novo_evento)
        session.commit()

        evento = session.scalar(
            select(Evento).where(Evento.titulo == 'Vem Zumbar')
        )

    assert asdict(evento) == {
        'id': 1,
        'data_criacao': time,
        'titulo': 'Vem Zumbar',
        'data': date(2026, 7, 10),
        'usuario_criador': 1,
        'tipo_evento': 1,
        'foto_evento': 1,
        'descricao': None,
        'capacidade_maxima': 10,
        'endereco': None,
        'status': None,
        'unidade_associada': None,
        'data_cancelamento': None,
        'data_ultima_atualizacao': None,
    }
