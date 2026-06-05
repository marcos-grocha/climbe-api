# Agente de IA — climbe-api

Contexto persistente para o agente de IA (Claude Code) trabalhando neste repositório. **Leia antes de qualquer task.**

## Sobre o projeto

API REST do sistema de gestão de contratos da **Climbe Investimentos** (escritório de investimentos independentes). Disciplina **Residência de Software III** (UNIT + Porto Digital).

Domínio: gerenciar o ciclo de vida de contratos entre a Climbe e empresas contratantes — propostas comerciais, documentação, reuniões e relatórios — com integração ao Google Workspace.

Documentos de referência (no workspace local, fora do repo):
- `Documento Climbe Investimentos - UNIT RSIV (1).pdf` — requisitos formais
- `Novo Fluxograma Climbe.pdf` — fluxo atual (substitui o `Fluxograma Climbe.pdf` antigo)
- Diagrama ER (imagem) — base do modelo de dados

## Stack

| Camada | Tecnologia |
|---|---|
| Linguagem | Python 3.12+ |
| Web | FastAPI + Uvicorn |
| ORM | SQLAlchemy 2.x |
| Migrations | Alembic |
| Validação | Pydantic v2 |
| Banco | PostgreSQL 16 (Docker) |
| Auth | python-jose (JWT) + bcrypt |
| Google APIs | google-api-python-client |
| Testes | pytest |
| Lint/format | ruff |

App roda nativa no Windows. Banco é o único container.

## Idioma

- **Domínio (nomes de tabelas, models, campos, mensagens de erro)**: português
- **Genérico (utilitários, decoradores, libs)**: inglês
- Ex: `class Empresa(Base): ...`, `def validar_cnpj(...)` mas `def get_current_user(...)`, `class JWTBearer(...)`

## Estrutura esperada de pastas

```
app/
├── main.py                  # FastAPI entrypoint
├── config.py                # Settings (Pydantic)
├── database.py              # SQLAlchemy engine/session/Base
├── models/                  # Models SQLAlchemy (usuario.py, empresa.py, ...)
├── schemas/                 # Pydantic schemas (request/response)
├── routers/                 # Endpoints por agregado (auth.py, usuarios.py, ...)
├── services/                # Regras de negócio
├── dependencies/            # Depends do FastAPI (auth, db, perms)
└── utils/                   # Funções puras (validadores, formatadores)
```

## Convenções de código

### Naming
- `snake_case` para variáveis, funções, módulos, colunas
- `PascalCase` para classes (models, schemas)
- `UPPER_SNAKE_CASE` para constantes
- Tabelas: plural em PT (`usuarios`, `empresas`, `contratos`)
- Endpoints: plural em PT (`/usuarios`, `/empresas`)

### Type hints obrigatórios
- Toda função pública tem hints em parâmetros e retorno
- `from __future__ import annotations` no topo
- Tipos modernos: `list[str]`, não `List[str]`

### Schemas Pydantic — convenção de nomes
- `EmpresaCreate` (POST input)
- `EmpresaUpdate` (PATCH/PUT input)
- `EmpresaResponse` (output)

### Endpoints
- Sempre `response_model` e `status_code` explícitos
- Sempre `tags`
- Erros via `HTTPException` ou exception handlers globais

```python
@router.post(
    "/empresas",
    response_model=EmpresaResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["empresas"],
)
def criar_empresa(...): ...
```

### Padrão de erro
```json
{
  "detail": "Mensagem amigável em português",
  "code": "EMPRESA_CNPJ_DUPLICADO"
}
```

### Database
- Toda mudança de schema → migration Alembic (nunca `metadata.create_all()` em produção)
- Estilo SQLAlchemy 2.0: `Mapped[]` + `mapped_column()`
- FKs com `ondelete` explícito quando faz sentido
- `created_at`, `updated_at` automáticos via `default=func.now()` e `onupdate=func.now()`

## Domínio Climbe — conceitos críticos

### Cargos (oito no doc oficial)
Compliance, CEO, CSO, CMO, CFO, Membro do Conselho, Analista de Valores Imobiliários (Trainee/Junior/Pleno/Sênior), Analista de BPO Financeiro.

**Simplificação interna**: 3 papéis principais — `admin`, `analista`, `contratante` — com permissões granulares quando necessário.

