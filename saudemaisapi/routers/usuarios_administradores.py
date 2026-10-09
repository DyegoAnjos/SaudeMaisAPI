from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from saudemaisapi.database import get_db
from saudemaisapi.models import Usuario_administrador
from saudemaisapi.schemas import (
    Filtro_Paginas,
    MessageSchema,
    Usuario_adiministrador_Schema,
    Usuario_administrador_retorno_Schema,
)

router = APIRouter(
    prefix='/usuarios/administrador', tags=['Usuarios administradores']
)

Session = Annotated[AsyncSession, Depends(get_db)]


@router.get(
    '/',
    status_code=HTTPStatus.OK,
    response_model=list[Usuario_administrador_retorno_Schema],
)
async def listar_usuarios_administradores(
    session: Session, filtro: Annotated[Filtro_Paginas, Query()]
):
    usuarios = await session.scalars(
        select(Usuario_administrador).limit(filtro.limit).offset(filtro.offset)
    )
    return usuarios


@router.get(
    '/{id_usuario}',
    status_code=HTTPStatus.OK,
    response_model=Usuario_administrador_retorno_Schema,
)
async def listar_usuario_administrador_por_id(
    id_usuario: int, session: Session
):
    usuario = await session.get(Usuario_administrador, id_usuario)
    if not usuario:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado'
        )
    return usuario


@router.post(
    '/criar_usuario/',
    status_code=HTTPStatus.CREATED,
    response_model=Usuario_administrador_retorno_Schema,
)
async def criar_usuario_administrador(
    dados: Usuario_adiministrador_Schema, session: Session
):
    usuario_existente = await session.scalar(
        select(Usuario_administrador).where(
            Usuario_administrador.email == dados.email
        )
    )
    if usuario_existente:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Usuário já existe!'
        )

    usuario = Usuario_administrador(**dados.model_dump())
    session.add(usuario)
    await session.commit()
    await session.refresh(usuario)
    return usuario


@router.put(
    '/atualizar_usuario/{id_usuario}',
    status_code=HTTPStatus.OK,
    response_model=Usuario_administrador_retorno_Schema,
)
async def atualizar_usuario_administrador(
    id_usuario: int,
    dados: Usuario_adiministrador_Schema,
    session: Session,
):
    usuario = await session.get(Usuario_administrador, id_usuario)
    if not usuario:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado'
        )

    email_em_uso = await session.scalar(
        select(Usuario_administrador).where(
            Usuario_administrador.email == dados.email,
            Usuario_administrador.id != id_usuario,
        )
    )
    if email_em_uso:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='E-mail já cadastrado!'
        )

    for campo, valor in dados.model_dump().items():
        setattr(usuario, campo, valor)

    await session.commit()
    await session.refresh(usuario)
    return usuario


@router.delete(
    '/deletar_usuario/{id_usuario}',
    status_code=HTTPStatus.OK,
    response_model=MessageSchema,
)
async def remover_usuario_administrador(id_usuario: int, session: Session):
    usuario = await session.get(Usuario_administrador, id_usuario)
    if not usuario:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado'
        )

    await session.delete(usuario)
    await session.commit()
    return {'mensagem': 'Usuário removido com sucesso!'}
