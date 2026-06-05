# Delta for data-model

## ADDED Requirements

### Requirement: Domain entities persisted

The system SHALL persist all 15 domain entities from the ER diagram as SQLAlchemy models inheriting from `Base`.

#### Scenario: Schema created by migration

- GIVEN a fresh database and dependencies installed
- WHEN running `alembic upgrade head`
- THEN all 15 tables exist: `usuarios`, `cargos`, `permissoes`, `usuario_permissoes`, `empresas`, `servicos`, `empresa_servico`, `propostas`, `contratos`, `documentos`, `reunioes`, `participantes_reuniao`, `planilhas`, `relatorios`, `notificacoes`

### Requirement: Unique business identifiers

The system SHALL enforce uniqueness of `usuarios.cpf`, `usuarios.email` and `empresas.cnpj` at the database level.

#### Scenario: Duplicate CNPJ rejected

- GIVEN an empresa with a given `cnpj` exists
- WHEN inserting another empresa with the same `cnpj`
- THEN the database raises a unique/integrity error

#### Scenario: Duplicate user email or cpf rejected

- GIVEN a usuario with a given `email` and `cpf` exists
- WHEN inserting another usuario with the same `email` or `cpf`
- THEN the database raises a unique/integrity error

### Requirement: Referential integrity with explicit delete behavior

The system SHALL define foreign keys with explicit `ondelete` behavior per the design.

#### Scenario: Deleting a contrato cascades dependents

- GIVEN a contrato with associated planilhas and relatorios
- WHEN the contrato is deleted
- THEN its planilhas and relatorios are deleted (CASCADE)

#### Scenario: Deleting a cargo in use is restricted

- GIVEN a cargo referenced by at least one usuario
- WHEN deleting the cargo
- THEN the database prevents the deletion (RESTRICT)

#### Scenario: Deleting an empresa nullifies optional meeting link

- GIVEN a reuniao referencing an empresa
- WHEN the empresa is deleted
- THEN `reunioes.empresa_id` becomes NULL (SET NULL)

### Requirement: Audit timestamps

The system SHALL automatically manage `created_at` and `updated_at` on domain entities.

#### Scenario: Timestamps populated and updated

- GIVEN a new row of any entity
- WHEN it is inserted
- THEN `created_at` and `updated_at` are set automatically
- AND `updated_at` changes when the row is later updated

### Requirement: Reference data seeds

The system SHALL seed `cargos` and `servicos` with the Climbe reference values via migration.

#### Scenario: Services seeded

- GIVEN migrations applied
- WHEN querying `servicos`
- THEN the 5 Climbe services are present (Contabilidade; Valuation; BPO; CFO sob Demanda; M&A)

#### Scenario: Cargos seeded

- GIVEN migrations applied
- WHEN querying `cargos`
- THEN the formal Climbe roles are present (including the Analista de Valores Imobiliários levels)

### Requirement: Initial migration via autogenerate

The system SHALL produce the initial schema migration using Alembic autogenerate from the models.

#### Scenario: Autogenerate detects all models

- GIVEN `alembic/env.py` imports `app.models`
- WHEN running `alembic revision --autogenerate`
- THEN the generated migration creates all entity tables with their columns, foreign keys and unique constraints
