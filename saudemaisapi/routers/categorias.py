from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

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
SessionDep = Annotated[Session, Depends(get_db)]


@router.get('/', response_model=Categorias_lista_Schema)
def listar_categorias(
    session: SessionDep,
    filtro: Annotated[Filtro_Paginas, Query()],
):
    categorias = session.scalars(
        select(Categoria).limit(filtro.limit).offset(filtro.offset)
    ).all()
    return {'categorias': categorias}


@router.get('/{id_categoria}', response_model=Categoria_retorno_Schema)
def buscar_categoria(id_categoria: int, session: SessionDep):
    categoria = session.get(Categoria, id_categoria)
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
def criar_categoria(dados: Categoria_Schema, session: SessionDep):
    categoria = Categoria(**dados.model_dump())
    session.add(categoria)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Categoria já existe',
        )
    session.refresh(categoria)
    return categoria


@router.put('/{id_categoria}', response_model=Categoria_retorno_Schema)
def atualizar_categoria(
    id_categoria: int,
    dados: Categoria_Schema,
    session: SessionDep,
):
    categoria = session.get(Categoria, id_categoria)
    if not categoria:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Categoria não encontrada',
        )
    for campo, valor in dados.model_dump().items():
        setattr(categoria, campo, valor)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Categoria já existe',
        )
    session.refresh(categoria)
    return categoria


@router.delete('/{id_categoria}', response_model=MessageSchema)
def remover_categoria(id_categoria: int, session: SessionDep):
    categoria = session.get(Categoria, id_categoria)
    if not categoria:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Categoria não encontrada',
        )
    session.delete(categoria)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Categoria está sendo utilizada',
        )
    return {'mensagem': 'Categoria removida com sucesso!'}
