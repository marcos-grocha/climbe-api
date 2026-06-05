# Tasks — CRUD Empresas

## 1. Validação
- [x] 1.1 `utils/validators.py`: `validar_cnpj` (normaliza 14 dígitos, dígito verificador, rejeita triviais)

## 2. Exceções
- [x] 2.1 `exceptions.py`: `CnpjInvalidoError`, `CnpjDuplicadoError`, `EmpresaNaoEncontradaError`, `EmpresaComVinculosError`, `ServicoNaoEncontradoError`

## 3. Schemas
- [x] 3.1 `servico.py`: `ServicoResponse`
- [x] 3.2 `empresa.py`: `EmpresaCreate`/`EmpresaUpdate` (com `servico_ids`), `EmpresaResponse` (com `servicos`)

## 4. Services
- [x] 4.1 `servico_service.py`: `listar_servicos`, `validar_servicos`
- [x] 4.2 `empresa_service.py`: criar (valida CNPJ, unicidade, vincula serviços), listar/obter, atualizar (sincroniza serviços), remover (trata `EMPRESA_COM_VINCULOS`)

## 5. Serviços (router)
- [x] 5.1 `GET /servicos` (autenticado)

## 6. Empresas (router)
- [x] 6.1 `GET /empresas` e `GET /empresas/{id}` (staff)
- [x] 6.2 `POST /empresas` (admin/analista)
- [x] 6.3 `PATCH /empresas/{id}` (admin/analista)
- [x] 6.4 `DELETE /empresas/{id}` (admin/analista; com proposta → 409)
- [x] 6.5 Incluir routers no `main`

## 7. Testes
- [x] 7.1 `validar_cnpj` (válido / inválido / trivial)
- [x] 7.2 criar empresa (admin/analista) com serviços; contratante → 403
- [x] 7.3 CNPJ inválido → 422; CNPJ duplicado → 409; servico inexistente → 404
- [x] 7.4 update sincroniza serviços
- [x] 7.5 delete ok; delete com proposta → 409
- [x] 7.6 `GET /empresas` e `GET /servicos`

## 8. Lint/validação
- [x] 8.1 `ruff check .` e `ruff format .`
- [x] 8.2 `pytest` verde (51 testes)
- [x] 8.3 Fluxo validado via TestClient
