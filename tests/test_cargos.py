from __future__ import annotations

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tests.factories import auth_header, criar_usuario


def test_listar_cargos(client_db: TestClient, db_session: Session) -> None:
    usuario = criar_usuario(db_session, email="a@x.com", cpf="20000000001")
    r = client_db.get("/cargos", headers=auth_header(usuario))
    assert r.status_code == 200
    assert len(r.json()) >= 8


def test_criar_cargo_admin(client_db: TestClient, db_session: Session) -> None:
    admin = criar_usuario(db_session, email="ad@x.com", cpf="20000000002", papel="admin")
    r = client_db.post("/cargos", json={"nome_cargo": "Estagiário"}, headers=auth_header(admin))
    assert r.status_code == 201
    assert r.json()["nome_cargo"] == "Estagiário"


def test_criar_cargo_nao_admin_proibido(client_db: TestClient, db_session: Session) -> None:
    usuario = criar_usuario(db_session, email="u@x.com", cpf="20000000003", papel="analista")
    r = client_db.post("/cargos", json={"nome_cargo": "X"}, headers=auth_header(usuario))
    assert r.status_code == 403
    assert r.json()["code"] == "AUTH_SEM_PERMISSAO"


def test_deletar_cargo_em_uso(client_db: TestClient, db_session: Session) -> None:
    admin = criar_usuario(db_session, email="ad2@x.com", cpf="20000000004", papel="admin")
    r = client_db.delete(f"/cargos/{admin.cargo_id}", headers=auth_header(admin))
    assert r.status_code == 409
    assert r.json()["code"] == "CARGO_EM_USO"
