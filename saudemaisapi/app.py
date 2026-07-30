from http import HTTPStatus

from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
)
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from saudemaisapi.database import get_db
from saudemaisapi.models import (
    Usuario_comum,
    Evento
)
from saudemaisapi.schemas import (
    Evento,
    Evento_retorno,
    EventosList,
    Message, Usuario_comum_lista, Usuario_comum_retorno,
)

app = FastAPI(title='Saude+API')


bd = []


# Eventos


# GET
@app.get('/eventos/', status_code=HTTPStatus.OK, response_model=EventosList)
def listar_eventos(
    limit: int = 10, offset: int = 0, session: Session = Depends(get_db)
):
    eventos = session.scalars(select(Evento).limit(limit).offset(offset))

    return {'eventos': eventos}


@app.get(
    '/eventos/{id_evento}',
    status_code=HTTPStatus.OK,
    response_model=Evento_retorno,
)
def listar_eventos_por_id(id_evento: int, session: Session = Depends(get_db)):

    eventos = session.scalar(select(Evento).where(Evento.id == id_evento))

    if not eventos:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Evento não encontrado'
        )

    return eventos


# POST
@app.post(
    '/criar_evento/',
    status_code=HTTPStatus.CREATED,
    response_model=Evento_retorno,
)
def criar_eventos(evento: Evento, session: Session = Depends(get_db)):
    evento_bd = session.scalar(
        select(Evento).where(Evento.titulo == evento.titulo)
    )

    if evento_bd:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Evento já existe!',
        )

    evento_bd = Evento(**evento.model_dump())

    session.add(evento_bd)
    session.commit()

    session.refresh(evento_bd)

    return evento_bd


# PUT
@app.put(
    '/atualizar_evento/{id_evento}',
    status_code=HTTPStatus.OK,
    response_model=Evento_retorno,
)
def atualizar_evento(
    evento: Evento, id_evento: int, session: Session = Depends(get_db)
):
    evento_bd = session.scalar(select(Evento).where(Evento.id == id_evento))
    if not evento_bd:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Evento não encontrado'
        )

    try:
        for chave, valor in evento.model_dump(exclude_unset=True).items():
            setattr(evento_bd, chave, valor)

        session.commit()
        session.refresh(evento_bd)

        return evento_bd
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Evento já existe!',
        )


# DELETE
@app.delete(
    '/remover_evento/{id_evento}',
    status_code=HTTPStatus.OK,
    response_model=Message,
)
def remover_evento(id_evento: int, session: Session = Depends(get_db)):
    evento_bd = session.scalar(select(Evento).where(Evento.id == id_evento))
    if not evento_bd:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Evento não encontrado'
        )
    session.delete(evento_bd)
    session.commit()

    return {'mensagem': 'Evento removido com sucesso!'}

# Usuario

# Usuario Comum

# GET
@app.get(
    '/usuarios/comum/',
    status_code=HTTPStatus.OK,
    response_model=Usuario_comum_lista,
)
def listar_usuarios_comum(
        limit: int = 10, offset: int = 0,
        session: Session = Depends(get_db)
):
    usuario_comuns = session.scalars(select(Usuario_comum).limit(limit).offset(offset))

    return usuario_comuns

@app.get(
    '/usuarios/comum/{id_comum}',
    status_code=HTTPStatus.OK,
    response_model=Usuario_comum_retorno,
)
def listar_usuario_comum_por_id(id_comum: int, session: Session = Depends(get_db)):

    usuario_comum = session.scalar(select(Usuario_comum).where(Usuario_comum.id == id_comum))

    if not usuario_comum:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado'
        )

    return usuario_comum

# POST

@app.post(
    '/usuarios/comum/criar_evento/',
    status_code=HTTPStatus.CREATED,
    response_model=Usuario_comum_retorno,
)
def criar_usuario_comum(usuario_comum: Usuario_comum, session: Session = Depends(get_db)):
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
@app.put(
    '/usuarios/comum/atualizar_usuario/{id_usuario}',
    status_code=HTTPStatus.OK,
    response_model=Usuario_comum_retorno,
)
def atualizar_usuario_comum(usuario_comum: Usuario_comum, id_usuario: int, session: Session = Depends(get_db)):
    usuario_comum_bd = session.scalar(select(Usuario_comum).where(Usuario_comum.id == id_usuario))

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
@app.delete(
    '/usuarios/comum/deletar_usuario/{id_usuario}',
    status_code=HTTPStatus.OK,
    response_model=Message
)
def remover_usuario_comum(id_usuario: int, session: Session = Depends(get_db)):
    usuario_comum_bd = session.scalar(select(Usuario_comum).where(Usuario_comum.id == id_usuario))

    if not usuario_comum_bd:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado'
        )
    session.delete(usuario_comum_bd)
    session.commit()

    return {'mensagem': 'Usuário removido com sucesso!'}