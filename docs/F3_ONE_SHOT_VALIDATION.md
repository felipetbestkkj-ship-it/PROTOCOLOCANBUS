# F3 — Validação física única de máxima informação

## Status

Este é o **gate físico atual da F3**. Ele substitui, como próximo passo, a antiga ideia de executar uma matriz manual de várias funções HVAC.

**Correção de alvo em 07/08/2026:** o proprietário confirmou que o veículo-alvo **não possui desembaçador traseiro**. Portanto a escolha anterior de `rear_defrost` como gate físico foi invalidada. O protocolo genérico Hiworld expor `rear_defrost` não prova que essa função exista no veículo-alvo.

O documento `docs/F3_RUNTIME_CAPTURE_PROTOCOL.md` permanece como referência geral de captura/fallback, mas **não é a sequência recomendada ao proprietário**.

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
- **recirculação OFF→ON como transição de um único campo** no retorno real.

A lacuna comum restante é somente provar, nesta unidade física:

`0x3B construído pela UI original → aceito no fio → retorno 0x31 correspondente`

Não é necessário testar cada função para provar esse elo comum.

## Ação única escolhida

Pré-condição: **recirculação atualmente OFF**.

Ação humana única:

> Na UI original do Car Info, tocar **recirculação ON uma vez**.

Nenhum replay e nenhum frame manual.

## Por que recirculação

Ela substitui rear-defrost porque reúne os critérios necessários **e existe no HVAC do alvo**:

1. comando estático único;
2. retorno real já observado mudando um único campo;
3. estado visível na própria UI;
4. operação reversível e curta;
5. alto poder de distinguir se o elo UI → Car Info → CANBOX → retorno está funcionando.

O desembaçador dianteiro existe no alvo, mas não foi escolhido porque a transição observada é composta: junto dele mudaram fan/airflow e outros campos, o que reduz o poder discriminatório do teste.

## Previsão fechada antes do teste

### TX

Property original:

- `16394`, valor lógico `1` (ON).

Builder `HdPsaProtocol`:

- subcomando `0x07`;
- a recirculação é **invertida no fio**;
- lógico ON gera valor `0x00`.

Frame previsto:

`5A A5 02 3B 07 00 43`

### RX

Na transição real já existente em `candata_8`, recirculação OFF→ON altera somente:

- `0x31 payload[1] bit4`: `0 → 1`.

Assinatura observada:

antes:

`5A A5 0C 31 45 00 00 01 06 04 FE FE 00 00 00 82 0A`

depois:

`5A A5 0C 31 45 10 00 01 06 04 FE FE 00 00 00 82 1A`

Os demais campos permaneceram iguais nessa transição.

## Critério de decisão

### PASS do elo físico comum

Se a única ação produzir:

1. `TX 5A A5 02 3B 07 00 43`;
2. ACK normal do protocolo;
3. `RX 0x31` com recirculação mudando OFF→ON;
4. estado da UI coerente;

então o elo comum `UI → 0x3B → CANBOX/veículo → 0x31` fica provado.

A partir daí, não pedir testes manuais função por função. Os outros comandos permanecem cobertos pelo mesmo builder/framing e pelos testes offline, com eventual validação posterior concentrada em regressão/laboratório.

### Se o TX previsto não aparecer

Isso não inicia uma bateria de tentativa e erro.

Registrar uma única captura e voltar à análise offline para identificar o produtor/caminho divergente. Não trocar de botão repetidamente no carro.

## Correção de interpretação do bit antes chamado rear-defrost

O parser genérico `HdPsaProtocol` rotula `0x31 payload[2] bit5` como rear-defrost e o builder possui property área `2`/subcomando `0x06`. Porém o proprietário confirmou que **o veículo-alvo não possui desembaçador traseiro**.

Portanto:

- a existência dessa capacidade no protocolo é preservada como **STATIC / protocolo genérico**;
- a mudança observada desse bit continua sendo um **OBSERVED bit transition**;
- ela **não deve mais ser descrita como atuação física de desembaçador traseiro no veículo-alvo**;
- sua semântica física específica neste alvo volta a ficar `INDETERMINADA/NÃO APLICÁVEL` até evidência contrária.

## Captura mínima

Usar `DbgAssist` com RX/TX habilitados e salvar o `candata` da sessão. Logcat paralelo é útil, mas o teste continua válido se o `candata` registrar claramente TX/RX.

O analisador deve ser executado depois sobre a captura; nenhuma transmissão é feita pelo analisador.

## Fronteira

Este documento **não autoriza automaticamente** a interação física. Ele apenas define a ação única que deverá ser executada quando essa fronteira for autorizada.
