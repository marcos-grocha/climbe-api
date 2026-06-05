"""seed admin inicial

Revision ID: 8b43ce22276b
Revises: a6703fd1b5bf
Create Date: 2026-06-05 00:11:00.424626

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

from app.config import settings
from app.utils.security import hash_password

# revision identifiers, used by Alembic.
revision: str = "8b43ce22276b"
down_revision: str | Sequence[str] | None = "a6703fd1b5bf"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Cria o usuário admin inicial (papel=admin), se ainda não existir."""
    bind = op.get_bind()
    ja_existe = bind.execute(
        sa.text("SELECT 1 FROM usuarios WHERE email = :email"),
        {"email": settings.admin_email},
    ).scalar()
    if ja_existe:
        return

    cargo_id = bind.execute(
        sa.text("SELECT id_cargo FROM cargos WHERE nome_cargo = 'Compliance' LIMIT 1")
    ).scalar()
    if cargo_id is None:
        cargo_id = bind.execute(
            sa.text("SELECT id_cargo FROM cargos ORDER BY id_cargo LIMIT 1")
        ).scalar()
    if cargo_id is None:
        raise RuntimeError("Nenhum cargo encontrado; rode o seed de cargos antes.")

    bind.execute(
        sa.text(
            "INSERT INTO usuarios "
            "(nome_completo, cargo_id, cpf, email, contato, situacao, papel, senha_hash) "
            "VALUES (:nome, :cargo_id, :cpf, :email, :contato, 'ativo', 'admin', :senha_hash)"
        ),
        {
            "nome": "Administrador",
            "cargo_id": cargo_id,
            "cpf": "00000000000",
            "email": settings.admin_email,
            "contato": "-",
            "senha_hash": hash_password(settings.admin_password),
        },
    )


def downgrade() -> None:
    """Remove o admin inicial."""
    bind = op.get_bind()
    bind.execute(
        sa.text("DELETE FROM usuarios WHERE email = :email"),
        {"email": settings.admin_email},
    )