### Serviços
Contabilidade, Avaliações (Valuation), BPO Financeiro, CFO sob Demanda, M&A.

### Fluxo resumido (ver "Novo Fluxograma Climbe.pdf")
1. Cadastro da empresa
2. Reunião com contratante
3. Proposta comercial (CMO/CSO/CEO/Analista/Contador)
4. Se aprovada: Compliance gera contrato
5. Solicitação de documentos (Balanço, DRE, planilhas, CNPJ, Contrato Social)
6. Validação dos documentos pelo Analista
7. Prazo de entrega definido pelo **Analista Sênior** (variável, não fixo em 30 dias)
8. Criação do relatório
9. **Revisão pelo Analista Sênior** antes da apresentação
10. Apresentação ao contratante
11. Se CFO ou BPO Financeiro: loop mensal recorrente

### Validações de domínio (não negociáveis)
- **CPF**: dígito verificador, não só regex
- **CNPJ**: dígito verificador + unicidade no banco
- **E-mail**: formato + unicidade no usuário

## Segurança

- Senhas: hash com `bcrypt` (lib `bcrypt` direta, sem passlib). **Nunca em texto plano**.
- JWT: HS256, expira em 60min por padrão
- OAuth 2.0 Google: Authorization Code Flow com PKCE
- Tokens sensíveis (Google): armazenar criptografados
- Nunca expor `JWT_SECRET` ou credenciais Google em logs/respostas
- Sempre validar permissões: `Depends(require_role(["admin"]))`

## Spec-Driven Workflow (OpenSpec)

**Toda mudança não-trivial passa por uma proposta em `openspec/changes/<id>/` ANTES de codar.**

### Roadmap

A lista de capabilities planejadas vive em [`openspec/roadmap.md`](openspec/roadmap.md). Use-a como guia da ordem das próximas propostas. **Sempre consulte o roadmap antes de propor uma capability nova.**

### Fluxo

Não usamos o OpenCode — o agente é o **Claude Code** (esta sessão). O usuário invoca cada passo conversando em PT. As ações esperadas:

| Quando o usuário pedir... | O agente faz |
|---|---|
| **"Propor `<change-id>`"** ou similar | 1. Confere o `roadmap.md` para entender escopo<br>2. Cria estrutura em `openspec/changes/<change-id>/` com `proposal.md`, `design.md`, `tasks.md`, `specs/`<br>3. Preenche cada arquivo com base no AGENTS.md + roadmap + estado atual do código<br>4. Atualiza status no roadmap para `[wip]`<br>5. Mostra os arquivos para o usuário revisar antes de aplicar |
| **"Aplicar `<change-id>`"** ou "executar" / "implementar" | 1. Lê `proposal.md` e `tasks.md` da change ativa<br>2. Cria branch `spec/<change-id>` se ainda não existe<br>3. Implementa cada task em ordem, marcando `[x]` no `tasks.md` à medida que finaliza<br>4. Cria testes pytest para cada scenario das specs<br>5. Roda `ruff check`, `ruff format`, `pytest` ao final<br>6. **Sugere mensagem de commit + corpo de PR** (regra abaixo) |
| **"Sincronizar"** ou "atualizar specs" | 1. Move/atualiza as specs em `openspec/specs/` conforme o que mudou na change<br>2. Roda `openspec validate` se disponível<br>3. Mantém a change na pasta `changes/` (ainda não arquiva) |
| **"Arquivar `<change-id>`"** ou "finalizar" | 1. Move `openspec/changes/<id>/` para `openspec/changes/archive/<id>/`<br>2. Atualiza `roadmap.md` para `[done]`<br>3. Confirma que specs/ está coerente |

A CLI do OpenSpec (`npm i -g @fission-ai/openspec`) é opcional e pode ser usada para `openspec list`, `openspec validate` e `openspec archive --sync`. O agente prefere a CLI quando disponível, mas faz tudo manual se necessário.

### Ao implementar uma change
- **Sempre** ler `proposal.md` e `tasks.md` da change ativa primeiro
- **Marcar tasks como concluídas** (`- [x]`) à medida que finaliza
- **Não desviar do escopo**; se precisar, atualizar a proposal antes
- **Criar testes** para cada scenario das specs

