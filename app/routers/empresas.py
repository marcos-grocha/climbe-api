from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import require_role
from app.models import Empresa
from app.schemas.empresa import EmpresaCreate, EmpresaResponse, EmpresaUpdate
from app.services import empresa_service

router = APIRouter(prefix="/empresas", tags=["empresas"])
_staff = Depends(require_role(["admin", "analista"]))


@router.get("", response_model=list[EmpresaResponse], dependencies=[_staff])
def listar(db: Annotated[Session, Depends(get_db)]) -> list[Empresa]:
    return empresa_service.listar_empresas(db)


@router.get("/{id_empresa}", response_model=EmpresaResponse, dependencies=[_staff])
def obter(id_empresa: int, db: Annotated[Session, Depends(get_db)]) -> Empresa:
    return empresa_service.obter_empresa(db, id_empresa)


@router.post(
    "",
    response_model=EmpresaResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[_staff],
)
def criar(dados: EmpresaCreate, db: Annotated[Session, Depends(get_db)]) -> Empresa:
    return empresa_service.criar_empresa(db, dados)


@router.patch("/{id_empresa}", response_model=EmpresaResponse, dependencies=[_staff])
def atualizar(
    id_empresa: int, dados: EmpresaUpdate, db: Annotated[Session, Depends(get_db)]
) -> Empresa:
    return empresa_service.atualizar_empresa(db, id_empresa, dados)


@router.delete("/{id_empresa}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[_staff])
def remover(id_empresa: int, db: Annotated[Session, Depends(get_db)]) -> None:
    empresa_service.remover_empresa(db, id_empresa)
