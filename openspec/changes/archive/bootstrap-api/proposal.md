# Proposal: Bootstrap API

## Intent

Estabelecer a base mínima da API: aplicação FastAPI rodando, conexão com PostgreSQL via SQLAlchemy + Alembic configurado, health check e estrutura de pastas conforme `AGENTS.md`. Esta proposta entrega o esqueleto sobre o qual as próximas capabilities (auth, usuários, empresas etc.) serão construídas.

Sem essa fundação não conseguimos iniciar o trabalho de domínio. Sem Alembic configurado, qualquer model novo vira problema. Sem health check, não dá pra validar que a infra está OK durante deploy.

## Scope

- Estrutura de pastas `app/` conforme `AGENTS.md`
- Aplicação FastAPI mínima com `/health` (sem DB) e `/health/db` (com DB)
- Configuração via `pydantic-settings` lendo do `.env`
- Conexão com PostgreSQL via SQLAlchemy 2.x (engine + session + `Base`)
- Alembic configurado (sem migrations ainda — primeira migration virá em uma proposta de modelos)
- CORS configurado para o frontend (`http://localhost:5173`)
- Testes básicos dos endpoints de health
- Ruff configurado para lint/format

## Approach

Estrutura modular separando `routers/`, `models/`, `schemas/`, `services/`, `dependencies/`. Settings centralizadas em `app/config.py` usando `pydantic-settings`. Engine SQLAlchemy criado uma vez em `app/database.py` e exposto via dependency `get_db()` que cuida do ciclo de vida da sessão.

Alembic configurado com `env.py` lendo `Base.metadata` para `--autogenerate` funcionar quando models forem adicionados. Migrations vivem em `alembic/versions/`.

Testes com `TestClient` do FastAPI (síncrono) para garantir que tudo sobe e responde.

**Fora do escopo desta proposta**: autenticação, models de domínio, qualquer endpoint além de health.
