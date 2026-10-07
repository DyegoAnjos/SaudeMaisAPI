from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from saudemaisapi.database import get_db
from saudemaisapi.models import Evento, Inscricao, Usuario_comum
from saudemaisapi.schemas import (
    Filtro_Paginas,
    Inscrever_Schema,
    Inscricao_Schema,
    MessageSchema,
)

router = APIRouter(prefix='/inscricao', tags=['Inscrição'])

Session = Annotated[AsyncSession, Depends(get_db)]


# UTIL
async def validar_inscricao(Inscricao: Inscricao_Schema, session: Session):
    usuario_db = await session.scalar(
        select(Usuario_comum).where(
            Usuario_comum.id == Inscrever_Schema.id_usuario
        )
    )

    if not usuario_db:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Usuário não encontrado!'
        )

    evento_db = await session.scalar(
        select(Evento).wherer(Evento.id == Inscrever_Schema.id_evento)
    )

    if not evento_db:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Evento não encontrado!'
        )


# GET


@router.get(
    '/{id_usuario}/',
    status_code=HTTPStatus.OK,
    response_model=list[Inscricao_Schema],
)
async def listar_inscircoes(
    id_usuario: int,
    session: Session,
    filtro: Annotated[Filtro_Paginas, Query()],
):
    inscricoes = (
        await session.scalars(
            select(Inscricao)
            .where(Inscricao.usuario == id_usuario)
            .limit(filtro.limit)
            .offset(filtro.offset)
        )
    ).all()

    return inscricoes


# POST


@router.post(
    '/inscrever',
    status_code=HTTPStatus.OK,
    response_model=Inscricao_Schema,
)
async def inscrever(inscricao: Inscrever_Schema, session: Session):

    await validar_inscricao(inscricao, session)

    inscricao_db = await session.scalar(
        select(Inscricao).where(Inscricao.usuario == inscricao.usuario)
    )

    if inscricao_db:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Usuário já inscrito!'
        )

    inscricao_db = Inscricao(**inscricao.model_dump())

    session.add(inscricao_db)
    await session.commit()

    await session.refresh(inscricao_db)

    return inscricao_db


# DELETE


@router.delete(
    '/cancelar_inscricao',
    status_code=HTTPStatus.OK,
    response_model=MessageSchema,
)
async def cancelar_inscricao(inscricao: Inscrever_Schema, session: Session):
    inscricao_db = await session.scalar(
        select(Inscricao).where(
            Inscricao.usuario == inscricao.id_usuario,
            Inscricao.evento == inscricao.id_evento,
        )
    )

    if not inscricao_db:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Usuário não inscrito no evento!',
        )

    session.delete(inscricao_db)
    await session.commit()

    return {'mensagem': 'Inscrição cancelada no evento!'}
