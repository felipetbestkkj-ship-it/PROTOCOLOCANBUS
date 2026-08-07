---
name: can-frame-differential-analysis
description: Analisa logs/frames CAN ou protocolos encapsulados de forma passiva, agrupando framing, periodicidade, request/response e diferenças de payload sem atribuir semântica por palpite.
---

# CAN Frame Differential Analysis

## Use quando

Há logs TX/RX ou capturas binárias e a pergunta exige identificar estrutura, diferenças ou candidatos a relação com um evento.

## Procedimento

1. Preserve o log original e registre identidade/hash quando material.
2. **Prove a camada e o transporte antes de interpretar IDs.** Determine se a captura representa CAN bruto do veículo, serial Android↔gateway/CANBOX, USB, IPC interno, encapsulamento diagnóstico ou outra camada. Se isso não estiver provado, registre a camada como aberta.
3. Identifique framing observado (por exemplo prefixos, comprimento, ID/comando, payload, checksum candidato) sem assumir protocolo além do que os bytes sustentam.
4. Separe TX e RX e normalize a timeline.
5. Agrupe frames por comprimento/campo estável/ID candidato.
6. Meça periodicidade e repetição; diferencie polling de evento espontâneo quando a evidência permitir.
7. Compare janelas antes/durante/depois do evento-alvo.
8. Marque bytes/campos constantes e variantes.
9. Procure pares request/response por tempo e estrutura, sem chamar correlação de causalidade automaticamente.
10. Teste hipóteses de checksum/contador somente quando houver amostras suficientes; registre hipóteses rejeitadas também quando útil.
11. Cruze com `runtime-static-correlation` antes de atribuir significado funcional específico.

## Saída mínima

```text
Camada/transporte confirmado/provável:
Framing confirmado/provável:
Grupos de mensagem:
Periodicidade:
Pares request/response candidatos:
Campos constantes:
Campos variantes:
Correlação temporal:
Hipóteses de semântica:
Hipóteses descartadas:
Próxima evidência discriminatória:
```

## Regras de evidência

- **command ID de gateway/protocolo encapsulado não é automaticamente CAN arbitration ID do veículo**;
- só chamar algo de “CAN ID do veículo” quando a captura da camada CAN inferior ou outra evidência direta sustentar isso;
- um byte variar junto com uma ação uma vez não prova comando;
- ID/nome encontrado em string ou log não prova semântica física;
- frame repetitivo pode ser polling/keepalive/estado e não comando;
- significado deve ser promovido somente após correlação repetível ou evidência independente convergente.

## Limites

Esta skill é **passiva por padrão**. Não transmite, replaya nem atua via CAN. Qualquer estímulo ativo no alvo real exige a fronteira material prevista em `AGENTS.md`.