# api-foundation

## Purpose

Fundação HTTP da API: a aplicação FastAPI como interface primária, com health
check de liveness, CORS para o frontend e configuração 100% orientada por
variáveis de ambiente.

## Requirements

### Requirement: API application

The system SHALL expose a FastAPI application as the primary HTTP interface.

#### Scenario: App boots successfully

- GIVEN a valid `.env` and the database reachable
- WHEN running `uvicorn app.main:app`
- THEN the application starts on port 8000 without errors
- AND `GET /docs` shows the OpenAPI documentation

### Requirement: Liveness health endpoint

The system SHALL expose `GET /health` for liveness probes that does NOT touch the database.

#### Scenario: Liveness probe responds quickly

- GIVEN the API running
- WHEN a request hits `GET /health`
- THEN response is 200
- AND body is exactly `{"status": "ok"}`
- AND no database connection is opened

### Requirement: CORS for the frontend

The system SHALL accept cross-origin requests from configured origins (`ALLOWED_ORIGINS` env var).

#### Scenario: Preflight from frontend

- GIVEN `ALLOWED_ORIGINS=http://localhost:5173`
- WHEN a preflight `OPTIONS` request arrives with `Origin: http://localhost:5173`
- THEN response includes `Access-Control-Allow-Origin: http://localhost:5173`
- AND credentials are allowed

#### Scenario: Origin not allowed

- GIVEN `ALLOWED_ORIGINS=http://localhost:5173`
- WHEN a request arrives with `Origin: http://evil.com`
- THEN response does NOT include `Access-Control-Allow-Origin` for that origin

### Requirement: Environment-driven configuration

The system SHALL read all configuration from environment variables (or `.env` file in dev).

#### Scenario: Missing required env var

- GIVEN `JWT_SECRET` is unset
- WHEN the application tries to start
- THEN it raises a clear `ValidationError` and refuses to start

#### Scenario: Sensible defaults

- GIVEN only required vars set
- WHEN the application starts
- THEN optional settings (like `JWT_ALGORITHM`, `JWT_EXPIRE_MINUTES`) use documented defaults
