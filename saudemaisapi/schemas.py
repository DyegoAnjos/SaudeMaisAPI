from datetime import date, datetime

from pydantic import BaseModel, ConfigDict

# Arquivo que gerencia o formato de entradas e retornos


class Comentario(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    # Garante compatibilidade ORM
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
    descricao: str | None = None
    endereco: str | None = None
    foto_evento: int
    link_externo: str | None = None
    tipo_evento: int
    capacidade_maxima: int | None = None
    data: datetime | date


class EventoGet(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    usuario_criador: int
    unidade_associada: int | None = None
    titulo: str
    descricao: str | None = None
    endereco: str | None = None
    foto_evento: int
    link_externo: str | None = None
    tipo_evento: int
    status: str | None = None
    qtd_inscricoes: int = 0
    capacidade_maxima: int | None = None

    # Flexibilidade total para as datas vindas do SQLite
    data: datetime | date | str
    data_criacao: datetime | date | str
    data_cancelamento: datetime | date | str | None = None
    data_ultima_atualizacao: datetime | date | str | None = None

    comentarios: list[Comentario] = []


class EventosList(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    eventos: list[EventoGet]
