from __future__ import annotations

from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.exceptions import ContratoNaoEncontradoError, ContratoTransicaoInvalidaError
from app.models import Contrato, Proposta
from app.schemas.contrato import ContratoUpdate


def criar_para_proposta(db: Session, proposta: Proposta) -> Contrato:
    """Cria o contrato da proposta aprovada (idempotente: 1:1 por proposta).

    Faz `flush` (não `commit`): o commit é do fluxo de aprovação da proposta.
    """
    existente = db.scalar(select(Contrato).where(Contrato.proposta_id == proposta.id_proposta))
    if existente is not None:
        return existente
    contrato = Contrato(proposta_id=proposta.id_proposta, data_inicio=date.today(), status="ativo")
    db.add(contrato)
    db.flush()
    return contrato


def listar_contratos(db: Session) -> list[Contrato]:
    return list(db.scalars(select(Contrato).order_by(Contrato.id_contrato)))


def obter_contrato(db: Session, id_contrato: int) -> Contrato:
    contrato = db.get(Contrato, id_contrato)
    if contrato is None:
        raise ContratoNaoEncontradoError
    return contrato


def atualizar_contrato(db: Session, id_contrato: int, dados: ContratoUpdate) -> Contrato:
    contrato = obter_contrato(db, id_contrato)
    if dados.data_inicio is not None:
        contrato.data_inicio = dados.data_inicio
    if dados.data_fim is not None:
        contrato.data_fim = dados.data_fim
    if dados.prazo_entrega is not None:
        contrato.prazo_entrega = dados.prazo_entrega
    if dados.recorrente is not None:
        contrato.recorrente = dados.recorrente
    db.commit()
    db.refresh(contrato)
    return contrato


def encerrar_contrato(db: Session, id_contrato: int) -> Contrato:
    contrato = obter_contrato(db, id_contrato)
    if contrato.status != "ativo":
        raise ContratoTransicaoInvalidaError
    contrato.status = "encerrado"
    db.commit()
    db.refresh(contrato)
    return contrato
