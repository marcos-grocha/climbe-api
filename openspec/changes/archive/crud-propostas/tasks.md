# Tasks — CRUD Propostas

## 1. Exceções
- [x] 1.1 `exceptions.py`: `PropostaNaoEncontradaError`, `PropostaTransicaoInvalidaError`, `PropostaComContratoError`

## 2. Schemas
- [x] 2.1 `proposta.py`: `PropostaCreate` (empresa_id), `PropostaUpdate` (empresa_id), `PropostaResponse` (id, empresa_id, usuario_id, status, data_criacao)

## 3. Service
- [x] 3.1 `proposta_service.py`: criar (valida empresa, autor = current_user, status rascunho), listar/obter, atualizar (empresa, só em rascunho)
- [x] 3.2 transições via mapa permitido (`enviar`/`aprovar`/`recusar`) → `PROPOSTA_TRANSICAO_INVALIDA`
- [x] 3.3 remover (trata `PROPOSTA_COM_CONTRATO`)

## 4. Router
- [x] 4.1 `GET /propostas` e `GET /propostas/{id}` (staff)
- [x] 4.2 `POST /propostas` (admin/analista)
- [x] 4.3 `PATCH /propostas/{id}` e `DELETE /propostas/{id}` (admin/analista)
- [x] 4.4 `POST /propostas/{id}/enviar`, `/aprovar`, `/recusar` (admin/analista)
- [x] 4.5 Incluir router no `main`

## 5. Testes
- [x] 5.1 criar (staff) → rascunho + autor correto; contratante → 403
- [x] 5.2 empresa inexistente → 404
- [x] 5.3 fluxo enviar → aprovar; enviar → recusar
- [x] 5.4 transição inválida (aprovar rascunho) → 409
- [x] 5.5 delete ok; delete com contrato → 409

## 6. Lint/validação
- [x] 6.1 `ruff check .` e `ruff format .`
- [x] 6.2 `pytest` verde (59 testes)
- [x] 6.3 Fluxo validado via TestClient
