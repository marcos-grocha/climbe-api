from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str | None = None
    papel: str | None = None


class UsuarioMe(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_usuario: int
    nome_completo: str
    email: str
    papel: str
    situacao: str
