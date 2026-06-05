from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class CargoCreate(BaseModel):
    nome_cargo: str


class CargoUpdate(BaseModel):
    nome_cargo: str | None = None


class CargoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_cargo: int
    nome_cargo: str
