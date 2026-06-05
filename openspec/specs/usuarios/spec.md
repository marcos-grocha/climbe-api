# usuarios

## Purpose

Gestão de usuários (colaboradores): criação por admin com validação de CPF e unicidade de
email/CPF, leitura e edição, soft delete via `situacao` e troca de senha self-service.

## Requirements

### Requirement: Create user (admin only)

The system SHALL allow only admins to create users, validating CPF (check digits) and uniqueness of email and CPF.

#### Scenario: Admin creates a valid user

- GIVEN an admin
- WHEN `POST /usuarios` with valid data (valid CPF, unique email, an existing cargo, a papel)
- THEN the response is 201 with the user (without `senha_hash`)
- AND the password is stored hashed

#### Scenario: Non-admin cannot create

- GIVEN a user whose papel is not admin
- WHEN `POST /usuarios`
- THEN the response is 403 with code `AUTH_SEM_PERMISSAO`

#### Scenario: Invalid CPF rejected

- GIVEN an admin
- WHEN `POST /usuarios` with a CPF that fails the check-digit validation
- THEN the response is 422 with code `CPF_INVALIDO`

#### Scenario: Duplicate email or CPF rejected

- GIVEN an existing user
- WHEN `POST /usuarios` with the same email or CPF
- THEN the response is 409 with code `USUARIO_EMAIL_DUPLICADO` or `USUARIO_CPF_DUPLICADO`

### Requirement: List and read users (admin only)

The system SHALL expose `GET /usuarios` and `GET /usuarios/{id}` to admins.

#### Scenario: Admin lists users

- GIVEN an admin
- WHEN `GET /usuarios`
- THEN the response is 200 with the users (no `senha_hash`)

### Requirement: Update user (admin only)

The system SHALL allow admins to update a user's editable fields (nome, contato, cargo, papel, situacao).

#### Scenario: Admin updates a user

- GIVEN an admin and an existing user
- WHEN `PATCH /usuarios/{id}` with new values
- THEN the response is 200 with the updated user

### Requirement: Soft delete user

The system SHALL deactivate a user via `DELETE /usuarios/{id}` by setting `situacao="inativo"` instead of removing the row.

#### Scenario: Deleted user cannot log in

- GIVEN an active user
- WHEN `DELETE /usuarios/{id}` is called by an admin
- THEN the user's `situacao` becomes `inativo`
- AND a subsequent `POST /auth/login` with their credentials fails (401)

### Requirement: Change own password

The system SHALL let an authenticated user change their own password via `POST /usuarios/me/senha`, requiring the current password.

#### Scenario: Successful password change

- GIVEN an authenticated user
- WHEN `POST /usuarios/me/senha` with the correct current password and a new one
- THEN the response is 200
- AND a login with the new password succeeds

#### Scenario: Wrong current password

- GIVEN an authenticated user
- WHEN `POST /usuarios/me/senha` with a wrong current password
- THEN the response is 400 with code `SENHA_ATUAL_INCORRETA`
