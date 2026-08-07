# F3 — Gêmeo digital offline do HVAC Hiworld/Peugeot

## Resultado executivo

O gêmeo digital existe para reduzir a dependência do carro a **uma validação final discriminatória**, em vez de uma sessão de tentativa e erro.

Ele combina:

1. código original decompilado do Car Info/HdPsaProtocol;
2. runtime real já capturado em `candata_8.log`;
3. método genérico de engenharia reversa de protocolos aplicado e verificado nas evidências deste projeto.

## Correção de alvo — capacidade do protocolo ≠ função do carro

Em 07/08/2026 o proprietário reafirmou que **o veículo-alvo possui apenas desembaçador dianteiro; não possui desembaçador traseiro**.

Isso corrige a interpretação anterior do gêmeo:

- o `HdPsaProtocol` possui property/bit/subcomando genérico chamado `rear_defrost`;
- o trace real mostra esse bit alternando;
- **isso não prova rear-defrost físico no alvo**, porque a função não existe no veículo;
- o nome permanece no código do gêmeo somente para espelhar o parser genérico original;
- a semântica física daquele bit neste alvo é considerada **indeterminada/não aplicável**.

Perfil autoritativo do alvo: `contracts/hvac_target_profile.json`.

## 1. Caminho da UI

A UI HVAC possui command/property mode e keycode-mode. Para a configuração Peugeot/Hiworld ativa, a property list do `HdPsaProtocol` não injeta IDs especiais `> 61440`, portanto a UI permanece em command/property mode:

`HvacFragment → property normal → HvacModel → setHvacProperty → HdPsaProtocol.buildHvacPackets → 0x3B`

Assim, a ausência de `0x3B` durante os pushes de `candata_8` não pode ser explicada por keycode-mode oculto da própria tela Peugeot.

## 2. Vocabulário modelado

Framing:

`5A A5 <LEN> <CMD> <DATA...> <CHECKSUM>`

Checksum:

`(sum(bytes de LEN até último DATA) - 1) & 0xFF`

Controle HVAC:

`5A A5 02 3B <SUBCOMANDO> <VALOR> <CHECKSUM>`

Estado HVAC:

`0x31`, com decode/encode byte a byte e round-trip exato dos oito estados reais.

O gêmeo replica regras importantes do builder: recirculação invertida no fio, fan/temperatura incrementais, airflow diferencial e supressões dependentes do estado.

## 3. Gramática observada — rótulos revisados

Os oito estados lógicos reais continuam válidos. O que mudou é a interpretação da transição do bit que o parser genérico chama `rear_defrost`.

| passo | interpretação atual | confiança | observação |
|---:|---|---:|---|
| 1 | `FRONT_DEFROST_ON` | 0,90 | inferência composta; função existe no alvo |
| 2 | `PROTOCOL_REAR_DEFROST_BIT_ON` | 1,00 para o bit / **sem semântica física atribuída ao alvo** | único bit do parser genérico mudou |
| 3 | `FRONT_DEFROST_OFF` | 0,86 | inferência composta |
| 4 | `PROTOCOL_REAR_DEFROST_BIT_OFF` | 1,00 para o bit / **sem semântica física atribuída ao alvo** | único bit do parser genérico mudou |
| 5 | `RECIRCULATION_ON` | 0,995 | único campo alterado e função aplicável ao alvo |
| 6 | `HVAC_POWER_OFF` | 0,98 | mudança composta coerente |
| 7 | `HVAC_POWER_ON` | 0,98 | retorno ao estado-base |

As etiquetas continuam `INFERRED`; os frames `0x31` são `OBSERVED`.

## 4. Endpoint fake CANBOX

`scripts/hiworld_hvac_digital_twin.py` contém `FakeCanbox` e trabalha totalmente offline na fronteira Android ↔ CANBOX.

Ele pode exercitar inclusive capacidades genéricas que não existem no alvo. Isso é útil para testar fidelidade ao protocolo, mas **não transforma essas capacidades em features do veículo**.

Portanto um teste fake de `rear_defrost` continua válido como teste de parser/builder genérico, não como teste de produto para este Peugeot.

## 5. Evidência do laboratório

Marco anterior consolidado:

- self-test do gêmeo: PASS;
- 11/11 testes do gêmeo: PASS;
- `candata_8`: 821 frames válidos, 8 estados lógicos `0x31`, 0 TX `0x3B`, round-trip/replay exato.

Após a correção do alvo foi criada uma camada adicional:

- `contracts/hvac_target_profile.json`;
- `scripts/validate_hvac_target_profile.py`;
- `tests/test_hvac_target_profile.py`.

Ela congela especificamente:

- front-defrost presente;
- rear-defrost ausente;
- rear-defrost genérico não aplicável ao alvo;
- gate único atual = recirculação.

## 6. Lacuna física residual

A pergunta continua a mesma:

> um `0x3B` construído pelo caminho original é realmente aceito pela CANBOX/veículo nesta unidade e provoca o `0x31` correspondente?

Mas o experimento correto mudou.

## 7. Experimento físico único atual

Pré-condição: **recirculação OFF**.

Ação única pela UI original:

**recirculação ON uma vez**.

Previsão:

`TX esperado: 5A A5 02 3B 07 00 43`

Retorno esperado:

`0x31 payload[1] bit4: 0 → 1`

### Por que recirculação

- existe no alvo;
- um único subcomando;
- valor lógico/wire já conhecido;
- trace real contém transição isolada desse campo;
- operação reversível;
- melhor poder discriminatório do que front-defrost, cuja transição observada é uma macro composta.

Se passar, não há motivo para uma bateria manual função por função. Se divergir, preservar essa única captura e voltar ao laboratório offline.

## 8. Regra nova que o gêmeo deve obedecer

Antes de escolher qualquer teste ou feature de produto:

`capacidade no parser/builder → verificar aplicabilidade ao alvo → só então promover para UI/teste físico`

Essa correção foi registrada como aprendizado reutilizável para evitar repetir o erro em outras funções genéricas do protocolo.
