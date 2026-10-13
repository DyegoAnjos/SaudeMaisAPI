from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, cast, Integer, func
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
async def validar_inscricao(inscricao: Inscrever_Schema, session: Session):
    usuario_db = await session.scalar(
        select(Usuario_comum).where(Usuario_comum.id == inscricao.usuario)
    )

    if not usuario_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado!'
        )

    evento_db = await session.scalar(
        select(Evento).where(Evento.id == inscricao.evento)
    )

    if not evento_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Evento não encontrado!'
        )


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

    # Força a checagem com valores inteiros
    id_usuario = int(inscricao.usuario)
    id_evento = int(inscricao.evento)

    inscricao_db = await session.scalar(
        select(Inscricao).where(
            cast(Inscricao.usuario, Integer) == id_usuario,
            cast(Inscricao.evento, Integer) == id_evento,
        )
    )

    if inscricao_db:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Usuário já inscrito!'
        )

    # Cria garantindo os tipos int
    nova_inscricao = Inscricao(
        usuario=id_usuario,
        evento=id_evento,
    )

    session.add(nova_inscricao)
    await session.commit()
    await session.refresh(nova_inscricao)

    return nova_inscricao


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
            status_code=HTTPStatus.NOT_FOUND,
            detail='Inscrição não encontrada!',
        )

    await session.delete(inscricao_db)
    await session.commit()

    return {'mensagem': 'Inscrição cancelada no evento!'}