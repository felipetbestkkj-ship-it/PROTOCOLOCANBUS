# EVIDENCE INDEX

Inventário inicial e fatos promovidos. Hash identifica o arquivo exato; não valida sozinho sua finalidade.

| Artefato | SHA-256 | Papel atual |
|---|---|---|
| CANBOX_RUNTIME_CAPTURE_2026-08-06_1201.zip | `308177150441e123b9001cd2d4ae9e4112543f01c0e16d1ffc2444c3a65fe567` | captura runtime central; 15 arquivos centrais |
| CANBOX_RUNTIME_CAPTURE_2026-08-06_1201 (2).zip | `e8cad3fd38ab887cd6ad719b4f6c1e18484e2217085f713ca7d181c01e13836f` | captura runtime ampliada; superset do ZIP menor para os 15 arquivos centrais + 76 diagnósticos adicionais |
| CANBOX-Baseline-20260806-104015.zip | `fb409903ac421a05b3fb2da48a7956f84bae1e5e68a969e7b79b92c390c2ccdf` | baseline + CarInfo instalado |
| CARINFO.apk | `b047b836b1ce62f72a2f7f1f6c83f3da926cfe2362f4b755e9256625d2dc1cf7` | APK de referência analisado na F1/F2/F3 |
| INSTALAR-v3854-CarInfo-HVAC-Visual-V1.apk | `d0741a541fc575d3b25bc853a171532b815e8c396451dcc9ebe0f678d1905a50` | v3854; confirmado como idêntico ao CarInfo instalado da baseline |
| CARINFO.part1.rar | `b3cd85b7eb0c5da3edec3be8b69a578b9f9de73988ab66313e5cdc4bd18fa26a` | multipart CarInfo |
| CARINFO.part2.rar | `6950a1ccb4abb7124fd14c7ab7211045aa5bb408ccd08c40320f9ce21a9d9e39` | multipart CarInfo |
| CARINFO.part3.rar | `fc4fc5a37cb4f6aa433e4cae1bd57cb67ea77fca96e6678a306594596c1885cb` | multipart CarInfo |
| candata_5.log | `2f802683a4cbb5584b294f1b7799a7e19e5f3dd3446e6be4dd61be265bcbd9be` | snapshot progressivo; prefixo exato de `candata_6` |
| candata_6.log | `4d19e3513cfd3b57d64b1e67b0c5b829117b2bf8c5b694beb0b41923edf298e1` | snapshot progressivo; contém 5 e é prefixo exato de 7 |
| candata_7.log | `032c1e72a06bb52b309153ef303e0eb7771fb8dd060cef61ac017de7139b430a` | snapshot progressivo; contém 6 e é prefixo exato de 8 |
| candata_8.log | `f52d1a7dfd936208208ecbfdc79e58a799a2f0fcfb8f2903ffa100dcd8e16211` | captura canônica mais completa do protocolo serial Hiworld Android ↔ CANBOX; não é CAN bruto do veículo |
| logcat_0.log | `721ca35ebcfb544695abe09400a274b771b44a5d730f85b9e674fb9898146139` | runtime Android/Jancar/CarInfo |
| 2910-H1H2PAF23A-230802.zip | `e20e6dc9adba91755b90217b58e628979ffd8cfe148840290857df6d4b196001` | IAP Hiworld da família PAF23A; anterior ao `PAF23A-240409` reportado pela CANBOX em runtime |
| 3043-H1H2TYF23A-240224.zip | `25cf2de3c0d9dc8f96f615c22332becf6d6234887c8d4ecdf8b8fae55ceb5349` | comparativo IAP de outra família |
| 2868-H1H2VWFA3A-230630.zip | `9ae03672c818ef7009737fd01bd4e298f59bae3270693840e7725cc4a1a3e169` | comparativo IAP de outra família |
| 2851-H1H2LNF13A-230611.zip | `45e7be52440367925882d084658e585dfe09bcee10761836767ddfbf4596745f` | comparativo IAP de outra família |
| jadx.zip | `a13d2be02ed640de54df937ead680f31ea06f4b8efd01860b9f0cf18a7d40e34` | ferramenta anexada; usada como auxiliar de análise estática |
| Engenharia-Reversa-CANBOX.zip | `49d82db8e0662a679d5be94459954ee411db20510ed1f83fa71f2c6fbf39a8a3` | artefato derivado; estrutura ZIP com diretório central/EOCD ausente, 4.122 entradas recuperáveis por cabeçalhos locais |
| OMEGAS_DIAGNOSTIC_20260608_1134.zip | `180b8daa074c5a5e7ed7c9c0a9a11eca6b7b33e77672069f5a966e78603f366b` | diagnóstico de ambiente/dispositivo; logs USB/CP2102 não devem ser confundidos com o enlace interno CarInfo ↔ CANBOX |

