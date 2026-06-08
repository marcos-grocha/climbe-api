from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import require_role
from app.models import Proposta, Usuario
from app.schemas.proposta import PropostaCreate, PropostaResponse, PropostaUpdate
from app.services import proposta_service

router = APIRouter(prefix="/propostas", tags=["propostas"])
_staff = Depends(require_role(["admin", "analista"]))


@router.get("", response_model=list[PropostaResponse], dependencies=[_staff])
def listar(db: Annotated[Session, Depends(get_db)]) -> list[Proposta]:
    return proposta_service.listar_propostas(db)


@router.get("/{id_proposta}", response_model=PropostaResponse, dependencies=[_staff])
def obter(id_proposta: int, db: Annotated[Session, Depends(get_db)]) -> Proposta:
    return proposta_service.obter_proposta(db, id_proposta)


@router.post("", response_model=PropostaResponse, status_code=status.HTTP_201_CREATED)
def criar(
    dados: PropostaCreate,
    db: Annotated[Session, Depends(get_db)],
    autor: Annotated[Usuario, Depends(require_role(["admin", "analista"]))],
) -> Proposta:
    return proposta_service.criar_proposta(db, dados, autor.id_usuario)


@router.patch("/{id_proposta}", response_model=PropostaResponse, dependencies=[_staff])
def atualizar(
    id_proposta: int, dados: PropostaUpdate, db: Annotated[Session, Depends(get_db)]
) -> Proposta:
    return proposta_service.atualizar_proposta(db, id_proposta, dados)


@router.delete("/{id_proposta}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[_staff])
def remover(id_proposta: int, db: Annotated[Session, Depends(get_db)]) -> None:
    proposta_service.remover_proposta(db, id_proposta)


@router.post("/{id_proposta}/enviar", response_model=PropostaResponse, dependencies=[_staff])
def enviar(id_proposta: int, db: Annotated[Session, Depends(get_db)]) -> Proposta:
    return proposta_service.transicionar(db, id_proposta, "enviada")


@router.post("/{id_proposta}/aprovar", response_model=PropostaResponse, dependencies=[_staff])
def aprovar(id_proposta: int, db: Annotated[Session, Depends(get_db)]) -> Proposta:
    return proposta_service.transicionar(db, id_proposta, "aprovada")


@router.post("/{id_proposta}/recusar", response_model=PropostaResponse, dependencies=[_staff])
def recusar(id_proposta: int, db: Annotated[Session, Depends(get_db)]) -> Proposta:
    return proposta_service.transicionar(db, id_proposta, "recusada")
