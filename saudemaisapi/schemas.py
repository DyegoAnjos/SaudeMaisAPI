from datetime import datetime

from pydantic import BaseModel, ConfigDict


# Arquivo que gerencia o formato de entradas e retornos
class Message(BaseModel):
    mensagem: str


class Usuario(BaseModel):
    email: str
    nome: str
    senha: str
    # foto_perfil


class Usuario_adiministrador(Usuario):
    telefone: str


class Usuario_comum(Usuario_adiministrador):
    cpf: str
    data_nascimento: datetime
    regiao_preferida: str


class Usuario_institucional(Usuario):
    cnpj: str
    vinculo_instituicao: str
    descricao: str
    endereco: str


class Usuario_retorno(Usuario):
    model_config = ConfigDict(from_attributes=True)
    id: int


class Usuario_comum_retorno(Usuario_comum):
    model_config = ConfigDict(from_attributes=True)
    id: int

class Usuario_comum_lista(Usuario_comum_retorno):
    model_config = ConfigDict(from_attributes=True)
    usuarios: list[Usuario_comum_retorno]


class Usuario_administrador_retorno(Usuario_adiministrador):
    model_config = ConfigDict(from_attributes=True)
    id: int


class Usuario_institucional_retorno(Usuario_institucional):
    model_config = ConfigDict(from_attributes=True)
    id: int
    status: str = 'Pendente'


class Sugestao(BaseModel):
    titulo: str
    conteudo: str

    usuario: int


class Sugestao_retorno(Sugestao):
    model_config = ConfigDict(from_attributes=True)
    id: int
    data_hora_envio: datetime


class Comentario(BaseModel):
    nota: int
    titulo: str
    conteudo: str

    usuario: int
    evento: int


class Comentario_retorno(Comentario):
    model_config = ConfigDict(from_attributes=True)
    # Garante compatibilidade ORM
    id: int

    data_hora_feito: datetime


class Inscricao(BaseModel):
    usuario: int
    evento: int


class Inscricao_retorno(Inscricao):
    model_config = ConfigDict(from_attributes=True)
    id: int


class Unidade_saude(BaseModel):
    nome: str
    endereco: str

    latitude: float
    longitude: float
    lotacao: int

    tempo_medio_atendimento: int
    especialidade: str


class Unidade_saude_retorno(Unidade_saude):
    model_config = ConfigDict(from_attributes=True)
    id: int


class Categoria(BaseModel):
    nome: str
    descricao: str


class Categoria_retorno(Categoria):
    model_config = ConfigDict(from_attributes=True)
    id: int


class Fotografias(BaseModel):
    nome: str
    arquivo: str
    foto_de_evento: bool


class Fotografia_retorno(Fotografias):
    model_config = ConfigDict(from_attributes=True)
    id: int

    data_hora_envio: datetime


class Evento(BaseModel):
    titulo: str
    descricao: str
    data_hora_evento: datetime
    data_hora_fim: datetime
    publico_alvo: str

    categoria: Categoria
    # foto_evento:
    criador_institucional: int

    capacidade_maxima: int | None = None
    unidade_associada: int | None = None
    endereco: str | None
    pagina_evento: str | None = None


class Evento_retorno(Evento):
    model_config = ConfigDict(from_attributes=True)

    id: int
    inscricoes_atuais: int = 0

    status: str

    data_hora_criacao: datetime
    data_cancelamento: datetime | None = None
    data_ultima_atualizacao: datetime | None = None

    comentarios: list[Comentario_retorno] = []


class EventosList(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    eventos: list[Evento_retorno]
