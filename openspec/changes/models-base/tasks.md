# Tasks — Models Base

## 1. Infra de models
- [x] 1.1 Criar `app/models/mixins.py` com `TimestampMixin` (`created_at`, `updated_at`)
- [x] 1.2 `app/models/__init__.py` reexporta todos os models

## 2. Referência e identidade
- [x] 2.1 `Cargo` (cargos) — nome_cargo unique
- [x] 2.2 `Servico` (servicos) — nome unique
- [x] 2.3 `Permissao` (permissoes)
- [x] 2.4 `Usuario` (usuarios) — cpf/email unique, cargo_id FK (RESTRICT)
- [x] 2.5 `UsuarioPermissao` (usuario_permissoes) — PK composta, CASCADE
- [x] 2.6 `EmpresaServico` (empresa_servico) — PK composta, CASCADE

## 3. Empresa e comercial
- [x] 3.1 `Empresa` (empresas) — cnpj unique, endereço, representante
- [x] 3.2 `Proposta` (propostas) — empresa_id, usuario_id (RESTRICT), status, data_criacao
- [x] 3.3 `Contrato` (contratos) — proposta_id (RESTRICT), data_inicio, data_fim, status

## 4. Operacional
- [x] 4.1 `Documento` (documentos) — empresa_id (CASCADE), analista_id (SET NULL), validado
- [x] 4.2 `Reuniao` (reunioes) — empresa_id nullable (SET NULL)
- [x] 4.3 `ParticipanteReuniao` (participantes_reuniao) — PK composta, CASCADE
- [x] 4.4 `Planilha` (planilhas) — contrato_id (CASCADE)
- [x] 4.5 `Relatorio` (relatorios) — contrato_id (CASCADE)
- [x] 4.6 `Notificacao` (notificacoes) — id_usuario (CASCADE)

## 5. Relacionamentos ORM
- [x] 5.1 `relationship()` nos dois lados onde útil (cargo, proposta→contrato, contrato→planilhas/relatorios, etc.)

## 6. Migration de schema
- [x] 6.1 `alembic/env.py` importa `app.models`
- [x] 6.2 `alembic revision --autogenerate -m "models base (schema inicial)"`
- [x] 6.3 Revisar a migration (15 tabelas, FKs, uniques, índices de FK)
- [x] 6.4 `alembic upgrade head` sem erros

## 7. Migration de seed
- [x] 7.1 `alembic revision -m "seed cargos e servicos"`
- [x] 7.2 upgrade: `op.bulk_insert` de servicos (5) e cargos (8)
- [x] 7.3 downgrade: remove os seeds
- [x] 7.4 `alembic upgrade head` popula as tabelas

## 8. Testes
- [x] 8.1 Schema cria as 15 tabelas (fixture + `Base.metadata`)
- [x] 8.2 Unicidade: cnpj / cpf / email duplicados levantam IntegrityError
- [x] 8.3 `ondelete`: cascade (contrato→planilhas/relatorios), restrict (cargo em uso), set null (reuniao.empresa_id)
- [x] 8.4 Seeds presentes (5 servicos e os 8 cargos)

## 9. Lint/validação
- [x] 9.1 `ruff check .` e `ruff format .`
- [x] 9.2 `pytest` verde (14 testes)
- [x] 9.3 Round-trip Alembic: `upgrade head` + `downgrade base` sem erro
