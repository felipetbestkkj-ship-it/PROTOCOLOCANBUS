# F2 — Cadeia HVAC original

## Resultado executivo

A F2 reconstrói, por análise estática dirigida e cruzamento com os logs já existentes, a cadeia original de HVAC desde a ação de interface até o pacote entregue à camada CAN e o caminho inverso de estado recebido até a UI.

A arquitetura observada não faz a tela manipular bytes CAN diretamente. A UI produz `CarPropertyValue`; a propriedade atravessa `HvacViewModel`, `HvacModel` e `CanBusManager`, chega por Binder ao `CanBusService`, é convertida pelo protocolo ativo em um ou mais pacotes e então entregue ao `CanRxTx` da plataforma.

Para a família Peugeot/Hiworld inspecionada, `PeugeotHiworldManager` constrói `ProtocolBean` com `com.autoai.canbus.psa.protocol.HdPsaProtocol`. O runtime disponível identifica a configuração como `Hiworld-Peugeot-208-2023~Present（Brazil）-All`, e os frames de estado observados usam exatamente a mensagem `0x31` que `HdPsaProtocol` registra e decodifica como informação de ar/HVAC.

A F2 também resolve a antiga dúvida sobre `0x31`: no protocolo `HdPsaProtocol`, `0x31` é o comando de informação HVAC recebido. Os logs atuais contêm frames `0x31` válidos e com alterações coerentes de estado. O que permanece para a F3 é correlacionar cada alteração com uma ação física/toque cronometrado e observar diretamente os TX de controle.

Nenhum comando CAN foi transmitido, nenhum replay foi feito e a multimídia/carro não foram modificados neste bloco.

## 1. Escopo e critério de saída

Objetivo oficial da F2:

`ação de UI → propriedade/método → controlador/serviço → mensagem → retorno → estado`

Gate:

- matriz por função;
- caminho de controle e retorno identificados;
- separação explícita entre prova estática e efeito físico ainda não correlacionado;
- nenhuma transmissão por hipótese.

Base técnica consolidada: `main @ eafe05da982928156e378104e8bb61e5ff5c2a5e`.

## 2. Caminho geral de controle

### 2.1 UI

O `com.autoai.canbus.ui.hvac.fragment.HvacFragment` cria `CarPropertyValue` para operações de HVAC. Entre os IDs observados:

| Propriedade | ID | Papel de alto nível |
|---|---:|---|
| HVAC power | `16385` | liga/desliga HVAC |
| A/C | `16386` | compressor/A-C |
| temperatura setpoint | `16387` | temperatura solicitada |
| temperatura ajuste | `16388` | subir/descer temperatura |
| fan setpoint | `16389` | nível solicitado |
| fan ajuste | `16390` | subir/descer fan |
| fan position | `16391` | direção do ar |
| wind intensity | `16392` | intensidade/modo adicional |
| auto recirculation | `16393` | recirculação automática |
| recirculation | `16394` | recirculação |
| automatic mode | `16395` | AUTO |
| MAX A/C | `16396` | MAX A/C |
| SYNC | `16404` | sincronização |
| window defroster | `24577` | desembaçadores por área |

O fragmento suporta envio por propriedade e, em configurações que usam teclas, converte a propriedade para keycode por `CanBusManager.HvacPropId.id2KeyCode(...)`.

### 2.2 ViewModel e Model

`HvacViewModel.setProperty(...)` delega para `HvacModel.setProperty(...)`.

`HvacModel`:

- cria `CanBusManager`;
- conecta ao serviço;
- consulta `getPropertyList("hvac")`;
- consulta o estado corrente com `getHvacInfo()`;
- registra callback para mudanças;
- encaminha `CarPropertyValue` por `CanBusManager.setHvacProperty(...)`.

### 2.3 Binder / serviço

`CanBusManager` faz bind explícito em:

`com.can.activity/com.can.ui.CanPopWind`

Obtém `ICanUI`, chama `getCanService("CanBusManager")` e recebe a interface `ICanBus`.

No serviço, `ICanBus.setHvacProperty(CarPropertyValue)` executa:

