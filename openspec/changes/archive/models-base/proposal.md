# Proposal: Models Base

## Intent

Definir os models SQLAlchemy de **todas as entidades do domínio Climbe** conforme o Diagrama ER, gerar a **primeira migration Alembic** (autogenerate) e popular as tabelas de referência (`cargos`, `servicos`) com **seeds** iniciais. É a camada de dados sobre a qual auth, CRUDs e integrações Google serão construídos.

Sem os models não há persistência; sem a migration não há schema no banco; sem os seeds de cargos/serviços os cadastros de usuário e empresa não têm valores válidos para referenciar.

## Scope

- Models SQLAlchemy 2.x (`Mapped[]` + `mapped_column()`) das **15 entidades** do ER:
  Usuario, Cargo, Permissao, UsuarioPermissao, Empresa, Servico, EmpresaServico,
  Proposta, Contrato, Documento, Reuniao, ParticipanteReuniao, Planilha, Relatorio, Notificacao.
- Relacionamentos (FKs com `ondelete` explícito) e constraints de unicidade (CPF e e-mail do usuário, CNPJ da empresa).
- `created_at`/`updated_at` automáticos via mixin (convenção do `AGENTS.md`).
- Primeira migration Alembic gerada por autogenerate, criando todo o schema.
- Migration de **seed** para `cargos` (cargos formais) e `servicos` (5 serviços).
- Testes validando criação do schema, constraints de unicidade, comportamento de `ondelete` e presença dos seeds.

## Out of scope

- Endpoints/CRUD (vêm em `crud-usuarios`, `crud-empresas`, etc.).
- Autenticação/RBAC e seed de `permissoes` (vêm em `auth-jwt`).
- Validação de CPF/CNPJ por dígito verificador (regra de aplicação, nos CRUDs).
- Upload de arquivos e integrações Google.

## Approach

Um model por agregado em `app/models/`, todos herdando de `Base` (de `app.database`) + `TimestampMixin`. Tabelas em PT no plural e **nomes de coluna fiéis ao ER** (PK `id_<entidade>`, FK `<entidade>_id`) para casar com o que o frontend (`climbe-app`) espera. Tabelas de associação (UsuarioPermissao, EmpresaServico, ParticipanteReuniao) com **PK composta**.

`app/models/__init__.py` reexporta todos os models e `alembic/env.py` passa a importar `app.models`, para o `--autogenerate` enxergar `Base.metadata`. A migration de schema é gerada por autogenerate, revisada manualmente e aplicada. Os **seeds** entram como uma migration de dados separada (`op.bulk_insert` no upgrade, remoção no downgrade), reproduzível em qualquer ambiente via `alembic upgrade head`.

## Issues

Fecha a **#5 — Configurar SQLAlchemy + Alembic + primeira migration**. (A `#43` listada no roadmap não existe no GitHub — ver nota no roadmap; seeds de cargos/serviços são cobertos por esta change.)
