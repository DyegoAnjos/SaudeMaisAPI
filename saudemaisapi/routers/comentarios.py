from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from saudemaisapi.database import get_db
from saudemaisapi.models import Comentario, Evento, Usuario_comum
from saudemaisapi.schemas import (
    Comentario_retorno_Schema,
    Comentario_Schema,
    Filtro_Paginas,
    MessageSchema,
)

router = APIRouter(prefix='/comentarios', tags=['Comentários'])

Session = Annotated[AsyncSession, Depends(get_db)]


async def validar_usuario_evento(dados: Comentario_Schema, session: Session):
    usuario = await session.get(Usuario_comum, dados.usuario)
    if not usuario:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Usuário não encontrado',
        )

    evento = await session.get(Evento, dados.evento)
    if not evento:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Evento não encontrado',
        )

    if dados.comentario_pai is not None:
        comentario_pai = await session.get(Comentario, dados.comentario_pai)
        if not comentario_pai:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Comentário original não encontrado',
            )
        if comentario_pai.evento != dados.evento:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='A resposta deve pertencer ao mesmo evento',
            )
        if comentario_pai.comentario_pai is not None:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Não é possível responder a outra resposta',
            )


async def preparar_comentario(comentario: Comentario, session: Session):
    usuario = await session.get(Usuario_comum, comentario.usuario)
    respostas = await session.scalars(
        select(Comentario)
        .where(Comentario.comentario_pai == comentario.id)
        .order_by(Comentario.data_hora_feito.asc())
    )
    dados = {
        'id': comentario.id,
        'titulo': comentario.titulo,
        'conteudo': comentario.conteudo,
        'nota': comentario.nota,
        'usuario': comentario.usuario,
        'evento': comentario.evento,
        'comentario_pai': comentario.comentario_pai,
        'data_hora_feito': comentario.data_hora_feito,
        'nome_usuario': usuario.nome,
        'respostas': [],
    }
    for resposta in respostas.all():
        dados['respostas'].append(await preparar_comentario(resposta, session))
    return dados


@router.get(
    '/',
    response_model=list[Comentario_retorno_Schema],
)
async def listar_comentarios(
    session: Session,
    filtro: Annotated[Filtro_Paginas, Query()],
):
    comentarios = await session.scalars(
        select(Comentario)
        .where(Comentario.comentario_pai.is_(None))
        .order_by(Comentario.data_hora_feito.desc())
        .limit(filtro.limit)
        .offset(filtro.offset)
    )
    return [
        await preparar_comentario(comentario, session)
        for comentario in comentarios.all()
    ]


@router.get(
    '/evento/{id_evento}',
    response_model=list[Comentario_retorno_Schema],
)
async def listar_comentarios_evento(id_evento: int, session: Session):
    evento = await session.get(Evento, id_evento)
    if not evento:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Evento não encontrado',
        )

    comentarios = await session.scalars(
        select(Comentario)
        .where(
            Comentario.evento == id_evento,
            Comentario.comentario_pai.is_(None),
        )
        .order_by(Comentario.data_hora_feito.desc())
    )
    return [
        await preparar_comentario(comentario, session)
        for comentario in comentarios.all()
    ]


@router.get(
    '/{id_comentario}',
    response_model=Comentario_retorno_Schema,
)
async def buscar_comentario(id_comentario: int, session: Session):
    comentario = await session.get(Comentario, id_comentario)
    if not comentario:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Comentário não encontrado',
        )
    return await preparar_comentario(comentario, session)


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=Comentario_retorno_Schema,
)
async def criar_comentario(dados: Comentario_Schema, session: Session):
    await validar_usuario_evento(dados, session)
    comentario = Comentario(**dados.model_dump())
    session.add(comentario)
    await session.commit()
    await session.refresh(comentario)
    return await preparar_comentario(comentario, session)


@router.put(
    '/{id_comentario}',
    response_model=Comentario_retorno_Schema,
)
async def atualizar_comentario(
    id_comentario: int,
    dados: Comentario_Schema,
    session: Session,
):
    comentario = await session.get(Comentario, id_comentario)
    if not comentario:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Comentário não encontrado',
        )

    if dados.comentario_pai != comentario.comentario_pai:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Não é possível alterar o comentário original',
        )

    await validar_usuario_evento(dados, session)
    for campo, valor in dados.model_dump().items():
        setattr(comentario, campo, valor)

    await session.commit()
    await session.refresh(comentario)
    return await preparar_comentario(comentario, session)


@router.delete(
    '/{id_comentario}',
    response_model=MessageSchema,
)
async def remover_comentario(id_comentario: int, session: Session):
    comentario = await session.get(Comentario, id_comentario)
    if not comentario:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Comentário não encontrado',
        )

    await session.execute(
        delete(Comentario).where(Comentario.comentario_pai == id_comentario)
    )
    await session.delete(comentario)
    await session.commit()
    return {'mensagem': 'Comentário removido com sucesso!'}
