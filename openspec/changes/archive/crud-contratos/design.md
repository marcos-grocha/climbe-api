# Design — CRUD Contratos

## Decisões e trade-offs

### 1. Gatilho de criação: chamada explícita no `aprovar` (não SQLAlchemy event)
O roadmap fala em "signal/event handler". Opto por **chamada explícita**: em `proposta_service.transicionar`, ao mudar para `aprovada`, chamar `contrato_service.criar_para_proposta(db, proposta)`. Mais explícito, fácil de testar e sem mágica de listeners. Para evitar import circular, `contrato_service` **não** importa `proposta_service`.
> ⚠️ **Confirmar:** gatilho explícito no service (escolhido) vs SQLAlchemy `event.listen`.

### 2. Novos campos (migration)
O model `Contrato` (do ER/`models-base`) tem `proposta_id`, `data_inicio`, `data_fim`, `status`. Faltam, do roadmap:
- `prazo_entrega: Mapped[date | None]` — prazo de entrega **variável** (definido depois pelo Analista Sênior, conforme Novo Fluxograma). Modelado como **data** (deadline), `NULL` na criação.
- `recorrente: Mapped[bool]` — `server_default false`, para o loop mensal de CFO/BPO.
> Migration `add prazo_entrega e recorrente a contratos`.
> ⚠️ **Confirmar:** `prazo_entrega` como **data** (deadline) vs inteiro de dias.

### 3. Criação automática
`criar_para_proposta`: idempotente — se a proposta já tem contrato (FK `unique` em `proposta_id`), não cria de novo. Define `data_inicio = date.today()`, `status = "ativo"`, `recorrente = False`, `prazo_entrega = None`. A aprovação fica **transacional** com a transição da proposta (mesmo commit).
> ⚠️ **Confirmar:** `recorrente` começa `false` e é ajustado por `PATCH` (não auto-detectado dos serviços CFO/BPO nesta change).

### 4. Sem POST/DELETE manual
Contrato nasce da aprovação e **não é apagado** — encerra-se (`POST /contratos/{id}/encerrar`, `ativo → encerrado`; encerrar um já encerrado → 409). Edição de termos via `PATCH`.

### 5. Erros de domínio
`ContratoNaoEncontradoError` (404 `CONTRATO_NAO_ENCONTRADO`), `ContratoTransicaoInvalidaError` (409 `CONTRATO_TRANSICAO_INVALIDA`).

## Arquivos a criar/alterar

- `app/models/contrato.py` — + `prazo_entrega`, `recorrente`
- `alembic/versions/*_add_prazo_entrega_recorrente.py`
- `app/schemas/contrato.py` — `ContratoUpdate`, `ContratoResponse`
- `app/services/contrato_service.py` — `criar_para_proposta`, listar/obter, atualizar, encerrar
- `app/services/proposta_service.py` — chama `criar_para_proposta` no `aprovar` (+)
- `app/routers/contratos.py` + `app/main.py`
- `app/exceptions.py` — novas exceções (+)
- `tests/test_contratos.py`

## Estratégia de testes

`client_db` + factories. Cobre: aprovar proposta **cria contrato** (`data_inicio` hoje, `ativo`); `GET /contratos`; `PATCH` (prazo_entrega/recorrente/data_fim); `encerrar` (ativo→encerrado) e encerrar de novo → 409. Cria empresa/proposta via factory/endpoint.
