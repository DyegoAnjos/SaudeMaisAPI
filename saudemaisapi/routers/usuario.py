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
    Login_Schema,
    Usuario_retorno_Schema,
)

router = APIRouter(prefix='/usuarios', tags=['Usuarios'])

Session = Annotated[AsyncSession, Depends(get_db)]
# Geral Usuario


@router.post(
    '/validar',
    status_code=HTTPStatus.OK,
    response_model=Usuario_retorno_Schema,
)
async def validar(session: Session, login: Login_Schema):
    usuario = await session.scalar(
        select(Usuario_comum).where(
            Usuario_comum.email == login.email
            and Usuario_comum.senha == login.senha
        )
    )

    if not usuario:
        usuario = await session.scalar(
            select(Usuario_administrador).where(
                Usuario_administrador.email == login.e_mail
                and Usuario_administrador.senha == login.senha
            )
        )

        if not usuario:
            usuario = await session.scalar(
                select(Usuario_institucional).where(
                    Usuario_institucional.email == login.e_mail
                    and Usuario_institucional.senha == login.senha
                )
            )

            if not usuario:
                raise HTTPException(
                    status_code=HTTPStatus.NOT_FOUND,
                    detail='Usuário não encontrado',
                )
    return usuario
