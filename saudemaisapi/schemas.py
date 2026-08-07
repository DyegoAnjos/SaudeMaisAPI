from datetime import datetime

from pydantic import BaseModel, ConfigDict


# Arquivo que gerencia o formato de entradas e retornos
class MessageSchema(BaseModel):
    mensagem: str


class UsuarioSchema(BaseModel):
    email: str
    nome: str
    senha: str
    # foto_perfil


class Usuario_adiministrador_Schema(UsuarioSchema):
    telefone: str


class Usuario_comum_Schema(Usuario_adiministrador_Schema):
    cpf: str
    data_nascimento: datetime
    regiao_preferida: str


class Usuario_Schema_institucional_Schema(UsuarioSchema):
    cnpj: str
    vinculo_instituicao: str
    descricao: str
    endereco: str


class Usuario_retorno_Schema(UsuarioSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int


class Usuario_comum_retorno_Schema(Usuario_comum_Schema):
    model_config = ConfigDict(from_attributes=True)
    id: int


class Usuario_comum_lista_Schema(Usuario_comum_retorno_Schema):
    model_config = ConfigDict(from_attributes=True)
    usuarios: list[Usuario_comum_retorno_Schema]


class Usuario_administrador_retorno_Schema(Usuario_adiministrador_Schema):
    model_config = ConfigDict(from_attributes=True)
    id: int


class Usuario_institucional_retorno_Schema(
    Usuario_Schema_institucional_Schema
):
    model_config = ConfigDict(from_attributes=True)
    id: int
    status: str = 'Pendente'


class Sugestao_Schema(BaseModel):
    titulo: str
    conteudo: str

    usuario: int


class Sugestao_retorno_Schema(Sugestao_Schema):
    model_config = ConfigDict(from_attributes=True)
    id: int
    data_hora_envio: datetime


class Comentario_Schema(BaseModel):
    nota: int
    titulo: str
    conteudo: str

    usuario: int
    evento: int


class Comentario_retorno_Schema(Comentario_Schema):
    model_config = ConfigDict(from_attributes=True)
    # Garante compatibilidade ORM
    id: int

    data_hora_feito: datetime


class Inscricao_Schema(BaseModel):
    usuario: int
    evento: int


class Inscricao_retorno_Schema(Inscricao_Schema):
    model_config = ConfigDict(from_attributes=True)
    id: int


class Unidade_saude_Schema(BaseModel):
    nome: str
    endereco: str

    latitude: float
    longitude: float
    lotacao: int

    tempo_medio_atendimento: int
    especialidade: str


class Unidade_saude_retorno_Schema(Unidade_saude_Schema):
    model_config = ConfigDict(from_attributes=True)
    id: int


class Categoria_Schema(BaseModel):
    nome: str
    descricao: str


class Categoria_retorno_Schema(Categoria_Schema):
    model_config = ConfigDict(from_attributes=True)
    id: int


class Fotografias_Schema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    nome: str
    arquivo: bytes
    foto_de_evento: bool


class Fotografia_retorno_Schema(Fotografias_Schema):
    model_config = ConfigDict(from_attributes=True)
    id: int

    data_hora_envio: datetime


class Fotografia_lista_Schema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    fotografias: list[Fotografia_retorno_Schema]


class Evento_Schema(BaseModel):
    titulo: str
    descricao: str
    data_hora_evento: datetime
    data_hora_fim: datetime
    publico_alvo: str

    categoria: int
    foto_evento: int
    criador_institucional: int

    capacidade_maxima: int | None = None
    unidade_associada: int | None = None
    endereco: str | None = None
    pagina_evento: str | None = None


class Evento_retorno_Schema(Evento_Schema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    inscricoes_atuais: int = 0

    status: str

    data_hora_criacao: datetime
    data_hora_cancelamento: datetime | None = None
    data_hora_ultima_atualizacao: datetime | None = None

    comentarios: list[Comentario_retorno_Schema] = []


class Eventos_list_Schema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    eventos: list[Evento_retorno_Schema]


class Filtro_Paginas(BaseModel):
    limit: int = 10
    offset: int = 0
