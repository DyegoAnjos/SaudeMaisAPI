from datetime import date, datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_as_dataclass, mapped_column, registry

registrador_tabela = registry()


@mapped_as_dataclass(registrador_tabela)
class Evento:
    __tablename__ = 'Evento'

    # 1. Campos de controle que o banco gera sozinhos (Ficam protegidos)
    id: Mapped[int] = mapped_column(
        init=False, primary_key=True, autoincrement='auto'
    )
    data_criacao: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )

    # 2. OBRIGATÓRIOS PRIMEIRO
    titulo: Mapped[str] = mapped_column(unique=True)
    data: Mapped[date]
    usuario_criador: Mapped[int]
    tipo_evento: Mapped[int]
    foto_evento: Mapped[int]

    # 3. OPCIONAIS DEPOIS
    descricao: Mapped[str | None] = mapped_column(default=None)
    capacidade_maxima: Mapped[int | None] = mapped_column(default=None)
    endereco: Mapped[str | None] = mapped_column(default=None)
    status: Mapped[str | None] = mapped_column(default='Pendente')
    unidade_associada: Mapped[int | None] = mapped_column(default=None)
    data_cancelamento: Mapped[date | None] = mapped_column(default=None)

    data_ultima_atualizacao: Mapped[datetime | None] = mapped_column(
        DateTime, init=False, onupdate=func.now(), default=None
    )

    link_externo: Mapped[str | None] = mapped_column(default=None)
