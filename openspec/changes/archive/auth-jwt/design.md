# Design — Auth JWT

## Decisões e trade-offs

### 1. `papel` como campo no Usuario (RBAC básico)
O modelo (do ER) não tem papel; tem `cargo_id` (8 cargos formais) e `permissoes` (M:N granular). Para o "RBAC básico" (`require_role`), adiciono `usuarios.papel` com 3 valores — `admin`, `analista`, `contratante` — conforme a simplificação do `AGENTS.md`. O cargo segue sendo o **título formal**; `papel` é o **controle de acesso**. Permissões granulares (`permissoes`) ficam para quando necessário.
- Migration: adiciona coluna `papel` (`String`, NOT NULL, `server_default='analista'`).
> ⚠️ **Confirmar:** `papel` como campo (escolhido) vs derivar do cargo vs usar a tabela `permissoes`.

### 2. Admin inicial via seed (migration)
Sem usuários, ninguém loga — e o `crud-usuarios` (que exige admin) não destrava. Então seedo um admin:
- Novas settings: `ADMIN_EMAIL` (default `admin@climbe.local`) e `ADMIN_PASSWORD` (default só p/ dev, **trocar em produção**).
- Migration de dados idempotente: cria o admin se não existir — `papel='admin'`, `cargo` = "Compliance" (cargo seedado), `senha_hash = bcrypt(ADMIN_PASSWORD)`, `situacao='ativo'`.
> ⚠️ **Confirmar:** credenciais default e a estratégia (seed via migration vs script à parte).

### 3. JWT
- HS256, `settings.jwt_secret`, expiração `settings.jwt_expire_minutes`.
- Claims: `sub` = `str(id_usuario)`, `papel`, `exp`.
- `python-jose` para encode/decode; erros de decode → 401.

### 4. Login via `OAuth2PasswordRequestForm`
`username` = email, `password` = senha. Facilita o **Authorize** do Swagger. Resposta: `{ "access_token": "...", "token_type": "bearer" }`.

### 5. `get_current_user` / `require_role`
- `OAuth2PasswordBearer(tokenUrl="auth/login")`.
- `get_current_user`: decodifica e valida assinatura/exp → busca o usuário → exige `situacao == "ativo"`; 401 em qualquer falha.
- `require_role(papeis: list[str])`: depende de `get_current_user`; 403 se `papel` não estiver em `papeis`.

### 6. Erros no padrão `{detail, code}`
Exceções próprias (`CredenciaisInvalidasError`, `TokenInvalidoError`, `SemPermissaoError`) + exception handlers globais devolvendo `{"detail": "...", "code": "AUTH_*"}`:
- `AUTH_CREDENCIAIS_INVALIDAS` (401), `AUTH_TOKEN_INVALIDO` (401), `AUTH_USUARIO_INATIVO` (401), `AUTH_SEM_PERMISSAO` (403).

## Arquivos a criar/alterar

- `app/utils/security.py` — hash/verify senha, create/decode token
- `app/schemas/auth.py` — `Token`, `TokenPayload`, `UsuarioMe`
- `app/dependencies/auth.py` — `oauth2_scheme`, `get_current_user`, `require_role`
- `app/routers/auth.py` — `POST /auth/login`, `GET /auth/me`
- `app/models/usuario.py` — + campo `papel`
- `app/config.py` — + `ADMIN_EMAIL`, `ADMIN_PASSWORD`
- `app/main.py` — registra exception handlers e o router de auth
- `alembic/versions/*_add_papel_usuario.py`, `*_seed_admin_inicial.py`
- `tests/test_auth.py`

## Estratégia de testes

Reaproveita a fixture `db_session` (transação revertida). Para `get_current_user`/endpoints, usa o `TestClient` com override de `get_db` apontando para a sessão de teste; cria um usuário com senha hasheada na hora e gera token via `create_access_token`. Cobre login ok/erro, `/me`, papel permitido/negado e usuário inativo.

## `.env.example`

Adicionar `ADMIN_EMAIL` e `ADMIN_PASSWORD` documentados.
