# Design — CRUD Usuários (e Cargos)

## Decisões e trade-offs

### 1. Escopo do CRUD de cargo
A issue #9 é "CRUD de cargo + seed". O seed já saiu em `models-base`, então aqui entram os **endpoints**: `GET /cargos` (qualquer autenticado — necessário para o formulário de usuário) e `POST`/`PATCH`/`DELETE` (admin). `DELETE` de cargo em uso é barrado pela FK `RESTRICT` → 409 `CARGO_EM_USO`.
> ⚠️ **Confirmar:** cargo com CRUD completo (escolhido, fecha #9) vs apenas `GET /cargos` por enquanto.

### 2. Validação de CPF (dígito verificador)
`utils/validators.py::validar_cpf(cpf) -> str` normaliza para 11 dígitos, valida os 2 dígitos verificadores e rejeita sequências triviais (000…, 111…). Inválido → `CPF_INVALIDO` (422). Armazenamos **11 dígitos** (sem máscara); a coluna `cpf CHAR(14)` acomoda.
> O admin seedado usa `00000000000` — é um placeholder; ajustável depois.

### 3. Troca de senha
`POST /usuarios/me/senha` (self-service): exige `senha_atual` + `nova_senha`; valida a atual com `verify_password`, regrava com `hash_password`. Senha errada → `SENHA_ATUAL_INCORRETA` (400). Reset por admin fica fora (futuro).
> ⚠️ **Confirmar:** troca self-service (escolhido) — admin não redefine senha de terceiros nesta change.

### 4. Soft delete
`DELETE /usuarios/{id}` seta `situacao="inativo"` (não remove a linha) → preserva FKs/histórico e o usuário deixa de logar (regra do `auth-jwt`). Reativar = `PATCH situacao="ativo"`.

### 5. Permissões e visibilidade
- Mutações de usuário e cargo: `require_role(["admin"])`.
- `GET /usuarios`: admin (dado sensível de RH).
- `GET /cargos`: qualquer autenticado (precisa para o form).
- `papel` aceita apenas `admin`/`analista`/`contratante` (validado no schema).

### 6. Erros de domínio (`{detail, code}`)
Novas exceções em `app/exceptions.py`: `CpfInvalidoError` (422 `CPF_INVALIDO`), `EmailDuplicadoError` (409 `USUARIO_EMAIL_DUPLICADO`), `CpfDuplicadoError` (409 `USUARIO_CPF_DUPLICADO`), `UsuarioNaoEncontradoError` (404 `USUARIO_NAO_ENCONTRADO`), `CargoNaoEncontradoError` (404 `CARGO_NAO_ENCONTRADO`), `CargoEmUsoError` (409 `CARGO_EM_USO`), `SenhaAtualIncorretaError` (400 `SENHA_ATUAL_INCORRETA`).

## Arquivos a criar/alterar

- `app/utils/validators.py` — `validar_cpf`
- `app/schemas/cargo.py` — `CargoCreate`, `CargoUpdate`, `CargoResponse`
- `app/schemas/usuario.py` — `UsuarioCreate`, `UsuarioUpdate`, `UsuarioResponse`, `TrocarSenha`
- `app/services/cargo_service.py`, `app/services/usuario_service.py`
- `app/routers/cargos.py`, `app/routers/usuarios.py`
- `app/exceptions.py` — novas exceções (+)
- `app/main.py` — incluir os routers
- `tests/test_cargos.py`, `tests/test_usuarios.py`, `tests/test_validators.py`

Sem migration (schema já tem tudo desde `models-base`/`auth-jwt`).

## Estratégia de testes

Usa `client_db` (TestClient + sessão de teste) e tokens via `create_access_token` para simular admin/analista. Cobre: criação por admin / proibição p/ não-admin, CPF inválido, email/CPF duplicados, soft delete (e bloqueio de login depois), troca de senha (ok / senha atual errada), `GET /cargos`, `DELETE` de cargo em uso. `validar_cpf` tem testes unitários (válido/ inválido/ sequência trivial).
