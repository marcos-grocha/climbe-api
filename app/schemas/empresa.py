from __future__ import annotations

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.schemas.servico import ServicoResponse


class EmpresaCreate(BaseModel):
    razao_social: str
    nome_fantasia: str | None = None
    cnpj: str
    logradouro: str | None = None
    numero: str | None = None
    bairro: str | None = None
    cidade: str | None = None
    uf: str | None = None
    cep: str | None = None
    telefone: str | None = None
    email: EmailStr | None = None
    representante_nome: str | None = None
    representante_cpf: str | None = None
    representante_contato: str | None = None
    servico_ids: list[int] = Field(default_factory=list)


class EmpresaUpdate(BaseModel):
    razao_social: str | None = None
    nome_fantasia: str | None = None
    cnpj: str | None = None
    logradouro: str | None = None
    numero: str | None = None
    bairro: str | None = None
    cidade: str | None = None
    uf: str | None = None
    cep: str | None = None
    telefone: str | None = None
    email: EmailStr | None = None
    representante_nome: str | None = None
    representante_cpf: str | None = None
    representante_contato: str | None = None
    # None = não altera os vínculos; lista (mesmo vazia) substitui o conjunto.
    servico_ids: list[int] | None = None


class EmpresaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_empresa: int
    razao_social: str
    nome_fantasia: str | None
    cnpj: str
    logradouro: str | None
    numero: str | None
    bairro: str | None
    cidade: str | None
    uf: str | None
    cep: str | None
    telefone: str | None
    email: str | None
    representante_nome: str | None
    representante_cpf: str | None
    representante_contato: str | None
    servicos: list[ServicoResponse] = []
