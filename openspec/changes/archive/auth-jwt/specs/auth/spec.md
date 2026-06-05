# Delta for auth

## ADDED Requirements

### Requirement: Email/password login

The system SHALL authenticate a user via email and password and return a JWT access token.

#### Scenario: Successful login

- GIVEN an active user with a known password
- WHEN `POST /auth/login` is called with the correct email and password
- THEN the response is 200
- AND the body is `{ "access_token": "<jwt>", "token_type": "bearer" }`

#### Scenario: Wrong credentials

- GIVEN an existing user
- WHEN `POST /auth/login` is called with a wrong password (or unknown email)
- THEN the response is 401
- AND the body has `detail` and `code` = `AUTH_CREDENCIAIS_INVALIDAS`

### Requirement: Authenticated identity

The system SHALL expose `GET /auth/me`, returning the current user and requiring a valid Bearer token.

#### Scenario: Me with a valid token

- GIVEN a valid access token
- WHEN `GET /auth/me` is requested with `Authorization: Bearer <token>`
- THEN the response is 200
- AND the body includes the user's `id_usuario`, `email` and `papel`

#### Scenario: Me without or with an invalid token

- GIVEN no token or an invalid/expired token
- WHEN `GET /auth/me` is requested
- THEN the response is 401
- AND the body has `detail` and `code` = `AUTH_TOKEN_INVALIDO`

### Requirement: Role-based authorization

The system SHALL provide `require_role` to restrict endpoints to a set of papéis.

#### Scenario: Allowed role

- GIVEN an authenticated user with `papel = "admin"`
- WHEN accessing an endpoint guarded by `require_role(["admin"])`
- THEN access is granted

#### Scenario: Forbidden role

- GIVEN an authenticated user with `papel = "contratante"`
- WHEN accessing an endpoint guarded by `require_role(["admin"])`
- THEN the response is 403
- AND the body has `detail` and `code` = `AUTH_SEM_PERMISSAO`

### Requirement: Inactive users cannot authenticate

The system SHALL reject access for users whose `situacao` is not `"ativo"`.

#### Scenario: Inactive user blocked

- GIVEN a user with `situacao = "inativo"` and an otherwise valid token
- WHEN `GET /auth/me` is requested
- THEN the response is 401
- AND the body has `code` = `AUTH_USUARIO_INATIVO`

### Requirement: Initial admin available

The system SHALL seed an initial admin user so the API is usable before `crud-usuarios`.

#### Scenario: Admin can log in after migrations

- GIVEN migrations applied with `ADMIN_EMAIL`/`ADMIN_PASSWORD` configured
- WHEN `POST /auth/login` is called with those credentials
- THEN the response is 200 with a token
- AND that user's `papel` is `"admin"`
