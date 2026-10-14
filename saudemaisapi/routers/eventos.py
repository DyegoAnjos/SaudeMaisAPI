from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy import Integer, cast, func, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from saudemaisapi.database import get_db
from saudemaisapi.models import Categoria, Evento, Inscricao, Comentario
from saudemaisapi.routers.comentarios import preparar_comentario
from saudemaisapi.schemas import (
    Evento_retorno_Schema,
    Evento_Schema,
    Filtro_Paginas,
    MessageSchema,
)

router = APIRouter(prefix='/eventos', tags=['Eventos'])

Session = Annotated[AsyncSession, Depends(get_db)]


async def preparar_evento(evento: Evento, session: Session, request: Request):
    # 1. Categoria
    categoria = await session.get(Categoria, evento.categoria)
    nome_categoria = categoria.nome if categoria else None

    # 2. Contagem Robusta de Inscrições
    id_ev = int(evento.id)
    stmt_count = select(func.count(Inscricao.id)).where(
        or_(
            cast(Inscricao.evento, Integer) == id_ev,
            Inscricao.evento == id_ev,
        )
    )
    total_inscritos = await session.scalar(stmt_count) or 0

    # 3. Busca de Comentarios Principais (emanuelle-api)
    comentarios_db = await session.scalars(
        select(Comentario)
        .where(
            Comentario.evento == evento.id,
            Comentario.comentario_pai.is_(None),
        )
        .order_by(Comentario.data_hora_feito.desc())
    )
    comentarios_formatados = [
        await preparar_comentario(comentario, session)
        for comentario in comentarios_db.all()
    ]

    # 4. Construção explícita do dicionário
    dados = {
        'id': int(evento.id),
        'titulo': evento.titulo,
        'descricao': evento.descricao,
        'data_hora_evento': evento.data_hora_evento,
        'data_hora_fim': evento.data_hora_fim,
        'publico_alvo': evento.publico_alvo,
        'categoria': evento.categoria,
        'foto_evento': evento.foto_evento,
        'criador_institucional': evento.criador_institucional,
        'status': evento.status,
        'capacidade_maxima': evento.capacidade_maxima,
        'unidade_associada': evento.unidade_associada,
        'endereco': evento.endereco,
        'pagina_evento': evento.pagina_evento,
        'data_hora_criacao': evento.data_hora_criacao,
        'data_hora_cancelamento': evento.data_hora_cancelamento,
        'data_hora_ultima_atualizacao': evento.data_hora_ultima_atualizacao,
        
        # Injeção das inscrições calculadas
        'inscricoes_atuais': int(total_inscritos),
        'numero_participantes': int(total_inscritos),
        'categoria_nome': nome_categoria,
        'foto_capa': str(
            request.url_for('obter_arquivo', id_fotografia=evento.foto_evento)
        ),
        'data': evento.data_hora_evento.date().isoformat(),
        'data_exibicao': evento.data_hora_evento.strftime('%d/%m/%Y'),
        'localizacao': evento.endereco,
        
        # Injeção da lista de comentários processados
        'comentarios': comentarios_formatados,
    }

    # 5. Validação com Pydantic
    return Evento_retorno_Schema.model_validate(dados)


# GET
    comentarios = await session.scalars(
        select(Comentario)
        .where(
            Comentario.evento == evento.id,
            Comentario.comentario_pai.is_(None),
        )
        .order_by(Comentario.data_hora_feito.desc())
    )
    dados['foto_capa'] = str(
        request.url_for('obter_arquivo', id_fotografia=evento.foto_evento)
    )
    dados['data'] = evento.data_hora_evento.date().isoformat()
    dados['data_exibicao'] = evento.data_hora_evento.strftime('%d/%m/%Y')
    dados['localizacao'] = evento.endereco
    dados['numero_participantes'] = dados['inscricoes_atuais']
    dados['categoria_nome'] = categoria.nome if categoria else None
    dados['comentarios'] = [
        await preparar_comentario(comentario, session)
        for comentario in comentarios.all()
    ]
    return dados


@router.get(
    '/', status_code=HTTPStatus.OK, response_model=list[Evento_retorno_Schema]
)
async def listar_eventos(
    request: Request,
    session: Session,
    filtro: Annotated[Filtro_Paginas, Query()],
):
    eventos = (
        await session.scalars(
            select(Evento).limit(filtro.limit).offset(filtro.offset)
        )
    ).all()

    return [
        await preparar_evento(evento, session, request) for evento in eventos
    ]


@router.get(
    '/{id_evento}',
    status_code=HTTPStatus.OK,
    response_model=Evento_retorno_Schema,
)
async def listar_eventos_por_id(
    id_evento: int, request: Request, session: Session
):

    eventos = await session.scalar(
        select(Evento).where(Evento.id == id_evento)
    )

    if not eventos:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Evento não encontrado'
        )

    return await preparar_evento(eventos, session, request)


@router.get(
    '/regiao/{regiao}',
    status_code=HTTPStatus.OK,
    response_model=list[Evento_retorno_Schema],  # Espera uma lista na resposta
)
async def listar_eventos_regiao(
    regiao: str, request: Request, session: Session
):
    query = await session.scalars(
        select(Evento).where(Evento.endereco.like(f'%{regiao}%'))
    )
    eventos = query.all()

    if not eventos:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Evento não encontrado'
        )

    return [
        await preparar_evento(evento, session, request) for evento in eventos
    ]


# POST
@router.post(
    '/criar_evento/',
    status_code=HTTPStatus.CREATED,
    response_model=Evento_retorno_Schema,
)
async def criar_eventos(
    evento: Evento_Schema, request: Request, session: Session
):
    evento_bd = await session.scalar(
        select(Evento).where(Evento.titulo == evento.titulo)
    )

    if evento_bd:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Evento já existe!',
        )

    evento_bd = Evento(**evento.model_dump())

    session.add(evento_bd)
    await session.commit()

    await session.refresh(evento_bd)

    return await preparar_evento(evento_bd, session, request)


# PUT
@router.put(
    '/atualizar_evento/{id_evento}',
    status_code=HTTPStatus.OK,
    response_model=Evento_retorno_Schema,
)
async def atualizar_evento(
    evento: Evento_Schema,
    id_evento: int,
    request: Request,
    session: Session,
):
    evento_bd = await session.scalar(
        select(Evento).where(Evento.id == id_evento)
    )
    if not evento_bd:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Evento não encontrado'
        )

    try:
        for chave, valor in evento.model_dump(exclude_unset=True).items():
            setattr(evento_bd, chave, valor)

        await session.commit()
        await session.refresh(evento_bd)

        return await preparar_evento(evento_bd, session, request)
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Evento já existe!',
        )


# DELETE
@router.delete(
    '/remover_evento/{id_evento}',
    status_code=HTTPStatus.OK,
    response_model=MessageSchema,
)
async def remover_evento(id_evento: int, session: Session):
    evento_bd = await session.scalar(
        select(Evento).where(Evento.id == id_evento)
    )
    if not evento_bd:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Evento não encontrado'
        )
    await session.delete(evento_bd)
    await session.commit()

    return {'mensagem': 'Evento removido com sucesso!'}
