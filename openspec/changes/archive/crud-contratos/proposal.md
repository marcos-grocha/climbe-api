# Proposal: CRUD Contratos

## Intent

Contratos — gerados **automaticamente quando uma proposta é aprovada** — com prazo de entrega (variável, definido depois pelo Analista Sênior), flag de recorrência (CFO/BPO) e ciclo `ativo → encerrado`. Liga o fluxo comercial (proposta) à execução (documentos, planilhas, relatórios).

## Scope

- **Geração automática:** aprovar uma proposta (`POST /propostas/{id}/aprovar`) passa a **criar o contrato** vinculado (1:1), com `data_inicio = hoje`, `status = ativo`.
- **Novos campos** em `contratos` (migration): `prazo_entrega` (data, definida depois) e `recorrente` (bool, default `false`).
- Endpoints: `GET /contratos`, `GET /contratos/{id}` (staff), `PATCH /contratos/{id}` (data_inicio/data_fim/prazo_entrega/recorrente), `POST /contratos/{id}/encerrar` (`ativo → encerrado`).

## Out of scope

- Criação/remoção manual de contrato (nasce da aprovação; não some — encerra-se).
- Documentos/planilhas/relatórios do contrato → capabilities próprias.
- Detecção automática de `recorrente` a partir dos serviços da empresa (CFO/BPO) → fica como ajuste manual via `PATCH` por ora.
- Notificações → `notificacoes`.

## Approach

Migration adiciona `prazo_entrega DATE NULL` e `recorrente BOOLEAN NOT NULL DEFAULT false` em `contratos`. O gatilho de criação é **explícito**: `proposta_service` (no caminho do `aprovar`) chama `contrato_service.criar_para_proposta(db, proposta)` — sem `event listener` mágico, mais testável. `contrato_service` não importa `proposta_service` (evita ciclo). Router `contratos.py`; regras em `services/contrato_service.py`. Reaproveita `require_role(["admin","analista"])` e o handler `{detail, code}`.

## Issues

Closes **#14 — Endpoints de contrato**.
