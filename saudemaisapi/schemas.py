from datetime import date, datetime
from pydantic import BaseModel, Field


# 1. Movido para cima para que o EventoGet possa usá-lo sem dar erro de sintaxe
class Comentario(BaseModel):
    id: int
    nota: int
    descricao: str
    id_usuario: int


class Message(BaseModel):
    mensagem: str


class EventoPost(BaseModel):
    usuario_criador: int
    unidade_associada: int | None = None

    titulo: str
    # Ajustado para opcional para bater com o model que aceita None por padrão
    descricao: str | None = None
    endereco: str | None = None
    foto_evento: int
    link_externo: str | None = None

    tipo_evento: int
    capacidade_maxima: int | None = None

    data: datetime


class EventoGet(BaseModel):
    id: int

    # Mapeamentos corrigidos para bater com os nomes exatos do SQLAlchemy (models.py)
    usuario_criador: int
    unidade_associada: int | None = None

    titulo: str
    descricao: str | None = None
    endereco: str | None = None
    foto_evento: int  # Antes estava 'foto'
    link_externo: str | None = None

    tipo_evento: int
    status: str | None = None  # Banco aceita None por padrão

    # Campos que não existem no banco mas têm valores padrão no schema
    qtd_inscricoes: int = 0
    capacidade_maxima: int | None = None  # Antes estava 'qtd_inscricoes_maxima'

    data: datetime  # Antes estava 'data_evento'
    data_criacao: datetime
    data_cancelamento: datetime | None = None

    # Ajustado para bater com o nome do banco 'data_ultima_atualizacao'
    data_ultima_atualizacao: datetime | None = None

    comentarios: list[Comentario] = []

    # Permite que o Pydantic leia o modelo do SQLAlchemy mesmo contendo campos extras (como comentarios)
    class Config:
        from_attributes = True


class EventosList(BaseModel):
    eventos: list[EventoGet]