from __future__ import annotations

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tests.factories import auth_header, criar_usuario

CPF_VALIDO = "529.982.247-25"


def _payload(**over: object) -> dict[str, object]:
    base: dict[str, object] = {
        "nome_completo": "Novo",
        "cpf": CPF_VALIDO,
        "email": "novo@x.com",
        "contato": "9999",
        "papel": "analista",
        "senha": "senha123",
    }
    base.update(over)
    return base


def test_criar_usuario_admin(client_db: TestClient, db_session: Session) -> None:
    admin = criar_usuario(db_session, email="ad@x.com", cpf="30000000001", papel="admin")
    r = client_db.post(
        "/usuarios", json=_payload(cargo_id=admin.cargo_id), headers=auth_header(admin)
    )
    assert r.status_code == 201
    body = r.json()
    assert body["email"] == "novo@x.com"
    assert body["cpf"] == "52998224725"
    assert "senha_hash" not in body


def test_criar_usuario_nao_admin_proibido(client_db: TestClient, db_session: Session) -> None:
    usuario = criar_usuario(db_session, email="u@x.com", cpf="30000000002", papel="analista")
    r = client_db.post(
        "/usuarios", json=_payload(cargo_id=usuario.cargo_id), headers=auth_header(usuario)
    )
    assert r.status_code == 403


def test_criar_usuario_cpf_invalido(client_db: TestClient, db_session: Session) -> None:
    admin = criar_usuario(db_session, email="ad@x.com", cpf="30000000003", papel="admin")
    r = client_db.post(
        "/usuarios",
        json=_payload(cargo_id=admin.cargo_id, cpf="111.111.111-11"),
        headers=auth_header(admin),
    )
    assert r.status_code == 422
    assert r.json()["code"] == "CPF_INVALIDO"


def test_criar_usuario_email_duplicado(client_db: TestClient, db_session: Session) -> None:
    admin = criar_usuario(db_session, email="ad@x.com", cpf="30000000004", papel="admin")
    criar_usuario(db_session, email="dup@x.com", cpf="30000000005")
    r = client_db.post(
        "/usuarios",
        json=_payload(cargo_id=admin.cargo_id, email="dup@x.com"),
        headers=auth_header(admin),
    )
    assert r.status_code == 409
    assert r.json()["code"] == "USUARIO_EMAIL_DUPLICADO"


def test_soft_delete_e_login_falha(client_db: TestClient, db_session: Session) -> None:
    admin = criar_usuario(db_session, email="ad@x.com", cpf="30000000006", papel="admin")
    alvo = criar_usuario(db_session, email="alvo@x.com", cpf="30000000007", senha="segredo")
    r = client_db.delete(f"/usuarios/{alvo.id_usuario}", headers=auth_header(admin))
    assert r.status_code == 204
    detalhe = client_db.get(f"/usuarios/{alvo.id_usuario}", headers=auth_header(admin))
    assert detalhe.json()["situacao"] == "inativo"
    login = client_db.post("/auth/login", data={"username": "alvo@x.com", "password": "segredo"})
    assert login.status_code == 401


def test_trocar_senha_ok(client_db: TestClient, db_session: Session) -> None:
    usuario = criar_usuario(db_session, email="t@x.com", cpf="30000000008", senha="antiga123")
    r = client_db.post(
        "/usuarios/me/senha",
        json={"senha_atual": "antiga123", "nova_senha": "novasenha1"},
        headers=auth_header(usuario),
    )
    assert r.status_code == 200
    login = client_db.post("/auth/login", data={"username": "t@x.com", "password": "novasenha1"})
    assert login.status_code == 200


def test_trocar_senha_atual_errada(client_db: TestClient, db_session: Session) -> None:
    usuario = criar_usuario(db_session, email="t2@x.com", cpf="30000000009", senha="antiga123")
    r = client_db.post(
        "/usuarios/me/senha",
        json={"senha_atual": "errada", "nova_senha": "novasenha1"},
        headers=auth_header(usuario),
    )
    assert r.status_code == 400
    assert r.json()["code"] == "SENHA_ATUAL_INCORRETA"
