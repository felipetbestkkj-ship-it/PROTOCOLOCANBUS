# PROJECT STATE

**Projeto:** PROTOCOLOCANBUS  
**Repositório:** `felipetbestkkj-ship-it/PROTOCOLOCANBUS`  
**Visibilidade:** pública por decisão explícita do proprietário  
**Fase:** F0 — Fundação limpa  
**Estado:** PARTIAL até a fundação ser publicada neste repositório  
**Última atualização:** 2026-08-06

## Missão atual

Fundar um projeto autossuficiente, sem herança técnica de repositórios anteriores, e preparar a investigação dirigida da cadeia Car Info/HVAC.

## Próximo bloco

**F1 — Triagem orientada e mapa do Car Info/HVAC.**

Objetivo: identificar original/candidato, versões, manifesto, componentes HVAC, privilégios e dependências observadas, cruzando análise estática com baseline e runtime.

## Invariantes

- projeto novo e isolado;
- Guardrails + GitHub + Notion no topo;
- autonomia por bloco;
- sem microautorizações;
- evidência original preservada;
- nenhuma capacidade de controle é declarada por nome/string apenas;
- UI/widget futuros compartilham uma única camada de controle;
- ROM/firmware somente se camadas superiores forem insuficientes;
- alvo real só é modificado dentro de bloco que inclua explicitamente essa fronteira.

## Estado técnico conhecido

As fontes anexadas sustentam como ponto de partida:

- Car Info / `com.can.activity` como alvo central do HVAC;
- presença de material runtime e baseline da multimídia;
- tráfego observado enquadrado por `5A A5`;
- logs com componentes Jancar/CarInfo e identificador Hiworld `H1H2PAF23A-240409`;
- controle HVAC completo ainda não tratado como provado.

## Não fazer nesta fase

- não importar código/governança de outro repo;
- não escolher arquitetura final de UI antes do mapa F1–F4;
- não transmitir CAN por hipótese;
- não mexer em ROM/firmware;
- não declarar assinatura/instalação compatível sem prova.
