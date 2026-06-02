<!--
  Antes de abrir, leia ../climbe-app/docs/03-fluxo-git.md (compartilhado entre repos).
  Preencha as seções abaixo e apague o que não se aplicar.
-->

## O que muda

<!-- O que essa PR faz e por quê, em 1-3 linhas. -->



## Tipo

<!-- Marque com [x] o tipo principal. -->

- [ ] feat — nova funcionalidade
- [ ] fix — correção de bug
- [ ] refactor — refatoração sem mudança de comportamento
- [ ] style — formatação, sem mudança de lógica
- [ ] docs — apenas documentação
- [ ] chore — config, dependências, build
- [ ] test — testes
- [ ] spec — proposta ou ajuste de spec do OpenSpec (sem código)

## Spec relacionada

<!-- Se a PR aplica uma mudança proposta no OpenSpec, aponte para a pasta da change. -->

- Change: `openspec/changes/<change-id>/`

## Como testar

<!-- Passo a passo para o revisor validar manualmente. -->

1. 
2. 

## Endpoints afetados

<!-- Liste se houve mudança na API. Apague se não aplicável. -->

- `GET /...`
- `POST /...`

## Checklist

- [ ] Rodei `ruff check .` (sem erros)
- [ ] Rodei `ruff format .`
- [ ] Rodei `pytest` (todos passaram)
- [ ] Testei manualmente via `/docs` (Swagger)
- [ ] Não deixei `print()` ou TODO órfão
- [ ] Não commitei `.env` ou credenciais
- [ ] Se mexeu no banco: criei migration Alembic
- [ ] Atualizei specs em `openspec/` quando aplicável
- [ ] Atualizei `openspec/roadmap.md` (status `[wip]`/`[done]` da capability)
- [ ] Branch rebaseada com `main`

## Issue relacionada

<!--
  Vincula a PR à task no GitHub Projects.
  Use "Closes" para fechar a issue AUTOMATICAMENTE quando esta PR for mergeada.
  Outras keywords aceitas: Fixes, Resolves.
  Múltiplas issues: "Closes #12, Closes #34" (repete a keyword, não "Closes #12, #34")
  Pega os números do campo `Closes:` da capability em `openspec/roadmap.md`.
-->

Closes #
