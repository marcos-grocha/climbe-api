# Proposal: CRUD Propostas

## Intent

CRUD de **propostas comerciais** com fluxo de status (`rascunho → enviada → aprovada/recusada`). A proposta liga uma empresa ao autor (usuário) e ao estado da negociação — é a porta de entrada do contrato (que será gerado quando ela for aprovada, em `crud-contratos`).

## Scope

- `POST /propostas` (cria como `rascunho`, autor = usuário logado), `GET /propostas`, `GET /propostas/{id}`, `PATCH /propostas/{id}` (troca a empresa enquanto `rascunho`), `DELETE /propostas/{id}`.
- **Transições de status** com validação:
  - `POST /propostas/{id}/enviar` — `rascunho → enviada`
  - `POST /propostas/{id}/aprovar` — `enviada → aprovada`
  - `POST /propostas/{id}/recusar` — `enviada → recusada`
  - Transição inválida → 409 `PROPOSTA_TRANSICAO_INVALIDA`.
- Permissionamento: ações por **admin/analista** (staff).

## Out of scope

- **Notificação automática aos envolvidos** → fica para `notificacoes` (Semana 3), que constrói o sistema de notificação e pluga os gatilhos.
- **Geração automática de contrato ao aprovar** → `crud-contratos` (#14, via event handler).
- **Aprovação self-service pelo contratante** → exige vínculo usuário↔empresa (que o modelo ainda não tem); fica para o futuro.

## Approach

Router `propostas.py`; regras em `services/proposta_service.py`. As transições passam por um **mapa de transições permitidas** (`rascunho→{enviada}`, `enviada→{aprovada,recusada}`), bloqueando saltos inválidos. `status` é `String` com valores documentados. Autor = `get_current_user`; empresa validada na criação. Reaproveita `require_role` e o handler `{detail, code}`. Sem migration (o model `Proposta` já existe desde `models-base`).

## Issues

Closes **#13 — Endpoints de proposta comercial**.
