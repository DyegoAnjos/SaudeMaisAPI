from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from saudemaisapi.database import get_db
from saudemaisapi.models import Categoria
from saudemaisapi.schemas import (
    Categoria_retorno_Schema,
    Categoria_Schema,
    Categorias_lista_Schema,
    Filtro_Paginas,
    MessageSchema,
)

router = APIRouter(prefix='/categorias', tags=['Categorias'])
SessionDep = Annotated[AsyncSession, Depends(get_db)]


@router.get('/', response_model=Categorias_lista_Schema)
async def listar_categorias(
    session: SessionDep,
    filtro: Annotated[Filtro_Paginas, Query()],
):
    categorias = (
        await session.scalars(
            select(Categoria).limit(filtro.limit).offset(filtro.offset)
        )
    ).all()
    return {'categorias': categorias}


@router.get('/{id_categoria}', response_model=Categoria_retorno_Schema)
async def buscar_categoria(id_categoria: int, session: SessionDep):
    categoria = await session.get(Categoria, id_categoria)
    if not categoria:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Categoria não encontrada',
        )
    return categoria


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=Categoria_retorno_Schema,
)
async def criar_categoria(dados: Categoria_Schema, session: SessionDep):
    categoria = Categoria(**dados.model_dump())
    session.add(categoria)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Categoria já existe',
        )
    await session.refresh(categoria)
    return categoria


@router.put('/{id_categoria}', response_model=Categoria_retorno_Schema)
async def atualizar_categoria(
    id_categoria: int,
    dados: Categoria_Schema,
    session: SessionDep,
):
    categoria = await session.get(Categoria, id_categoria)
    if not categoria:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Categoria não encontrada',
        )
    for campo, valor in dados.model_dump().items():
        setattr(categoria, campo, valor)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Categoria já existe',
        )
    await session.refresh(categoria)
    return categoria


@router.delete('/{id_categoria}', response_model=MessageSchema)
async def remover_categoria(id_categoria: int, session: SessionDep):
    categoria = await session.get(Categoria, id_categoria)
    if not categoria:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Categoria não encontrada',
        )
    await session.delete(categoria)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Categoria está sendo utilizada',
        )
    return {'mensagem': 'Categoria removida com sucesso!'}
