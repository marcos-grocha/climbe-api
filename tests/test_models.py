from __future__ import annotations

import pytest
from sqlalchemy import delete, func, inspect, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import engine
from app.models import (
    Cargo,
    Contrato,
    Empresa,
    Planilha,
    Proposta,
    Relatorio,
    Reuniao,
    Servico,
    Usuario,
)

EXPECTED_TABLES = {
    "usuarios",
    "cargos",
    "permissoes",
    "usuario_permissoes",
    "empresas",
    "servicos",
    "empresa_servico",
    "propostas",
    "contratos",
    "documentos",
    "reunioes",
    "participantes_reuniao",
    "planilhas",
    "relatorios",
    "notificacoes",
}

SERVICOS_SEED = {
    "Contabilidade",
    "Avaliações de Empresas (Valuation)",
    "Terceirização de Rotinas Financeiras (BPO)",
    "Diretoria Financeira Sob Demanda (CFO)",
    "Fusões & Aquisições (M&A)",
}

CARGOS_SEED = {
    "Compliance",
    "CEO",
    "Membro do Conselho",
    "CSO",
    "CMO",
    "CFO",
    "Analista de Valores Imobiliários",
    "Analista de BPO Financeiro",
}


def _novo_cargo(db_session: Session) -> int:
    cargo = Cargo(nome_cargo="Cargo de Teste")
    db_session.add(cargo)
    db_session.flush()
    return cargo.id_cargo


def test_todas_as_tabelas_existem() -> None:
    tabelas = set(inspect(engine).get_table_names())
    assert EXPECTED_TABLES <= tabelas


def test_servicos_seedados(db_session: Session) -> None:
    nomes = set(db_session.scalars(select(Servico.nome)).all())
    assert SERVICOS_SEED <= nomes


def test_cargos_seedados(db_session: Session) -> None:
    nomes = set(db_session.scalars(select(Cargo.nome_cargo)).all())
    assert CARGOS_SEED <= nomes


def test_cnpj_unico(db_session: Session) -> None:
    db_session.add(Empresa(razao_social="Alpha", cnpj="11.111.111/0001-11"))
    db_session.flush()
    db_session.add(Empresa(razao_social="Beta", cnpj="11.111.111/0001-11"))
    with pytest.raises(IntegrityError):
        db_session.flush()


def test_usuario_cpf_unico(db_session: Session) -> None:
    cargo_id = _novo_cargo(db_session)
    db_session.add(
        Usuario(
            nome_completo="A",
            cargo_id=cargo_id,
            cpf="12345678901",
            email="a@x.com",
            contato="1",
            senha_hash="h",
        )
    )
    db_session.flush()
    db_session.add(
        Usuario(
            nome_completo="B",
            cargo_id=cargo_id,
            cpf="12345678901",
            email="b@x.com",
            contato="1",
            senha_hash="h",
        )
    )
    with pytest.raises(IntegrityError):
        db_session.flush()


def test_usuario_email_unico(db_session: Session) -> None:
    cargo_id = _novo_cargo(db_session)
    db_session.add(
        Usuario(
            nome_completo="A",
            cargo_id=cargo_id,
            cpf="11111111111",
            email="dup@x.com",
            contato="1",
            senha_hash="h",
        )
    )
    db_session.flush()
    db_session.add(
        Usuario(
            nome_completo="B",
            cargo_id=cargo_id,
            cpf="22222222222",
            email="dup@x.com",
            contato="1",
            senha_hash="h",
        )
    )
    with pytest.raises(IntegrityError):
        db_session.flush()


def test_contrato_cascade_apaga_planilhas_e_relatorios(db_session: Session) -> None:
    cargo_id = _novo_cargo(db_session)
    empresa = Empresa(razao_social="C", cnpj="22.222.222/0001-22")
    usuario = Usuario(
        nome_completo="U",
        cargo_id=cargo_id,
        cpf="33333333333",
        email="u@x.com",
        contato="1",
        senha_hash="h",
    )
    db_session.add_all([empresa, usuario])
    db_session.flush()
    proposta = Proposta(empresa_id=empresa.id_empresa, usuario_id=usuario.id_usuario)
    db_session.add(proposta)
    db_session.flush()
    contrato = Contrato(proposta_id=proposta.id_proposta)
    db_session.add(contrato)
    db_session.flush()
    db_session.add_all(
        [
            Planilha(contrato_id=contrato.id_contrato),
            Relatorio(contrato_id=contrato.id_contrato),
        ]
    )
    db_session.flush()

    db_session.execute(delete(Contrato).where(Contrato.id_contrato == contrato.id_contrato))
    db_session.expire_all()

    planilhas = db_session.scalar(
        select(func.count())
        .select_from(Planilha)
        .where(Planilha.contrato_id == contrato.id_contrato)
    )
    relatorios = db_session.scalar(
        select(func.count())
        .select_from(Relatorio)
        .where(Relatorio.contrato_id == contrato.id_contrato)
    )
    assert planilhas == 0
    assert relatorios == 0


def test_cargo_em_uso_nao_pode_ser_apagado(db_session: Session) -> None:
    cargo_id = _novo_cargo(db_session)
    db_session.add(
        Usuario(
            nome_completo="U",
            cargo_id=cargo_id,
            cpf="44444444444",
            email="r@x.com",
            contato="1",
            senha_hash="h",
        )
    )
    db_session.flush()
    with pytest.raises(IntegrityError):
        db_session.execute(delete(Cargo).where(Cargo.id_cargo == cargo_id))


def test_apagar_empresa_anula_reuniao(db_session: Session) -> None:
    empresa = Empresa(razao_social="D", cnpj="33.333.333/0001-33")
    db_session.add(empresa)
    db_session.flush()
    reuniao = Reuniao(titulo="Kickoff", empresa_id=empresa.id_empresa)
    db_session.add(reuniao)
    db_session.flush()

    db_session.execute(delete(Empresa).where(Empresa.id_empresa == empresa.id_empresa))
    db_session.expire_all()

    atualizada = db_session.get(Reuniao, reuniao.id_reuniao)
    assert atualizada is not None
    assert atualizada.empresa_id is None
