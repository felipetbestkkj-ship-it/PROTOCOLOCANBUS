# F3 — Continuação passiva: cobertura TX, push HVAC e narrowing

## Resultado executivo

Este complemento aprofunda somente lacunas ainda abertas após `docs/F3_CAN_RUNTIME_EVIDENCE_DEEP_DIVE.md`. Nenhuma transmissão, replay, ação no carro, instalação, ROM ou firmware foi executado.

Os principais resultados são:

1. o caminho HVAC conhecido do Car Info passa por `mCanProxy → CanSender → CanBusService.doTx(...)`; o mesmo `doTx` envia o pacote à porta e entrega o mesmo byte array ao callback do `DbgAssist` que alimenta o `candata`;
2. o frame HVAC `0x3B` tem 7 bytes totais e não seria excluído pelo filtro de debug que ignora apenas pacotes com menos de 3 bytes fora do modo update;
3. o vocabulário TX de `candata_8` foi esgotado: `0xFF`, `0xCB`, `0x6A`, `0xA1` e `0xA4`; não existe qualquer outro comando TX oculto entre os 821 frames reconstruídos;
4. `0xA1` e `0xA4`, antes apenas observados, são pacotes de mídia no `HdPsaProtocol`, não controles HVAC;
5. dos oito eventos lógicos de `RX 0x31`, somente o primeiro é resposta direta a uma consulta `TX 0x6A ... 0x31`; os sete seguintes são recepções não solicitadas por `0x6A` e representam pushes de estado da CANBOX em relação a esse mecanismo de polling;
6. como não há `TX 0x3B` e o caminho conhecido do Car Info teria sido visível no logger, as sete mudanças de estado não foram produzidas pelo caminho HVAC conhecido `setHvacProperty → mCanProxy → doTx` durante essa captura;
7. a origem material das mudanças ainda não pode ser escolhida entre controles físicos/veículo e algum produtor ou caminho alternativo fora do fluxo conhecido;
8. `0x1A` continua não registrado pelo `HdPsaProtocol` ativo, mas um campo de 16 bits apresenta uma assinatura fortemente compatível com rotação do motor após uma transição de ACC; isso permanece hipótese, não fato promovido.

## 1. Prova da cobertura do TX conhecido do Car Info

### 1.1 Caminho de saída

No `CanBusService`, o `mCanProxy.sendData2Can(byte[])` coloca o pacote no `CanSender`.

O `CanSender` finalmente chama `CanBusService.doTx(byte[])` para a porta principal.

`doTx(...)` executa, na mesma chamada:

1. `mCanRxTx.sendData(bArr, bArr.length)`;
2. quando existe callback de debug, `dbgRxTxCallback.txData(bArr, bArr.length)`;
3. notifica `RxTxDataObserver`.

Na plataforma Jancar, `CanRxTx.sendData(...)` encaminha para `HandlerMainServer.sendCanData2Mcu(...)`, que usa o transporte ARM/Jancar configurado.

### 1.2 Como o `candata` recebe TX

`DbgAssist` implementa `DbgRxTxCallback`. Seu método `txData(...)` adiciona o pacote à lista quando a exibição de dados e TX estão habilitados. Os próprios `candata_*` contêm centenas de linhas TX, portanto TX estava habilitado na sessão.

O único corte de tamanho observado em `doTx(...)`, fora do modo de atualização, rejeita apenas `bArr.length < 3` para o callback de debug.

O controle HVAC conhecido construído pelo `HdPsaProtocol` é:

`5A A5 02 3B <subcomando> <valor> <checksum>`

ou seja, 7 bytes totais. Ele seria elegível para o logger.

### 1.3 Alcance e limite desta prova

**Confirmado:** qualquer comando HVAC que percorresse o caminho conhecido do Car Info `setHvacProperty → mCanProxy → CanSender → doTx` durante a sessão apareceria no `candata`.

**Não confirmado:** um processo externo ou outro produtor que escrevesse por um caminho diferente e bypassasse `CanBusService.doTx` não é coberto automaticamente por essa conclusão.

Portanto, a ausência de `0x3B` exclui o caminho HVAC conhecido do Car Info nesta captura, mas não prova sozinha qual produtor alternativo originou as mudanças observadas.

## 2. Inventário TX esgotado em `candata_8`

O reparser de framing recupera os mesmos **821 frames** já validados no deep dive. O conjunto TX contém somente cinco IDs:

