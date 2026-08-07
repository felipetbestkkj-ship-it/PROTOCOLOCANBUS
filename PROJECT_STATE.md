# PROJECT STATE

**Projeto:** PROTOCOLOCANBUS  
**Repositório:** `felipetbestkkj-ship-it/PROTOCOLOCANBUS`  
**Linha consolidada:** `main`; qualquer outra branch exige autorização explícita  
**F0:** PASS  
**F1:** PASS — triagem Car Info/HVAC  
**F2:** PASS — cadeia HVAC original  
**F3:** ATIVA / PARTIAL — investigação offline e prontidão para implementação concluídas; resta um único gate físico  
**Última atualização:** 2026-08-07

## Em linguagem simples

```text
Car Info deixou de ser caixa-preta
        ↓
controle HVAC foi mapeado
        ↓
protocolo e retorno foram reconstruídos
        ↓
gêmeo digital testa sem carro
        ↓
catálogo genérico + perfil real do veículo separados
        ↓
arquitetura futura já tem candidato líder
        ↓
resta 1 confirmação física antes de F4/F5
```

## Correção crítica do alvo — 07/08/2026

O proprietário confirmou novamente:

- **desembaçador dianteiro: presente**;
- **desembaçador traseiro: ausente**.

Isso corrige uma inferência anterior. O `HdPsaProtocol` possuir property/bit/subcomando genérico chamado `rear_defrost` **não prova que essa feature exista no veículo-alvo**.

Regra vigente:

`capacidade do protocolo ≠ capacidade física do alvo`

Artefatos:

- catálogo genérico: `contracts/hvac_behavior_contract.json`;
- perfil autoritativo do veículo: `contracts/hvac_target_profile.json`;
- aprendizado: `docs/L011_PROTOCOL_CAPABILITY_VS_TARGET_FEATURE.md`;
- skill refinada: `skills/protocol-digital-twin-inference/SKILL.md`.

A alternância observada do bit que o parser genérico chama `rear_defrost` continua sendo dado real de runtime, mas **não é mais atribuída a um desembaçador traseiro físico neste carro**.

## F1/F2 — base já fechada

- alvo central: `Car Info / com.can.activity`;
- v3854 fornecida é byte a byte o APK registrado na baseline como instalado;
- fluxo original mapeado:

```text
HvacFragment
→ CarPropertyValue
→ HvacViewModel/HvacModel
→ CanBusManager
→ ICanUI/ICanBus Binder
→ CanBusService.setHvacProperty
→ HdPsaProtocol.buildHvacPackets
→ CanProxy/CanSender
→ CanRxTx.sendData
```

- TX HVAC genérico: `5A A5 02 3B <subcomando> <valor> <checksum>`;
- RX `0x31` = estado HVAC retornando por `HvacInfo`.

## F3 — runtime e laboratório offline

Confirmado:

- `candata_*` registra protocolo serial Hiworld/Jancar Android ↔ CANBOX, não CAN bruto do Peugeot;
- transporte observado: `/dev/ttyS5 @ 38400`;
- `candata_8`: 821 frames / 821 checksums válidos;
- TX observado naquela captura: ACK, hora/data, polling e mídia; `0x3B=0`;
- 8 estados lógicos `0x31`; 1 solicitado e 7 não solicitados pelo polling conhecido;
- logger cobre o caminho TX normal da UI;
- keycode-mode foi eliminado para a configuração Peugeot ativa;
- gêmeo digital reproduz framing, builder, parser/encoder, state machine e fake CANBOX totalmente offline.

### Perfil do alvo

`contracts/hvac_target_profile.json` é a camada que responde **o que realmente existe neste carro**. Ela prevalece sobre rótulos genéricos do protocolo para decisão de UI/teste.

Estado confirmado até agora:

- front defrost: presente;
- rear defrost: ausente;
- recirculação: função escolhida como gate físico único;
- demais capacidades só devem ser promovidas para produto conforme aplicabilidade ao alvo for conhecida/provada.

## F3.1 — prontidão para implementação

Entregue:

- catálogo de 18 operações genéricas do protocolo;
- perfil específico do alvo;
- validador do contrato genérico;
- validador do perfil do alvo;
- testes automáticos;
- contrato Binder do Car Info;
- rascunho F4;
- ranking arquitetural F5;
- workflow `🧪 TESTAR HVAC SEM MEXER NO CARRO`.

## Arquitetura F5 — recomendação preliminar

Candidato líder:

```text
NOSSA UI / WIDGET
      ↓
NOSSA CAMADA HVAC
      ↓
Binder ICanBus do Car Info
      ↓
Hiworld / CANBOX
      ↓
veículo
```

Motivo: trocar a experiência visual sem reimplementar imediatamente serial, ACK, polling e timing. Ainda não é decisão F5 definitiva.

## Único gate físico atual da F3

Documento: `docs/F3_ONE_SHOT_VALIDATION.md`.

**Não usar rear-defrost.**

Quando houver autorização material:

> com recirculação inicialmente OFF, tocar **recirculação ON uma única vez** na UI original, com RX/TX capturados.

Previsão congelada:

- property: `16394`, lógico ON;
- wire value invertido = `0x00`;
- TX: `5A A5 02 3B 07 00 43`;
- RX `0x31 payload[1] bit4`: `0 → 1`;
- estado da UI coerente.

Por que recirculação: existe no alvo, usa comando único e já apareceu nos logs como transição real de **um único campo**. Front-defrost existe, mas a transição observada é composta e menos discriminatória.

Se passar: fechar F3 e promover F4/F5 sem bateria função por função.  
Se divergir: preservar uma única captura e voltar offline. Sem tentativa e erro em sequência.

## Lacunas secundárias que não bloqueiam o gate

- semântica física do bit genérico antes rotulado rear-defrost neste alvo;
- origem material dos pushes `RX_NAO_SOLICITADO` antigos;
- arbitration IDs abaixo da CANBOX;
- IAP exato instalado;
- `0x1A` ainda hipótese forte de RPM;
- causa raiz do crash `sourceDir`.

## Próximo passo único

**Fechar F3 pelo gate físico único de recirculação quando o proprietário autorizar essa interação real.** Até lá, nenhum replay, frame manual, instalação, ROM ou firmware.
