from __future__ import annotations

from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions import (
    CnpjDuplicadoError,
    EmpresaComVinculosError,
    EmpresaNaoEncontradaError,
)
from app.models import Empresa, EmpresaServico
from app.schemas.empresa import EmpresaCreate, EmpresaUpdate
from app.services.servico_service import validar_servicos
from app.utils.validators import validar_cnpj

_CAMPOS_SIMPLES = (
    "razao_social",
    "nome_fantasia",
    "logradouro",
    "numero",
    "bairro",
    "cidade",
    "uf",
    "cep",
    "telefone",
    "representante_nome",
    "representante_cpf",
    "representante_contato",
)


def listar_empresas(db: Session) -> list[Empresa]:
    return list(db.scalars(select(Empresa).order_by(Empresa.razao_social)))


def obter_empresa(db: Session, id_empresa: int) -> Empresa:
    empresa = db.get(Empresa, id_empresa)
    if empresa is None:
        raise EmpresaNaoEncontradaError
    return empresa


def _checar_cnpj_unico(db: Session, cnpj: str, ignorar_id: int | None = None) -> None:
    existente = db.scalar(select(Empresa).where(Empresa.cnpj == cnpj))
    if existente is not None and existente.id_empresa != ignorar_id:
        raise CnpjDuplicadoError


def _definir_servicos(db: Session, empresa: Empresa, servico_ids: list[int]) -> None:
    validar_servicos(db, servico_ids)
    db.execute(delete(EmpresaServico).where(EmpresaServico.id_empresa == empresa.id_empresa))
    for sid in dict.fromkeys(servico_ids):
        db.add(EmpresaServico(id_empresa=empresa.id_empresa, id_servico=sid))
    db.flush()


def criar_empresa(db: Session, dados: EmpresaCreate) -> Empresa:
    cnpj = validar_cnpj(dados.cnpj)
    _checar_cnpj_unico(db, cnpj)
    validar_servicos(db, dados.servico_ids)
    empresa = Empresa(
        razao_social=dados.razao_social,
        nome_fantasia=dados.nome_fantasia,
        cnpj=cnpj,
        logradouro=dados.logradouro,
        numero=dados.numero,
        bairro=dados.bairro,
        cidade=dados.cidade,
        uf=dados.uf,
        cep=dados.cep,
        telefone=dados.telefone,
        email=str(dados.email) if dados.email else None,
        representante_nome=dados.representante_nome,
        representante_cpf=dados.representante_cpf,
        representante_contato=dados.representante_contato,
    )
    db.add(empresa)
    db.flush()
    _definir_servicos(db, empresa, dados.servico_ids)
    db.commit()
    db.refresh(empresa)
    return empresa


def atualizar_empresa(db: Session, id_empresa: int, dados: EmpresaUpdate) -> Empresa:
    empresa = obter_empresa(db, id_empresa)
    if dados.cnpj is not None:
        cnpj = validar_cnpj(dados.cnpj)
        _checar_cnpj_unico(db, cnpj, ignorar_id=empresa.id_empresa)
        empresa.cnpj = cnpj
    for campo in _CAMPOS_SIMPLES:
        valor = getattr(dados, campo)
        if valor is not None:
            setattr(empresa, campo, valor)
    if dados.email is not None:
        empresa.email = str(dados.email)
    if dados.servico_ids is not None:
        _definir_servicos(db, empresa, dados.servico_ids)
    db.commit()
    db.refresh(empresa)
    return empresa


def remover_empresa(db: Session, id_empresa: int) -> None:
    empresa = obter_empresa(db, id_empresa)
    db.delete(empresa)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise EmpresaComVinculosError from exc