1. `mObjProtocol.buildHvacPackets(carPropertyValue)`;
2. rejeita lista nula/vazia;
3. envia cada pacote por `mCanProxy.sendData2Can(...)` ou pelo canal alternativo quando configurado.

O proxy encaminha o pacote ao `CanSender`; no fim da cadeia, `doTx(...)` chama `mCanRxTx.sendData(...)`.

### Cadeia consolidada

`HvacFragment → CarPropertyValue → HvacViewModel → HvacModel → CanBusManager → ICanUI/ICanBus Binder → CanBusService.setHvacProperty → protocolo.buildHvacPackets → CanProxy/CanSender → CanRxTx.sendData`

## 3. Protocolo Peugeot/Hiworld inspecionado

`PeugeotHiworldManager` declara:

- baud rate `38400`;
- versão `V4.4.4_2025.05.15`;
- protocolo `com.autoai.canbus.psa.protocol.HdPsaProtocol`;
- suporte HVAC quando o `ProtocolBean` é construído com HVAC habilitado.

O ramo `modelID == 19` constrói `ProtocolBean` com HVAC e demais capacidades habilitadas; para `modelYearID == 3` adiciona CD e mantém o mesmo protocolo.

O runtime disponível registra:

`Hiworld-Peugeot-208-2023~Present（Brazil）-All`

Classificação: **fortemente sustentado por estático + runtime** que esta configuração usa a família `PeugeotHiworldManager/HdPsaProtocol`. A F2 não afirma ter observado em log a instanciação Java da classe pelo nome; essa confirmação de runtime pode ser reforçada na F3.

### Observação sobre classe de HVAC declarada pelo manager

O manager contém a string:

`com.autoai.canbus.base.mvvm.air.HvacFragment`

Essa classe não foi localizada no `CARINFO.apk` pela busca dirigida realizada. Em contrapartida, a superfície HVAC do próprio APK usa o conjunto `com.autoai.canbus.ui.hvac.fragment.*`, incluindo `PopWindowHvacFragment` e o `HvacFragment` já mapeado.

Portanto, a string do manager é registrada como **referência de configuração, não prova do entrypoint visual efetivamente carregado**.

## 4. Tradução de propriedades para comandos de baixo nível

`HdPsaProtocol.buildHvacPackets(...)` traduz propriedades de alto nível para subcomandos e gera cada pacote por:

`getPacket(59, 59, new byte[]{subcomando, valor})`

`59 decimal = 0x3B`.

O formato produzido por `HdProtocol.getPacket(...)` é:

`5A A5 <len> <cmd> <dados...> <checksum>`

Para HVAC de controle, com dois bytes de dados:

`5A A5 02 3B <subcomando> <valor> <checksum>`

O checksum implementado equivale, para esse frame, a:

`(0x02 + 0x3B + subcomando + valor - 1) & 0xFF`

### Matriz de controle estático

