# Delta for contratos

## ADDED Requirements

### Requirement: Contract auto-created on proposta approval

The system SHALL automatically create a contrato (1:1) when a proposta is approved, with `data_inicio = today` and `status = ativo`.

#### Scenario: Approving a proposta creates its contrato

- GIVEN a proposta in status `enviada`
- WHEN `POST /propostas/{id}/aprovar`
- THEN the proposta becomes `aprovada`
- AND a contrato linked to that proposta exists with `status = ativo` and `data_inicio` set to today

### Requirement: Contract extra fields

The system SHALL store `prazo_entrega` (a variable delivery deadline, nullable) and `recorrente` (boolean, default false) on a contrato.

#### Scenario: Defaults on auto-created contrato

- GIVEN a contrato just created by approval
- WHEN it is read
- THEN `recorrente` is false and `prazo_entrega` is null

### Requirement: List and read contratos (staff)

The system SHALL expose `GET /contratos` and `GET /contratos/{id}` to authenticated staff.

#### Scenario: Staff lists contratos

- GIVEN an authenticated staff user
- WHEN `GET /contratos`
- THEN the response is 200 with the contratos

### Requirement: Update contract terms (staff)

The system SHALL allow admins and analistas to update `data_inicio`, `data_fim`, `prazo_entrega` and `recorrente` via `PATCH /contratos/{id}`.

#### Scenario: Set delivery deadline and recurrence

- GIVEN an active contrato
- WHEN `PATCH /contratos/{id}` with `prazo_entrega` and `recorrente = true`
- THEN the response is 200 with the updated values

### Requirement: Close contract

The system SHALL close a contrato via `POST /contratos/{id}/encerrar` (`ativo → encerrado`), rejecting if already closed.

#### Scenario: Close an active contrato

- GIVEN an active contrato
- WHEN `POST /contratos/{id}/encerrar`
- THEN the status becomes `encerrado`

#### Scenario: Closing an already closed contrato is rejected

- GIVEN a contrato already `encerrado`
- WHEN `POST /contratos/{id}/encerrar`
- THEN the response is 409 with code `CONTRATO_TRANSICAO_INVALIDA`
