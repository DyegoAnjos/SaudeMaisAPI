from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from saudemaisapi.database import get_db
from saudemaisapi.models import Unidade_saude
from saudemaisapi.schemas import (
    Filtro_Paginas,
    MessageSchema,
    Unidade_saude_retorno_Schema,
    Unidade_saude_Schema,
    Unidades_saude_lista_Schema,
)

router = APIRouter(prefix='/unidades-saude', tags=['Unidades de saúde'])
SessionDep = Annotated[AsyncSession, Depends(get_db)]


@router.get('/', response_model=Unidades_saude_lista_Schema)
async def listar_unidades(
    session: SessionDep,
    filtro: Annotated[Filtro_Paginas, Query()],
):
    unidades = (
        await session.scalars(
            select(Unidade_saude).limit(filtro.limit).offset(filtro.offset)
        )
    ).all()
    return {'unidades': unidades}


@router.get('/{id_unidade}', response_model=Unidade_saude_retorno_Schema)
async def buscar_unidade(id_unidade: int, session: SessionDep):
    unidade = await session.get(Unidade_saude, id_unidade)
    if not unidade:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Unidade de saúde não encontrada',
        )
    return unidade


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=Unidade_saude_retorno_Schema,
)
async def criar_unidade(dados: Unidade_saude_Schema, session: SessionDep):
    unidade = Unidade_saude(**dados.model_dump())
    session.add(unidade)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Unidade de saúde já existe',
        )
    await session.refresh(unidade)
    return unidade


@router.put('/{id_unidade}', response_model=Unidade_saude_retorno_Schema)
async def atualizar_unidade(
    id_unidade: int,
    dados: Unidade_saude_Schema,
    session: SessionDep,
):
    unidade = await session.get(Unidade_saude, id_unidade)
    if not unidade:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Unidade de saúde não encontrada',
        )
    for campo, valor in dados.model_dump().items():
        setattr(unidade, campo, valor)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Unidade de saúde já existe',
        )
    await session.refresh(unidade)
    return unidade


@router.delete('/{id_unidade}', response_model=MessageSchema)
async def remover_unidade(id_unidade: int, session: SessionDep):
    unidade = await session.get(Unidade_saude, id_unidade)
    if not unidade:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Unidade de saúde não encontrada',
        )
    await session.delete(unidade)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Unidade de saúde está sendo utilizada',
        )
    return {'mensagem': 'Unidade de saúde removida com sucesso!'}
