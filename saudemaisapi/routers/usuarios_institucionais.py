from http import HTTPStatus
from pathlib import Path
from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from saudemaisapi.database import get_db
from saudemaisapi.models import Usuario_institucional
from saudemaisapi.schemas import (
    Filtro_Paginas,
    MessageSchema,
    Usuario_institucional_retorno_Schema,
    Usuario_Schema_institucional_Schema,
)

router = APIRouter(
    prefix='/usuarios/institucional', tags=['Usuarios institucionais']
)

Session = Annotated[AsyncSession, Depends(get_db)]

PASTA_DOCUMENTOS = (
    Path(__file__).resolve().parents[2] / 'uploads' / 'documentos'
)
TAMANHO_MAXIMO = 5 * 1024 * 1024
TIPOS_PERMITIDOS = {
    'application/pdf': '.pdf',
    'image/jpeg': '.jpg',
    'image/png': '.png',
}


async def salvar_documento(arquivo: UploadFile):
    if arquivo.content_type not in TIPOS_PERMITIDOS:
        raise HTTPException(
            status_code=HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
            detail='Formato de documento não permitido',
        )

    conteudo = await arquivo.read(TAMANHO_MAXIMO + 1)
    if not conteudo:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='O documento está vazio',
        )
    if len(conteudo) > TAMANHO_MAXIMO:
        raise HTTPException(
            status_code=HTTPStatus.REQUEST_ENTITY_TOO_LARGE,
            detail='O documento deve ter no máximo 5 MB',
        )

    PASTA_DOCUMENTOS.mkdir(parents=True, exist_ok=True)
    nome = f'{uuid4()}{TIPOS_PERMITIDOS[arquivo.content_type]}'
    caminho = PASTA_DOCUMENTOS / nome
    caminho.write_bytes(conteudo)
    return caminho


@router.get(
    '/',
    status_code=HTTPStatus.OK,
    response_model=list[Usuario_institucional_retorno_Schema],
)
async def listar_usuarios_institucionais(
    session: Session, filtro: Annotated[Filtro_Paginas, Query()]
):
    usuarios = await session.scalars(
        select(Usuario_institucional).limit(filtro.limit).offset(filtro.offset)
    )
    return usuarios


@router.get(
    '/{id_usuario}',
    status_code=HTTPStatus.OK,
    response_model=Usuario_institucional_retorno_Schema,
)
async def listar_usuario_institucional_por_id(
    id_usuario: int, session: Session
):
    usuario = await session.get(Usuario_institucional, id_usuario)
    if not usuario:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado'
        )
    return usuario


@router.post(
    '/criar_usuario/',
    status_code=HTTPStatus.CREATED,
    response_model=Usuario_institucional_retorno_Schema,
)
async def criar_usuario_institucional(
    dados: Usuario_Schema_institucional_Schema, session: Session
):
    usuario_existente = await session.scalar(
        select(Usuario_institucional).where(
            or_(
                Usuario_institucional.email == dados.email,
                Usuario_institucional.cnpj == dados.cnpj,
                Usuario_institucional.nome == dados.nome,
            )
        )
    )
    if usuario_existente:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Usuário já existe!'
        )

    usuario = Usuario_institucional(**dados.model_dump())
    session.add(usuario)
    await session.commit()
    await session.refresh(usuario)
    return usuario


@router.post(
    '/{id_usuario}/documentos',
    status_code=HTTPStatus.OK,
    response_model=Usuario_institucional_retorno_Schema,
)
async def enviar_documentos_institucionais(
    id_usuario: int,
    session: Session,
    documento_cnpj: Annotated[UploadFile, File(alias='docCnpj')],
    documento_responsavel: Annotated[UploadFile, File(alias='docResponsavel')],
    documento_vinculo: Annotated[
        UploadFile | None, File(alias='docVinculo')
    ] = None,
):
    usuario = await session.get(Usuario_institucional, id_usuario)
    if not usuario:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado'
        )

    caminhos_novos = []
    try:
        caminho_cnpj = await salvar_documento(documento_cnpj)
        caminhos_novos.append(caminho_cnpj)
        caminho_responsavel = await salvar_documento(documento_responsavel)
        caminhos_novos.append(caminho_responsavel)
        caminho_vinculo = None
        if documento_vinculo:
            caminho_vinculo = await salvar_documento(documento_vinculo)
            caminhos_novos.append(caminho_vinculo)
    except Exception:
        for caminho in caminhos_novos:
            caminho.unlink(missing_ok=True)
        raise

    caminhos_antigos = [
        usuario.documento_cnpj,
        usuario.documento_responsavel,
        usuario.documento_vinculo,
    ]
    usuario.documento_cnpj = str(caminho_cnpj)
    usuario.documento_responsavel = str(caminho_responsavel)
    usuario.documento_vinculo = (
        str(caminho_vinculo) if caminho_vinculo else None
    )

    try:
        await session.commit()
    except Exception:
        await session.rollback()
        for caminho in caminhos_novos:
            caminho.unlink(missing_ok=True)
        raise

    await session.refresh(usuario)
    for caminho in caminhos_antigos:
        if caminho:
            Path(caminho).unlink(missing_ok=True)
    return usuario


@router.put(
    '/atualizar_usuario/{id_usuario}',
    status_code=HTTPStatus.OK,
    response_model=Usuario_institucional_retorno_Schema,
)
async def atualizar_usuario_institucional(
    id_usuario: int,
    dados: Usuario_Schema_institucional_Schema,
    session: Session,
):
    usuario = await session.get(Usuario_institucional, id_usuario)
    if not usuario:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado'
        )

    dados_em_uso = await session.scalar(
        select(Usuario_institucional).where(
            or_(
                Usuario_institucional.email == dados.email,
                Usuario_institucional.cnpj == dados.cnpj,
                Usuario_institucional.nome == dados.nome,
            ),
            Usuario_institucional.id != id_usuario,
        )
    )
    if dados_em_uso:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='E-mail, CNPJ ou nome já cadastrado!',
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
async def remover_usuario_institucional(id_usuario: int, session: Session):
    usuario = await session.get(Usuario_institucional, id_usuario)
    if not usuario:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado'
        )

    documentos = [
        usuario.documento_cnpj,
        usuario.documento_responsavel,
        usuario.documento_vinculo,
    ]
    await session.delete(usuario)
    await session.commit()
    for documento in documentos:
        if documento:
            Path(documento).unlink(missing_ok=True)
    return {'mensagem': 'Usuário removido com sucesso!'}
