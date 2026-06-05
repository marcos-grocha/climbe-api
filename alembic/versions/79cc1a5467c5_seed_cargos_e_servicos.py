"""seed cargos e servicos

Revision ID: 79cc1a5467c5
Revises: 8213fa4c3b5f
Create Date: 2026-06-04 22:13:29.249423

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "79cc1a5467c5"
down_revision: str | Sequence[str] | None = "8213fa4c3b5f"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

# Cargos formais da Climbe (req. de domínio 1 do Documento de Requisitos v1.1).
CARGOS = [
    "Compliance",
    "CEO",
    "Membro do Conselho",
    "CSO",
    "CMO",
    "CFO",
    "Analista de Valores Imobiliários",
    "Analista de BPO Financeiro",
]

# Serviços oferecidos pela Climbe (req. de domínio 2).
SERVICOS = [
    "Contabilidade",
    "Avaliações de Empresas (Valuation)",
    "Terceirização de Rotinas Financeiras (BPO)",
    "Diretoria Financeira Sob Demanda (CFO)",
    "Fusões & Aquisições (M&A)",
]


def upgrade() -> None:
    """Insere os cargos e serviços iniciais (created_at/updated_at via server_default)."""
    cargos = sa.table("cargos", sa.column("nome_cargo", sa.String))
    servicos = sa.table("servicos", sa.column("nome", sa.String))
    op.bulk_insert(cargos, [{"nome_cargo": nome} for nome in CARGOS])
    op.bulk_insert(servicos, [{"nome": nome} for nome in SERVICOS])


def downgrade() -> None:
    """Remove os cargos e serviços iniciais."""
    cargos = sa.table("cargos", sa.column("nome_cargo", sa.String))
    servicos = sa.table("servicos", sa.column("nome", sa.String))
    op.execute(cargos.delete().where(cargos.c.nome_cargo.in_(CARGOS)))
    op.execute(servicos.delete().where(servicos.c.nome.in_(SERVICOS)))
