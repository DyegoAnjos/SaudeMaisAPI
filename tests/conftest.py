from datetime import datetime

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import StaticPool

from saudemaisapi.app import app
from saudemaisapi.database import get_db
from saudemaisapi.models import (
    Categoria,
    Comentario,
    Evento,
    Fotografias,
    Sugestao,
    Unidade_saude,
    Usuario_administrador,
    Usuario_comum,
    Usuario_institucional,
    registrador_tabela,
)
from saudemaisapi.routers import fotografias as fotografias_router


@pytest.fixture
def client(session):
    def pergar_sessao_sobreescrita():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_db] = pergar_sessao_sobreescrita
        yield client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def session():
    engine = create_async_engine(
        'sqlite+aiosqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(registrador_tabela.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(registrador_tabela.metadata.drop_all)


@pytest.fixture(autouse=True)
def pasta_de_upload_temporaria(tmp_path, monkeypatch):
    monkeypatch.setattr(fotografias_router, 'PASTA_UPLOADS', tmp_path)
    return tmp_path


@pytest.fixture
def mock_db_time():
    time = datetime(2026, 7, 10, 10, 10)

    def fake_time_hook(mapper, connection, target):
        if hasattr(target, 'data_hora_criacao'):
            target.data_hora_criacao = time
        elif hasattr(target, 'data_hora_envio'):
            target.data_hora_envio = time
        elif hasattr(target, 'data_hora_feito'):
            target.data_hora_feito = time
        elif hasattr(target, 'data_hora_evento'):
            target.data_hora_evento = datetime(2026, 7, 24, 10, 10, 10)
        elif hasattr(target, 'data_hora_fim'):
            target.data_hora_fim = datetime(2026, 7, 30, 10, 10, 10)
        elif hasattr(target, 'data_hora_envio'):
            target.data_hora_envio = time

    event.listen(Evento, 'before_insert', fake_time_hook)
    event.listen(Fotografias, 'before_insert', fake_time_hook)

    yield time

    event.remove(Evento, 'before_insert', fake_time_hook)
    event.remove(Fotografias, 'before_insert', fake_time_hook)


@pytest_asyncio.fixture
async def usuario_comum(session: AsyncSession):
    usuario = Usuario_comum(
        email='exemplo@gmail.com',
        nome='exemplo',
        senha='segredo',
        cpf='123456',
        data_nascimento=datetime(2026, 7, 10, 10, 10),
        regiao_preferida='Urca',
        telefone='123456',
    )
    session.add(usuario)
    await session.commit()
    await session.refresh(usuario)

    return usuario


@pytest.fixture
def usuario_institucional(session):
    usuario = Usuario_institucional(
        email='institucional@gmail.com',
        nome='institutoExemplo',
        senha='segredo',
        cnpj='123456',
        vinculo_institucao='Posto',
        descricao='Posto de saúde',
        endereco='Pavuna',
        telefone='123456',
    )

    session.add(usuario)
    session.commit()
    session.refresh(usuario)

    return usuario


@pytest.fixture
def usuario_administrador(session):
    usuario = Usuario_administrador(
        email='institucional@gmail.com',
        nome='institutoExemplo',
        senha='segredo',
        telefone='123456',
    )

    session.add(usuario)
    session.commit()
    session.refresh(usuario)

    return usuario


@pytest.fixture
def sugestao(session):
    sugestao = Sugestao(
        titulo='Trocar o nome',
        conteudo='Seria bom trocar o nome',
        data_hora_envio=mock_db_time,
        usuario=1,
    )

    session.add(sugestao)
    session.commit()
    session.refresh(sugestao)

    return sugestao


@pytest.fixture
def comentario(session):
    comentario = Comentario(
        data_hora_feito=mock_db_time,
        titulo='Evento top',
        conteudo='Esse evento é muito bom!',
        usuario=1,
        evento=1,
        nota=5,
    )

    session.add(comentario)
    session.commit()
    session.refresh(comentario)

    return comentario


@pytest.fixture
def unidade_saude(session):
    unidade_saude = Unidade_saude(
        nome='Posto X',
        endereco='Urca',
        latitude=1.5,
        longitude=1.6,
        lotacao=10,
        tempo_medio_atendimento=50,
        especialidade='Coração',
    )

    session.add(unidade_saude)
    session.commit()
    session.refresh(unidade_saude)

    return unidade_saude


@pytest.fixture
def categoria(session):
    categoria = Categoria(
        nome='Zumba', descricao='Evendos da modalidade Zumba'
    )

    session.add(categoria)
    session.commit()
    session.refresh(categoria)

    return categoria


@pytest_asyncio.fixture
async def evento(session: AsyncSession, mock_db_time):
    evento = Evento(
        titulo='Vem Zumbar',
        descricao='Evento de zumba para 60+',
        data_hora_evento=mock_db_time,
        data_hora_fim=mock_db_time,
        publico_alvo='Idosos',
        categoria=1,
        foto_evento=1,
        criador_institucional=1,
        capacidade_maxima=10,
        unidade_associada=1,
        endereco='Jovelina',
        pagina_evento='www.vemzumbar60.com',
    )
    evento.data_hora_criacao = mock_db_time
    session.add(evento)
    await session.commit()
    await session.refresh(evento)

    return evento


@pytest.fixture
def fotografia_de_evento(session, mock_db_time, pasta_de_upload_temporaria):
    caminho = pasta_de_upload_temporaria / 'evento.jpg'
    caminho.write_bytes(b'foto_evento')
    fotografias = Fotografias(
        nome='evento.jpg',
        caminho=str(caminho),
        tipo='image/jpeg',
        tamanho=11,
        foto_de_evento=True,
    )

    fotografias.data_hora_envio = mock_db_time
    session.add(fotografias)
    session.commit()
    session.refresh(fotografias)

    return fotografias


@pytest.fixture
def fotografia_de_usuario(session, mock_db_time, pasta_de_upload_temporaria):
    caminho = pasta_de_upload_temporaria / 'usuario.png'
    caminho.write_bytes(b'foto_usuario')
    fotografias = Fotografias(
        nome='usuario.png',
        caminho=str(caminho),
        tipo='image/png',
        tamanho=12,
        foto_de_evento=False,
    )

    fotografias.data_hora_envio = mock_db_time
    session.add(fotografias)
    session.commit()
    session.refresh(fotografias)

    return fotografias
