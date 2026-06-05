from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.exceptions import ServicoNaoEncontradoError
from app.models import Servico


def listar_servicos(db: Session) -> list[Servico]:
    return list(db.scalars(select(Servico).order_by(Servico.nome)))


def validar_servicos(db: Session, servico_ids: list[int]) -> None:
    """Garante que todos os ids existem; senão levanta `ServicoNaoEncontradoError`."""
    if not servico_ids:
        return
    existentes = set(
        db.scalars(select(Servico.id_servico).where(Servico.id_servico.in_(servico_ids)))
    )
    if set(servico_ids) - existentes:
        raise ServicoNaoEncontradoError
