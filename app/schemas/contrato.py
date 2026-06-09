from __future__ import annotations

from datetime import date

from pydantic import BaseModel, ConfigDict


class ContratoUpdate(BaseModel):
    data_inicio: date | None = None
    data_fim: date | None = None
    prazo_entrega: date | None = None
    recorrente: bool | None = None


class ContratoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_contrato: int
    proposta_id: int
    data_inicio: date | None
    data_fim: date | None
    prazo_entrega: date | None
    recorrente: bool
    status: str