## Ao finalizar uma implementação

Quando você (agente) terminar de implementar uma proposta — todas as tasks marcadas como `[x]`, código rodando, `pytest` passando, `ruff check` limpo — **antes de devolver o controle pro usuário**, você DEVE sugerir, **na ordem**:

### 1. Mensagem de commit

Formato (Conventional Commits, em português):

```
<tipo>: <descrição curta no imperativo, minúscula, sem ponto final>

<corpo opcional explicando o porquê em 2-3 linhas>
```

Tipos permitidos: `feat`, `fix`, `refactor`, `style`, `docs`, `chore`, `test`, `spec`.

Exemplo:

```
feat: adiciona autenticação por email/senha com JWT

Implementa endpoint /auth/login com hash bcrypt e geração de JWT
HS256. Inclui dependency get_current_user e require_role pra RBAC.
Aplicação da proposta openspec/changes/auth-jwt.
```

### 2. Mensagem de Pull Request

Use exatamente o template em `.github/pull_request_template.md` preenchido. Pegue as issues do GitHub a fechar do campo `Closes:` da capability correspondente em `openspec/roadmap.md`. Se mais de uma issue, repete a keyword: `Closes #12, Closes #34` (não `Closes #12, #34`).

Modelo de saída (preencher e devolver pro usuário):

```markdown
## O que muda

<1-3 linhas resumindo a capability implementada>

## Tipo

- [x] feat   <!-- ou fix/refactor/etc, marcar APENAS UM -->

## Spec relacionada

- Change: `openspec/changes/<change-id>/`

## Como testar

1. <passo a passo manual>
2. <validações via Swagger /docs ou curl>

## Endpoints afetados

- `METHOD /path` — descrição curta
- ...

## Checklist

- [x] ruff check . sem erros
- [x] ruff format .
- [x] pytest verde (N testes)
- [x] Testado manualmente via /docs (Swagger)
- [x] Sem print() ou TODO órfão
- [x] Sem .env commitado
- [x] Migration Alembic criada (se aplicável)
- [x] Specs em openspec/ atualizadas
- [x] Roadmap atualizado (status mudou para [done])
- [x] Branch rebaseada com main

## Issue relacionada

Closes #X
Closes #Y
```

### Regras

- **Sempre** sugerir os dois ao terminar — não esperar o usuário pedir
- **Sempre** consultar `openspec/roadmap.md` para pegar os números reais das issues a fechar
- **Nunca** rodar `git commit` ou `git push` por conta própria — apenas sugerir o texto. O usuário commita com a assinatura dele
- Se o `Closes:` da capability estiver com `_a preencher_`, **avise o usuário** que precisa preencher os números antes de abrir a PR

## Git workflow

- `main` é estável; tudo entra via PR
- Branches: `feature/<desc>`, `fix/<desc>`, `spec/<change-id>`
- Commits em PT: `tipo: descrição no imperativo`
- Tipos: `feat`, `fix`, `refactor`, `style`, `docs`, `chore`, `test`, `spec`
- Toda PR tem 1 revisor (mesmo eu sendo solo no back, peço review do trio quando puder)

## Comandos comuns

```bash
docker compose up -d                                       # subir banco
alembic revision --autogenerate -m "descricao"             # nova migration
alembic upgrade head                                       # aplicar migrations
ruff check . && ruff format .                              # lint + format
pytest                                                     # testes
uvicorn app.main:app --reload                              # subir API
openspec list                                              # listar changes
openspec validate                                          # validar specs/changes
```

## O que NÃO fazer

- Commitar `.env` ou credenciais
- Push direto em `main`
- Criar tabelas com `metadata.create_all()` (sempre Alembic)
- Senhas em texto plano em qualquer lugar
- Endpoints sem `response_model` ou type hints
- Implementar feature sem proposta no OpenSpec
- Validar CPF/CNPJ só com regex
- Confiar em input sem schema Pydantic
- Engolir exceções silenciosamente

## Equipe

- **Tech Lead / Backend (solo)**: Marcão (este repo)
- **Frontend**: Hunald, Valtson, Gabriel (no repo `climbe-app`)

## Referências externas

- Repo do frontend: `../climbe-app`
- Docs do squad: `../climbe-app/docs/`
- OpenSpec: https://openspec.dev
