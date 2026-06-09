from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import require_role
from app.models import Contrato
from app.schemas.contrato import ContratoResponse, ContratoUpdate
from app.services import contrato_service

router = APIRouter(prefix="/contratos", tags=["contratos"])
_staff = Depends(require_role(["admin", "analista"]))


@router.get("", response_model=list[ContratoResponse], dependencies=[_staff])
def listar(db: Annotated[Session, Depends(get_db)]) -> list[Contrato]:
    return contrato_service.listar_contratos(db)


@router.get("/{id_contrato}", response_model=ContratoResponse, dependencies=[_staff])
def obter(id_contrato: int, db: Annotated[Session, Depends(get_db)]) -> Contrato:
    return contrato_service.obter_contrato(db, id_contrato)


@router.patch("/{id_contrato}", response_model=ContratoResponse, dependencies=[_staff])
def atualizar(
    id_contrato: int, dados: ContratoUpdate, db: Annotated[Session, Depends(get_db)]
) -> Contrato:
    return contrato_service.atualizar_contrato(db, id_contrato, dados)


@router.post("/{id_contrato}/encerrar", response_model=ContratoResponse, dependencies=[_staff])
def encerrar(id_contrato: int, db: Annotated[Session, Depends(get_db)]) -> Contrato:
    return contrato_service.encerrar_contrato(db, id_contrato)
