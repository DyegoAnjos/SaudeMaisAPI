from contextlib import contextmanager
from datetime import date

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session

from saudemaisapi.app import app
from saudemaisapi.models import Evento, registrador_tabela


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')
    registrador_tabela.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    registrador_tabela.metadata.drop_all(engine)
    engine.dispose()


@contextmanager
def _mock_db_time(*, model, time=date(2026, 7, 10)):

    def fake_time_hook(mapper, connection, target):
        if hasattr(target, 'data_criacao'):
            target.data_criacao = time
        if hasattr(target, 'data_atualizacao'):
            target.data_criacao = date(2026, 7, 20)

    event.listen(Evento, 'before_insert', fake_time_hook)

    yield time

    event.remove(Evento, 'before_insert', fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time
