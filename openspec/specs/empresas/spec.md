# empresas

## Purpose

Gestão de empresas (contratantes): cadastro com endereço e representante legal, validação de
CNPJ (dígito verificador) e unicidade, e vínculo M:N com os serviços contratados. Mutações
restritas ao staff (admin/analista); remoção protegida por integridade referencial.

## Requirements

### Requirement: Create empresa (staff)

The system SHALL allow admins and analistas to create empresas, validating CNPJ (check digits) and its uniqueness, and linking the contracted services.

#### Scenario: Staff creates a valid empresa

- GIVEN an admin or analista
- WHEN `POST /empresas` with valid data (valid unique CNPJ, address, representante) and `servico_ids`
- THEN the response is 201 with the empresa
- AND the response includes the linked `servicos`

#### Scenario: Contratante cannot create

- GIVEN a user whose papel is `contratante`
- WHEN `POST /empresas`
- THEN the response is 403 with code `AUTH_SEM_PERMISSAO`

#### Scenario: Invalid CNPJ rejected

- GIVEN an admin
- WHEN `POST /empresas` with a CNPJ that fails the check-digit validation
- THEN the response is 422 with code `CNPJ_INVALIDO`

#### Scenario: Duplicate CNPJ rejected

- GIVEN an empresa with a given CNPJ exists
- WHEN `POST /empresas` with the same CNPJ
- THEN the response is 409 with code `EMPRESA_CNPJ_DUPLICADO`

#### Scenario: Unknown service rejected

- GIVEN an admin
- WHEN `POST /empresas` with a `servico_ids` containing a non-existent id
- THEN the response is 404 with code `SERVICO_NAO_ENCONTRADO`

### Requirement: List and read empresas (staff)

The system SHALL expose `GET /empresas` and `GET /empresas/{id}` to authenticated staff, including the linked services.

#### Scenario: Staff lists empresas

- GIVEN an authenticated staff user
- WHEN `GET /empresas`
- THEN the response is 200 with the empresas

### Requirement: Update empresa (staff)

The system SHALL allow admins and analistas to update an empresa, re-syncing its linked services when `servico_ids` is provided.

#### Scenario: Update re-syncs services

- GIVEN an empresa linked to services A and B
- WHEN `PATCH /empresas/{id}` with `servico_ids` = [A, C]
- THEN the empresa ends linked to exactly A and C

### Requirement: Delete empresa with referential safety

The system SHALL delete an empresa via `DELETE /empresas/{id}`, but SHALL refuse if it has propostas (FK RESTRICT).

#### Scenario: Delete empresa without propostas

- GIVEN an empresa with no propostas
- WHEN `DELETE /empresas/{id}` by staff
- THEN the response is 204
- AND its `empresa_servico` links are removed (CASCADE)

#### Scenario: Cannot delete empresa with propostas

- GIVEN an empresa referenced by a proposta
- WHEN `DELETE /empresas/{id}`
- THEN the response is 409 with code `EMPRESA_COM_VINCULOS`
