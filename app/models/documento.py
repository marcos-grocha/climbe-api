from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.empresa import Empresa
    from app.models.usuario import Usuario


class Documento(Base, TimestampMixin):
    __tablename__ = "documentos"

    id_documento: Mapped[int] = mapped_column(primary_key=True)
    empresa_id: Mapped[int] = mapped_column(ForeignKey("empresas.id_empresa", ondelete="CASCADE"))
    tipo_documento: Mapped[str] = mapped_column(String(255))
    url: Mapped[str | None] = mapped_column(String(255))
    validado: Mapped[str] = mapped_column(
        String(255), default="pendente", server_default="pendente"
    )
    analista_id: Mapped[int | None] = mapped_column(
        ForeignKey("usuarios.id_usuario", ondelete="SET NULL")
    )

    empresa: Mapped[Empresa] = relationship(back_populates="documentos")
    analista: Mapped[Usuario | None] = relationship(back_populates="documentos_validados")