| TX | Quantidade | Classificação atual |
|---|---:|---|
| `0xFF` | 251 | ACK do protocolo |
| `0xCB` | 50 | ajuste/sincronização de data e hora |
| `0x6A` | 8 | solicitação de relatório/estado |
| `0xA1` | 7 | dados de mídia/source/volume |
| `0xA4` | 3 | informação de mídia/CD-CDC |
| `0x3B` | **0** | controle HVAC previsto estaticamente, não observado |

Não existe um sexto comando TX não classificado que possa ser promovido por conveniência a “HVAC oculto”.

## 3. `0xA1` — dados de mídia, não HVAC

No `HdPsaProtocol`:

- `DATA_TYPE_HOST_SHOW_CMD = 0xA1`;
- `getMediaData(MediaInfo)` usa `0xA1` para veículos deste ramo que não são Citroën C5 Aircross;
- `buildMetaDataPackets()` adiciona `getMediaData(...)` quando há fonte de mídia e telefone não está ocupado.

O payload de três bytes para esse ramo é:

- byte 0: marcador fixo `0x80`;
- byte 1: código derivado da fonte/mídia;
- byte 2: volume atual.

Todos os sete `TX 0xA1` observados carregam:

`80 07 0F`

Classificação segura:

- marcador: `0x80`;
- código source/media observado: `0x07`;
- volume observado: `0x0F` = 15.

A equivalência do código `0x07` com uma fonte humana específica não é promovida aqui sem prova adicional.

## 4. `0xA4` — informação de mídia/CD-CDC, não HVAC

No `HdPsaProtocol`:

- `DATA_TYPE_CD_CDC_CMD = 0xA4`;
- `buildMediaInfoPackets(PlatformMediaInfo)` chama `getMediaSource(...)`;
- `getMediaSource(...)` cria um payload de 11 bytes e o empacota em `0xA4`.

Quando `source` é 1 ou 2, o builder preenche tipo, faixa atual, tempo e total de faixas. Fora desses ramos, os 11 bytes permanecem zerados.

Os três `TX 0xA4` observados são exatamente:

`00 00 00 00 00 00 00 00 00 00 00`

Logo `0xA4` deixa de ser TX semântico aberto nesta investigação: é pacote de mídia, não candidato HVAC.

## 5. `0x31` — separar polling de push não solicitado

Existem 16 linhas RX `0x31`. Colapsando pares adjacentes idênticos produzidos na captura, há **8 eventos lógicos**.

A única consulta explícita a `0x31` é:

- `19:48:18.129` — `TX 0x6A` com alvo `0x31`;
- `19:48:18.193` — `RX 0x31` correspondente;
- latência aproximada: 64 ms.

Não existe outro `TX 0x6A` solicitando `0x31` depois disso.

Assim, os sete eventos lógicos `0x31` posteriores são classificados como:

**`RX_OBSERVADO / NÃO SOLICITADO POR 0x6A`**.

Isto não significa automaticamente “causado por botão físico”; significa somente que não são respostas ao mecanismo de polling `0x6A → 0x31`.

### Timeline dos oito eventos lógicos

| Hora | Payload `0x31` | Leitura HVAC resumida |
|---|---|---|
| 19:48:18.193 | `45 10 00 01 06 04 FE FE 00 00 00 82` | snapshot inicial solicitado; HVAC/A-C ativos, fan 4 |
| 19:48:22.871 | `45 10 10 01 0B 07 FF FE 00 00 00 82` | front defrost ativo; fan 7; airflow alterado |
| 19:48:23.894 | `45 10 30 01 0B 07 FF FE 00 00 00 82` | rear defrost adicionado |
| 19:48:24.369 | `45 00 20 01 06 04 FE FE 00 00 00 82` | front defrost desliga; rear permanece; recirc muda |
| 19:48:24.923 | `45 00 00 01 06 04 FE FE 00 00 00 82` | rear defrost desliga |
| 19:48:26.326 | `45 10 00 01 06 04 FE FE 00 00 00 82` | recirculação retorna ao snapshot-base |
| 19:48:26.758 | `04 10 00 01 06 00 FE FE 00 00 00 82` | HVAC/A-C desligados; fan 0 |
| 19:48:28.278 | `45 10 00 01 06 04 FE FE 00 00 00 82` | HVAC/A-C/fan retornam ao estado-base |

A sequência é coerente com múltiplas ações HVAC deliberadas, porém a fonte humana/física continua sem marcador independente.

## 6. Não há outro TX de aplicação próximo que explique a sequência HVAC

`0xA1` ocorre de `19:48:12.982` a `19:48:15.285`.

`0xA4` ocorre de `19:48:13.383` a `19:48:15.488`.

