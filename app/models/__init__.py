"""Models SQLAlchemy do domínio Climbe.

Importar este pacote registra todas as entidades em `Base.metadata`
(necessário para o autogenerate do Alembic e para o ORM).
"""

from __future__ import annotations

from app.models.cargo import Cargo
from app.models.contrato import Contrato
from app.models.documento import Documento
from app.models.empresa import Empresa
from app.models.notificacao import Notificacao
from app.models.permissao import Permissao, UsuarioPermissao
from app.models.planilha import Planilha
from app.models.proposta import Proposta
from app.models.relatorio import Relatorio
from app.models.reuniao import ParticipanteReuniao, Reuniao
from app.models.servico import EmpresaServico, Servico
from app.models.usuario import Usuario

__all__ = [
    "Cargo",
    "Contrato",
    "Documento",
    "Empresa",
    "EmpresaServico",
    "Notificacao",
    "ParticipanteReuniao",
    "Permissao",
    "Planilha",
    "Proposta",
    "Relatorio",
    "Reuniao",
    "Servico",
    "Usuario",
    "UsuarioPermissao",
]
