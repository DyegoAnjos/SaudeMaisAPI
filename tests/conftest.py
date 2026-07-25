from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from saudemaisapi.app import app
from saudemaisapi.database import get_db
from saudemaisapi.models import Evento, registrador_tabela
from saudemaisapi.schemas import Usuario, Usuario_comum


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
def usuario_comum(session):
    usuario = Usuario_comum(
        email='exemplo@gmail.com',
        nome= 'exemplo',
        senha='segredo',
        cpf='123456',
        data_nascimento=datetime(2026, 7, 10, 10, 10),
        regiao_preferida= 'Urca'
    )
    session.add(usuario)
    session.commit()
    session.refresh(usuario)

    return usuario


@pytest.fixture
def usuario_institucional(session):
    usuario = Usuario_institucional()


@pytest.fixture
def evento(session, mock_db_time):
    evento = Evento(
        titulo='Vem Zumbar',
        descricao='Evento de zumba para 60+',
        data_hora_evneto= datetime(2026, 7, 24, 10, 10,10),
        data_hora_fim= datetime(2026, 7, 30, 10, 10,10),
        publico_alvo= 'Idosos',
        categoria= 'Zumba',
        criador_institucional= 1,
        capacidade_maxima= 10,
        unidade_associada= 1,
        endereco = 'Jovelina',
        pagina_evento= 'www.vemzumbar60.com',
        data_hora_criacao=mock_db_time
    )
    session.add(evento)
    session.commit()
    session.refresh(evento)

    return evento
