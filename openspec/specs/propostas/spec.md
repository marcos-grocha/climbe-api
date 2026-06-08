# propostas

## Purpose

Propostas comerciais com ciclo de vida `rascunho → enviada → aprovada/recusada`. Ligam uma
empresa ao autor e ao estado da negociação; mutações restritas ao staff (admin/analista).
A geração do contrato ao aprovar e as notificações são tratadas em outras capabilities.

## Requirements

### Requirement: Create proposta (staff)

The system SHALL allow admins and analistas to create a proposta for an existing empresa, starting in status `rascunho` with the current user as author.

#### Scenario: Staff creates a proposta

- GIVEN an admin or analista and an existing empresa
- WHEN `POST /propostas` with that `empresa_id`
- THEN the response is 201 with the proposta
- AND its `status` is `rascunho` and `usuario_id` is the current user

#### Scenario: Contratante cannot create

- GIVEN a user whose papel is `contratante`
- WHEN `POST /propostas`
- THEN the response is 403 with code `AUTH_SEM_PERMISSAO`

#### Scenario: Unknown empresa rejected

- GIVEN an admin
- WHEN `POST /propostas` with a non-existent `empresa_id`
- THEN the response is 404 with code `EMPRESA_NAO_ENCONTRADA`

### Requirement: List and read propostas (staff)

The system SHALL expose `GET /propostas` and `GET /propostas/{id}` to authenticated staff.

#### Scenario: Staff lists propostas

- GIVEN an authenticated staff user
- WHEN `GET /propostas`
- THEN the response is 200 with the propostas

### Requirement: Status transitions

The system SHALL enforce the proposta lifecycle: `rascunho → enviada → aprovada | recusada`, rejecting invalid transitions.

#### Scenario: Send then approve

- GIVEN a proposta in `rascunho`
- WHEN `POST /propostas/{id}/enviar` then `POST /propostas/{id}/aprovar`
- THEN the status becomes `enviada` and then `aprovada`

#### Scenario: Send then refuse

- GIVEN a proposta in `rascunho`
- WHEN `POST /propostas/{id}/enviar` then `POST /propostas/{id}/recusar`
- THEN the status becomes `enviada` and then `recusada`

#### Scenario: Invalid transition rejected

- GIVEN a proposta in `rascunho`
- WHEN `POST /propostas/{id}/aprovar` (without sending first)
- THEN the response is 409 with code `PROPOSTA_TRANSICAO_INVALIDA`

### Requirement: Delete proposta with referential safety

The system SHALL delete a proposta via `DELETE /propostas/{id}`, but SHALL refuse if it already has a contrato (FK RESTRICT).

#### Scenario: Cannot delete proposta with contrato

- GIVEN a proposta that already has a contrato
- WHEN `DELETE /propostas/{id}`
- THEN the response is 409 with code `PROPOSTA_COM_CONTRATO`
