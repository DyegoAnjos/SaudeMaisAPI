from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from saudemaisapi.database import get_db
from saudemaisapi.models import Fotografias
from saudemaisapi.schemas import (
    Filtro_Paginas,
    Fotografia_lista_Schema,
    Fotografia_retorno_Schema,
    Fotografias_Schema,
    MessageSchema,
)

router = APIRouter(prefix='/fotografias', tags=['Fotografias'])

SessionDep = Annotated[Session, Depends(get_db)]


@router.get(
    '/',
    status_code=HTTPStatus.OK,
    response_model=Fotografia_lista_Schema,
)
def listar_fotografias(
    session: SessionDep, filtro: Annotated[Filtro_Paginas, Query()]
):
    fotografias_db = session.scalars(
        select(Fotografias).limit(filtro.limit).offset(filtro.offset)
    ).all()

    return {
        'fotografias': [
            Fotografia_retorno_Schema.model_validate(f) for f in fotografias_db
        ]
    }


@router.get(
    '/{id_fotografia}',
    status_code=HTTPStatus.OK,
    response_model=Fotografia_retorno_Schema,
)
def listar_fotografia_por_id(id_fotografia: int, session: SessionDep):

    fotografia = session.scalar(
        select(Fotografias).where(Fotografias.id == id_fotografia)
    )

    if not fotografia:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Fotografia não encontrada',
        )

    return fotografia


@router.post(
    '/criar_fotografia',
    status_code=HTTPStatus.CREATED,
    response_model=Fotografia_retorno_Schema,
)
def criar_fotografia(fotografia: Fotografias_Schema, session: SessionDep):

    fotografia = Fotografias(**fotografia.model_dump())

    session.add(fotografia)
    session.commit()

    session.refresh(fotografia)

    return fotografia


@router.put(
    '/atualizar_fotografia/{id_fotografia}',
    status_code=HTTPStatus.OK,
    response_model=Fotografia_retorno_Schema,
)
def atualizar_fotografia(
    fotografia: Fotografias_Schema, id_fotografia, session: SessionDep
):
    fotografia_bd = session.scalar(
        select(Fotografias).where(Fotografias.id == id_fotografia)
    )
    if not fotografia_bd:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Fotografia não encontrada',
        )
    try:
        for chave, valor in fotografia.model_dump(exclude_unset=True).items():
            setattr(fotografia_bd, chave, valor)

        session.commit()
        session.refresh(fotografia_bd)

        return fotografia_bd
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Fotografia já existe!',
        )


@router.delete(
    '/remover_fotografia/{id_fotografia}',
    status_code=HTTPStatus.OK,
    response_model=MessageSchema,
)
def remover_fotografia(id_fotografia, session: SessionDep):
    fotografia = session.scalar(
        select(Fotografias).where(Fotografias.id == id_fotografia)
    )
    if not fotografia:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Fotografia não encontrada',
        )

    session.delete(fotografia)
    session.commit()

    return {'message': 'Fotografia removida com sucesso!'}
