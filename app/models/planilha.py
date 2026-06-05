from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.contrato import Contrato


class Planilha(Base, TimestampMixin):
    __tablename__ = "planilhas"

    id_planilha: Mapped[int] = mapped_column(primary_key=True)
    contrato_id: Mapped[int] = mapped_column(
        ForeignKey("contratos.id_contrato", ondelete="CASCADE")
    )
    url_google_sheets: Mapped[str | None] = mapped_column(String(255))
    bloqueada: Mapped[bool] = mapped_column(default=False)
    permissao_visualizacao: Mapped[str | None] = mapped_column(String(255))

    contrato: Mapped[Contrato] = relationship(back_populates="planilhas")
