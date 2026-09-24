from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from saudemaisapi.database import get_db
from saudemaisapi.models import (
    Usuario_administrador,
    Usuario_comum,
    Usuario_institucional,
)
from saudemaisapi.schemas import (
    Login_retorno_Schema,
    Login_Schema,
)

router = APIRouter(prefix='/usuarios', tags=['Usuarios'])

Session = Annotated[AsyncSession, Depends(get_db)]
# Geral Usuario


@router.post(
    '/validar',
    status_code=HTTPStatus.OK,
    response_model=Login_retorno_Schema,
)
async def validar(session: Session, login: Login_Schema):
    tipos_usuarios = [
        Usuario_comum,
        Usuario_institucional,
        Usuario_administrador,
    ]

    for modelo in tipos_usuarios:
        # Busca apenas a coluna id do banco de dados
        resultado = await session.execute(
            select(modelo.id).where(
                modelo.email == login.email, modelo.senha == login.senha
            )
        )
        id_encontrado = resultado.scalar_one_or_none()

        if id_encontrado is not None:
            return {
                'id': id_encontrado,
                'tipo': modelo.__name__,
            }

    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND,
        detail='Usuário não encontrado',
    )
