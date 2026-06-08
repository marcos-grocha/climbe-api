from __future__ import annotations

from datetime import date

from pydantic import BaseModel, ConfigDict


class PropostaCreate(BaseModel):
    empresa_id: int


class PropostaUpdate(BaseModel):
    empresa_id: int | None = None


class PropostaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_proposta: int
    empresa_id: int
    usuario_id: int
    status: str
    data_criacao: date
