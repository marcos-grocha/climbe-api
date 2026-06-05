from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.exceptions import CredenciaisInvalidasError, UsuarioInativoError
from app.models import Usuario
from app.schemas.auth import Token, UsuarioMe
from app.utils.security import create_access_token, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
def login(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
) -> Token:
    usuario = db.scalar(select(Usuario).where(Usuario.email == form.username))
    if usuario is None or not verify_password(form.password, usuario.senha_hash):
        raise CredenciaisInvalidasError
    if usuario.situacao != "ativo":
        raise UsuarioInativoError
    token = create_access_token(sub=str(usuario.id_usuario), papel=usuario.papel)
    return Token(access_token=token)


@router.get("/me", response_model=UsuarioMe)
def me(usuario: Annotated[Usuario, Depends(get_current_user)]) -> Usuario:
    return usuario
