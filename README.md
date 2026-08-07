# PROTOCOLOCANBUS

Projeto iniciado do zero para investigar e reconstruir de forma controlada a integração entre a multimídia Android, Car Info/Jancar/Hiworld e recursos automotivos, começando pelo HVAC.

## Fontes oficiais

- **GitHub:** fonte técnica versionada.
- **Notion:** norte operacional, roadmap, decisões, aprendizados e handoff.
- **Codex Engineering Guardrails:** método obrigatório para análise e mudança.

Este repositório **não herda código, governança, estado, decisões ou dependências de projetos anteriores**.

## Objetivo do primeiro ciclo

Chegar a uma arquitetura em que uma nova UI HVAC e um widget compartilhem uma única camada de controle, preservem o comportamento comprovado do sistema, reflitam o estado real, tenham build/testes/rollback reproduzíveis e possam ser validados no equipamento real quando autorizado.

## Onde começar

Leia, nesta ordem:

1. `AGENTS.md`
2. `PROJECT_STATE.md`
3. `ROADMAP.md`
4. `EVIDENCE_INDEX.md`
5. `DECISIONS.md`
6. `LEARNINGS.md`

A instrução personalizada e o estado humano do projeto ficam na Central Oficial do Notion.
