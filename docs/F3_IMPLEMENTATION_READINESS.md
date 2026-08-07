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
18 operações HVAC
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

## Painel de prontidão

| Camada | Situação |
|---|---|
| Entender componentes Car Info | 🟢 fechado |
| Caminho UI → backend | 🟢 fechado |
| Protocolo Hiworld / framing/checksum | 🟢 fechado |
| Builder dos comandos HVAC | 🟢 fechado |
| Parser do estado HVAC | 🟢 fechado |
| Gêmeo digital/fake CANBOX | 🟢 fechado |
| Contrato de 18 operações | 🟢 criado e validado offline |
| Arquitetura futura | 🟡 candidato líder definido, ainda não promovido |
| Elo físico comum `0x3B → veículo → 0x31` | 🔴 1 teste pendente |
| Nova camada de controle / UI | ⚪ ainda não iniciada por desenho |

## Cobertura do contrato

O validador atual reporta:

- **18** operações de controle catalogadas;
- **14** com vetores estáticos completos de frame;
- **2** com transição runtime de campo único (`rear_defrost`, `recirculation`);
- **5** com campos observados em transições compostas;
- **11** sem transição de controle observada, porém mapeadas pelo código original;
- **18/18** ainda compartilham o mesmo elo físico `PHYSICAL_PENDING`.

Isso não significa “18 testes no carro”. Significa exatamente o contrário: existe **um elo de transporte comum** a validar; por isso o gate físico escolhido continua sendo um único rear-defrost ON.

## Critério para sair da F3

```text
rear-defrost ON na UI original
        ↓
TX 5A A5 02 3B 06 01 43
        ↓
ACK
        ↓
RX 0x31: rear_defrost 0→1
        ↓
efeito físico coerente
        ↓
F3 fecha
```

Se passar, promover o rascunho `docs/F4_BEHAVIOR_CONTRACT_DRAFT.md` para contrato oficial e seguir para F5. Se divergir, usar somente aquela captura para análise offline.

## Próxima construção provável depois do gate

A evidência atual favorece uma arquitetura onde **nossa UI/widget são próprios, mas o Car Info permanece temporariamente como backend Binder invisível**. Isso evita reimplementar a serial Hiworld antes de existir motivo.

Detalhe: `docs/F5_ARCHITECTURE_READINESS_DRAFT.md`.
