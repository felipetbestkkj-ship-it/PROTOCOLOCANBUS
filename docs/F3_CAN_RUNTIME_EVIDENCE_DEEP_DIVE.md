# F3 — Deep dive passivo das evidências CANBOX/runtime

## Resultado executivo

Este marco passivo da F3 reorganiza os ZIPs e logs disponíveis por **camada técnica real** e evita uma interpretação incorreta importante: os arquivos `candata_*` inspecionados **não são uma captura bruta da rede CAN veicular do Peugeot**. Eles registram pacotes do protocolo Hiworld/Jancar no enlace entre o Android/Car Info e a CANBOX.

Para o equipamento observado, a cadeia sustentada por runtime + configuração + código estático é:

```text
Car Info / com.can.activity
  ↓
Jancar / HandlerMainServer
  ↓
Serial ARM
  ↓
/dev/ttyS5 @ 38400 baud
  ↓
CANBOX Hiworld
  ↓
redes CAN do veículo
```

O enquadramento observado nesse enlace é `5A A5 <len> <cmd> <data...> <checksum>`, com checksum aditivo de 8 bits. Em `candata_8.log` foram reconstruídos 821 pacotes, todos com checksum válido.

O principal achado operacional é que o Car Info executa consultas explícitas com `TX 0x6A` para pedir estados à CANBOX, inclusive `0x31` (HVAC). Cada consulta do conjunto observado recebe o relatório solicitado em seguida. Portanto, pelo menos parte dos frames `RX 0x31` da captura é **estado solicitado pelo aplicativo**, e não prova de um toque em botão HVAC.

Também foram observadas transições reais de estado HVAC em `RX 0x31` — power, A/C, recirculação, desembaçadores, fan e direção do ar —, mas nenhum `TX 0x3B` aparece na captura. Assim, a F3 continua aberta: as mudanças de estado estão comprovadas, porém sua origem (UI original, controles físicos ou outro emissor) não está correlacionada.

Nenhum frame foi transmitido por este trabalho, nenhum replay foi realizado e nenhum equipamento foi modificado.

---

## 1. Hierarquia e relação entre as fontes

### 1.1 `candata_5.log` a `candata_8.log`

Os quatro arquivos são snapshots progressivos da mesma coleta:

| Arquivo | Linhas | Tamanho aproximado | Relação |
|---|---:|---:|---|
| `candata_5.log` | 44 | 2.1 KiB | prefixo exato de `candata_6` |
| `candata_6.log` | 64 | 2.9 KiB | prefixo exato de `candata_7` |
| `candata_7.log` | 149 | 6.9 KiB | prefixo exato de `candata_8` |
| `candata_8.log` | 816 | 40 KiB | captura canônica mais completa |

Conclusão: para análise de conteúdo, `candata_8.log` supersede integralmente 5/6/7. Os anteriores permanecem úteis apenas para proveniência da coleta progressiva.

### 1.2 ZIPs de runtime

`CANBOX_RUNTIME_CAPTURE_2026-08-06_1201.zip` contém 15 arquivos centrais.

`CANBOX_RUNTIME_CAPTURE_2026-08-06_1201 (2).zip` contém 91 entradas de arquivo; os 15 arquivos centrais equivalentes são byte a byte idênticos aos do ZIP menor e o segundo pacote acrescenta 76 diagnósticos.

Conclusão: o `(2)` é uma **captura ampliada/superset**, não uma captura conflitante.

Entre os adicionais há diagnósticos OMEGAS, bugreport/logcats e `communication_logs.txt`. As linhas CP2102/USB observadas nesse material pertencem ao contexto dos diagnósticos OMEGAS e não devem ser confundidas com a porta serial interna usada pelo Car Info para a CANBOX.

### 1.3 `Engenharia-Reversa-CANBOX.zip`

O arquivo começa com registros ZIP válidos, mas não possui o registro final de diretório central/EOCD. A leitura padrão como ZIP completo falha, porém a varredura de cabeçalhos locais permitiu identificar **4.122 entradas recuperáveis**.

Classificação correta: **artefato derivado de engenharia reversa com diretório central truncado/incompleto, parcialmente recuperável**. Não deve ser chamado simplesmente de “ZIP corrompido”, nem tratado como captura original de runtime.

Entre os itens recuperáveis relevantes estão:

- `com.can.activity/assets/canbox/peugeot.xml`;
- `com.can.activity/assets/protocol/peugeot.xml`;
- artefatos de auditoria serial/UI;
- árvore extensa de recursos decompilados.

