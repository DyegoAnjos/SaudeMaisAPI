from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, update, func
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
async def validar_inscricao(inscricao: Inscricao_Schema, session: Session):
    usuario_db = await session.scalar(
        select(Usuario_comum).where(Usuario_comum.id == inscricao.usuario)
    )

    if not usuario_db:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Usuário não encontrado!'
        )

    evento_db = await session.scalar(
        select(Evento).where(Evento.id == inscricao.evento)
    )

    if not evento_db:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Evento não encontrado!'
        )


async def atualizar_inscricao_evento(inscricao: Inscricao_Schema, session: Session):
    # 1. Conta quantas inscrições existem para este evento específico
    stmt_count = (
        select(func.count())
        .select_from(Inscricao)
        .where(Inscricao.evento == inscricao.id_evento) # 👈 Nome da coluna de evento na tabela Inscricao
    )
    total_inscricoes = await session.scalar(stmt_count) or 0

    # 2. Atualiza a contagem na tabela Evento
    stmt_update = (
        update(Evento)
        .where(Evento.id == inscricao.id_evento)
        .values(quantidade_inscricoes=total_inscricoes) # 👈 Substitua pelo nome exato da coluna na tabela Evento
    )

    await session.execute(stmt_update)
    await session.commit()

    return total_inscricoes

# GET


@router.get(
    '/{id_usuario}/',
    status_code=HTTPStatus.OK,
    response_model=list[Inscricao_Schema],
)
async def listar_inscricoes(
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

    if not inscricoes:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Usuário sem inscrição!',
        )


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

    await atualizar_inscricao_evento(Inscrever_Schema, session)

    return inscricao_db


# DELETE


@router.delete(
    '/cancelar_inscricao/{id_inscricao}',
    status_code=HTTPStatus.OK,
    response_model=MessageSchema,
)
async def cancelar_inscricao(id_inscricao: int, session: Session):
    inscricao_db = await session.scalar(
        select(Inscricao).where(Inscricao.id == id_inscricao)
    )

    if not inscricao_db:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Usuário não inscrito no evento!',
        )

    session.delete(inscricao_db)
    await session.commit()

    await atualizar_inscricao_evento(Inscrever_Schema, session)

    return {'mensagem': 'Inscrição cancelada no evento!'}