| Função lógica | Property ID | Área/entrada relevante | Subcomando `0x3B` | Valor de baixo nível | Exemplo estático |
|---|---:|---|---:|---|---|
| HVAC dianteiro ON | `16385` | área `8`, valor `1` | `0x01` | `1` | `5A A5 02 3B 01 01 3E` |
| HVAC traseiro ON | `16385` | área `128`, valor `1` | `0x11` | `1` | `5A A5 02 3B 11 01 4E` |
| A/C ON | `16386` | valor `1` | `0x02` | `1` | `5A A5 02 3B 02 01 3F` |
| MAX A/C ON | `16396` | valor `1` | `0x03` | `1` | `5A A5 02 3B 03 01 40` |
| AUTO ON | `16395` | valor não-zero | `0x04` | `1` | `5A A5 02 3B 04 01 41` |
| desembaçador dianteiro ON | `24577` | área `1` | `0x05` | `1` | `5A A5 02 3B 05 01 42` |
| desembaçador traseiro ON | `24577` | área `2` | `0x06` | `1` | `5A A5 02 3B 06 01 43` |
| recirculação | `16394` | valor lógico | `0x07` | invertido pelo protocolo | padrão `5A A5 02 3B 07 vv cc` |
| posição do ar bit 1 | `16391` | comparação com estado | `0x08` | `0/1` | padrão |
| posição do ar bit 2 | `16391` | comparação com estado | `0x09` | `0/1` | padrão |
| posição do ar bit 4 | `16391` | comparação com estado | `0x0A` | `0/1` | padrão |
| fan + | `16390` | input `1` | `0x0B` | `1` | `5A A5 02 3B 0B 01 48` |
| fan - | `16390` | input `0` | `0x0B` | `2` | padrão |
| temp esquerda + | `16388` | área diferente de `4`, input `1` | `0x0C` | `1` | `5A A5 02 3B 0C 01 49` |
| temp esquerda - | `16388` | input `0` | `0x0C` | `2` | padrão |
| temp direita + | `16388` | área `4`, input `1` | `0x0D` | `1` | `5A A5 02 3B 0D 01 4A` |
| temp direita - | `16388` | área `4`, input `0` | `0x0D` | `2` | padrão |
| wind intensity | `16392` | `0..2` | `0x0E` | direto | `5A A5 02 3B 0E 01 4B` para `1` |
| SYNC ON | `16404` | valor `1` | `0x0F` | `1` | `5A A5 02 3B 0F 01 4C` |
| auto recirculation ON | `16393` | valor `1` | `0x10` | `1` | `5A A5 02 3B 10 01 4D` |

**Importante:** os exemplos acima são resultado direto da função de construção do protocolo. Eles não são classificados como TX observado no carro.

### Comandos que dependem do estado atual

Algumas propriedades não viram um único “set absoluto”:

- `16387` temperatura absoluta compara a temperatura desejada com `HvacInfo` e emite 1 ou 2 passos de `0x0C/0x0D` para cima/baixo;
- `16389` fan absoluto compara com `frontWindLevel` e emite `0x0B` repetidamente até alcançar o nível solicitado;
- `16391` direção do ar compara o bitmask atual e emite somente os subcomandos `0x08/0x09/0x0A` que precisam mudar;
- `16394` recirculação inverte o valor lógico antes de gerar o subcomando `0x07` e evita envio redundante quando o estado já coincide;
- power dianteiro também evita envio quando o estado já coincide.

Esse desenho confirma que `HvacInfo` recebido não é apenas visual: ele participa da geração correta de comandos.

## 5. Lista de propriedades HVAC exposta pelo protocolo

`HdPsaProtocol.initHvacPropertyList()` publica, entre outras:

- temperatura atual esquerda/direita: `16400`, faixa nominal `16.0..32.0`, passo `0.5`;
- ajuste de temperatura `16388`;
- posição do ar `16391`;
- fan atual `16401`, `0..8`;
- ajuste de fan `16390`;
- power dianteiro/traseiro `16385`;
- A/C `16386`;
- MAX A/C `16396`;
- AUTO `16395`;
- SYNC `16404`;
- wind intensity `16392`;
- desembaçadores `24577` áreas 1 e 2;
- recirculação `16394`;
- recirculação automática `16393`.

A UI usa `getPropertyList("hvac")` para adaptar controles à capacidade exposta pelo protocolo.

## 6. Caminho de retorno: `0x31` → HvacInfo → UI

### 6.1 Identificação do comando

No `HdProtocol`:

- cabeçalho: `0x5A 0xA5`;
- `rxAirInfoCmdId = 49` = **`0x31`**.

No `HdPsaProtocol.create()` o comando é registrado com payload de comprimento `12`.

No dispatcher do protocolo:

- se `parseRegisterCmdId == rxAirInfoCmdId`;
- chama `parseAirInfo(...)`;
- envia o `HvacInfo` ao proxy com mensagem `102`.

Portanto, para `HdPsaProtocol`, **`0x31` é explicitamente a mensagem de informação do ar/HVAC**.

### 6.2 Decodificação do payload `0x31`

`HdPsaProtocol.parseAirInfo(...)` interpreta:

