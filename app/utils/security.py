from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

import bcrypt
from jose import jwt

from app.config import settings

# bcrypt usa no máximo 72 bytes da senha; truncamos para não estourar com senhas longas.
_MAX_BCRYPT_BYTES = 72


def _to_bytes(senha: str) -> bytes:
    return senha.encode("utf-8")[:_MAX_BCRYPT_BYTES]


def hash_password(senha: str) -> str:
    return bcrypt.hashpw(_to_bytes(senha), bcrypt.gensalt()).decode("utf-8")


def verify_password(senha: str, senha_hash: str) -> bool:
    return bcrypt.checkpw(_to_bytes(senha), senha_hash.encode("utf-8"))


def create_access_token(sub: str, papel: str) -> str:
    expira = datetime.now(UTC) + timedelta(minutes=settings.jwt_expire_minutes)
    payload = {"sub": sub, "papel": papel, "exp": expira}
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> dict[str, Any]:
    return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
