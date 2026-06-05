# Tasks — Auth JWT

## 1. Config e segurança
- [x] 1.1 `app/config.py`: settings `ADMIN_EMAIL`, `ADMIN_PASSWORD` (+ `.env.example`)
- [x] 1.2 `app/utils/security.py`: `hash_password`, `verify_password` (lib `bcrypt`)
- [x] 1.3 `app/utils/security.py`: `create_access_token`, `decode_access_token` (jose HS256)

## 2. Campo papel
- [x] 2.1 `Usuario` + campo `papel` (`String`, `server_default='analista'`)
- [x] 2.2 Migration `add coluna papel`
- [x] 2.3 `alembic upgrade head`

## 3. Schemas
- [x] 3.1 `Token` (access_token, token_type)
- [x] 3.2 `TokenPayload` (sub, papel)
- [x] 3.3 `UsuarioMe` (response de `/auth/me`)

## 4. Dependencies
- [x] 4.1 `oauth2_scheme` (`OAuth2PasswordBearer`, `auto_error=False`)
- [x] 4.2 `get_current_user` (decodifica, busca, exige `ativo`)
- [x] 4.3 `require_role(papeis)`

## 5. Endpoints
- [x] 5.1 `POST /auth/login` (`OAuth2PasswordRequestForm` → `Token`)
- [x] 5.2 `GET /auth/me` (`UsuarioMe`)

## 6. Erros
- [x] 6.1 Exceções próprias + handler 401/403 no padrão `{detail, code}`
- [x] 6.2 Registrar handler e router no `main`

## 7. Admin inicial
- [x] 7.1 Migration de seed do admin (idempotente, `bcrypt(ADMIN_PASSWORD)`, cargo "Compliance")
- [x] 7.2 `alembic upgrade head` cria o admin

## 8. Testes
- [x] 8.1 login ok retorna token
- [x] 8.2 login senha errada → 401 com `code`
- [x] 8.3 `/auth/me` com token válido retorna o usuário
- [x] 8.4 `/auth/me` sem token / token inválido → 401
- [x] 8.5 `require_role` permite papel certo e nega errado (403)
- [x] 8.6 usuário inativo → 401

## 9. Lint/validação
- [x] 9.1 `ruff check .` e `ruff format .`
- [x] 9.2 `pytest` verde (23 testes)
- [x] 9.3 Fluxo login/`me`/admin validado via TestClient (smoke no uvicorn bloqueado por sandbox)
