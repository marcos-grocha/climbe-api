from __future__ import annotations

from datetime import date

from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Contrato, Usuario
from tests.factories import auth_header, criar_empresa, criar_usuario


def _criar_contrato(
    client: TestClient, db_session: Session, admin: Usuario, *, cnpj: str
) -> Contrato:
    empresa = criar_empresa(db_session, cnpj=cnpj)
    pid = client.post(
        "/propostas", json={"empresa_id": empresa.id_empresa}, headers=auth_header(admin)
    ).json()["id_proposta"]
    client.post(f"/propostas/{pid}/enviar", headers=auth_header(admin))
    client.post(f"/propostas/{pid}/aprovar", headers=auth_header(admin))
    db_session.expire_all()
    contrato = db_session.scalar(select(Contrato).where(Contrato.proposta_id == pid))
    assert contrato is not None
    return contrato


def test_aprovar_proposta_cria_contrato(client_db: TestClient, db_session: Session) -> None:
    admin = criar_usuario(db_session, email="ad@x.com", cpf="60000000001", papel="admin")
    contrato = _criar_contrato(client_db, db_session, admin, cnpj="60000000000001")
    assert contrato.status == "ativo"
    assert contrato.data_inicio == date.today()
    assert contrato.recorrente is False
    assert contrato.prazo_entrega is None


def test_listar_contratos(client_db: TestClient, db_session: Session) -> None:
    admin = criar_usuario(db_session, email="ad@x.com", cpf="60000000002", papel="admin")
    _criar_contrato(client_db, db_session, admin, cnpj="60000000000002")
    r = client_db.get("/contratos", headers=auth_header(admin))
    assert r.status_code == 200
    assert len(r.json()) >= 1


def test_patch_contrato(client_db: TestClient, db_session: Session) -> None:
    admin = criar_usuario(db_session, email="ad@x.com", cpf="60000000003", papel="admin")
    contrato = _criar_contrato(client_db, db_session, admin, cnpj="60000000000003")
    r = client_db.patch(
        f"/contratos/{contrato.id_contrato}",
        json={"prazo_entrega": "2026-12-31", "recorrente": True},
        headers=auth_header(admin),
    )
    assert r.status_code == 200
    body = r.json()
    assert body["prazo_entrega"] == "2026-12-31"
    assert body["recorrente"] is True


def test_encerrar_contrato(client_db: TestClient, db_session: Session) -> None:
    admin = criar_usuario(db_session, email="ad@x.com", cpf="60000000004", papel="admin")
    contrato = _criar_contrato(client_db, db_session, admin, cnpj="60000000000004")
    r = client_db.post(f"/contratos/{contrato.id_contrato}/encerrar", headers=auth_header(admin))
    assert r.status_code == 200
    assert r.json()["status"] == "encerrado"
    r2 = client_db.post(f"/contratos/{contrato.id_contrato}/encerrar", headers=auth_header(admin))
    assert r2.status_code == 409
    assert r2.json()["code"] == "CONTRATO_TRANSICAO_INVALIDA"
