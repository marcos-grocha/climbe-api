from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.exceptions import (
    CpfDuplicadoError,
    EmailDuplicadoError,
    SenhaAtualIncorretaError,
    UsuarioNaoEncontradoError,
)
from app.models import Usuario
from app.schemas.usuario import TrocarSenha, UsuarioCreate, UsuarioUpdate
from app.services.cargo_service import obter_cargo
from app.utils.security import hash_password, verify_password
from app.utils.validators import validar_cpf


def listar_usuarios(db: Session) -> list[Usuario]:
    return list(db.scalars(select(Usuario).order_by(Usuario.id_usuario)))


def obter_usuario(db: Session, id_usuario: int) -> Usuario:
    usuario = db.get(Usuario, id_usuario)
    if usuario is None:
        raise UsuarioNaoEncontradoError
    return usuario


def criar_usuario(db: Session, dados: UsuarioCreate) -> Usuario:
    cpf = validar_cpf(dados.cpf)
    obter_cargo(db, dados.cargo_id)
    if db.scalar(select(Usuario).where(Usuario.email == dados.email)):
        raise EmailDuplicadoError
    if db.scalar(select(Usuario).where(Usuario.cpf == cpf)):
        raise CpfDuplicadoError
    usuario = Usuario(
        nome_completo=dados.nome_completo,
        cargo_id=dados.cargo_id,
        cpf=cpf,
        email=str(dados.email),
        contato=dados.contato,
        papel=dados.papel,
        senha_hash=hash_password(dados.senha),
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


def atualizar_usuario(db: Session, id_usuario: int, dados: UsuarioUpdate) -> Usuario:
    usuario = obter_usuario(db, id_usuario)
    if dados.cargo_id is not None:
        obter_cargo(db, dados.cargo_id)
        usuario.cargo_id = dados.cargo_id
    if dados.nome_completo is not None:
        usuario.nome_completo = dados.nome_completo
    if dados.contato is not None:
        usuario.contato = dados.contato
    if dados.papel is not None:
        usuario.papel = dados.papel
    if dados.situacao is not None:
        usuario.situacao = dados.situacao
    db.commit()
    db.refresh(usuario)
    return usuario


def desativar_usuario(db: Session, id_usuario: int) -> None:
    usuario = obter_usuario(db, id_usuario)
    usuario.situacao = "inativo"
    db.commit()


def trocar_senha(db: Session, usuario: Usuario, dados: TrocarSenha) -> None:
    if not verify_password(dados.senha_atual, usuario.senha_hash):
        raise SenhaAtualIncorretaError
    usuario.senha_hash = hash_password(dados.nova_senha)
    db.commit()
