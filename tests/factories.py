from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Cargo, Usuario
from app.utils.security import create_access_token, hash_password


def criar_usuario(
    db: Session,
    *,
    email: str,
    cpf: str,
    papel: str = "analista",
    situacao: str = "ativo",
    senha: str = "segredo123",
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


def auth_header(usuario: Usuario) -> dict[str, str]:
    token = create_access_token(sub=str(usuario.id_usuario), papel=usuario.papel)
    return {"Authorization": f"Bearer {token}"}