| Byte do frame | Bits/valor | Estado produzido |
|---|---|---|
| `[4]` | bit 6 | HVAC power |
| `[4]` | bit 5 | MAX A/C |
| `[4]` | bit 4 | rear HVAC power |
| `[4]` | bit 3 | AUTO light 1 |
| `[4]` | bit 2 | SYNC |
| `[4]` | bit 0 | A/C |
| `[5]` | bit 4 | recirculação |
| `[5]` | bit 3 | auto recirculação |
| `[6]` | bit 5 | rear defrost |
| `[6]` | bit 4 | front defrost |
| `[7]` | bits 0–1 | wind intensity |
| `[8]` | nibble baixo | modo/direção do ar, convertido para bitmask |
| `[9]` | byte | fan dianteiro |
| `[10]` | byte | temperatura esquerda |
| `[11]` | byte | temperatura direita |
| `[15]` | byte | temperatura externa |

Depois, `CanPopWind` recebe a mensagem 102, atualiza o `HvacInfo` compartilhado e notifica os listeners externos. O callback chega ao `HvacModel/ViewModel`, e `HvacFragment.setHvacInfo(...)` atualiza power, direção do ar, fan e temperaturas com o estado recebido.

### Cadeia de retorno consolidada

`CAN/serial → CanRxTx → protocolo HdPsaProtocol → frame 0x31 → parseAirInfo → HvacInfo → CanPopWind/ICanBus callback → HvacModel/ViewModel → HvacFragment.setHvacInfo → controles visuais`

## 7. Cruzamento com `candata_8.log`

Foram encontrados frames RX reais com:

`5A A5 0C 31 ... checksum`

O tamanho `0x0C` coincide com o registro de 12 bytes feito por `HdPsaProtocol`, e os checksums dos frames únicos inspecionados são válidos segundo a gramática `HdProtocol`.

Exemplos reais:

- `5A A5 0C 31 45 10 00 01 06 04 FE FE 00 00 00 82 1A`
- `5A A5 0C 31 45 10 10 01 0B 07 FF FE 00 00 00 82 33`
- `5A A5 0C 31 45 10 30 01 0B 07 FF FE 00 00 00 82 53`
- `5A A5 0C 31 45 00 20 01 06 04 FE FE 00 00 00 82 2A`
- `5A A5 0C 31 45 00 00 01 06 04 FE FE 00 00 00 82 0A`
- `5A A5 0C 31 04 10 00 01 06 00 FE FE 00 00 00 82 D5`

Mudanças que o parser interpreta nesses frames incluem, por exemplo:

- front/rear defrost alterando bits do byte `[6]`;
- recirculação alterando o byte `[5]`;
- fan variando entre `4`, `7` e `0`;
- power/A-C mudando no último estado listado.

Isso valida que os frames reais têm formato e campos compatíveis com o parser estático. **Não associa ainda cada mudança a um toque específico**, porque a captura atual não contém marcação controlada de ação → horário → TX → RX. Essa é a tarefa da F3.

## 8. TX observado x TX previsto

Busca dirigida nos `candata_5.log` a `candata_8.log` não encontrou frame TX com comando `0x3B` no conjunto atual.

Classificação:

- **CONFIRMADO ESTATICAMENTE:** `HdPsaProtocol.buildHvacPackets` produz `0x3B` para controle HVAC;
- **NÃO OBSERVADO NESTES LOGS:** um TX `0x3B` disparado por ação de UI;
- **CONFIRMADO EM RUNTIME:** RX `0x31` de estado HVAC está presente e muda de payload.

Essa lacuna não bloqueia o gate da F2 porque o roadmap separa a reconstrução da cadeia estática (F2) da correlação ação/TX/RX (F3).

## 9. Matriz final da F2

