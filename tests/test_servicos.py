from __future__ import annotations

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tests.factories import auth_header, criar_usuario


def test_listar_servicos(client_db: TestClient, db_session: Session) -> None:
    usuario = criar_usuario(db_session, email="serv@x.com", cpf="40000000001")
    r = client_db.get("/servicos", headers=auth_header(usuario))
    assert r.status_code == 200
    assert len(r.json()) == 5