---

## 2. O que `candata` representa neste equipamento

A distinção de camada foi fechada por evidências convergentes.

### 2.1 Plataforma Android

A captura de propriedades identifica:

```text
ro.board.platform = rk3326
```

No código do Car Info, `JancarConfigPlatform` mapeia RK3326 para a plataforma que usa ferramentas ARM/serial.

`HandlerMainServer` mantém baudrate padrão/ativo `B38400`, envia dados CANBOX pelo `JancarConfigPlatform` e, nesta plataforma, abre a porta serial correspondente.

`PlatformRK3326` define:

```text
/dev/ttyS5
```

como a porta usada pelo enlace e encaminha RX/TX entre `SerialGpioUtils` e `HandlerMainServer`.

### 2.2 Configuração Peugeot/Hiworld

A configuração recuperada para Peugeot contém:

- modelo: `208` (id 19);
- ano: `2023_Now` (id 3);
- região: South America/Brazil;
- CANBOX: Hiworld (id 2);
- baudrate: **38400**.

O runtime registra:

`Hiworld-Peugeot-208-2023~Present（Brazil）-All`

### 2.3 Conclusão de camada

Portanto, a interpretação correta dos `candata_*` é:

**pacotes seriais do protocolo CANBOX Hiworld no limite Android ↔ CANBOX**, e não frames CAN veiculares com arbitration IDs diretamente extraídos do barramento do Peugeot.

Consequência prática: IDs como `0x31`, `0x6A`, `0xFF` e `0x3B` são IDs/comandos **do protocolo CANBOX**, não devem ser apresentados como CAN IDs do veículo.

---

## 3. Framing Hiworld confirmado

O parser passivo sobre `candata_8.log` reconstruiu 821 frames. Algumas linhas do arquivo contêm mais de um pacote concatenado, por isso existem mais frames que linhas.

Formato observado e confirmado pelo código `HdProtocol`:

```text
5A A5 <LEN> <CMD> <DATA...> <CHECKSUM>
```

- `5A A5`: preâmbulo;
- `LEN`: comprimento dos dados do protocolo;
- `CMD`: ID/comando Hiworld;
- `DATA`: carga útil;
- `CHECKSUM`: soma de todos os bytes anteriores módulo 256.

Resultado da validação:

- frames reconstruídos: **821**;
- checksums válidos: **821/821**.

Isso dá alta confiança no recorte e agrupamento dos pacotes usados nas análises seguintes.

---

## 4. ACKs: por que existem tantos `0xFF`

O protocolo original exige confirmação.

No código:

- `shouldSendAck()` retorna verdadeiro;
- `0xFF`/`0xFE` são tratados como ACK;
- para um pacote recebido que não seja ACK, `JancarRx` envia:

```text
5A A5 01 FF <cmd recebido> <checksum>
```

Exemplo observado:

- chega `RX 0x31`;
- Android responde `TX 5A A5 01 FF 31 30`.

Isso explica o volume alto de `0xFF`: são **confirmações do protocolo**, não funções independentes do veículo.

Também há ACK na direção inversa: por exemplo, um `TX 0x6A` ou `TX 0xCB` recebe `RX 0xFF` referenciando o comando transmitido.

---

## 5. Mapa dos grupos encontrados em `candata_8`

### RX

| CMD | Frames | Variantes | Significado sustentado pelo parser inspecionado |
|---:|---:|---:|---|
| `0x11` | 16 | 3 | informações básicas do carro |
| `0x12` | 10 | 1 | portas/base misc |
| `0x13` | 8 | 1 | trip computer PSA |
| `0x14` | 6 | 1 | trip computer PSA |
| `0x15` | 6 | 1 | trip computer PSA |
| `0x1A` | 136 | 57 | **não mapeado no `HdPsaProtocol` inspecionado** |
| `0x21` | 10 | 1 | tecla/painel |
| `0x22` | 10 | 1 | knob/painel |
| `0x31` | 16 | 6 | HVAC / air info |
| `0x42` | 6 | 1 | warning info |
| `0x71` | 14 | 1 | enable/config PSA 01 |
| `0x72` | 14 | 1 | enable/config PSA 02 |
| `0x76` | 12 | 1 | estado do carro PSA |
| `0x79` | 14 | 2 | estado adicional PSA |
| `0x81` | 12 | 1 | remembered speed |
| `0x82` | 12 | 1 | speed/cruise info |
| `0x83` | 12 | 1 | SOS info |
| `0x85` | 12 | 1 | engine info |
| `0x94` | 8 | 1 | idioma do carro |
| `0xC1` | 6 | 1 | unidades |
| `0xC2` | 14 | 4 | data/hora recebida; encoding ainda não totalmente fechado |
| `0xF0` | 12 | 1 | versão da CANBOX |
| `0xFF` | 136 | 4 | ACK |

