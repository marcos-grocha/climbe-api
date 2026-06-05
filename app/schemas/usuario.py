from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field

Papel = Literal["admin", "analista", "contratante"]


class UsuarioCreate(BaseModel):
    nome_completo: str
    cargo_id: int
    cpf: str
    email: EmailStr
    contato: str
    papel: Papel = "analista"
    senha: str = Field(min_length=6)


class UsuarioUpdate(BaseModel):
    nome_completo: str | None = None
    cargo_id: int | None = None
    contato: str | None = None
    papel: Papel | None = None
    situacao: Literal["ativo", "inativo"] | None = None


class UsuarioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_usuario: int
    nome_completo: str
    cargo_id: int
    cpf: str
    email: str
    contato: str
    papel: str
    situacao: str


class TrocarSenha(BaseModel):
    senha_atual: str
    nova_senha: str = Field(min_length=6)
