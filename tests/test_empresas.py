from __future__ import annotations

from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Proposta, Servico
from tests.factories import auth_header, criar_empresa, criar_usuario

CNPJ_VALIDO = "11.222.333/0001-81"


def _servico_ids(db: Session, n: int = 2) -> list[int]:
    return list(db.scalars(select(Servico.id_servico)))[:n]


def _payload(servico_ids: list[int], **over: object) -> dict[str, object]:
    base: dict[str, object] = {
        "razao_social": "Acme",
        "cnpj": CNPJ_VALIDO,
        "servico_ids": servico_ids,
    }
    base.update(over)
    return base


def test_criar_empresa_staff(client_db: TestClient, db_session: Session) -> None:
    analista = criar_usuario(db_session, email="an@x.com", cpf="40000000002", papel="analista")
    sids = _servico_ids(db_session)
    r = client_db.post("/empresas", json=_payload(sids), headers=auth_header(analista))
    assert r.status_code == 201
    body = r.json()
    assert body["cnpj"] == "11222333000181"
    assert len(body["servicos"]) == len(sids)


def test_criar_empresa_contratante_proibido(client_db: TestClient, db_session: Session) -> None:
    contratante = criar_usuario(db_session, email="c@x.com", cpf="40000000003", papel="contratante")
    r = client_db.post("/empresas", json=_payload([]), headers=auth_header(contratante))
    assert r.status_code == 403


def test_criar_empresa_cnpj_invalido(client_db: TestClient, db_session: Session) -> None:
    admin = criar_usuario(db_session, email="ad@x.com", cpf="40000000004", papel="admin")
    r = client_db.post(
        "/empresas",
        json=_payload([], cnpj="11.222.333/0001-80"),
        headers=auth_header(admin),
    )
    assert r.status_code == 422
    assert r.json()["code"] == "CNPJ_INVALIDO"


def test_criar_empresa_cnpj_duplicado(client_db: TestClient, db_session: Session) -> None:
    admin = criar_usuario(db_session, email="ad@x.com", cpf="40000000005", papel="admin")
    criar_empresa(db_session, cnpj="11222333000181")
    r = client_db.post("/empresas", json=_payload([]), headers=auth_header(admin))
    assert r.status_code == 409
    assert r.json()["code"] == "EMPRESA_CNPJ_DUPLICADO"


def test_criar_empresa_servico_inexistente(client_db: TestClient, db_session: Session) -> None:
    admin = criar_usuario(db_session, email="ad@x.com", cpf="40000000006", papel="admin")
    r = client_db.post("/empresas", json=_payload([999999]), headers=auth_header(admin))
    assert r.status_code == 404
    assert r.json()["code"] == "SERVICO_NAO_ENCONTRADO"


def test_update_sincroniza_servicos(client_db: TestClient, db_session: Session) -> None:
    admin = criar_usuario(db_session, email="ad@x.com", cpf="40000000007", papel="admin")
    sids = _servico_ids(db_session, 3)
    criado = client_db.post("/empresas", json=_payload(sids[:2]), headers=auth_header(admin))
    id_empresa = criado.json()["id_empresa"]
    atualizado = client_db.patch(
        f"/empresas/{id_empresa}",
        json={"servico_ids": [sids[0], sids[2]]},
        headers=auth_header(admin),
    )
    assert atualizado.status_code == 200
    retornados = {s["id_servico"] for s in atualizado.json()["servicos"]}
    assert retornados == {sids[0], sids[2]}


def test_deletar_empresa_ok(client_db: TestClient, db_session: Session) -> None:
    admin = criar_usuario(db_session, email="ad@x.com", cpf="40000000008", papel="admin")
    criado = client_db.post(
        "/empresas", json=_payload(_servico_ids(db_session)), headers=auth_header(admin)
    )
    id_empresa = criado.json()["id_empresa"]
    r = client_db.delete(f"/empresas/{id_empresa}", headers=auth_header(admin))
    assert r.status_code == 204


def test_deletar_empresa_com_proposta(client_db: TestClient, db_session: Session) -> None:
    admin = criar_usuario(db_session, email="ad@x.com", cpf="40000000009", papel="admin")
    empresa = criar_empresa(db_session, cnpj="99888777000166")
    db_session.add(Proposta(empresa_id=empresa.id_empresa, usuario_id=admin.id_usuario))
    db_session.flush()
    r = client_db.delete(f"/empresas/{empresa.id_empresa}", headers=auth_header(admin))
    assert r.status_code == 409
    assert r.json()["code"] == "EMPRESA_COM_VINCULOS"
