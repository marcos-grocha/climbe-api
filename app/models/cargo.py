from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.usuario import Usuario


class Cargo(Base, TimestampMixin):
    __tablename__ = "cargos"

    id_cargo: Mapped[int] = mapped_column(primary_key=True)
    nome_cargo: Mapped[str] = mapped_column(String(255), unique=True)

    usuarios: Mapped[list[Usuario]] = relationship(back_populates="cargo")
