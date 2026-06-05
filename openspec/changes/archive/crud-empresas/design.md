# Design — CRUD Empresas

## Decisões e trade-offs

### 1. Quem pode mutar empresas
Criação/edição/remoção de empresa: `require_role(["admin", "analista"])` — quem opera o cadastro de clientes é o staff (analista/admin), não o contratante. Leitura (`GET`): qualquer usuário autenticado do staff.
> ⚠️ **Confirmar:** admin+analista (escolhido) vs só admin.

### 2. Validação e armazenamento do CNPJ
`utils/validators.py::validar_cnpj(cnpj) -> str` normaliza para 14 dígitos, valida os 2 dígitos verificadores e rejeita sequências triviais. Inválido → `CNPJ_INVALIDO` (422). Unicidade: checagem em service + constraint do banco → duplicado vira `EMPRESA_CNPJ_DUPLICADO` (409). Armazenamos **14 dígitos** (sem máscara); a coluna `cnpj CHAR(18)` acomoda.

### 3. Vínculo M:N com serviços
`servico_ids: list[int]` no `EmpresaCreate`/`EmpresaUpdate`. No create cria os vínculos em `empresa_servico`; no update **sincroniza** (substitui o conjunto). Cada id é validado — inexistente → `SERVICO_NAO_ENCONTRADO` (404). `EmpresaResponse` inclui `servicos: list[ServicoResponse]`. `GET /servicos` (autenticado) lista as opções para o formulário.
> Sem CRUD de serviços: são dados de referência (seed de `models-base`).

### 4. Delete = hard delete (ER não tem `situacao` em empresa)
`DELETE /empresas/{id}` remove a linha. Por FK: `empresa_servico` e `documentos` caem em CASCADE; `reunioes.empresa_id` vira NULL; se houver `propostas` (RESTRICT), o banco barra → `EMPRESA_COM_VINCULOS` (409).
> ⚠️ **Confirmar:** hard delete (fiel ao ER) vs adicionar um campo `situacao`/`ativo` para soft delete (exigiria migration).

### 5. Erros de domínio (`{detail, code}`)
Novas exceções em `app/exceptions.py`: `CnpjInvalidoError` (422 `CNPJ_INVALIDO`), `CnpjDuplicadoError` (409 `EMPRESA_CNPJ_DUPLICADO`), `EmpresaNaoEncontradaError` (404 `EMPRESA_NAO_ENCONTRADA`), `EmpresaComVinculosError` (409 `EMPRESA_COM_VINCULOS`), `ServicoNaoEncontradoError` (404 `SERVICO_NAO_ENCONTRADO`).

## Arquivos a criar/alterar

- `app/utils/validators.py` — `validar_cnpj` (+)
- `app/schemas/empresa.py` — `EmpresaCreate`, `EmpresaUpdate`, `EmpresaResponse`
- `app/schemas/servico.py` — `ServicoResponse`
- `app/services/empresa_service.py`, `app/services/servico_service.py`
- `app/routers/empresas.py`, `app/routers/servicos.py`
- `app/exceptions.py` — novas exceções (+)
- `app/main.py` — incluir os routers
- `tests/test_empresas.py`, `tests/test_servicos.py`, `tests/test_validators.py` (+ casos de CNPJ)

Sem migration (schema já tem `empresas`, `servicos`, `empresa_servico` desde `models-base`).

## Estratégia de testes

Reaproveita `client_db` + `tests/factories.py` (admin/analista/contratante via token). Cobre: criar empresa (admin/analista) com serviços vinculados; CNPJ inválido → 422; CNPJ duplicado → 409; servico_id inexistente → 404; `GET /empresas` e `/servicos`; update sincroniza serviços; delete ok e delete com proposta → 409; contratante não pode mutar (403). `validar_cnpj` ganha testes unitários (válido/inválido/trivial).
