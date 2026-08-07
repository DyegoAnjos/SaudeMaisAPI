from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from saudemaisapi.database import get_db
from saudemaisapi.models import Usuario_comum
from saudemaisapi.schemas import (
    Filtro_Paginas,
    MessageSchema,
    Usuario_comum_lista_Schema,
    Usuario_comum_retorno_Schema,
)

router = APIRouter(prefix='/usuarios/comum', tags=['Usuarios comuns'])

Session = Annotated[Session, Depends(get_db)]
# Usuario Comum


# GET


@router.get(
    '/',
    status_code=HTTPStatus.OK,
    response_model=Usuario_comum_lista_Schema,
)
def listar_usuarios_comum(
    session: Session, filtro: Annotated[Filtro_Paginas, Query()]
):
    usuario_comuns = session.scalars(
        select(Usuario_comum).limit(filtro.limit).offset(filtro.offset)
    )

    return usuario_comuns


@router.get(
    '/{id_comum}',
    status_code=HTTPStatus.OK,
    response_model=Usuario_comum_retorno_Schema,
)
def listar_usuario_comum_por_id(id_comum: int, session: Session):

    usuario_comum = session.scalar(
        select(Usuario_comum).where(Usuario_comum.id == id_comum)
    )

    if not usuario_comum:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado'
        )

    return usuario_comum


# POST


@router.post(
    '/criar_evento/',
    status_code=HTTPStatus.CREATED,
    response_model=Usuario_comum_retorno_Schema,
)
def criar_usuario_comum(usuario_comum: Usuario_comum, session: Session):
    usuario_comum_bd = session.scalar(
        select(Usuario_comum).where(Usuario_comum.nome == usuario_comum.nome)
    )

    if usuario_comum_bd:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Usuário já existe!',
        )

    usuario_comum_bd = Usuario_comum(**usuario_comum.model_dump())

    session.add(usuario_comum_bd)
    session.commit()

    session.refresh(usuario_comum_bd)

    return usuario_comum_bd


# PUT
@router.put(
    '/atualizar_usuario/{id_usuario}',
    status_code=HTTPStatus.OK,
    response_model=Usuario_comum_retorno_Schema,
)
def atualizar_usuario_comum(
    usuario_comum: Usuario_comum,
    id_usuario: int,
    session: Session,
):
    usuario_comum_bd = session.scalar(
        select(Usuario_comum).where(Usuario_comum.id == id_usuario)
    )

    if usuario_comum_bd:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Usuário já existe!',
        )

    usuario_comum_bd = Usuario_comum(**usuario_comum.model_dump())

    session.add(usuario_comum_bd)
    session.commit()

    session.refresh(usuario_comum_bd)

    return usuario_comum_bd


# DELETE
@router.delete(
    '/deletar_usuario/{id_usuario}',
    status_code=HTTPStatus.OK,
    response_model=MessageSchema,
)
def remover_usuario_comum(id_usuario: int, session: Session):
    usuario_comum_bd = session.scalar(
        select(Usuario_comum).where(Usuario_comum.id == id_usuario)
    )

    if not usuario_comum_bd:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado'
        )
    session.delete(usuario_comum_bd)
    session.commit()

    return {'mensagem': 'Usuário removido com sucesso!'}
