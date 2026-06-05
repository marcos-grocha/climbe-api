# Proposal: Auth JWT

## Intent

Autenticação por email/senha com JWT e controle de acesso por papel (RBAC básico). Entrega o login, a identidade do usuário logado (`get_current_user`) e o gate de autorização (`require_role`) — base sobre a qual todos os endpoints protegidos (usuários, empresas, propostas, …) vão depender.

Sem auth não dá pra proteger recurso nenhum; sem RBAC não dá pra restringir ações (ex.: "apenas admin cadastra usuário").

## Scope

- Hash de senha com **bcrypt** (lib `bcrypt` direta) + verificação.
- Geração/validação de **JWT** (HS256, exp 60min) com python-jose, usando `settings.jwt_*`.
- `POST /auth/login` (email + senha → access token).
- `GET /auth/me` (dados do usuário autenticado).
- Dependencies `get_current_user` (Bearer) e `require_role([...])`.
- Campo **`papel`** no `Usuario` (`admin`/`analista`/`contratante`) + migration.
- Seed de um **admin inicial** (credenciais via env) — para conseguir logar de cara.
- Exception handlers globais **401/403** no padrão `{detail, code}`.
- Testes dos fluxos (login ok/falha, `/me`, `require_role` permite/nega, usuário inativo).

## Out of scope

- CRUD de usuário (cadastro, edição, troca de senha) → `crud-usuarios`.
- Permissões granulares via `permissoes`/`usuario_permissoes` → futuro ("quando necessário").
- OAuth Google → `auth-google`.

## Approach

`papel` (3 valores) é a simplificação operacional dos 8 cargos formais (AGENTS.md); `require_role` checa `usuario.papel`. Login via `OAuth2PasswordRequestForm` (`username` = email) para o botão **Authorize** do Swagger funcionar. O token carrega `sub` (id_usuario) + `papel` + `exp`. `get_current_user` decodifica o Bearer, busca o usuário e exige `situacao == "ativo"`. O admin inicial entra por uma migration de seed idempotente, com senha vinda de `ADMIN_EMAIL`/`ADMIN_PASSWORD` (settings).

## Issues

Closes **#8 — Autenticação por email/senha + JWT** e **#12 — RBAC básico (sistema de permissões)**.
