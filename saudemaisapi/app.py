from http import HTTPStatus

from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
)
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from saudemaisapi.database import get_db
from saudemaisapi.models import Evento
from saudemaisapi.schemas import EventoGet, EventoPost, EventosList, Message

app = FastAPI(title='Saude+API')


bd = []


# GET
@app.get('/eventos/', status_code=HTTPStatus.OK, response_model=EventosList)
def listar_eventos(
    limit: int = 10, offset: int = 0, session: Session = Depends(get_db)
):
    eventos = session.scalars(select(Evento).limit(limit).offset(offset))

    return {'eventos': eventos}


@app.get(
    '/eventos/{id_evento}',
    status_code=HTTPStatus.OK,
    response_model=EventoGet,
)
def listar_eventos_por_id(id_evento: int, session: Session = Depends(get_db)):

    eventos = session.scalar(select(Evento).where(Evento.id == id_evento))

    if not eventos:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Evento não encontrado'
        )

    return eventos


# POST
@app.post(
    '/criar_evento/',
    status_code=HTTPStatus.CREATED,
    response_model=EventoGet,
)
def criar_eventos(evento: EventoPost, session: Session = Depends(get_db)):
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

    session.refresh(evento_bd)

    return evento_bd


# PUT
@app.put(
    '/atualizar_evento/{id_evento}',
    status_code=HTTPStatus.OK,
    response_model=EventoGet,
)
def atualizar_evento(
    evento: EventoPost, id_evento: int, session: Session = Depends(get_db)
):
    evento_bd = session.scalar(select(Evento).where(Evento.id == id_evento))
    if not evento_bd:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Evento não encontrado'
        )

    try:
        for chave, valor in evento.model_dump(exclude_unset=True).items():
            setattr(evento_bd, chave, valor)

        session.commit()
        session.refresh(evento_bd)

        return evento_bd
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Evento já existe!',
        )


# DELETE
@app.delete(
    '/remover_evento/{id_evento}',
    status_code=HTTPStatus.OK,
    response_model=Message,
)
def remover_evento(id_evento: int, session: Session = Depends(get_db)):
    evento_bd = session.scalar(select(Evento).where(Evento.id == id_evento))
    if not evento_bd:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Evento não encontrado'
        )
    session.delete(evento_bd)
    session.commit()

    return {'mensagem': 'Evento removido com sucesso!'}
