# Design — Models Base

## Fonte da verdade

Diagrama ER (imagem em `squad-x/`) + Documento de Requisitos v1.1 (RSIV). Nomes de tabela e coluna seguem o ER **literalmente** para casar com o frontend (`climbe-app`), construído a partir do mesmo ER.

## Convenções de modelagem

- SQLAlchemy 2.0: `class X(Base, TimestampMixin)` com `Mapped[...]` + `mapped_column(...)`.
- PK: `id_<entidade>` (INT, autoincrement) — como no ER.
- FK: `<entidade>_id` (ex.: `cargo_id`, `empresa_id`) — como no ER.
- Tipos: VARCHAR→`String(n)`, CHAR→`String(n)`, DATE→`Date`, TIME→`Time`, BOOLEAN→`bool`, TEXT→`Text`.
- Um arquivo por agregado em `app/models/`.

## Mapa de entidades (campos-chave do ER)

| Tabela | Campos | FKs (ondelete) |
|---|---|---|
| `cargos` | id_cargo, nome_cargo (unique) | — |
| `servicos` | id_servico, nome (unique) | — |
| `permissoes` | id_permissao, descricao | — |
| `usuarios` | id_usuario, nome_completo, cpf (unique), email (unique), contato, situacao, senha_hash | cargo_id → cargos (RESTRICT) |
| `usuario_permissoes` | (id_usuario, id_permissao) PK composta | ambos CASCADE |
| `empresas` | id_empresa, razao_social, nome_fantasia, cnpj (unique), logradouro, numero, bairro, cidade, uf, cep, telefone, email, representante_nome, representante_cpf, representante_contato | — |
| `empresa_servico` | (id_empresa, id_servico) PK composta | ambos CASCADE |
| `propostas` | id_proposta, status, data_criacao | empresa_id → empresas (RESTRICT), usuario_id → usuarios (RESTRICT) |
| `contratos` | id_contrato, data_inicio, data_fim (null), status | proposta_id → propostas (RESTRICT) |
| `documentos` | id_documento, tipo_documento, url, validado | empresa_id → empresas (CASCADE), analista_id → usuarios (SET NULL, null) |
| `reunioes` | id_reuniao, titulo, data, hora, presencial, local (null), pauta (null), status | empresa_id → empresas (SET NULL, null) |
| `participantes_reuniao` | (id_reuniao, id_usuario) PK composta | ambos CASCADE |
| `planilhas` | id_planilha, url_google_sheets, bloqueada, permissao_visualizacao | contrato_id → contratos (CASCADE) |
| `relatorios` | id_relatorio, url_pdf, data_envio | contrato_id → contratos (CASCADE) |
| `notificacoes` | id_notificacao, mensagem, data_envio, tipo | id_usuario → usuarios (CASCADE) |

## Decisões e trade-offs

### 1. created_at / updated_at em todas as entidades (além do ER)
O ER não tem timestamps de auditoria, mas o `AGENTS.md` os exige. Adiciono via `TimestampMixin` (`default=func.now()`, `onupdate=func.now()`). Mantenho também os campos de data do ER (`data_criacao`, `data_envio`) por serem **datas de domínio**, distintas da auditoria.
> ⚠️ **Confirmar no review:** adicionar timestamps mesmo não estando no ER.

### 2. status/validado como String (VARCHAR), não Enum nativo
O ER usa VARCHAR. Mantenho `String` por fidelidade e simplicidade da migration; valores válidos documentados (constantes/Enum de aplicação virão nos CRUDs):
- `proposta.status`: rascunho → enviada → aprovada / recusada
- `contrato.status`: ativo / encerrado
- `documento.validado`: pendente → valido / invalido
- `reuniao.status`: agendada / realizada / cancelada

### 3. Unicidade
`usuarios.cpf`, `usuarios.email`, `empresas.cnpj` → `unique=True` (requisitos 9b e 10c). Validação de dígito verificador fica na camada de aplicação (CRUDs).

### 4. Nulabilidade notável
`reunioes.empresa_id` (req "Empresa se houver"), `documentos.analista_id` (atribuído na validação) e `contratos.data_fim` (contrato em aberto) são nullable. Demais FKs/identificadores: NOT NULL.

### 5. Seeds (cargos e servicos)
Migration de dados separada, após o schema.
- **servicos** (5, req 2): Contabilidade; Avaliações de Empresas (Valuation); Terceirização de Rotinas Financeiras (BPO); Diretoria Financeira Sob Demanda (CFO); Fusões & Aquisições (M&A).
- **cargos** (8, req 1): Compliance; CEO; Membro do Conselho; CSO; CMO; CFO; Analista de Valores Imobiliários; Analista de BPO Financeiro. A *Analista de Valores Imobiliários* fica como **cargo único** (decidido); os níveis Trainee/Júnior/Pleno/Sênior viram outro conceito (campo `nivel` ou permissão) numa change futura.

### 6. Relacionamentos ORM
`relationship()` nos dois lados onde útil (`Usuario.cargo`, `Empresa.servicos` via `secondary`, `Contrato.proposta`, etc.). Não adicionam colunas; facilitam os CRUDs.

## Estratégia de testes

DB de teste = Postgres do Docker. Fixture cria o schema via `Base.metadata.create_all()` numa transação com rollback ao fim (`create_all` é aceitável **em teste**; produção usa Alembic). Seeds testados aplicando a migration ou inserindo no fixture.

## Migration

1. `alembic/env.py` passa a `import app.models` (autogenerate enxerga `Base.metadata`).
2. `alembic revision --autogenerate -m "models base (schema inicial)"` → **revisar** o arquivo gerado.
3. `alembic revision -m "seed cargos e servicos"` com `op.bulk_insert` (upgrade) e remoção (downgrade).
4. `alembic upgrade head`.

## Arquivos a criar/alterar

- `app/models/`: `mixins.py`, `cargo.py`, `usuario.py`, `permissao.py`, `empresa.py`, `servico.py`, `proposta.py`, `contrato.py`, `documento.py`, `reuniao.py`, `planilha.py`, `relatorio.py`, `notificacao.py`, `__init__.py`
- `alembic/env.py` (importa `app.models`)
- `alembic/versions/*_models_base_schema_inicial.py`, `alembic/versions/*_seed_cargos_e_servicos.py`
- `tests/test_models.py`
