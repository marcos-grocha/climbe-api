from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.cargo import Cargo
    from app.models.documento import Documento
    from app.models.notificacao import Notificacao
    from app.models.proposta import Proposta


class Usuario(Base, TimestampMixin):
    __tablename__ = "usuarios"

    id_usuario: Mapped[int] = mapped_column(primary_key=True)
    nome_completo: Mapped[str] = mapped_column(String(255))
    cargo_id: Mapped[int] = mapped_column(ForeignKey("cargos.id_cargo", ondelete="RESTRICT"))
    cpf: Mapped[str] = mapped_column(String(14), unique=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    contato: Mapped[str] = mapped_column(String(50))
    situacao: Mapped[str] = mapped_column(String(255), default="ativo", server_default="ativo")
    senha_hash: Mapped[str] = mapped_column(String(60))

    cargo: Mapped[Cargo] = relationship(back_populates="usuarios")
    propostas: Mapped[list[Proposta]] = relationship(back_populates="usuario")
    documentos_validados: Mapped[list[Documento]] = relationship(back_populates="analista")
    notificacoes: Mapped[list[Notificacao]] = relationship(back_populates="usuario")