### TX

| CMD | Frames | Variantes | Papel observado/estático |
|---:|---:|---:|---|
| `0x6A` | 8 | 8 | consulta de relatório/estado específico |
| `0xA1` | 7 | 1 | presente; semântica não promovida neste marco |
| `0xA4` | 3 | 1 | presente; semântica não promovida neste marco |
| `0xCB` | 50 | 3 | sincronização de hora/data |
| `0xFF` | 251 | 23 | ACK dos pacotes recebidos |

**TX `0x3B`: 0 ocorrências.**

---

## 6. `0x6A`: consulta explícita de estados

No `HdPsaProtocol`, `txRequestCmdId = 0x6A`.

`buildInquiryInfoPackets()` monta oito consultas, nesta ordem:

1. `0x11` — base info;
2. `0x31` — HVAC;
3. `0x94` — idioma;
4. `0x71` — configuração/enable 01;
5. `0x72` — configuração/enable 02;
6. `0x76` — estado;
7. `0x79` — estado adicional;
8. `0xF0` — versão CANBOX.

A captura contém exatamente essa sequência. Após cada pedido, a CANBOX envia ACK e o relatório solicitado aparece logo depois.

Latência pedido → relatório observada na sequência principal:

| Relatório solicitado | Latência aproximada |
|---:|---:|
| `0x11` | 66 ms |
| `0x31` | 64 ms |
| `0x94` | 60 ms |
| `0x71` | 65 ms |
| `0x72` | 64 ms |
| `0x76` | 242 ms |
| `0x79` | 60 ms |
| `0xF0` | 59 ms |

Conclusão: há convergência independente entre código e runtime para afirmar que `0x6A` é o mecanismo original de **consulta de relatórios da CANBOX**.

Consequência para F3: o primeiro `RX 0x31` desta sequência é um **estado HVAC solicitado**, não evidência de comando de alteração do HVAC.

---

## 7. `0x31`: decodificação HVAC e transições observadas

O `HdPsaProtocol.parseAirInfo()` usa os bytes do frame para atualizar `HvacInfo`.

Campos relevantes do frame completo:

- byte `[4]`: power, MAX A/C, rear air, auto, SYNC, A/C;
- byte `[5]`: recirculação / auto recirculação;
- byte `[6]`: rear/front defrost;
- byte `[7]`: wind intensity;
- byte `[8]`: airflow mode bruto;
- byte `[9]`: fan level;
- byte `[10]`: temperatura esquerda;
- byte `[11]`: temperatura direita;
- byte `[15]`: temperatura ambiente externa, fórmula `(raw × 0.5) - 40`.

O byte ambiente `0x82` corresponde a **25,0 °C**.

Após colapsar pares duplicados praticamente simultâneos, aparecem oito eventos de estado distintos:

### Evento 1 — 19:48:18.193

Estado base observado:

- HVAC power ON;
- A/C ON;
- SYNC ON;
- recirculação ON;
- desembaçadores OFF;
- fan 4;
- airflow bruto 6;
- temperatura externa 25 °C.

### Evento 2 — 19:48:22.871

Mudanças:

- front defrost ON;
- fan 4 → 7;
- airflow 6 → 11;
- código especial de temperatura esquerda `FE → FF`.

### Evento 3 — 19:48:23.894

- rear defrost também ON;
- front + rear defrost simultaneamente ativos.

### Evento 4 — 19:48:24.369

- recirculação OFF;
- front defrost OFF;
- rear defrost permanece ON;
- fan 7 → 4;
- airflow 11 → 6;
- temperatura esquerda `FF → FE`.

### Evento 5 — 19:48:24.923

- rear defrost OFF.

### Evento 6 — 19:48:26.326

- retorno ao estado base com recirculação ON.

### Evento 7 — 19:48:26.758

- HVAC power OFF;
- A/C OFF;
- fan 0;
- bit SYNC permanece ativo no relatório.

### Evento 8 — 19:48:28.278

- retorno ao estado base;
- HVAC power ON;
- A/C ON;
- fan 4;
- recirculação ON.

