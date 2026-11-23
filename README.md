# TechFlow Tasks

Sistema web de gerenciamento de tarefas com quadro Kanban, desenvolvido pela **TechFlow Solutions** (empresa fictícia) para uma startup de logística que precisa acompanhar o fluxo de trabalho da equipe em tempo real.

Projeto acadêmico da disciplina de Engenharia de Software.

## Objetivo

Permitir que uma equipe crie, acompanhe, edite e conclua tarefas em um quadro visual, com validação de dados, testes automatizados e integração contínua.

## Escopo inicial

- CRUD de tarefas (título, descrição e status)
- Quadro Kanban com as colunas **A Fazer**, **Em Progresso** e **Concluído**
- API REST em JSON
- Testes automatizados (unitários e de API)
- Pipeline de CI no GitHub Actions

Fora do escopo inicial: autenticação, múltiplos usuários e notificações.

## Metodologia

Kanban, com ciclos curtos inspirados no Scrum. Todas as atividades viram cards no GitHub Projects (A Fazer, Em Progresso, Concluído) e cada entrega é registrada em commits semânticos (`feat`, `fix`, `test`, `docs`, `ci`, `chore`).

## Como executar

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
python src/run.py
```

Acesse http://127.0.0.1:5000. O banco SQLite (`techflow.db`) é criado automaticamente.

## Testes e qualidade

```bash
flake8 src tests
pytest --cov=src/techflow
```

O mesmo fluxo roda a cada push e pull request no GitHub Actions (`.github/workflows/ci.yml`).

## API

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/api/tasks` | Lista tarefas ordenadas por prioridade (filtros `?status=` e `?priority=`) |
| POST | `/api/tasks` | Cria tarefa |
| GET | `/api/tasks/<id>` | Busca tarefa |
| PUT | `/api/tasks/<id>` | Atualiza tarefa (parcial) |
| DELETE | `/api/tasks/<id>` | Remove tarefa |

## Estrutura

```
src/techflow/   código da aplicação
tests/          testes automatizados
docs/           diagramas UML
.github/        pipeline de CI
```

## Gestão de mudanças

**Mudança de escopo: prioridade das tarefas.**

Após a primeira entrega, o cliente (startup de logística) pediu para destacar e tratar primeiro as tarefas críticas, algo que o escopo inicial não previa.

- **Mudança:** cada tarefa passa a ter prioridade (`low`, `medium`, `high`, `critical`), com padrão `medium`; o quadro ordena por prioridade e a API e a interface permitem filtrar.
- **Justificativa:** atende diretamente ao objetivo do cliente de priorizar tarefas críticas, com baixo custo por reaproveitar o CRUD existente.
- **Impacto:** novo campo no banco (com migração automática para bancos já existentes), validação, API, interface e testes.
- **Kanban:** novos cards "Adicionar prioridade às tarefas" e "Migração do banco para a coluna priority" criados na coluna A Fazer e movidos até Concluído.
- **Principal desafio:** não quebrar dados já criados. Resolvido com migração que adiciona a coluna quando ela não existe e com testes cobrindo o cenário.
