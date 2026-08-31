from http import HTTPStatus
from pathlib import Path
from typing import Annotated
from uuid import uuid4

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Query,
    UploadFile,
)
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from saudemaisapi.database import get_db
from saudemaisapi.models import Fotografias
from saudemaisapi.schemas import (
    Filtro_Paginas,
    Fotografia_lista_Schema,
    Fotografia_retorno_Schema,
    MessageSchema,
)

router = APIRouter(prefix='/fotografias', tags=['Fotografias'])
SessionDep = Annotated[Session, Depends(get_db)]

PASTA_UPLOADS = Path(__file__).resolve().parents[2] / 'uploads'
TAMANHO_MAXIMO = 5 * 1024 * 1024
TIPOS_PERMITIDOS = {
    'image/jpeg': '.jpg',
    'image/png': '.png',
    'image/webp': '.webp',
}


async def salvar_arquivo(arquivo: UploadFile):
    if arquivo.content_type not in TIPOS_PERMITIDOS:
        raise HTTPException(
            status_code=HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
            detail='Formato de imagem não permitido',
        )

    conteudo = await arquivo.read(TAMANHO_MAXIMO + 1)
    if not conteudo:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='O arquivo está vazio',
        )
    if len(conteudo) > TAMANHO_MAXIMO:
        raise HTTPException(
            status_code=HTTPStatus.REQUEST_ENTITY_TOO_LARGE,
            detail='A imagem deve ter no máximo 5 MB',
        )

    PASTA_UPLOADS.mkdir(exist_ok=True)
    nome_salvo = f'{uuid4()}{TIPOS_PERMITIDOS[arquivo.content_type]}'
    caminho = PASTA_UPLOADS / nome_salvo
    caminho.write_bytes(conteudo)
    return caminho, len(conteudo)


@router.get('/', response_model=Fotografia_lista_Schema)
async def listar_fotografias(
    session: SessionDep,
    filtro: Annotated[Filtro_Paginas, Query()],
):
    fotografias = await session.scalars(
        select(Fotografias).limit(filtro.limit).offset(filtro.offset)
    ).all()
    return {'fotografias': fotografias}


@router.get('/{id_fotografia}', response_model=Fotografia_retorno_Schema)
async def listar_fotografia_por_id(id_fotografia: int, session: SessionDep):
    fotografia = await session.get(Fotografias, id_fotografia)
    if not fotografia:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Fotografia não encontrada',
        )
    return fotografia


@router.get('/{id_fotografia}/arquivo', response_class=FileResponse)
async def obter_arquivo(id_fotografia: int, session: SessionDep):
    fotografia = await session.get(Fotografias, id_fotografia)
    if not fotografia or not Path(fotografia.caminho).is_file():
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Fotografia não encontrada',
        )
    return FileResponse(
        fotografia.caminho,
        media_type=fotografia.tipo,
        filename=fotografia.nome,
    )


@router.post(
    '/criar_fotografia',
    status_code=HTTPStatus.CREATED,
    response_model=Fotografia_retorno_Schema,
)
async def criar_fotografia(
    session: SessionDep,
    arquivo: Annotated[UploadFile, File()],
    foto_de_evento: Annotated[bool, Form()] = False,
):
    caminho, tamanho = await salvar_arquivo(arquivo)
    fotografia = Fotografias(
        nome=arquivo.filename or caminho.name,
        caminho=str(caminho),
        tipo=arquivo.content_type or '',
        tamanho=tamanho,
        foto_de_evento=foto_de_evento,
    )
    session.add(fotografia)
    try:
        await session.commit()
    except Exception:
        session.rollback()
        caminho.unlink(missing_ok=True)
        raise
    session.refresh(fotografia)
    return fotografia


@router.put(
    '/atualizar_fotografia/{id_fotografia}',
    response_model=Fotografia_retorno_Schema,
)
async def atualizar_fotografia(
    id_fotografia: int,
    session: SessionDep,
    arquivo: Annotated[UploadFile, File()],
    foto_de_evento: Annotated[bool, Form()] = False,
):
    fotografia = await session.get(Fotografias, id_fotografia)
    if not fotografia:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Fotografia não encontrada',
        )

    caminho_antigo = Path(fotografia.caminho)
    caminho_novo, tamanho = await salvar_arquivo(arquivo)
    fotografia.nome = arquivo.filename or caminho_novo.name
    fotografia.caminho = str(caminho_novo)
    fotografia.tipo = arquivo.content_type or ''
    fotografia.tamanho = tamanho
    fotografia.foto_de_evento = foto_de_evento
    try:
        await session.commit()
    except Exception:
        session.rollback()
        caminho_novo.unlink(missing_ok=True)
        raise
    session.refresh(fotografia)
    caminho_antigo.unlink(missing_ok=True)
    return fotografia


@router.delete(
    '/remover_fotografia/{id_fotografia}',
    response_model=MessageSchema,
)
async def remover_fotografia(id_fotografia: int, session: SessionDep):
    fotografia = await session.get(Fotografias, id_fotografia)
    if not fotografia:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Fotografia não encontrada',
        )

    caminho = Path(fotografia.caminho)
    await session.delete(fotografia)
    await session.commit()
    caminho.unlink(missing_ok=True)
    return {'mensagem': 'Fotografia removida com sucesso!'}
