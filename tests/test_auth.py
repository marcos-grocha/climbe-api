from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import settings
from app.dependencies.auth import require_role
from app.exceptions import SemPermissaoError
from app.models import Cargo, Usuario
from app.utils.security import create_access_token, hash_password


def _criar_usuario(
    db: Session,
    *,
    email: str,
    cpf: str,
    senha: str = "segredo123",
    papel: str = "analista",
    situacao: str = "ativo",
) -> Usuario:
    cargo_id = db.scalar(select(Cargo.id_cargo))
    usuario = Usuario(
        nome_completo="Usuário Teste",
        cargo_id=cargo_id,
        cpf=cpf,
        email=email,
        contato="-",
        senha_hash=hash_password(senha),
        papel=papel,
        situacao=situacao,
    )
    db.add(usuario)
    db.flush()
    return usuario


def test_login_ok(client_db: TestClient, db_session: Session) -> None:
    _criar_usuario(db_session, email="a@x.com", cpf="10000000001", senha="segredo")
    r = client_db.post("/auth/login", data={"username": "a@x.com", "password": "segredo"})
    assert r.status_code == 200
    body = r.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]


def test_login_senha_errada(client_db: TestClient, db_session: Session) -> None:
    _criar_usuario(db_session, email="b@x.com", cpf="10000000002", senha="segredo")
    r = client_db.post("/auth/login", data={"username": "b@x.com", "password": "errado"})
    assert r.status_code == 401
    assert r.json()["code"] == "AUTH_CREDENCIAIS_INVALIDAS"


def test_me_com_token(client_db: TestClient, db_session: Session) -> None:
    usuario = _criar_usuario(db_session, email="c@x.com", cpf="10000000003", papel="admin")
    token = create_access_token(sub=str(usuario.id_usuario), papel=usuario.papel)
    r = client_db.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    body = r.json()
    assert body["email"] == "c@x.com"
    assert body["papel"] == "admin"


def test_me_sem_token(client_db: TestClient) -> None:
    r = client_db.get("/auth/me")
    assert r.status_code == 401
    assert r.json()["code"] == "AUTH_TOKEN_INVALIDO"


def test_me_token_invalido(client_db: TestClient) -> None:
    r = client_db.get("/auth/me", headers={"Authorization": "Bearer abc.def.ghi"})
    assert r.status_code == 401
    assert r.json()["code"] == "AUTH_TOKEN_INVALIDO"


def test_usuario_inativo_bloqueado(client_db: TestClient, db_session: Session) -> None:
    usuario = _criar_usuario(db_session, email="d@x.com", cpf="10000000004", situacao="inativo")
    token = create_access_token(sub=str(usuario.id_usuario), papel=usuario.papel)
    r = client_db.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 401
    assert r.json()["code"] == "AUTH_USUARIO_INATIVO"


def test_require_role_permite(db_session: Session) -> None:
    usuario = _criar_usuario(db_session, email="e@x.com", cpf="10000000005", papel="admin")
    checar = require_role(["admin"])
    assert checar(usuario) is usuario


def test_require_role_nega(db_session: Session) -> None:
    usuario = _criar_usuario(db_session, email="f@x.com", cpf="10000000006", papel="contratante")
    checar = require_role(["admin"])
    with pytest.raises(SemPermissaoError):
        checar(usuario)


def test_admin_seedado_loga(client: TestClient) -> None:
    r = client.post(
        "/auth/login",
        data={"username": settings.admin_email, "password": settings.admin_password},
    )
    assert r.status_code == 200
    assert r.json()["access_token"]