| Função | UI/propriedade | Backend | TX estático | Retorno/estado | Situação |
|---|---|---|---|---|---|
| Power dianteiro | `16385`, área 8 | `HdPsaProtocol` | `0x3B/0x01` | `0x31` byte4 bit6 | cadeia mapeada; efeito físico vai à F3 |
| Power traseiro | `16385`, área 128 | `HdPsaProtocol` | `0x3B/0x11` | `0x31` byte4 bit4 | cadeia mapeada |
| A/C | `16386` | `HdPsaProtocol` | `0x3B/0x02` | `0x31` byte4 bit0 | cadeia mapeada |
| MAX A/C | `16396` | `HdPsaProtocol` | `0x3B/0x03` | `0x31` byte4 bit5 | cadeia mapeada |
| AUTO | `16395` | `HdPsaProtocol` | `0x3B/0x04` | `0x31` byte4 bit3 | cadeia mapeada |
| Front defrost | `24577`, área1 | `HdPsaProtocol` | `0x3B/0x05` | `0x31` byte6 bit4 | cadeia mapeada; mudança já aparece nos RX existentes |
| Rear defrost | `24577`, área2 | `HdPsaProtocol` | `0x3B/0x06` | `0x31` byte6 bit5 | cadeia mapeada; mudança já aparece nos RX existentes |
| Recirculação | `16394` | `HdPsaProtocol` | `0x3B/0x07`, valor invertido | `0x31` byte5 bit4 | cadeia mapeada; mudança já aparece nos RX existentes |
| Direção do ar | `16391` | `HdPsaProtocol` | `0x3B/0x08..0x0A` | `0x31` byte8 | cadeia mapeada |
| Fan +/- | `16390` | `HdPsaProtocol` | `0x3B/0x0B`, `1/2` | `0x31` byte9 | cadeia mapeada; níveis variam nos RX existentes |
| Fan setpoint | `16389` | comparação com estado | múltiplos `0x0B` | `0x31` byte9 | cadeia mapeada |
| Temp esquerda +/- | `16388` | `HdPsaProtocol` | `0x3B/0x0C`, `1/2` | `0x31` byte10 | cadeia mapeada |
| Temp direita +/- | `16388` | `HdPsaProtocol` | `0x3B/0x0D`, `1/2` | `0x31` byte11 | cadeia mapeada |
| Temp setpoint | `16387` | comparação com estado | passos `0x0C/0x0D` | `0x31` bytes10/11 | cadeia mapeada |
| Wind intensity | `16392` | `HdPsaProtocol` | `0x3B/0x0E` | `0x31` byte7 bits0-1 | cadeia mapeada |
| SYNC | `16404` | `HdPsaProtocol` | `0x3B/0x0F` | `0x31` byte4 bit2 | cadeia mapeada |
| Auto recirc | `16393` | `HdPsaProtocol` | `0x3B/0x10` | `0x31` byte5 bit3 | cadeia mapeada |

## 10. O que a F2 prova e o que não prova

### Provado

- a UI trabalha por propriedades de alto nível;
- a cadeia Binder/serviço é identificada até `CanRxTx.sendData`;
- `HdPsaProtocol` possui tradução completa das propriedades HVAC relevantes para frames `0x3B`;
- a gramática `5A A5` e checksum usados por esses frames foram identificados;
- `0x31` é o comando de estado HVAC no `HdPsaProtocol`;
- o payload `0x31` é decodificado para power/A-C/SYNC/recirc/defrost/fan/modos/temperaturas;
- frames `0x31` reais e checksum-válidos estão presentes nos logs existentes;
- o retorno alimenta `HvacInfo` e volta à UI por callback.

### Não provado ainda

- qual toque específico gerou qual TX `0x3B` no equipamento real;
- observação direta de TX `0x3B` nos logs disponíveis;
- latência ação → TX → RX → UI;
- comportamento físico de cada subcomando no carro;
- instanciação runtime da classe `HdPsaProtocol` registrada nominalmente em log;
- motivo da referência `com.autoai.canbus.base.mvvm.air.HvacFragment` não localizada neste APK;
- causa raiz do crash loop de `sourceDir` observado na F1.

Esses itens não são mascarados como falha da F2: os quatro primeiros pertencem explicitamente à **F3 — Correlação runtime**.

## 11. Gate da F2

**Atendido.** Existe agora uma matriz por função com ação/propriedade, caminho de serviço, tradução de protocolo, frame estático previsto, retorno de estado e lacunas explícitas.

Próximo passo técnico: **F3 — Correlação runtime**, criando evidência temporal controlada `ação → logcat → TX 0x3B → RX 0x31 → estado`, sem transmitir frames construídos manualmente e sem modificar o equipamento fora de autorização própria.