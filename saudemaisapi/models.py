from datatime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_as_dataclass, mapped_column, registry

table_registry = registry()


@mapped_as_dataclass(table_registry)
class Evento:
    __tablename__ = 'evento'
    id: [Mapped[int]] = mapped_column(init=False, primary_key=True)
    titulo: Mapped[str] = mapped_column(unique=True, not_null=True)
    descricao: Mapped[str] = mapped_column(not_null=True)
    data_evento: Mapped[datetime] = mapped_column(not_null=True)
    data_envio: Mapped[datetime] = mapped_column(
        not_null=True, server_default=func.now()
    )
    capacidade_maxima: Mapped[int] = mapped_column(default=0)
    endereco: Mapped[str] = mapped_column(default='')
    # status: Mapped[str] =
    # mapped_column(default="") como fazer na questão de ENUM
    usuario_criador: Mapped[int] = mapped_column(not_null=True)
    unidade_associada: Mapped[int] = mapped_column(not_null=True)
    # tipo_evento: Mapped[str] =
    # mapped_column() como fazer na questão de ENUM
    # status_aprovacao: Mapped[str] =
    # mapped_column() como fazer na questão de ENUM
    motivo_recusa: Mapped[str] = mapped_column(default='')
    usuario_aprovadores: Mapped[int] = mapped_column(default=0)
    data_aprovacao: Mapped[datetime]
