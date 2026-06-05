from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.documento import Documento
    from app.models.proposta import Proposta
    from app.models.reuniao import Reuniao


class Empresa(Base, TimestampMixin):
    __tablename__ = "empresas"

    id_empresa: Mapped[int] = mapped_column(primary_key=True)
    razao_social: Mapped[str] = mapped_column(String(255))
    nome_fantasia: Mapped[str | None] = mapped_column(String(255))
    cnpj: Mapped[str] = mapped_column(String(18), unique=True)
    logradouro: Mapped[str | None] = mapped_column(String(255))
    numero: Mapped[str | None] = mapped_column(String(255))
    bairro: Mapped[str | None] = mapped_column(String(255))
    cidade: Mapped[str | None] = mapped_column(String(255))
    uf: Mapped[str | None] = mapped_column(String(255))
    cep: Mapped[str | None] = mapped_column(String(255))
    telefone: Mapped[str | None] = mapped_column(String(50))
    email: Mapped[str | None] = mapped_column(String(255))
    representante_nome: Mapped[str | None] = mapped_column(String(255))
    representante_cpf: Mapped[str | None] = mapped_column(String(14))
    representante_contato: Mapped[str | None] = mapped_column(String(50))

    propostas: Mapped[list[Proposta]] = relationship(back_populates="empresa")
    documentos: Mapped[list[Documento]] = relationship(back_populates="empresa")
    reunioes: Mapped[list[Reuniao]] = relationship(back_populates="empresa")
