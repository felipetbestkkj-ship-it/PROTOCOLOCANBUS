# F3.1 — Prontidão para implementação HVAC

## O que este bloco muda na prática

Antes:

```text
muito conhecimento técnico
        ↓
ainda difícil responder “o que já posso construir?”
```

Depois deste bloco:

```text
catálogo do protocolo HVAC
        ↓
perfil real do veículo-alvo
        ↓
contrato legível por máquina
        ↓
validador + testes
        ↓
rascunho de contrato F4
        ↓
arquitetura F5 já ranqueada
        ↓
1 único gate físico restante
```

## Correção de alvo — 07/08/2026

O proprietário confirmou que **o veículo-alvo possui apenas desembaçador dianteiro; não possui desembaçador traseiro**.

Isso corrige uma inferência anterior: o `HdPsaProtocol` possuir property/bit/subcomando rotulados como `rear_defrost` prova uma **capacidade do protocolo genérico**, não uma função física do veículo-alvo.

A partir desta correção:

- `contracts/hvac_behavior_contract.json` continua sendo o catálogo genérico de operações do protocolo;
- `contracts/hvac_target_profile.json` é a camada que diz o que é realmente aplicável ao alvo;
- rear-defrost fica `NOT_PRESENT_ON_TARGET` no perfil do alvo;
- a transição observada do bit genérico continua preservada como dado de runtime, mas não é atribuída a rear-defrost físico;
- o gate físico único passa a ser **recirculação OFF→ON**.

## Painel de prontidão

| Camada | Situação |
|---|---|
| Entender componentes Car Info | 🟢 fechado |
| Caminho UI → backend | 🟢 fechado |
| Protocolo Hiworld / framing/checksum | 🟢 fechado |
| Builder dos comandos HVAC | 🟢 fechado |
| Parser do estado HVAC | 🟢 fechado |
| Gêmeo digital/fake CANBOX | 🟢 fechado |
| Catálogo de operações do protocolo | 🟢 criado e validado offline |
| Perfil real do veículo-alvo | 🟢 criado; rear-defrost explicitamente ausente |
| Arquitetura futura | 🟡 candidato líder definido, ainda não promovido |
| Elo físico comum `0x3B → veículo → 0x31` | 🔴 1 teste pendente |
| Nova camada de controle / UI | ⚪ ainda não iniciada por desenho |

## Cobertura do contrato

O protocolo genérico continua expondo 18 operações catalogadas. Isso **não significa que todas as 18 existam fisicamente neste carro**.

Essa distinção agora é obrigatória:

```text
CAPACIDADE DO PROTOCOLO
          ≠
CAPACIDADE DO VEÍCULO-ALVO
```

Para o alvo já confirmado:

- desembaçador dianteiro: **presente**;
- desembaçador traseiro: **ausente**;
- rear-defrost genérico do protocolo: preservado apenas como capacidade/bit do protocolo, não como feature do carro.

## Critério para sair da F3

```text
recirculação inicialmente OFF
        ↓
recirculação ON na UI original
        ↓
TX 5A A5 02 3B 07 00 43
        ↓
ACK
        ↓
RX 0x31 payload[1] bit4: 0→1
        ↓
estado da UI coerente
        ↓
F3 fecha
```

A recirculação foi escolhida porque já existe uma transição real de **campo único** nos logs e porque é uma função efetivamente aplicável ao HVAC do alvo. O desembaçador dianteiro existe, mas sua transição observada é composta e portanto é menos discriminatória como teste de infraestrutura.

Se passar, promover o rascunho `docs/F4_BEHAVIOR_CONTRACT_DRAFT.md` para contrato oficial e seguir para F5. Se divergir, usar somente aquela captura para análise offline.

## Próxima construção provável depois do gate

A evidência atual favorece uma arquitetura onde **nossa UI/widget são próprios, mas o Car Info permanece temporariamente como backend Binder invisível**. Isso evita reimplementar a serial Hiworld antes de existir motivo.

Detalhe: `docs/F5_ARCHITECTURE_READINESS_DRAFT.md`.
