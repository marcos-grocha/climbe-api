from __future__ import annotations

from collections.abc import Callable
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.database import get_db
from app.exceptions import SemPermissaoError, TokenInvalidoError, UsuarioInativoError
from app.models import Usuario
from app.schemas.auth import TokenPayload
from app.utils.security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login", auto_error=False)


def get_current_user(
    token: Annotated[str | None, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
) -> Usuario:
    if not token:
        raise TokenInvalidoError
    try:
        payload = decode_access_token(token)
    except JWTError:
        raise TokenInvalidoError from None
    dados = TokenPayload(**payload)
    if dados.sub is None or not dados.sub.isdigit():
        raise TokenInvalidoError
    usuario = db.get(Usuario, int(dados.sub))
    if usuario is None:
        raise TokenInvalidoError
    if usuario.situacao != "ativo":
        raise UsuarioInativoError
    return usuario


def require_role(papeis: list[str]) -> Callable[[Usuario], Usuario]:
    """Dependency factory: restringe o acesso aos `papeis` informados."""

    def _checar(usuario: Annotated[Usuario, Depends(get_current_user)]) -> Usuario:
        if usuario.papel not in papeis:
            raise SemPermissaoError
        return usuario

    return _checar
