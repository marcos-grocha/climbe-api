# Proposal: CRUD Usuários (e Cargos)

## Intent

CRUD de **usuários** e de **cargos** — o cadastro de colaboradores do sistema, com papéis (RBAC), validação de CPF, unicidade de email/CPF, troca de senha e soft delete. Destrava a gestão de pessoas: o admin inicial (de `auth-jwt`) passa a poder cadastrar o time.

## Scope

- **Cargos** (#9): `GET /cargos` (lista, para formulários) + `POST`/`PATCH`/`DELETE /cargos/{id}` (admin). O seed dos cargos já foi feito em `models-base`.
- **Usuários** (#10):
  - `GET /usuarios` (lista, admin), `GET /usuarios/{id}` (admin)
  - `POST /usuarios` (admin cria)
  - `PATCH /usuarios/{id}` (admin edita)
  - `DELETE /usuarios/{id}` (soft delete → `situacao="inativo"`)
  - `POST /usuarios/me/senha` (usuário troca a própria senha)
- Validação de **CPF com dígito verificador** (não só regex).
- **Unicidade** de email e CPF (constraint do banco + erro amigável `{detail, code}`).
- Senha sempre **hasheada** (bcrypt) no cadastro e na troca.
- Permissionamento: mutações de usuário e de cargo só por **admin** (`require_role(["admin"])`).

## Out of scope

- **Email de boas-vindas** (req 10d) — depende de infra de email; fica para `notificacoes`.
- CRUD de empresa → `crud-empresas`.
- Permissões granulares (`permissoes`/`usuario_permissoes`) → futuro.
- Reset de senha por admin (esqueci minha senha) → futuro, se necessário.

## Approach

Routers `cargos.py` e `usuarios.py`; regras de negócio em `services/`; validador em `utils/validators.py::validar_cpf`. Schemas Pydantic no padrão `*Create` / `*Update` / `*Response` (sem `senha_hash` nas respostas). Reaproveita `get_current_user`/`require_role` (auth-jwt) e o exception handler `{detail, code}`. Soft delete não apaga a linha (preserva histórico e FKs). CPF é normalizado para 11 dígitos antes de validar/gravar.

## Issues

Closes **#9 — CRUD de cargo + seed** e **#10 — CRUD de usuário**.
