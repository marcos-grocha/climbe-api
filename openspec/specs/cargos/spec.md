# cargos

## Purpose

Gestão dos cargos formais da Climbe: listagem (para formulários) e CRUD restrito a admin.
Os cargos são populados pelo seed em `models-base`.

## Requirements

### Requirement: List cargos

The system SHALL expose `GET /cargos` to any authenticated user (needed for the user form).

#### Scenario: Authenticated user lists cargos

- GIVEN an authenticated user
- WHEN `GET /cargos` is requested
- THEN the response is 200 with the list of cargos (including the seeded ones)

### Requirement: Manage cargos (admin only)

The system SHALL allow only admins to create, update and delete cargos.

#### Scenario: Admin creates a cargo

- GIVEN an admin
- WHEN `POST /cargos` with a unique `nome_cargo`
- THEN the response is 201 with the created cargo

#### Scenario: Non-admin cannot create

- GIVEN a user whose papel is not admin
- WHEN `POST /cargos`
- THEN the response is 403 with code `AUTH_SEM_PERMISSAO`

#### Scenario: Cannot delete a cargo in use

- GIVEN a cargo referenced by at least one usuario
- WHEN `DELETE /cargos/{id_cargo}`
- THEN the response is 409 with code `CARGO_EM_USO`