### O que isso prova

**Confirmado:** a CANBOX reportou mudanças de estado HVAC correspondentes a power, A/C, recirculação, desembaçadores, fan e direção do ar.

**Não confirmado:** quem originou cada mudança. A captura não contém touch/action markers sincronizados e não contém `TX 0x3B`.

As mudanças podem ter vindo de controles físicos do carro, UI original por um caminho não capturado, outro produtor ou outro subsistema. Não atribuir origem sem a correlação dinâmica da F3.

---

## 8. Por que o `TX 0x3B` continua sendo a peça que falta

No código original `HdPsaProtocol.buildHvacPackets()`, comandos de HVAC construídos a partir de `CarPropertyValue` usam comando `0x3B` com subcomando + valor.

Subcomandos mapeados estaticamente:

| Subcomando | Função |
|---:|---|
| `0x01` | power |
| `0x02` | A/C |
| `0x03` | MAX A/C |
| `0x04` | AUTO |
| `0x05` | front defrost |
| `0x06` | rear defrost |
| `0x07` | recirculação |
| `0x08..0x0A` | componentes de airflow |
| `0x0B` | fan +/- |
| `0x0C` | temperatura esquerda +/- |
| `0x0D` | temperatura direita +/- |
| `0x0E` | wind intensity |
| `0x0F` | SYNC |
| `0x10` | auto recirculação |
| `0x11` | rear HVAC power |

Mas `candata_8.log` contém **zero TX `0x3B`**.

Isso é particularmente discriminatório porque o mesmo logger registra claramente outros TX do Android (`0x6A`, `0xCB`, `0xFF`, etc.). Ainda assim, ausência de `0x3B` sozinha não prova que as mudanças `0x31` vieram do painel físico.

A prova necessária permanece:

`ação original controlada → timestamp → TX 0x3B → ACK → RX 0x31 → estado/efeito físico`.

---

## 9. `0x11`: transições de estado básico também aparecem

O `HdPsaProtocol.parseBaseInfo()` usa o byte de flags para informações como key-in, park, reverse, illumination e ACC.

Transições observadas incluem:

- estado `D9`: key-in ativo, park ativo, ACC ativo, iluminação OFF, brightness 15;
- 19:48:12.518: estado `C8`, com key-in/ACC desativados;
- 19:48:13.242: retorno a `D9`;
- 19:48:13.651: `DB`, iluminação ON e brightness 15 → 11.

Esses são estados recebidos; não há base para atribuir a mudança a uma ação humana específica nesta captura.

---

## 10. Correção importante: `0x1A` não é 360° no parser PSA inspecionado

`0x1A` é o grupo RX mais variável da captura:

- 136 frames brutos;
- 57 variantes.

Porém, no `HdPsaProtocol` inspecionado:

- `create()` não registra `0x1A`;
- `handlePacket()` não contém ramo para `0x1A`;
- o ID configurado para informação 360/parking é `0xE8`, não `0x1A`.

Portanto, qualquer associação anterior de `0x1A` a 360/parking deve ser descartada para esta implementação.

Estado atual de `0x1A`: **mensagem Hiworld altamente variável, não mapeada pelo parser PSA inspecionado; sem semântica funcional promovida**.

---

## 11. Firmware/IAP Hiworld

Os quatro ZIPs `H1H2...` contêm exatamente uma imagem `.iap` cada:

| ZIP | IAP | Tamanho |
|---|---|---:|
| `2851-H1H2LNF13A-230611.zip` | `H1H2LNF13A-230611.iap` | 56.848 B |
| `2868-H1H2VWFA3A-230630.zip` | `H1H2VWFA3A-230630.iap` | 127.296 B |
| `2910-H1H2PAF23A-230802.zip` | `H1H2PAF23A-230802.iap` | 43.656 B |
| `3043-H1H2TYF23A-240224.zip` | `H1H2TYF23A-240224.iap` | 68.000 B |

SHA-256 dos IAPs extraídos:

- `H1H2LNF13A-230611.iap`: `ee4db42dd4b250bc64c65c0956b27ae7e5a5340106c7ca61948cc33153968ace`;
- `H1H2VWFA3A-230630.iap`: `ee284986b232255e33380b1714b502e54f54f9320b39d4a6db6edf25ae643a6a`;
- `H1H2PAF23A-230802.iap`: `000c33037b83cf3117517ab892fe90370c69c113dcc3288585dd5e7d14550318`;
- `H1H2TYF23A-240224.iap`: `9b916bc6d371de6684b327bf74208aec0a06b2f83e97853febfa4f2b44754785`.

