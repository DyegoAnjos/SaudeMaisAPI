from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from saudemaisapi.app import app
from saudemaisapi.database import get_db
from saudemaisapi.models import Evento, registrador_tabela


@pytest.fixture
def client(session):
    def pergar_sessao_sobreescrita():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_db] = pergar_sessao_sobreescrita
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    registrador_tabela.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    registrador_tabela.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def mock_db_time():
    time = datetime(2026, 7, 10, 10, 10)

    def fake_time_hook(mapper, connection, target):
        if hasattr(target, 'data_criacao'):
            target.data_criacao = time

    event.listen(Evento, 'before_insert', fake_time_hook)

    yield time

    event.remove(Evento, 'before_insert', fake_time_hook)


@pytest.fixture
def evento(session, mock_db_time):
    evento = Evento(
        titulo='Vem Zumbar',
        data=mock_db_time,
        usuario_criador=1,
        tipo_evento=1,
        foto_evento=1,
        descricao='Zumba para idosos',
        capacidade_maxima=20,
        endereco='Jovelina Pérola Negra',
        unidade_associada=1,
        link_externo='www.vemzumbar60.com',
    )
    session.add(evento)
    session.commit()
    session.refresh(evento)

    return evento
