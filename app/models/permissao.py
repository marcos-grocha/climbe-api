from __future__ import annotations

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.mixins import TimestampMixin


class Permissao(Base, TimestampMixin):
    __tablename__ = "permissoes"

    id_permissao: Mapped[int] = mapped_column(primary_key=True)
    descricao: Mapped[str] = mapped_column(String(255))


class UsuarioPermissao(Base):
    """Associação M:N entre usuários e permissões."""

    __tablename__ = "usuario_permissoes"

    id_usuario: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id_usuario", ondelete="CASCADE"), primary_key=True
    )
    id_permissao: Mapped[int] = mapped_column(
        ForeignKey("permissoes.id_permissao", ondelete="CASCADE"), primary_key=True
    )
