from __future__ import annotations

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models import Contrato, Proposta
from tests.factories import auth_header, criar_empresa, criar_usuario


def _criar_proposta_api(client: TestClient, admin, empresa_id: int) -> int:
    r = client.post("/propostas", json={"empresa_id": empresa_id}, headers=auth_header(admin))
    assert r.status_code == 201
    return r.json()["id_proposta"]


def test_criar_proposta_staff(client_db: TestClient, db_session: Session) -> None:
    analista = criar_usuario(db_session, email="an@x.com", cpf="50000000001", papel="analista")
    empresa = criar_empresa(db_session, cnpj="50000000000001")
    r = client_db.post(
        "/propostas", json={"empresa_id": empresa.id_empresa}, headers=auth_header(analista)
    )
    assert r.status_code == 201
    body = r.json()
    assert body["status"] == "rascunho"
    assert body["usuario_id"] == analista.id_usuario
    assert body["empresa_id"] == empresa.id_empresa


def test_criar_proposta_contratante_proibido(client_db: TestClient, db_session: Session) -> None:
    contratante = criar_usuario(db_session, email="c@x.com", cpf="50000000002", papel="contratante")
    empresa = criar_empresa(db_session, cnpj="50000000000002")
    r = client_db.post(
        "/propostas", json={"empresa_id": empresa.id_empresa}, headers=auth_header(contratante)
    )
    assert r.status_code == 403


def test_criar_proposta_empresa_inexistente(client_db: TestClient, db_session: Session) -> None:
    admin = criar_usuario(db_session, email="ad@x.com", cpf="50000000003", papel="admin")
    r = client_db.post("/propostas", json={"empresa_id": 999999}, headers=auth_header(admin))
    assert r.status_code == 404
    assert r.json()["code"] == "EMPRESA_NAO_ENCONTRADA"


def test_fluxo_enviar_aprovar(client_db: TestClient, db_session: Session) -> None:
    admin = criar_usuario(db_session, email="ad@x.com", cpf="50000000004", papel="admin")
    empresa = criar_empresa(db_session, cnpj="50000000000004")
    pid = _criar_proposta_api(client_db, admin, empresa.id_empresa)
    enviar = client_db.post(f"/propostas/{pid}/enviar", headers=auth_header(admin))
    assert enviar.json()["status"] == "enviada"
    aprovar = client_db.post(f"/propostas/{pid}/aprovar", headers=auth_header(admin))
    assert aprovar.status_code == 200
    assert aprovar.json()["status"] == "aprovada"


def test_fluxo_enviar_recusar(client_db: TestClient, db_session: Session) -> None:
    admin = criar_usuario(db_session, email="ad@x.com", cpf="50000000005", papel="admin")
    empresa = criar_empresa(db_session, cnpj="50000000000005")
    pid = _criar_proposta_api(client_db, admin, empresa.id_empresa)
    client_db.post(f"/propostas/{pid}/enviar", headers=auth_header(admin))
    recusar = client_db.post(f"/propostas/{pid}/recusar", headers=auth_header(admin))
    assert recusar.json()["status"] == "recusada"


def test_transicao_invalida(client_db: TestClient, db_session: Session) -> None:
    admin = criar_usuario(db_session, email="ad@x.com", cpf="50000000006", papel="admin")
    empresa = criar_empresa(db_session, cnpj="50000000000006")
    pid = _criar_proposta_api(client_db, admin, empresa.id_empresa)
    r = client_db.post(f"/propostas/{pid}/aprovar", headers=auth_header(admin))
    assert r.status_code == 409
    assert r.json()["code"] == "PROPOSTA_TRANSICAO_INVALIDA"


def test_deletar_proposta_ok(client_db: TestClient, db_session: Session) -> None:
    admin = criar_usuario(db_session, email="ad@x.com", cpf="50000000007", papel="admin")
    empresa = criar_empresa(db_session, cnpj="50000000000007")
    pid = _criar_proposta_api(client_db, admin, empresa.id_empresa)
    r = client_db.delete(f"/propostas/{pid}", headers=auth_header(admin))
    assert r.status_code == 204


def test_deletar_proposta_com_contrato(client_db: TestClient, db_session: Session) -> None:
    admin = criar_usuario(db_session, email="ad@x.com", cpf="50000000008", papel="admin")
    empresa = criar_empresa(db_session, cnpj="50000000000008")
    proposta = Proposta(empresa_id=empresa.id_empresa, usuario_id=admin.id_usuario)
    db_session.add(proposta)
    db_session.flush()
    db_session.add(Contrato(proposta_id=proposta.id_proposta))
    db_session.flush()
    r = client_db.delete(f"/propostas/{proposta.id_proposta}", headers=auth_header(admin))
    assert r.status_code == 409
    assert r.json()["code"] == "PROPOSTA_COM_CONTRATO"
