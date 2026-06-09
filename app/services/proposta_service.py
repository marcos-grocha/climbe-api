from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions import (
    PropostaComContratoError,
    PropostaNaoEncontradaError,
    PropostaTransicaoInvalidaError,
)
from app.models import Proposta
from app.schemas.proposta import PropostaCreate, PropostaUpdate
from app.services import contrato_service
from app.services.empresa_service import obter_empresa

# Transições de status permitidas (máquina de estados da proposta).
_TRANSICOES: dict[str, set[str]] = {
    "rascunho": {"enviada"},
    "enviada": {"aprovada", "recusada"},
    "aprovada": set(),
    "recusada": set(),
}


def listar_propostas(db: Session) -> list[Proposta]:
    return list(db.scalars(select(Proposta).order_by(Proposta.id_proposta)))


def obter_proposta(db: Session, id_proposta: int) -> Proposta:
    proposta = db.get(Proposta, id_proposta)
    if proposta is None:
        raise PropostaNaoEncontradaError
    return proposta


def criar_proposta(db: Session, dados: PropostaCreate, autor_id: int) -> Proposta:
    obter_empresa(db, dados.empresa_id)  # valida a empresa (404 se não existe)
    proposta = Proposta(empresa_id=dados.empresa_id, usuario_id=autor_id)
    db.add(proposta)
    db.commit()
    db.refresh(proposta)
    return proposta


def atualizar_proposta(db: Session, id_proposta: int, dados: PropostaUpdate) -> Proposta:
    proposta = obter_proposta(db, id_proposta)
    if dados.empresa_id is not None:
        if proposta.status != "rascunho":
            raise PropostaTransicaoInvalidaError
        obter_empresa(db, dados.empresa_id)
        proposta.empresa_id = dados.empresa_id
    db.commit()
    db.refresh(proposta)
    return proposta


def transicionar(db: Session, id_proposta: int, novo_status: str) -> Proposta:
    proposta = obter_proposta(db, id_proposta)
    if novo_status not in _TRANSICOES.get(proposta.status, set()):
        raise PropostaTransicaoInvalidaError
    proposta.status = novo_status
    if novo_status == "aprovada":
        contrato_service.criar_para_proposta(db, proposta)
    db.commit()
    db.refresh(proposta)
    return proposta


def remover_proposta(db: Session, id_proposta: int) -> None:
    proposta = obter_proposta(db, id_proposta)
    db.delete(proposta)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise PropostaComContratoError from exc
