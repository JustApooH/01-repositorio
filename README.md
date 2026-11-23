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
