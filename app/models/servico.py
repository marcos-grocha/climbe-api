from __future__ import annotations

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.mixins import TimestampMixin


class Servico(Base, TimestampMixin):
    __tablename__ = "servicos"

    id_servico: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(255), unique=True)


class EmpresaServico(Base):
    """Associação M:N entre empresas e serviços contratados."""

    __tablename__ = "empresa_servico"

    id_empresa: Mapped[int] = mapped_column(
        ForeignKey("empresas.id_empresa", ondelete="CASCADE"), primary_key=True
    )
    id_servico: Mapped[int] = mapped_column(
        ForeignKey("servicos.id_servico", ondelete="CASCADE"), primary_key=True
    )