## Fatos promovidos pela F1

- O APK `CarInfo/CarInfo-atualmente-instalado.apk` extraído da baseline possui SHA-256 `d0741a541fc575d3b25bc853a171532b815e8c396451dcc9ebe0f678d1905a50`, idêntico ao `INSTALAR-v3854-CarInfo-HVAC-Visual-V1.apk`.
- A baseline registra `com.can.activity`, `versionCode=3854`, shared user `android.uid.system/1000` e processo persistente/privilegiado.
- A captura runtime de 12:01 prova um ciclo de crash/restart de `com.can.activity` com tentativa de acesso a um caminho antigo de `base.apk` inexistente; a causa raiz permanece aberta.
- Relatório: `docs/F1_CARINFO_HVAC_TRIAGEM.md`.

## Fatos promovidos pela F2

- A UI original envia `CarPropertyValue` e a cadeia chega a `CanBusService.setHvacProperty → buildHvacPackets → CanRxTx.sendData`.
- `HdPsaProtocol` constrói controles HVAC com comando Hiworld `0x3B` e decodifica `0x31` como informação HVAC.
- Os `candata_5..8` já continham RX `0x31`, mas nenhum TX `0x3B` observado.
- Relatório: `docs/F2_HVAC_ORIGINAL_CHAIN.md`.

## Fatos promovidos pelo marco passivo da F3

### Hierarquia das fontes

- `candata_5 → 6 → 7 → 8` são prefixos exatos progressivos; `candata_8` é a captura canônica mais completa.
- O runtime ZIP `(2)` contém todos os 15 arquivos centrais do ZIP menor de forma byte a byte idêntica e adiciona 76 diagnósticos.
- `Engenharia-Reversa-CANBOX.zip` é derivado e incompleto no diretório central, mas contém milhares de entradas recuperáveis; não substitui evidência original de runtime.

### Camada e transporte

- `candata_*` registra o **protocolo serial Hiworld/Jancar no limite Android ↔ CANBOX**, não frames CAN brutos do veículo.
- No equipamento RK3326 analisado, código + configuração sustentam `/dev/ttyS5` a **38400 baud** para esse enlace.
- A configuração converge para `Hiworld-Peugeot-208-2023~Present（Brazil）-All`.

### Framing e runtime

- Framing: `5A A5 <len> <cmd> <data...> <checksum>`.
- `candata_8` contém **821 frames reconstruídos e 821/821 checksums aditivos válidos**.
- `0xFF`/`0xFE` são ACKs do protocolo; o volume de `0xFF` não representa funções automotivas distintas.
- `TX 0x6A` é usado pelo Car Info para consultar relatórios específicos da CANBOX. A captura contém a sequência `0x11, 0x31, 0x94, 0x71, 0x72, 0x76, 0x79, 0xF0`, seguida dos respectivos relatórios.
- Parte dos `RX 0x31` é, portanto, **estado HVAC solicitado**, não prova de um toque HVAC.
- Os `RX 0x31` mostram transições de power, A/C, recirculação, front/rear defrost, fan e airflow.
- Continua havendo **zero TX `0x3B`** em `candata_5..8`; a origem das transições `0x31` não está provada.
- `0x1A` é altamente variável, mas não está registrado/decodificado pelo `HdPsaProtocol` inspecionado; o ID de 360/parking nessa implementação é `0xE8`, portanto `0x1A` permanece sem semântica promovida.

### Firmware

- O relatório `0xF0` da CANBOX em runtime expõe `H1H2PAF23A-240409`.
- O IAP fornecido `H1H2PAF23A-230802` é da mesma família PAF23A, mas é mais antigo e não é a imagem exata comprovadamente instalada.
- Os IAPs fornecidos compartilham um cabeçalho binário comum de 13 bytes e depois divergem; a evidência atual não permite classificar o conteúdo como criptografado ou comprimido.

Relatório detalhado: `docs/F3_CAN_RUNTIME_EVIDENCE_DEEP_DIVE.md`.

## Política

Abrir somente o artefato necessário para responder à pergunta do bloco. Ferramenta anexada não é evidência do comportamento do alvo. Nunca converter ID/comando do protocolo CANBOX em “CAN ID do veículo” sem evidência da camada CAN inferior.