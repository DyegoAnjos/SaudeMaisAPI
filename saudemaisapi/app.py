from datetime import date
from http import HTTPStatus

from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from saudemaisapi.models import Evento
from saudemaisapi.schemas import EventoGet, EventoPost, EventosList, Message
from saudemaisapi.settings import Settings

app = FastAPI(title='Saude+API')

bd = []


# GET
@app.get('/eventos/', status_code=HTTPStatus.OK, response_model=EventosList)
def listar_eventos():
    return {'eventos': bd}


@app.get(
    '/eventos/{id_evento}',
    status_code=HTTPStatus.OK,
    response_model=EventoGet,
)
def listar_eventos_por_id(id_evento: int):
    if id_evento < 0 or id_evento > len(bd):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Evento não encontrado'
        )
    return bd[id_evento - 1].model_dump()


# POST
@app.post(
    '/criar_evento/',
    status_code=HTTPStatus.CREATED,
    response_model=EventoGet,
)
def criar_eventos(evento: EventoPost):

    engine = create_engine(Settings().DATABASE_URL)

    session = Session(engine)

    evento_bd = session.scalar(
        select(Evento).where(Evento.titulo == evento.titulo)
    )

    if evento_bd:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Evento já existe!',
        )

    evento_bd = Evento(**evento.model_dump())

    session.add(evento_bd)
    session.commit()

    return evento_bd


# PUT
@app.put(
    '/atualizar_evento/{id_evento}',
    status_code=HTTPStatus.OK,
    response_model=EventoGet,
)
def atualizar_evento(evento: EventoPost, id_evento: int):
    if id_evento < 0 or id_evento > len(bd):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Evento não encontrado'
        )

    evento_basic = EventoGet(
        **evento.model_dump(),
        id=id_evento,
        status='Pendente',
        data_criacao=date.today().isoformat(),
    )
    bd[id_evento - 1] = evento_basic

    return evento_basic


# DELETE
@app.delete(
    '/remover_evento/{id_evento}',
    status_code=HTTPStatus.OK,
    response_model=Message,
)
def remover_evento(id_evento: int):
    if id_evento < 0 or id_evento > len(bd):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Evento não encontrado'
        )

    del bd[id_evento - 1]

    return {'mensagem': 'Evento removido com sucesso!'}
