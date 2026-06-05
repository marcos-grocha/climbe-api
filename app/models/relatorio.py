from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.contrato import Contrato


class Relatorio(Base, TimestampMixin):
    __tablename__ = "relatorios"

    id_relatorio: Mapped[int] = mapped_column(primary_key=True)
    contrato_id: Mapped[int] = mapped_column(
        ForeignKey("contratos.id_contrato", ondelete="CASCADE")
    )
    url_pdf: Mapped[str | None] = mapped_column(String(255))
    data_envio: Mapped[date | None] = mapped_column()

    contrato: Mapped[Contrato] = relationship(back_populates="relatorios")
