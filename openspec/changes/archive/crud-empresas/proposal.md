# Proposal: CRUD Empresas

## Intent

CRUD de **empresas** (contratantes) — cadastro com endereço, representante legal, validação de CNPJ e vínculo com os serviços contratados (M:N). É o segundo agregado central do domínio (depois de usuários) e pré-requisito de propostas, contratos e documentos.

## Scope

- **Empresas** (#11):
  - `GET /empresas` (lista) e `GET /empresas/{id}` (detalhe) — staff
  - `POST /empresas` (cria) e `PATCH /empresas/{id}` (edita) — admin/analista
  - `DELETE /empresas/{id}` — remove (bloqueado se houver propostas → 409)
- **Validação de CNPJ** (dígito verificador) + **unicidade** no banco.
- Endereço completo (logradouro, número, bairro, cidade, UF, CEP) e representante legal (nome, CPF, contato).
- **Vínculo M:N com serviços** via `empresa_servico`: `servico_ids` no create/update; resposta inclui os serviços.
- `GET /servicos` (lista, autenticado) — para o formulário de empresa.

## Out of scope

- Propostas/contratos/documentos da empresa → capabilities próprias.
- CRUD de serviços (servicos é dado de referência seedado; aqui só lista).
- Validação de CEP via API externa (correios) — só formato.

## Approach

Routers `empresas.py` e `servicos.py`; regras em `services/empresa_service.py` (+ `servico_service.py`); validador `utils/validators.py::validar_cnpj` (ao lado de `validar_cpf`). Schemas no padrão `*Create`/`*Update`/`*Response`. Mutações exigem `require_role(["admin", "analista"])`; leitura exige autenticação. CNPJ normalizado para 14 dígitos. O vínculo de serviços é sincronizado a partir de `servico_ids` (valida cada id; serviço inexistente → 404). `DELETE` é hard delete: `empresa_servico`/`documentos` caem por CASCADE, `reunioes.empresa_id` vira NULL; se houver `propostas` (FK RESTRICT), retorna 409.

## Issues

Closes **#11 — CRUD de empresa**.
