from __future__ import annotations

from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from app.config import settings
from app.database import Base

# Quando houver models (proposta models-base), importe-os aqui para que o
# autogenerate detecte as tabelas, por exemplo: ``from app import models``.

# Objeto Config do Alembic — dá acesso aos valores do alembic.ini.
config = context.config

# Usa a mesma DATABASE_URL da aplicação, sem duplicar configuração.
config.set_main_option("sqlalchemy.url", settings.database_url)

# Configura o logging do Python a partir do .ini.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata-alvo para o --autogenerate.
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Roda migrations em modo offline (apenas com a URL, sem Engine)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Roda migrations em modo online (cria Engine e associa uma conexão)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
