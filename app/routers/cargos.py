from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user, require_role
from app.models import Cargo
from app.schemas.cargo import CargoCreate, CargoResponse, CargoUpdate
from app.services import cargo_service

router = APIRouter(prefix="/cargos", tags=["cargos"])
_admin = Depends(require_role(["admin"]))


@router.get("", response_model=list[CargoResponse], dependencies=[Depends(get_current_user)])
def listar(db: Annotated[Session, Depends(get_db)]) -> list[Cargo]:
    return cargo_service.listar_cargos(db)


@router.post(
    "",
    response_model=CargoResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[_admin],
)
def criar(dados: CargoCreate, db: Annotated[Session, Depends(get_db)]) -> Cargo:
    return cargo_service.criar_cargo(db, dados)


@router.patch("/{id_cargo}", response_model=CargoResponse, dependencies=[_admin])
def atualizar(id_cargo: int, dados: CargoUpdate, db: Annotated[Session, Depends(get_db)]) -> Cargo:
    return cargo_service.atualizar_cargo(db, id_cargo, dados)


@router.delete("/{id_cargo}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[_admin])
def remover(id_cargo: int, db: Annotated[Session, Depends(get_db)]) -> None:
    cargo_service.remover_cargo(db, id_cargo)
