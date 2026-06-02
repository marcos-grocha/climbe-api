# OpenSpec Roadmap — climbe-api

Lista de capabilities planejadas para a API. **Não são specs detalhadas** — só um guia da ordem em que pretendemos implementar.

## Como usar

- A lista abaixo mostra a **ordem aproximada** das próximas propostas.
- Cada capability vira uma pasta `openspec/changes/<id>/` completa (com `proposal.md`, `design.md`, `tasks.md`, `specs/`) **só quando for hora de implementar** — não criamos tudo upfront.
- Mudanças de prioridade são esperadas. Atualize este arquivo quando isso acontecer.
- O campo **`Closes:`** de cada capability lista as issues do GitHub Projects que serão fechadas quando a PR daquela capability for mergeada. Use os números aqui ao montar o `Closes #N` na PR (ver [AGENTS.md > Ao finalizar uma implementação]).
- Os números abaixo refletem a numeração da lista original de 44 issues sugeridas. Se as suas issues no GitHub tiverem outros números, ajuste aqui.

## Convenção de status

| Status | Significado |
|---|---|
| `[done]` | Aplicada e arquivada (movida para `openspec/changes/archive/`) |
| `[wip]` | Proposta criada em `changes/`, sendo implementada |
| `[todo]` | Planejada — ainda só nesta lista |

---

## Semana 1 — Fundação

### `[wip]` bootstrap-api
> Aplicação FastAPI rodando, conexão PostgreSQL via SQLAlchemy 2.x + Alembic configurado, health checks (`/health` e `/health/db`), CORS para o frontend, estrutura de pastas modular, ruff configurado.

**Pasta:** `changes/bootstrap-api/`
**Closes:** #3, #4

### `[todo]` models-base
> Models SQLAlchemy de **todas** as entidades do diagrama ER (Usuario, Cargo, Empresa, Servico, EmpresaServico, Proposta, Contrato, Documento, Reuniao, ParticipanteReuniao, Planilha, Relatorio, Permissao, UsuarioPermissao, Notificacao). Primeira migration Alembic gerada com autogenerate. Seeds de cargos e serviços iniciais.

**Closes:** #5, #43

### `[todo]` auth-jwt
> Login por email/senha. Hash bcrypt via passlib. JWT HS256 com expiração 60min. Endpoints `/auth/login`, `/auth/me`. Dependency `get_current_user`. RBAC básico com `require_role(["admin", "analista"])`. Exception handlers globais para 401/403.

**Closes:** #6, #10

### `[todo]` crud-usuarios
> CRUD de usuário (`/usuarios`). Validação de CPF com dígito verificador. Email único. Vínculo com cargo. Apenas admin cadastra. Endpoint de mudança de senha. Soft delete via campo `situacao` (ativo/inativo).

**Closes:** #7, #8

### `[todo]` crud-empresas
> CRUD de empresa (`/empresas`). Validação de CNPJ (dígito verificador + unicidade no banco). Endereço completo (logradouro, número, bairro, cidade, UF, CEP). Dados do representante legal (nome, CPF, contato). Vínculo com serviços contratados (M:N via `empresa_servico`).

**Closes:** #9

---

## Semana 2 — Núcleo do negócio

### `[todo]` crud-propostas
> CRUD de proposta comercial. Status: `rascunho` → `enviada` → `aprovada`/`recusada`. Apenas cargos autorizados criam (CMO, CSO, CEO, Analista, Contador). Endpoints `/propostas/{id}/aprovar` e `/propostas/{id}/recusar` com permissionamento. Notificação automática aos envolvidos.

**Closes:** #19

### `[todo]` crud-contratos
> Contrato gerado automaticamente quando proposta é aprovada pela Compliance (signal/event handler). Campos: `data_inicio`, `data_fim`, `prazo_entrega` (variável, definido pelo Analista Sênior — conforme Novo Fluxograma). Flag `recorrente` para serviços CFO/BPO. Status: `ativo`, `encerrado`.

**Closes:** #20

