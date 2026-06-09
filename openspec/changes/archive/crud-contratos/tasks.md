# Tasks — CRUD Contratos

## 1. Model + migration
- [x] 1.1 `Contrato` + `prazo_entrega` (`date | None`) e `recorrente` (`bool`, server_default false)
- [x] 1.2 Migration `add prazo_entrega e recorrente a contratos`
- [x] 1.3 `alembic upgrade head`

## 2. Exceções
- [x] 2.1 `exceptions.py`: `ContratoNaoEncontradoError`, `ContratoTransicaoInvalidaError`

## 3. Schemas
- [x] 3.1 `contrato.py`: `ContratoUpdate` (data_inicio/data_fim/prazo_entrega/recorrente), `ContratoResponse`

## 4. Service
- [x] 4.1 `contrato_service.py`: `criar_para_proposta` (idempotente; data_inicio hoje, ativo)
- [x] 4.2 listar/obter, atualizar, `encerrar` (ativo→encerrado; senão `CONTRATO_TRANSICAO_INVALIDA`)

## 5. Gatilho na aprovação
- [x] 5.1 `proposta_service.transicionar`: ao aprovar, chama `contrato_service.criar_para_proposta` (mesmo commit, sem ciclo de import)

## 6. Router
- [x] 6.1 `GET /contratos` e `GET /contratos/{id}` (staff)
- [x] 6.2 `PATCH /contratos/{id}` (staff)
- [x] 6.3 `POST /contratos/{id}/encerrar` (staff)
- [x] 6.4 Incluir router no `main`

## 7. Testes
- [x] 7.1 aprovar proposta cria contrato (data_inicio hoje, status ativo, 1:1)
- [x] 7.2 `GET /contratos` lista
- [x] 7.3 `PATCH` ajusta prazo_entrega/recorrente/data_fim
- [x] 7.4 `encerrar` (ativo→encerrado); encerrar de novo → 409

## 8. Lint/validação
- [x] 8.1 `ruff check .` e `ruff format .`
- [x] 8.2 `pytest` verde (63 testes)
- [x] 8.3 Round-trip Alembic (upgrade/downgrade) da migration nova
