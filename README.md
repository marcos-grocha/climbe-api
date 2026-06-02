# climbe-api

API REST do sistema de gestão de contratos da **Climbe Investimentos**. Pareada com o frontend [`climbe-app`](../climbe-app).

Desenvolvida com **Spec-Driven Development** usando OpenSpec — propostas, design e tasks ficam versionadas em `openspec/` e dirigem a implementação. O agente de IA que aplica as propostas é o **Claude Code** (não usamos OpenCode neste projeto).

## Stack

- **Python** 3.12+
- **FastAPI** — framework web async
- **SQLAlchemy** 2.x + **Alembic** — ORM e migrations
- **PostgreSQL** 16 — banco (rodando em Docker)
- **Pydantic** v2 — validação e schemas
- **python-jose** + **passlib** — JWT e hash de senha
- **google-api-python-client** — Drive, Calendar, Gmail
- **pytest** — testes

## Pré-requisitos

- Python 3.12+
- Docker (apenas para o banco)
- Node.js 20.19+ (para a CLI do OpenSpec — opcional mas recomendado)

## Setup

```bash
git clone <url-do-repo>
cd climbe-api

# 1) Subir o banco
docker compose up -d

# 2) Configurar variáveis de ambiente
cp .env.example .env
# (edite .env, principalmente JWT_SECRET)

# 3) Criar virtualenv e instalar deps
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
# source .venv/bin/activate

pip install -r requirements.txt

# 4) Rodar migrations (depois da primeira proposal aplicada)
alembic upgrade head

# 5) Subir a API
uvicorn app.main:app --reload
```

API em `http://localhost:8000`. Docs interativos em `http://localhost:8000/docs`.

> Algumas etapas (alembic, `app/`) só funcionam **após aplicar a primeira proposta `bootstrap-api`**.

## Ferramentas de IA

### OpenSpec CLI (opcional)

```bash
npm install -g @fission-ai/openspec
```

A CLI ajuda em comandos como `openspec list`, `openspec validate` e `openspec archive --sync`. Não é obrigatória — a estrutura `openspec/` é só pasta + markdown e dá pra trabalhar sem ela.

### Claude Code (este repo)

O agente que aplica as propostas é o Claude Code. O contexto, padrões e regras de execução vivem em [`AGENTS.md`](AGENTS.md). O fluxo de proposta → aplicação → arquivamento é descrito em texto natural — você pede no chat ("propõe `crud-empresas`", "aplica `bootstrap-api`", "arquiva") e o agente segue o protocolo definido em `AGENTS.md`.

## Spec-Driven Workflow

Toda mudança de comportamento passa por uma proposta antes do código:

1. **Propor** — você pede ao agente: "propõe `<change-id>`". O agente cria `openspec/changes/<id>/` com `proposal.md`, `design.md`, `tasks.md` e diffs de specs, baseando-se no contexto do projeto e no `roadmap.md`.
2. **Revisar** — você lê e ajusta os artefatos (proposal/design/tasks). É a fase mais importante.
3. **Aplicar** — você pede: "aplica `<change-id>`". O agente implementa task por task, rodando lint e testes ao final, e sugere mensagem de commit + corpo de PR.
4. **Sincronizar** — você pede: "sincroniza". O agente atualiza `openspec/specs/` com as mudanças que se tornaram permanentes.
5. **Arquivar** — você pede: "arquiva `<change-id>`". O agente move a change para `openspec/changes/archive/` e atualiza o roadmap.

As specs vivem em `openspec/specs/` e são **a fonte da verdade** do comportamento esperado da API.

## Estrutura do repositório

```
climbe-api/
├── app/                    # código da aplicação (criado após bootstrap-api)
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models/             # modelos SQLAlchemy
│   ├── schemas/            # modelos Pydantic
│   ├── routers/            # endpoints FastAPI
│   ├── services/           # regras de negócio
│   └── dependencies/       # dependências FastAPI (auth, db, etc.)
├── alembic/                # migrations
├── tests/                  # testes pytest
├── openspec/               # specs e propostas (spec-driven)
│   ├── specs/              # specs ativas (fonte da verdade)
│   ├── changes/            # propostas em andamento
│   └── roadmap.md          # lista de capabilities planejadas
├── .github/                # PR template
├── docker-compose.yml      # apenas PostgreSQL
├── AGENTS.md               # contexto e regras para o agente de IA
├── requirements.txt
└── README.md
```

## Comandos comuns

```bash
# Testes
pytest

# Lint/format
ruff check .
ruff format .

# Migration nova
alembic revision --autogenerate -m "descricao"
alembic upgrade head

# Subir api em produção (sem reload)
uvicorn app.main:app --host 0.0.0.0 --port 8000

# OpenSpec
openspec list
openspec validate
```

## Documentação relacionada

- [AGENTS.md](AGENTS.md) — contexto e padrões para o agente de IA
- [openspec/roadmap.md](openspec/roadmap.md) — capabilities planejadas
- [Frontend (climbe-app)](../climbe-app)
- [Docs do squad](../climbe-app/docs/) — padrões de código, fluxo git, roadmap
