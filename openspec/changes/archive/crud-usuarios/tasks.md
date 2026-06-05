# Tasks — CRUD Usuários (e Cargos)

## 1. Validação
- [x] 1.1 `app/utils/validators.py`: `validar_cpf` (normaliza 11 dígitos, dígito verificador, rejeita sequências triviais)

## 2. Exceções
- [x] 2.1 `app/exceptions.py`: `CpfInvalidoError`, `EmailDuplicadoError`, `CpfDuplicadoError`, `UsuarioNaoEncontradoError`, `CargoNaoEncontradoError`, `CargoEmUsoError`, `SenhaAtualIncorretaError`

## 3. Schemas
- [x] 3.1 `cargo.py`: `CargoCreate`, `CargoUpdate`, `CargoResponse`
- [x] 3.2 `usuario.py`: `UsuarioCreate` (com `papel`/`senha`), `UsuarioUpdate`, `UsuarioResponse` (sem `senha_hash`), `TrocarSenha`

## 4. Services
- [x] 4.1 `cargo_service.py`: listar/criar/atualizar/remover (trata `CARGO_EM_USO`)
- [x] 4.2 `usuario_service.py`: criar (valida CPF, unicidade, hash senha), listar/obter, atualizar, soft delete, trocar senha

## 5. Cargos (router)
- [x] 5.1 `GET /cargos` (autenticado)
- [x] 5.2 `POST /cargos` (admin)
- [x] 5.3 `PATCH /cargos/{id_cargo}` (admin)
- [x] 5.4 `DELETE /cargos/{id_cargo}` (admin; em uso → 409)

## 6. Usuários (router)
- [x] 6.1 `GET /usuarios` (admin) e `GET /usuarios/{id}` (admin)
- [x] 6.2 `POST /usuarios` (admin)
- [x] 6.3 `PATCH /usuarios/{id}` (admin)
- [x] 6.4 `DELETE /usuarios/{id}` (soft delete → `inativo`)
- [x] 6.5 `POST /usuarios/me/senha` (troca a própria senha)
- [x] 6.6 Incluir os routers no `main`

## 7. Testes
- [x] 7.1 `validar_cpf` (válido / inválido / sequência trivial)
- [x] 7.2 cria usuário (admin) ok; não-admin → 403
- [x] 7.3 CPF inválido → 422; email/CPF duplicado → 409
- [x] 7.4 soft delete → `inativo` e login passa a falhar
- [x] 7.5 troca de senha ok / senha atual errada → 400
- [x] 7.6 `GET /cargos` lista; `DELETE` de cargo em uso → 409

## 8. Lint/validação
- [x] 8.1 `ruff check .` e `ruff format .`
- [x] 8.2 `pytest` verde (38 testes)
- [x] 8.3 Fluxo validado via TestClient
