from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user, require_role
from app.models import Usuario
from app.schemas.usuario import TrocarSenha, UsuarioCreate, UsuarioResponse, UsuarioUpdate
from app.services import usuario_service

router = APIRouter(prefix="/usuarios", tags=["usuarios"])
_admin = Depends(require_role(["admin"]))


@router.post("/me/senha", status_code=status.HTTP_200_OK)
def trocar_minha_senha(
    dados: TrocarSenha,
    db: Annotated[Session, Depends(get_db)],
    usuario: Annotated[Usuario, Depends(get_current_user)],
) -> dict[str, str]:
    usuario_service.trocar_senha(db, usuario, dados)
    return {"status": "ok"}


@router.get("", response_model=list[UsuarioResponse], dependencies=[_admin])
def listar(db: Annotated[Session, Depends(get_db)]) -> list[Usuario]:
    return usuario_service.listar_usuarios(db)


@router.get("/{id_usuario}", response_model=UsuarioResponse, dependencies=[_admin])
def obter(id_usuario: int, db: Annotated[Session, Depends(get_db)]) -> Usuario:
    return usuario_service.obter_usuario(db, id_usuario)


@router.post(
    "",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[_admin],
)
def criar(dados: UsuarioCreate, db: Annotated[Session, Depends(get_db)]) -> Usuario:
    return usuario_service.criar_usuario(db, dados)


@router.patch("/{id_usuario}", response_model=UsuarioResponse, dependencies=[_admin])
def atualizar(
    id_usuario: int, dados: UsuarioUpdate, db: Annotated[Session, Depends(get_db)]
) -> Usuario:
    return usuario_service.atualizar_usuario(db, id_usuario, dados)


@router.delete("/{id_usuario}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[_admin])
def remover(id_usuario: int, db: Annotated[Session, Depends(get_db)]) -> None:
    usuario_service.desativar_usuario(db, id_usuario)
