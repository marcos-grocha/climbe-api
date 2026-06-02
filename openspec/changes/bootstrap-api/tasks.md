# Tasks — Bootstrap API

## 1. Estrutura de pastas
- [ ] 1.1 Criar `app/` e subpastas (`models`, `schemas`, `routers`, `services`, `dependencies`)
- [ ] 1.2 Adicionar `__init__.py` vazios em todas
- [ ] 1.3 Criar `alembic/` e `tests/`

## 2. Configuração base
- [ ] 2.1 Criar `app/config.py` com classe `Settings(BaseSettings)`
- [ ] 2.2 Carregar do `.env` via `SettingsConfigDict(env_file=".env")`
- [ ] 2.3 Adicionar `field_validator` para `ALLOWED_ORIGINS` (string CSV → list)
- [ ] 2.4 Expor `settings` como singleton (`@lru_cache`)

## 3. Database
- [ ] 3.1 Criar `app/database.py` com `engine`, `SessionLocal`, `Base`, `get_db`
- [ ] 3.2 Usar `settings.database_url`
- [ ] 3.3 Configurar `echo=settings.debug`
- [ ] 3.4 `Base` herda de `DeclarativeBase`

## 4. Aplicação FastAPI
- [ ] 4.1 Criar `app/main.py` com app FastAPI (`title="Climbe API"`)
- [ ] 4.2 Configurar `CORSMiddleware` com `settings.allowed_origins`
- [ ] 4.3 Incluir router de health

## 5. Health endpoints
- [ ] 5.1 Criar `app/routers/health.py` com `APIRouter(prefix="/health", tags=["health"])`
- [ ] 5.2 `GET /health` retorna `{"status": "ok"}`
- [ ] 5.3 `GET /health/db` executa `SELECT 1` via session; retorna 200 ou 503

## 6. Alembic
- [ ] 6.1 Rodar `alembic init alembic` (ou criar arquivos manualmente)
- [ ] 6.2 Editar `alembic/env.py` para importar `Base` e usar `settings.database_url`
- [ ] 6.3 Configurar `alembic.ini` com `script_location = alembic`
- [ ] 6.4 Validar com `alembic current` (deve responder sem erro)

## 7. Lint/format
- [ ] 7.1 Criar `pyproject.toml` com `[tool.ruff]` (line-length 100, target-version py312)
- [ ] 7.2 Configurar `[tool.pytest.ini_options]` com `testpaths = ["tests"]`
- [ ] 7.3 Rodar `ruff check .` e `ruff format .` (sem alterações pendentes)

## 8. Testes
- [ ] 8.1 Criar `tests/conftest.py` com fixture `client` (TestClient)
- [ ] 8.2 Criar `tests/test_health.py` com testes dos dois endpoints
- [ ] 8.3 `pytest` passa (mínimo 2 testes)

## 9. Validação manual
- [ ] 9.1 `docker compose up -d` sobe Postgres sem erro
- [ ] 9.2 `uvicorn app.main:app --reload` sobe sem erros
- [ ] 9.3 `curl http://localhost:8000/health` retorna 200 e `{"status":"ok"}`
- [ ] 9.4 `curl http://localhost:8000/health/db` retorna 200 e DB connected
- [ ] 9.5 `http://localhost:8000/docs` (Swagger UI) carrega