### `[todo]` documentos
> Upload de documentos (multipart/form-data). Storage local em `uploads/{contrato_id}/{tipo}/`. Tipos obrigatórios: Balanço, DRE, planilhas gerenciais, CNPJ, Contrato Social. Validação pelo analista responsável (`/documentos/{id}/validar` e `/reprovar`). Status: `pendente` → `valido`/`invalido` (com observação).

**Closes:** #21, #22

### `[todo]` auth-google
> OAuth 2.0 com Google (Authorization Code Flow com PKCE). Endpoint `/auth/google/callback`. Se usuário não existe, cria com status `pendente_aprovacao` e notifica admin via email + in-app. Armazena `access_token` e `refresh_token` criptografados (Fernet) — serão usados nas integrações Google posteriores.

**Closes:** #23

---

## Semana 3 — Integrações Google e polimento

### `[todo]` agendamento-reunioes
> CRUD de reunião (`/reunioes`). Verificação de disponibilidade dos participantes e da sala (para presencial). Integração com Google Calendar: cria evento real no Calendar do organizador usando o `access_token` armazenado em `auth-google`. Envia convites.

**Closes:** #29

### `[todo]` google-drive
> Quando contrato é criado, cria pasta no Drive (`/Climbe/Contratos/{empresa}/{contrato_id}/`). Upload dos documentos do contrato pra essa pasta. Permissões de leitura para o analista chefe e participantes do contrato.

**Closes:** #31

### `[todo]` notificacoes
> Endpoints `/notificacoes` (lista do usuário logado) e `/notificacoes/{id}/lida`. Trigger automático em eventos: nova proposta, contrato aprovado, doc inválido, reunião marcada, vencimento próximo de qualquer prazo. Envio de email — primeira tentativa via Gmail API (com OAuth do usuário), fallback SMTP do Gmail com App Password.

**Closes:** #30, #32

### `[todo]` relatorios-pdf
> Criação de relatório de contrato. Status: `pendente` → `revisao_senior` → `aprovado` (conforme Novo Fluxograma, há revisão do Analista Sênior). Geração de PDF server-side com WeasyPrint ou ReportLab. Anexa ao contrato. Endpoint `/relatorios/{id}/pdf` para download.

**Closes:** #44

---

## Capabilities provavelmente WON'T

Se o tempo apertar, estas ficam pra fora:

- `google-sheets` — não está no caminho crítico do fluxo
- `notificacoes-tempo-real` (websocket) — usar polling de 30s no front
- `permissoes-granulares-por-cargo` — simplificar com 3 papéis (admin/analista/contratante)
- `audit-trail-completo` — versionamento de mudanças em contratos

---

## Issues que NÃO fecham via capability do backend

Algumas issues da lista original não correspondem 1:1 a uma capability do backend e devem ser tratadas separadamente:

- **#1** Criar repositório `climbe-api` no GitHub — já feito manualmente
- **#2** Configurar Google Cloud Console — pré-requisito externo (não é código). Fechar manualmente quando concluir
- **#11 a #18** — issues do frontend (não pertencem ao backend)
- **#24 a #28** — issues do frontend
- **#33 a #37** — issues do frontend
- **#38** Teste manual end-to-end — fechar manualmente após validação
- **#39** Atualizar README de execução — fechar com a PR que finalizar
- **#40** Deploy mínimo — capability avulsa de operação (não está no roadmap)
- **#41** Vídeo demo de backup — manual
- **#42** Preparar slides — manual

---

## Como manter este arquivo

- **Ao criar uma proposta** (você pediu "propõe X" ao agente): mudar status para `[wip]` aqui
- **Ao arquivar uma proposta** (você pediu "arquiva X"): mudar para `[done]` aqui
- **Ao criar/renumerar issues no GitHub**: ajustar o campo `Closes:` da capability correspondente
- **Se escopo expandir**: ajustar o resumo da capability aqui também
- **Descobriu algo novo**: adicionar capability no fim da seção correspondente
- Este arquivo é **commitado normalmente** com cada PR de proposta
