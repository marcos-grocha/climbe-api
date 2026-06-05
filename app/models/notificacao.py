from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.usuario import Usuario


class Notificacao(Base, TimestampMixin):
    __tablename__ = "notificacoes"

    id_notificacao: Mapped[int] = mapped_column(primary_key=True)
    id_usuario: Mapped[int] = mapped_column(ForeignKey("usuarios.id_usuario", ondelete="CASCADE"))
    mensagem: Mapped[str] = mapped_column(String(255))
    data_envio: Mapped[date | None] = mapped_column()
    tipo: Mapped[str | None] = mapped_column(String(255))

    usuario: Mapped[Usuario] = relationship(back_populates="notificacoes")