As mudanças HVAC não solicitadas começam apenas em `19:48:22.871`.

Durante a sequência HVAC, os TX não-ACK encontrados são essencialmente:

- `0xCB`, periódico de data/hora;
- os últimos `0x6A`, consultando outros relatórios (`0x76`, `0x79`, `0xF0`).

Nenhum deles é construtor HVAC no protocolo estático.

Consequência atual:

> As mudanças `0x31` não foram produzidas pelo caminho HVAC conhecido do Car Info e não há outro TX de aplicação observado que possa ser reinterpretado como comando HVAC sem contradizer o código estático.

## 7. Linha de inicialização — ACC, mídia, consultas e `0x1A`

O `0x11` fornece bits de estado básico no `HdPsaProtocol`.

Pontos relevantes:

- `19:48:12.518` — data0 `0xC8`: ACC=0, KeyIn=0, Park=1;
- `19:48:13.242` — data0 `0xD9`: ACC=1, KeyIn=1, Park=1;
- `19:48:13.651` — data0 `0xDB`: ACC/KeyIn permanecem ativos e outro bit de iluminação muda.

Em seguida:

- `19:48:12.982..15.488` — bursts `0xA1/0xA4` de mídia;
- `19:48:17.128..24.260` — sweep `0x6A` pedindo `0x11, 0x31, 0x94, 0x71, 0x72, 0x76, 0x79, 0xF0`.

Esta ordem é consistente com uma sequência de inicialização/sincronização após ACC, mas a intenção interna exata de cada temporização não é necessária para a F3.

## 8. `0x1A` — comportamento provável e limite de prova

### Fato estático

O `HdProtocol` base usa `0x1A` como valor padrão de `rx360InfoCmdId`, porém o `HdPsaProtocol` ativo sobrescreve esse ID para `0xE8`.

No `HdPsaProtocol.create()`, `0x1A` não é registrado para processamento de aplicação. O `JancarRx` somente chama `handlePacket(...)` para IDs registrados. Portanto `0x1A` pode aparecer no debug/ser reconhecido no framing e receber ACK, sem atualizar diretamente `HvacInfo` ou outro estado por `HdPsaProtocol.handlePacket`.

### Fato runtime

O payload `0x1A` mantém vários campos estáveis, mas o campo de 16 bits formado por `data[9] << 8 | data[10]` apresenta:

- 0 antes da transição de ACC;
- 1356 em `19:48:13.601`, cerca de 359 ms após `ACC=1/KeyIn=1`;
- pico observado 1474 em `19:48:13.821`;
- queda progressiva por 1420, 1331, 1240, 1180, 1123, ...;
- estabilização posterior aproximadamente na faixa de 800–900.

### Hipótese preservada

A forma temporal e a escala são **fortemente compatíveis com rotação do motor (RPM) durante partida e estabilização de marcha lenta**.

Contudo, não existe parser ativo do PSA ligando esse campo a `mRotationlSpeed`, nem fonte independente com RPM timestampado nesta captura.

Classificação: **HIPÓTESE FORTE / NÃO PROMOVIDA**.

Próxima prova adequada, se isso virar objetivo relevante: capturar `0x1A` junto com uma fonte independente de RPM e fazer correlação quantitativa. Não é necessário bloquear a F3 HVAC por isso.

## 9. Conclusão de narrowing passivo

### Eliminado

- `0xA1` como candidato HVAC — é mídia;
- `0xA4` como candidato HVAC — é mídia/CD-CDC;
- “talvez haja algum TX desconhecido no `candata_8` representando HVAC” — o vocabulário TX foi esgotado;
- “todos os `0x31` são apenas respostas a polling” — somente o primeiro evento lógico é resposta à consulta `0x6A → 0x31`.

### Sustentado

- o conhecido controle HVAC do Car Info via `setHvacProperty/mCanProxy/doTx` não ocorreu durante as sete mudanças `0x31` não solicitadas;
- a CANBOX publicou estados HVAC mudando coerentemente sem um `0x3B` observado do caminho conhecido;
- a origem material continua aberta entre controle veicular/físico e algum caminho produtor alternativo que bypassaria o fluxo conhecido.

### Próxima evidência discriminatória

A evidência passiva atual não separa essas duas origens. O próximo experimento de maior valor continua sendo uma sessão controlada no equipamento real, com ação marcada e captura sincronizada:

`ação conhecida → timestamp → TX observado/ausente → RX 0x31 → estado → efeito físico`

Esse experimento cruza a fronteira material de atuação real e não foi executado neste complemento.
