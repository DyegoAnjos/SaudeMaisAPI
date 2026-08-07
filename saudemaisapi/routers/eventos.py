from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from saudemaisapi.database import get_db
from saudemaisapi.models import Evento
from saudemaisapi.schemas import (
    Evento_retorno_Schema,
    Evento_Schema,
    Eventos_list_Schema,
    Filtro_Paginas,
    MessageSchema,
)

router = APIRouter(prefix='/eventos', tags=['Eventos'])

Session = Annotated[Session, Depends(get_db)]

# GET


@router.get('/', status_code=HTTPStatus.OK, response_model=Eventos_list_Schema)
def listar_eventos(
    session: Session, filtro: Annotated[Filtro_Paginas, Query()]
):
    eventos = session.scalars(
        select(Evento).limit(filtro.limit).offset(filtro.offset)
    )

    return {'eventos': eventos}


@router.get(
    '/{id_evento}',
    status_code=HTTPStatus.OK,
    response_model=Evento_retorno_Schema,
)
def listar_eventos_por_id(id_evento: int, session: Session):

    eventos = session.scalar(select(Evento).where(Evento.id == id_evento))

    if not eventos:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Evento não encontrado'
        )

    return eventos


# POST
@router.post(
    '/criar_evento/',
    status_code=HTTPStatus.CREATED,
    response_model=Evento_retorno_Schema,
)
def criar_eventos(evento: Evento_Schema, session: Session):
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
@router.put(
    '/atualizar_evento/{id_evento}',
    status_code=HTTPStatus.OK,
    response_model=Evento_retorno_Schema,
)
def atualizar_evento(evento: Evento_Schema, id_evento: int, session: Session):
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
@router.delete(
    '/remover_evento/{id_evento}',
    status_code=HTTPStatus.OK,
    response_model=MessageSchema,
)
def remover_evento(id_evento: int, session: Session):
    evento_bd = session.scalar(select(Evento).where(Evento.id == id_evento))
    if not evento_bd:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Evento não encontrado'
        )
    session.delete(evento_bd)
    session.commit()

    return {'mensagem': 'Evento removido com sucesso!'}
