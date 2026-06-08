# Design — CRUD Propostas

## Decisões e trade-offs

### 1. Permissionamento: staff (admin/analista) em todas as ações
O `AGENTS.md`/requisitos dizem que cria quem é CMO/CSO/CEO/Analista/Contador e **aprova o contratante**. Como nosso RBAC é por `papel` (admin/analista/contratante) e **não há vínculo usuário↔empresa**, gateio tudo por `require_role(["admin", "analista"])` — o staff registra também a aprovação/recusa em nome do cliente.
> ⚠️ **Confirmar:** staff em tudo (escolhido) vs `aprovar`/`recusar` pelo `contratante`. A aprovação self-service do contratante precisa de um vínculo usuário↔empresa (proponho numa change futura).

### 2. Máquina de estados
```
rascunho ──enviar──▶ enviada ──aprovar──▶ aprovada
                        └────recusar────▶ recusada
```
Mapa de transições permitidas no service; qualquer outra → `PROPOSTA_TRANSICAO_INVALIDA` (409). Ex.: aprovar um `rascunho` (sem enviar) falha; reaprovar uma `aprovada` falha.
> ⚠️ Incluí `POST /propostas/{id}/enviar` (o roadmap citava só `aprovar`/`recusar`, mas o estado `enviada` exige uma transição de saída do `rascunho`).

### 3. Notificações e contrato automático — fora
- Notificações aos envolvidos: o sistema de notificação é a capability `notificacoes`; ela plugará os gatilhos (proposta enviada/aprovada) quando existir. Aqui não disparamos nada.
- Contrato automático ao aprovar: é a `crud-contratos` (event handler). Aqui `aprovar` só muda o status.

### 4. Edição e remoção
- `PATCH /propostas/{id}`: só faz sentido trocar `empresa_id` enquanto `rascunho` (valida a empresa). Demais campos do model são controlados (status via transições; autor/data fixos).
- `DELETE /propostas/{id}`: hard delete; se já houver `contrato` (FK RESTRICT) → `PROPOSTA_COM_CONTRATO` (409).

### 5. Erros de domínio (`{detail, code}`)
`PropostaNaoEncontradaError` (404 `PROPOSTA_NAO_ENCONTRADA`), `PropostaTransicaoInvalidaError` (409 `PROPOSTA_TRANSICAO_INVALIDA`), `PropostaComContratoError` (409 `PROPOSTA_COM_CONTRATO`). Empresa inexistente na criação reaproveita `EmpresaNaoEncontradaError`.

## Arquivos a criar/alterar

- `app/schemas/proposta.py` — `PropostaCreate`, `PropostaUpdate`, `PropostaResponse`
- `app/services/proposta_service.py`
- `app/routers/propostas.py`
- `app/exceptions.py` — novas exceções (+)
- `app/main.py` — incluir o router
- `tests/test_propostas.py`

Sem migration.

## Estratégia de testes

`client_db` + `tests/factories.py`. Cobre: criar (staff) como `rascunho` e autor correto; contratante → 403; fluxo enviar→aprovar e enviar→recusar; transição inválida (aprovar rascunho) → 409; empresa inexistente → 404; delete ok e delete com contrato → 409. Cria empresa/contrato via factory/ORM quando necessário.
