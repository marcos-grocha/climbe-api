# Design — Bootstrap API

## Decisões técnicas

### 1. SQLAlchemy 2.0 — estilo declarativo moderno

Usar `DeclarativeBase` + `Mapped[]` + `mapped_column()` em vez do estilo legado. Mais tipo-seguro e a maneira recomendada no SQLAlchemy 2.x.

```python
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass
```

### 2. Driver: psycopg 3 (não psycopg2)

`psycopg` v3 é o driver moderno do projeto Psycopg, mais rápido e ativamente mantido. URL: `postgresql+psycopg://...`.

### 3. Settings via pydantic-settings

Única fonte: `app.config.settings`. Qualquer módulo importa de lá; o `.env` é lido uma vez (com `lru_cache`).

```python
from app.config import settings
```

### 4. Health check em dois níveis

- `GET /health` — só responde se a app está de pé. **Não toca o banco.**
- `GET /health/db` — testa `SELECT 1` no banco.

Separa liveness (app respondendo) de readiness (banco funcionando). Útil em deploy.

### 5. CORS via env var

Variável `ALLOWED_ORIGINS` (lista separada por vírgula) parseada via `field_validator`. Default inclui `http://localhost:5173` (Vite do frontend).

### 6. Alembic com env.py customizado

`env.py` importa `Base` de `app.database` e `settings` de `app.config` para usar `DATABASE_URL`. Evita duplicação de config.

## Estrutura de pastas a criar

```
app/
├── __init__.py
├── main.py
├── config.py
├── database.py
├── models/__init__.py
├── schemas/__init__.py
├── routers/
│   ├── __init__.py
│   └── health.py
├── services/__init__.py
└── dependencies/__init__.py

alembic/
├── env.py
├── script.py.mako
└── versions/.gitkeep

tests/
├── __init__.py
├── conftest.py
└── test_health.py

pyproject.toml
alembic.ini
```

## Trade-offs

| Decisão | Trade-off |
|---|---|
| psycopg 3 em vez de psycopg2 | Menos material em PT, mas é o futuro; tutoriais ≥2024 cobrem |
| SQLAlchemy 2.x estilo novo | Equipe (solo) precisa estudar; ganho em segurança de tipo |
| Health check separado p/ DB | +1 endpoint, mas separa "API viva" de "banco vivo" |
| Sync em vez de async | Mais simples no começo; pode migrar pra async quando integrar Google APIs |
| Sem testes de integração ainda | Só TestClient + DB mockado/in-memory? Decidir na próxima proposta |
