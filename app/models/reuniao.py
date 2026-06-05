from __future__ import annotations

from datetime import date, time
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.empresa import Empresa


class Reuniao(Base, TimestampMixin):
    __tablename__ = "reunioes"

    id_reuniao: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(String(255))
    empresa_id: Mapped[int | None] = mapped_column(
        ForeignKey("empresas.id_empresa", ondelete="SET NULL")
    )
    data: Mapped[date | None] = mapped_column()
    hora: Mapped[time | None] = mapped_column()
    presencial: Mapped[bool] = mapped_column(default=False)
    local: Mapped[str | None] = mapped_column(String(255))
    pauta: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(255), default="agendada", server_default="agendada")

    empresa: Mapped[Empresa | None] = relationship(back_populates="reunioes")


class ParticipanteReuniao(Base):
    """Associação M:N entre reuniões e usuários participantes."""

    __tablename__ = "participantes_reuniao"

    id_reuniao: Mapped[int] = mapped_column(
        ForeignKey("reunioes.id_reuniao", ondelete="CASCADE"), primary_key=True
    )
    id_usuario: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id_usuario", ondelete="CASCADE"), primary_key=True
    )
