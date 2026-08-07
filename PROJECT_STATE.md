# PROJECT STATE

**Projeto:** PROTOCOLOCANBUS  
**Repositório:** `felipetbestkkj-ship-it/PROTOCOLOCANBUS`  
**Visibilidade:** pública por decisão explícita do proprietário  
**Fundação F0:** PASS — publicada e verificável  
**Governança F0.1:** PASS — operação remote-first, branches e workflows definidos  
**Fase atual:** F1 — pronta para iniciar  
**Última atualização:** 2026-08-06

## Missão atual

Investigar de forma dirigida a cadeia Car Info/HVAC a partir das evidências locais, mantendo o projeto autossuficiente e sem herança técnica de repositórios anteriores.

## Fundação concluída

A fundação estabeleceu no próprio repositório:

- `README.md` como porta de entrada técnica;
- `AGENTS.md` como contrato operacional;
- `PROJECT_STATE.md` como fotografia técnica mutável;
- `ROADMAP.md` como sequência de fases e gates;
- `EVIDENCE_INDEX.md` como inventário inicial com SHA-256;
- `DECISIONS.md` como decisões vigentes;
- `LEARNINGS.md` como aprendizado fechado;
- `REMOTE_OPERATION_POLICY.md` como contrato remote-first;
- `WORKFLOWS.md` como política didática de branches, Actions e artefatos;
- `scripts/check_governance.py` como verificador mínimo;
- `.github/workflows/governance.yml` como checagem automática com nome humano e controle de branches.

O Notion permanece como primeiro norte operacional. Codex Engineering Guardrails é carregado depois do contexto do Notion e antes da primeira ação técnica. O GitHub Connector confirma a fotografia técnica remota antes da execução.

## Ordem de entrada oficial

`Notion → Codex Engineering Guardrails → GitHub Connector → execução → GitHub atualizado → Notion sincronizado`

Estado local nunca substitui o GitHub remoto.

## Política de branches vigente

Máximo normal de **3 branches remotas ativas**:

1. `main` — estado oficial consolidado;
2. uma única `work/*` — trabalho técnico atual;
3. uma única `lab/*` — investigação temporária somente quando necessária.

Nomes:

- `work/f<fase>-<objetivo-curto>`;
- `lab/f<fase>-<pergunta-curta>`.

Não existe `develop` por padrão e não se cria branch por correção pequena.

## Workflows em linguagem simples

O GitHub Actions deve mostrar resultados compreensíveis ao proprietário.

Workflow atual:

- `✅ VERIFICAR SE O PROJETO ESTÁ ORGANIZADO`.

Nomes reservados quando essas capacidades realmente existirem:

- `📱 GERAR APK PARA INSTALAR`;
- `🧪 TESTAR APK SEM MEXER NO CARRO`;
- `🚀 PREPARAR VERSÃO FINAL`.

Quando houver APK instalável, o artefato principal deve ser autoexplicativo, preferencialmente `INSTALAR-ESTE-APK_<versao-ou-fase>_<sha-curto>.apk`.

## Próximo bloco

**F1 — Triagem orientada e mapa do Car Info/HVAC.**

Objetivo: identificar original/candidato, versões, manifesto, componentes HVAC, privilégios e dependências observadas, cruzando análise estática com baseline e runtime.

A branch técnica deverá ser criada no preflight de F1 apenas quando o bloco realmente iniciar. Nome preferido: `work/f1-hvac-mapeamento`.

### Gate de saída de F1

Entregar um mapa verificável de componentes e dependências relevantes, com perguntas prioritárias e lacunas explícitas, sem desmontagem indiscriminada e sem atuação no alvo real.

## Invariantes

- projeto novo e isolado;
- Notion + Guardrails + GitHub Connector no topo, nessa ordem operacional;
- estado oficial remoto;
- autonomia por bloco;
- sem microautorizações;
- poucas branches remotas;
- workflows/artefatos autoexplicativos;
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

## Não fazer sem evidência ou fronteira autorizada

- não importar código/governança de outro repo;
- não escolher arquitetura final de UI antes do mapa F1–F4;
- não transmitir CAN por hipótese;
- não mexer em ROM/firmware;
- não declarar assinatura/instalação compatível sem prova;
- não instalar ou modificar o equipamento real fora de bloco que inclua explicitamente essa fronteira.
