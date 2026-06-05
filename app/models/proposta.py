from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.contrato import Contrato
    from app.models.empresa import Empresa
    from app.models.usuario import Usuario


class Proposta(Base, TimestampMixin):
    __tablename__ = "propostas"

    id_proposta: Mapped[int] = mapped_column(primary_key=True)
    empresa_id: Mapped[int] = mapped_column(ForeignKey("empresas.id_empresa", ondelete="RESTRICT"))
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id_usuario", ondelete="RESTRICT"))
    status: Mapped[str] = mapped_column(String(255), default="rascunho", server_default="rascunho")
    data_criacao: Mapped[date] = mapped_column(default=date.today)

    empresa: Mapped[Empresa] = relationship(back_populates="propostas")
    usuario: Mapped[Usuario] = relationship(back_populates="propostas")
    contrato: Mapped[Contrato | None] = relationship(back_populates="proposta")
