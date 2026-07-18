from datetime import date, datetime

from pydantic import BaseModel, ConfigDict

# Arquivo que gerencia o formato de entradas e retornos


class Comentario(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    # Garante compatibilidade ORM
    id: int
    nota: int
    titulo: str
    conteudo: str
    data_hora_feito: datetime
    usuario: int


class Categoria(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nome: str
    descricao: str


class Message(BaseModel):
    mensagem: str


class EventoPost(BaseModel):
    usuario_criador: int
    unidade_associada: int | None = None
    titulo: str
    descricao: str | None = None
    endereco: str | None = None
    foto_evento: int  # passar arquivo
    pagina_evento: str | None = None
    categoria: int
    capacidade_maxima: int | None = None
    data_hora: datetime | date
    # publico alvo
    # data_hora_fim


class EventoGet(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    titulo: str
    descricao: str
    endereco: str | None = None
    pagina_evento: str | None = None
    foto_evento: int
    publico_alvo: str
    categoria: Categoria
    status: str

    unidade_associada: int | None = None

    data_hora_criacao: datetime
    data_hora_evento: datetime
    data_hora_fim: datetime

    quantidade_inscricao: int = 0
    capacidade_maxima: int | None = None

    data_cancelamento: datetime | None = None
    data_ultima_atualizacao: datetime | None = None

    comentarios: list[Comentario] = []


class EventosList(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    eventos: list[EventoGet]
