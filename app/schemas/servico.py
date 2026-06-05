from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class ServicoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_servico: int
    nome: str