Todos compartilham os mesmos 13 bytes iniciais:

```text
01 09 07 08 00 02 01 07 91 32 47 A4 49
```

Depois divergem, com entropia alta (~7,83–7,95 bits/byte).

Classificação segura: **mesma família de container/binário IAP opaco**. A evidência atual não permite afirmar se o payload é criptografado, comprimido ou outra codificação.

### Firmware observado no equipamento

O relatório `0xF0` recebido em runtime contém ASCII:

`H1H2PAF23A-240409`

O arquivo fornecido `H1H2PAF23A-230802` pertence à mesma família **PAF23A**, mas tem build/data anterior.

Conclusão: ele é útil como comparativo da família, porém **não é prova de ser a imagem exata instalada** na CANBOX capturada.

---

## 12. Sincronização de tempo `0xCB` / `0xC2`

O código original usa `TX 0xCB` para enviar data/hora.

Na captura há principalmente payloads coerentes com 2026-08-05 19:47/19:48, porém existe uma ocorrência isolada em que o byte de hora aparece como `0x07` no meio de uma sequência que usa `0x13` (19 decimal).

Esse desvio é real na captura; sua causa não está determinada. Pode ser produtor concorrente, transformação de horário, estado transitório ou outra condição.

O `RX 0xC2` também contém bits superiores que não devem ser lidos ingenuamente como mês/data sem fechar a máscara/encoding.

Status: **anomalia documentada, não usada para conclusão HVAC**.

---

## 13. O que os ZIPs/logs permitem afirmar hoje

### Confirmado

1. `candata_8` é a captura progressiva mais completa; 5/6/7 são prefixos exatos.
2. O runtime ZIP `(2)` é um superset do ZIP menor para os arquivos centrais.
3. `candata` registra o protocolo serial Hiworld Android ↔ CANBOX, não CAN bruto do veículo.
4. Para RK3326, o caminho observado usa `/dev/ttyS5` a 38400 baud.
5. O protocolo usa framing `5A A5`, comprimento, comando, dados e checksum aditivo.
6. 821 frames foram reconstruídos em `candata_8`, 821 com checksum válido.
7. `0xFF` é ACK do protocolo.
8. `0x6A` solicita relatórios; a sequência observada pede inclusive `0x31` e recebe respostas correspondentes.
9. `0x31` é estado HVAC no parser Peugeot/Hiworld e mostra mudanças reais de estado na captura.
10. Nenhum `TX 0x3B` existe no conjunto `candata_5..8`.
11. `0x1A` não tem semântica mapeada no `HdPsaProtocol` inspecionado; 360/parking usa `0xE8` nessa implementação.
12. A CANBOX em runtime reporta `H1H2PAF23A-240409`.
13. O IAP PAF23A fornecido é da mesma família, mas mais antigo que o runtime.

### Não confirmado

1. arbitration IDs / payloads da CAN veicular abaixo da CANBOX;
2. origem de cada transição `0x31` observada;
3. ação de UI original → `TX 0x3B` → `RX 0x31`;
4. imagem IAP exata instalada da build `PAF23A-240409`;
5. semântica de `0x1A`;
6. encoding completo de `0xC2` e causa do evento atípico em `0xCB`.

---

## 14. Próxima evidência discriminatória da F3

A coleta útil seguinte não é “mais um log genérico”. Deve ser uma sessão sincronizada e controlada:

1. iniciar `candata` + `logcat` com relógio comum;
2. registrar estado HVAC inicial;
3. executar **uma ação por vez na UI original** somente após a fronteira de interação real estar autorizada;
4. marcar timestamp da ação;
5. procurar `TX 0x3B` e subcomando;
6. procurar ACK correspondente;
7. procurar `RX 0x31` posterior;
8. registrar novo `HvacInfo`, latência e efeito físico;
9. repetir para power, A/C, fan, temperaturas, AUTO, SYNC, recirculação, airflow e defrost;
10. manter controle negativo/intervalo para distinguir polling de evento.

Nenhum replay ou frame manual é necessário para essa prova.

## Estado do marco

**Marco passivo F3: forte avanço, mas F3 ainda incompleta.**

O material existente já esclarece a arquitetura e vários estados, porém o gate dinâmico `ação → TX → RX → estado/efeito` ainda requer uma captura controlada com interação real autorizada.