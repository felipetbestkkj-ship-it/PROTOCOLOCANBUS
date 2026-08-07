# F3 — Validação física única de máxima informação

## Status

Este é o **gate físico atual da F3**. Ele substitui, como próximo passo, a antiga ideia de executar uma matriz manual de várias funções HVAC.

O documento `docs/F3_RUNTIME_CAPTURE_PROTOCOL.md` permanece como referência geral de captura/fallback, mas **não é mais a sequência recomendada ao proprietário**.

## Por que só um teste

A investigação offline já provou:

- protocolo ativo Peugeot/Hiworld e framing `5A A5`;
- checksum;
- parser `0x31` byte a byte;
- builder `0x3B` e subcomandos;
- caminho da UI normal até `buildHvacPackets`;
- cobertura TX do logger;
- ausência de keycode-mode para a property list do `HdPsaProtocol` ativo;
- oito estados HVAC reais em `candata_8` e uma state machine reexecutável;
- rear-defrost ON/OFF como transições de **um único campo** no retorno real.

A lacuna comum restante é somente provar, nesta unidade física:

`0x3B construído pela UI original → aceito no fio → retorno 0x31 correspondente`

Não é necessário testar cada função para provar esse elo comum.

## Ação única escolhida

Pré-condição: **rear defrost atualmente OFF**.

Ação humana única:

> Na UI original do Car Info, tocar **rear defrost ON uma vez**.

Nenhum replay e nenhum frame manual.

## Previsão fechada antes do teste

### TX

Property original:

- `24577`, área `2`, valor `1`.

Builder `HdPsaProtocol`:

- subcomando `0x06`;
- valor `0x01`.

Frame previsto:

`5A A5 02 3B 06 01 43`

### RX

Na transição real já existente em `candata_8`, rear defrost OFF→ON altera somente:

- `0x31 payload[2] bit5`: `0 → 1`.

A assinatura completa observada para essa mudança foi:

antes:

`5A A5 0C 31 45 10 10 01 0B 07 FF FE 00 00 00 82 33`

depois:

`5A A5 0C 31 45 10 30 01 0B 07 FF FE 00 00 00 82 53`

Os demais campos permaneceram iguais nessa transição.

## Critério de decisão

### PASS do elo físico comum

Se a única ação produzir:

1. `TX 5A A5 02 3B 06 01 43`;
2. ACK normal do protocolo;
3. `RX 0x31` com rear-defrost mudando OFF→ON;
4. estado/UI física coerente;

então o elo comum `UI → 0x3B → CANBOX/veículo → 0x31` fica provado.

A partir daí, não pedir testes manuais função por função. Os outros comandos permanecem cobertos pelo mesmo builder/framing e pelos testes offline, com eventual validação posterior concentrada em regressão/laboratório.

### Se o TX previsto não aparecer

Isso não inicia uma bateria de tentativa e erro.

Registrar uma única captura e voltar à análise offline para identificar o produtor/caminho divergente. Não trocar de botão repetidamente no carro.

## Captura mínima

Usar `DbgAssist` com RX/TX habilitados e salvar o `candata` da sessão. Logcat paralelo é útil, mas o teste continua válido se o `candata` registrar claramente TX/RX.

O analisador deve ser executado depois sobre a captura; nenhuma transmissão é feita pelo analisador.

## Fronteira

Este documento **não autoriza automaticamente** a interação física. Ele apenas define a ação única que deverá ser executada quando essa fronteira for autorizada.
