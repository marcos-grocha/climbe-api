# Delta for database

## ADDED Requirements

### Requirement: PostgreSQL connection

The system SHALL connect to a PostgreSQL database via SQLAlchemy 2.x using the `psycopg` driver.

#### Scenario: Connection works

- GIVEN PostgreSQL running and `DATABASE_URL` configured
- WHEN the engine is initialized at startup
- THEN it connects successfully
- AND `SELECT 1` returns 1 through a session

#### Scenario: Connection fails

- GIVEN PostgreSQL not reachable
- WHEN `GET /health/db` is requested
- THEN response is 503
- AND body contains a clear error message about database unavailability

### Requirement: Database session dependency

The system SHALL expose `get_db()` as a FastAPI dependency that yields a SQLAlchemy session and closes it on request completion.

#### Scenario: Session opened and closed on each request

- GIVEN a request to an endpoint depending on `get_db`
- WHEN the request completes (successfully or with an exception)
- THEN the session is always closed (no connection leak)

### Requirement: Declarative Base available

The system SHALL expose a `Base` class (from `DeclarativeBase`) that future models will inherit from.

#### Scenario: Base importable

- GIVEN the `app.database` module
- WHEN any model module imports `Base`
- THEN it can define classes inheriting from `Base` using `Mapped[]` + `mapped_column()`

### Requirement: Alembic configured

The system SHALL have Alembic configured to manage schema migrations.

#### Scenario: Alembic ready

- GIVEN the repository fresh checkout with deps installed
- WHEN running `alembic current`
- THEN the command exits with code 0
- AND reports no current revision (no migrations yet — initial state)

#### Scenario: Autogenerate works

- GIVEN any future model added inheriting from `Base`
- WHEN running `alembic revision --autogenerate -m "msg"`
- THEN Alembic detects the new table and writes a migration file in `alembic/versions/`

### Requirement: Health check for DB

The system SHALL expose `GET /health/db` that verifies database connectivity.

#### Scenario: DB up

- GIVEN database reachable
- WHEN `GET /health/db` is requested
- THEN response is 200
- AND body is `{"status": "ok", "database": "connected"}`
