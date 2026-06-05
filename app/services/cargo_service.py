from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions import CargoEmUsoError, CargoNaoEncontradoError
from app.models import Cargo
from app.schemas.cargo import CargoCreate, CargoUpdate


def listar_cargos(db: Session) -> list[Cargo]:
    return list(db.scalars(select(Cargo).order_by(Cargo.nome_cargo)))


def obter_cargo(db: Session, id_cargo: int) -> Cargo:
    cargo = db.get(Cargo, id_cargo)
    if cargo is None:
        raise CargoNaoEncontradoError
    return cargo


def criar_cargo(db: Session, dados: CargoCreate) -> Cargo:
    cargo = Cargo(nome_cargo=dados.nome_cargo)
    db.add(cargo)
    db.commit()
    db.refresh(cargo)
    return cargo


def atualizar_cargo(db: Session, id_cargo: int, dados: CargoUpdate) -> Cargo:
    cargo = obter_cargo(db, id_cargo)
    if dados.nome_cargo is not None:
        cargo.nome_cargo = dados.nome_cargo
    db.commit()
    db.refresh(cargo)
    return cargo


def remover_cargo(db: Session, id_cargo: int) -> None:
    cargo = obter_cargo(db, id_cargo)
    db.delete(cargo)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise CargoEmUsoError from exc
