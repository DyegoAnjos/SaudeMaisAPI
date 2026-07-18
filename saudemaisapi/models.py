from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, LargeBinary, func
from sqlalchemy.orm import Mapped, mapped_as_dataclass, mapped_column, registry

registrador_tabela = registry()


@mapped_as_dataclass(registrador_tabela)
class Usuario_Comum:
    __tablename__ = 'usuario_comum'

    id: Mapped[int] = mapped_column(
        init=False, primary_key=True, autoincrement='auto'
    )

    email: Mapped[str] = mapped_column(unique=True)
    cpf: Mapped[str] = mapped_column(unique=True)
    nome: Mapped[str]
    senha: Mapped[str]
    data_nascimento: Mapped[datetime]

    telefone: Mapped[int] = mapped_column(default=0)

    foto_perfil: Mapped[int | None] = mapped_column(
        ForeignKey('fotografias.id'), default=None
    )

    regiao_preferida: Mapped[str | None] = mapped_column(default=None)


@mapped_as_dataclass(registrador_tabela)
class Usuario_administrador:
    __tablename__ = 'usuario_administrador'

    id: Mapped[int] = mapped_column(
        init=False, primary_key=True, autoincrement='auto'
    )

    email: Mapped[str] = mapped_column(unique=True)
    nome: Mapped[str]
    senha: Mapped[str]

    telefone: Mapped[int] = mapped_column(default=0)

    foto_perfil: Mapped[int | None] = mapped_column(
        ForeignKey('fotografias.id'), default=None
    )


@mapped_as_dataclass(registrador_tabela)
class Usuario_institucional:
    __tablename__ = 'usuario_institucional'

    id: Mapped[int] = mapped_column(
        init=False, primary_key=True, autoincrement='auto'
    )
    email: Mapped[str] = mapped_column(unique=True)
    nome: Mapped[str] = mapped_column(unique=True)
    cnpj: Mapped[str] = mapped_column(unique=True)

    senha: Mapped[str]
    vinculo_instituicao: Mapped[str]

    status: Mapped[str] = mapped_column(default='Pendente')

    foto_perfil: Mapped[int | None] = mapped_column(
        ForeignKey('fotografias.id'), default=None
    )

    descricao: Mapped[str | None] = mapped_column(default=None)
    endereco: Mapped[str | None] = mapped_column(default=None)


@mapped_as_dataclass(registrador_tabela)
class Sugestao:
    __tablename__ = 'sugestao'

    id: Mapped[int] = mapped_column(
        init=False, primary_key=True, autoincrement='auto'
    )

    titulo: Mapped[str]
    conteudo: Mapped[str]

    data_hora_envio: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )

    usuario: Mapped[int] = mapped_column(ForeignKey('usuario_comum.id'))


@mapped_as_dataclass(registrador_tabela)
class Comentario:
    __tablename__ = 'comentario'

    id: Mapped[int] = mapped_column(
        init=False, primary_key=True, autoincrement='auto'
    )
    data_hora_feito: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )

    titulo: Mapped[str]
    conteudo: Mapped[str]

    usuario: Mapped[int] = mapped_column(ForeignKey('usuario_comum.id'))
    evento: Mapped[int] = mapped_column(ForeignKey('evento.id'))

    nota: Mapped[int] = mapped_column(default=0)


@mapped_as_dataclass(registrador_tabela)
class Inscricao:
    __tablename__ = 'inscricao'

    id: Mapped[int] = mapped_column(
        init=False, primary_key=True, autoincrement='auto'
    )

    usuario: Mapped[int] = mapped_column(ForeignKey('usuario_comum.id'))
    evento: Mapped[int] = mapped_column(ForeignKey('evento.id'))


@mapped_as_dataclass(registrador_tabela)
class Unidade_saude:
    __tablename__ = 'unidade_saude'

    id: Mapped[int] = mapped_column(
        init=False, primary_key=True, autoincrement='auto'
    )
    nome: Mapped[str] = mapped_column(unique=True)
    endereco: Mapped[str]

    latitude: Mapped[float] = mapped_column(default=0)
    longitude: Mapped[float] = mapped_column(default=0)
    lotacao: Mapped[int] = mapped_column(default=0)

    tempo_medio_atendimento: Mapped[int | None] = mapped_column(default=None)
    especialidade: Mapped[str | None] = mapped_column(default=None)


@mapped_as_dataclass(registrador_tabela)
class Categoria:
    __tablename__ = 'categoria'
    id: Mapped[int] = mapped_column(
        init=False, primary_key=True, autoincrement='auto'
    )
    nome: Mapped[str] = mapped_column(unique=True)
    descricao: Mapped[str]


@mapped_as_dataclass(registrador_tabela)
class Fotografias:
    __tablename__ = 'fotografias'
    id: Mapped[int] = mapped_column(
        init=False, primary_key=True, autoincrement='auto'
    )

    data_hora_envio: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )

    nome: Mapped[str]
    arquivo: Mapped[bytes] = mapped_column(LargeBinary)

    foto_de_evento: Mapped[bool] = mapped_column(default=False)


@mapped_as_dataclass(registrador_tabela)
class Evento:
    __tablename__ = 'evento'

    # 1. Campos de controle (init=False ficam protegidos no início)
    id: Mapped[int] = mapped_column(
        init=False, primary_key=True, autoincrement='auto'
    )
    data_hora_criacao: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )

    # 2. OBRIGATÓRIOS PRIMEIRO (Nenhum destes possui valor padrão)
    titulo: Mapped[str] = mapped_column(unique=True)
    descricao: Mapped[str | None]
    data_hora_evento: Mapped[datetime]
    data_hora_fim: Mapped[datetime]
    publico_alvo: Mapped[str]

    # 💡 Corrigidos para ForeignKey maiúsculo
    categoria: Mapped[int] = mapped_column(ForeignKey('categoria.id'))
    foto_evento: Mapped[int] = mapped_column(ForeignKey('fotografias.id'))
    criador_institucional: Mapped[int] = mapped_column(
        ForeignKey('usuario_institucional.id')
    )

    # 3. OPCIONAIS COM VALOR PADRÃO DEPOIS (Todos têm default ou default=None)
    status: Mapped[str] = mapped_column(default='Pendente')
    capacidade_maxima: Mapped[int | None] = mapped_column(default=None)
    unidade_associada: Mapped[int | None] = mapped_column(default=None)
    endereco: Mapped[str | None] = mapped_column(default=None)
    data_cancelamento: Mapped[datetime | None] = mapped_column(default=None)

    data_ultima_atualizacao: Mapped[datetime | None] = mapped_column(
        DateTime, init=False, onupdate=func.now(), default=None
    )
    pagina_evento: Mapped[str | None] = mapped_column(default=None)
