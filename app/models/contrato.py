from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.planilha import Planilha
    from app.models.proposta import Proposta
    from app.models.relatorio import Relatorio


class Contrato(Base, TimestampMixin):
    __tablename__ = "contratos"

    id_contrato: Mapped[int] = mapped_column(primary_key=True)
    proposta_id: Mapped[int] = mapped_column(
        ForeignKey("propostas.id_proposta", ondelete="RESTRICT"), unique=True
    )
    data_inicio: Mapped[date | None] = mapped_column()
    data_fim: Mapped[date | None] = mapped_column()
    status: Mapped[str] = mapped_column(String(255), default="ativo", server_default="ativo")

    proposta: Mapped[Proposta] = relationship(back_populates="contrato")
    planilhas: Mapped[list[Planilha]] = relationship(back_populates="contrato")
    relatorios: Mapped[list[Relatorio]] = relationship(back_populates="contrato")
