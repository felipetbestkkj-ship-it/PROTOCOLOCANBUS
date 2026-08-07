# PROJECT STATE

**Projeto:** PROTOCOLOCANBUS  
**Repositório:** `felipetbestkkj-ship-it/PROTOCOLOCANBUS`  
**Visibilidade:** pública por decisão explícita do proprietário  
**Linha consolidada:** somente `main` durante a descoberta, salvo autorização explícita para branch  
**F0:** PASS  
**F1:** PASS — triagem Car Info/HVAC  
**F2:** PASS — cadeia HVAC original  
**F3:** ATIVA / PARTIAL — gêmeo digital offline concluído; resta somente o gate físico único  
**Última atualização:** 2026-08-07

## Missão atual

Reconstruir de forma dirigida a cadeia Car Info/HVAC a partir das evidências do próprio projeto, sem herança técnica de repositórios anteriores, até obter uma camada própria, testável e reproduzível.

## Ordem operacional

`Notion → Codex Engineering Guardrails → GitHub Connector → execução → GitHub atualizado → Notion sincronizado`

Estado local e memória do chat nunca substituem o remoto.

## Governança vigente

- `main` é o padrão e estado consolidado;
- qualquer branch diferente de `main` exige autorização clara e explícita do proprietário;
- concorrência durante descoberta é resolvida por serialização/fresh-read, não por branch automática;
- operação remote-first;
- alvo real, transmissão CAN, replay, instalação, ROM/firmware/root e outras fronteiras materiais exigem autorização própria;
- D-013 vigente: descoberta material deve deixar **detalhe reproduzível/versionado no GitHub + mapa humano anti-retrabalho no Notion**.

Detalhes: `AGENTS.md`, `REMOTE_OPERATION_POLICY.md`, `WORKFLOWS.md`, `ROADMAP.md`, `docs/BRANCH_POLICY.md`.

## F1 — triagem Car Info/HVAC

Relatório: `docs/F1_CARINFO_HVAC_TRIAGEM.md`.

Confirmado:

- alvo central: `Car Info / com.can.activity`;
- `INSTALAR-v3854-CarInfo-HVAC-Visual-V1.apk` é byte a byte o APK registrado como instalado na baseline, SHA-256 `d0741a541fc575d3b25bc853a171532b815e8c396451dcc9ebe0f678d1905a50`;
- baseline: `versionCode=3854`, shared user `android.uid.system/1000`, contexto privilegiado/persistente;
- diferenças significativas da v3854 na superfície HVAC concentram-se em layout/cores/drawables; `HvacActivity`, `HvacFragment` e `HvacModel` permaneceram iguais na comparação realizada;
- cadeia estática alcança `HvacFragment → HvacViewModel/HvacModel → CanBusManager → CanPopWind → ICanUI/ICanBus`;
- runtime confirma Car Info/Jancar, framing `5A A5` e Hiworld `H1H2PAF23A-240409`;
- crash/restart loop de `com.can.activity` tentando caminho antigo de `base.apk` permanece aprendizado L-004 com causa ainda não provada.

## F2 — cadeia HVAC original

Relatório: `docs/F2_HVAC_ORIGINAL_CHAIN.md`.

Confirmado:

- a UI envia `CarPropertyValue`, não bytes diretamente;
- controle: `HvacFragment → HvacViewModel/HvacModel → CanBusManager → ICanBus → CanBusService.setHvacProperty → HdPsaProtocol.buildHvacPackets → CanProxy/CanSender → CanRxTx.sendData`;
- `PeugeotHiworldManager` aponta para `HdPsaProtocol`, coerente com runtime `Hiworld-Peugeot-208-2023~Present（Brazil）-All`;
- controles HVAC são construídos como `5A A5 02 3B <subcomando> <valor> <checksum>`;
- `0x31` é registrado/decodificado como estado HVAC e retorna a `HvacInfo → HvacModel/ViewModel → HvacFragment`.

## F3 — correlação runtime e laboratório offline

Relatórios:

- `docs/F3_CAN_RUNTIME_EVIDENCE_DEEP_DIVE.md`;
- `docs/F3_PASSIVE_CONTINUATION_TX_COVERAGE.md`;
- `docs/F3_HVAC_DIGITAL_TWIN.md`;
- `docs/F3_ONE_SHOT_VALIDATION.md`;
- `docs/F3_RUNTIME_CAPTURE_PROTOCOL.md` — referência geral/fallback de captura; **não é mais a sequência recomendada ao proprietário**.

Ferramentas:

- `scripts/analyze_hiword_candata.py` — parser passivo de captures Hiworld;
- `scripts/hiworld_hvac_digital_twin.py` — gêmeo digital offline/fake CANBOX; sem I/O de dispositivo e sem transmissão.

Testes:

- `tests/test_hiword_hvac_digital_twin.py`.

### Camada e framing comprovados

- `candata_5 → 6 → 7 → 8` são snapshots progressivos; `candata_8` é a captura canônica mais completa;
- `candata_*` registra **serial Hiworld/Jancar Android ↔ CANBOX**, não CAN bruto do Peugeot;
- caminho observado: `Car Info/Jancar → /dev/ttyS5 @ 38400 → CANBOX Hiworld → CAN veicular`;
- framing: `5A A5 <LEN> <CMD> <DATA...> <CHECKSUM>`;
- `candata_8`: 821 frames reconstruídos e 821/821 checksums válidos;
- `0xFF/0xFE` são ACKs;
- `0x6A` consulta relatórios; o polling inclui `0x31` HVAC;
- Hiworld runtime: `H1H2PAF23A-240409`.

### TX/RX runtime

Todo o vocabulário TX de `candata_8` foi esgotado:

- `0xFF` = 251 ACK;
- `0xCB` = 50 hora/data;
- `0x6A` = 8 consultas;
- `0xA1` = 7 mídia/source/volume;
- `0xA4` = 3 mídia/CD-CDC;
- `0x3B` = **0**.

O caminho conhecido `setHvacProperty → mCanProxy → CanSender → doTx` entrega ao logger TX o mesmo pacote enviado à porta. Um `0x3B` de 7 bytes seria capturável. Portanto os sete pushes HVAC existentes **não foram produzidos pelo caminho HVAC conhecido do Car Info durante aquela captura**.

Os 16 RX `0x31` representam 8 estados lógicos; somente o primeiro é resposta a `0x6A → 0x31`. Os outros 7 são `RX_NAO_SOLICITADO` pelo mecanismo de polling conhecido.

### Keycode-mode eliminado para a configuração Peugeot ativa

A UI HVAC possui command/property mode e um modo alternativo por keycodes. A análise do fluxo de `HvacFragment.customizeView(...)` + `CanBusManager.HvacPropId.isKeyCode(...)` + property list do `HdPsaProtocol` fechou que:

- keycodes especiais são IDs `> 61440`;
- `HdPsaProtocol.initHvacPropertyList()` publica apenas propriedades normais do HVAC (`16385...24577` relevantes);
- a lista-base começa vazia e a mutação posterior localizada só ajusta temperatura `16400` para unidade;
- não há injeção de IDs keycode para esta configuração.

**Consequência:** a UI Peugeot ativa permanece em command/property mode e seu caminho previsto termina no builder `0x3B`. A ausência de `0x3B` não pode ser explicada por um keycode-mode oculto dessa tela.

### Gêmeo digital HVAC — resultado

O gêmeo digital separa `STATIC`, `OBSERVED`, `SIMULATED` e `INFERRED`.

Ele reproduz:

- framing/checksum;
- builder `0x3B`, incluindo supressões e comandos dependentes do estado;
- parser/encoder `0x31` com round-trip byte a byte dos oito estados reais;
- state machine empírica;
- endpoint fake CANBOX: recebe `0x3B` offline e gera `0x31` previsto, usando assinatura empírica quando existe match exato e somente efeito mínimo estático quando não existe.

A sequência diferencial dos oito estados reais é inferida como:

1. `FRONT_DEFROST_ON` — confiança 0,90;
2. `REAR_DEFROST_ON` — 0,999, único campo alterado;
3. `FRONT_DEFROST_OFF` — 0,86;
4. `REAR_DEFROST_OFF` — 0,999, único campo alterado;
5. `RECIRCULATION_ON` — 0,995, único campo alterado;
6. `HVAC_POWER_OFF` — 0,98;
7. `HVAC_POWER_ON` — 0,98, retorno exato ao estado-base.

Estas etiquetas são `INFERRED`, não `CORRELATED`; o fato observado é a transição `0x31`.

### Validação offline

Executado antes da consolidação do gêmeo:

- `python scripts/hiworld_hvac_digital_twin.py --self-test` → PASS;
- `python -m unittest discover -s tests -v` → **11/11 PASS**;
- regressão contra `candata_8.log` → 821 frames válidos, 8 estados `0x31`, `0x3B=0`, replay/state vector exato e sequência inferida reproduzida.

Cobertura inclui checksum, vetores `0x3B`, round-trip `0x31`, power redundante, inversão de recirculação, fan absoluto, airflow por bits, passos de temperatura, replay da state machine e fake CANBOX para rear-defrost.

## Gate físico residual da F3 — UMA ação

A antiga matriz manual de múltiplas funções foi substituída por `docs/F3_ONE_SHOT_VALIDATION.md`.

Quando houver autorização material para usar o carro, a única ação humana necessária é:

> com **rear defrost OFF**, tocar **rear defrost ON uma vez** na UI original do Car Info, com `DbgAssist` capturando RX/TX.

Previsão fechada antes do teste:

- property `24577`, área `2`, valor `1`;
- TX estático esperado: `5A A5 02 3B 06 01 43`;
- retorno esperado: `0x31 payload[2] bit5` muda `0 → 1`;
- na transição real já observada de rear-defrost, nenhum outro campo `0x31` mudou.

Se aparecer `TX 0x3B` previsto + ACK + `RX 0x31` correspondente + efeito físico coerente, o elo comum `UI → 0x3B → CANBOX/veículo → 0x31` fica provado. **Não pedir teste função por função depois disso.**

Se o TX previsto não aparecer, preservar essa única captura e voltar à análise offline; não iniciar tentativa e erro no carro.

## Lacunas que permanecem abertas

- o gate físico único acima ainda não foi executado;
- produtor material dos sete `RX_NAO_SOLICITADO` anteriores ainda não foi identificado, embora o fluxo normal da UI Car Info e keycode-mode tenham sido excluídos para aquela captura/configuração;
- arbitration IDs/payloads da CAN veicular abaixo da CANBOX não foram observados;
- imagem IAP exata `PAF23A-240409` não foi fornecida;
- `0x1A data[9:10]` continua hipótese forte de RPM, não fato promovido;
- causa raiz do crash `sourceDir` continua pendente.

## Sistema de aprendizado

Skills canônicas: `SKILLS_INDEX.md` + `skills/*/SKILL.md`.

Aprendizados recentes:

- L-005 → `runtime-static-correlation`: frame estático ≠ TX observado;
- L-006 → `reusable-engineering-learning`: fresh-read antes de reservar ID;
- L-007 → `can-frame-differential-analysis`: provar camada/transporte antes de interpretar ID;
- L-008 → documentação em duas camadas/teste anti-retrabalho;
- L-009 → separar resposta solicitada/push antes de inferir causa;
- **L-010 → `protocol-digital-twin-inference`: antes de pedir bateria de testes físicos, construir gêmeo digital e escolher um experimento de máxima informação.**

A nova skill foi metodologicamente adaptada de práticas públicas de reverse engineering de protocolos/binary analysis e validada contra as evidências do próprio projeto; nenhuma conclusão externa virou fato do PROTOCOLOCANBUS sem verificação local.

## Próximo passo único

**Não executar matriz de tentativa e erro.**

Após autorização explícita para interação física, executar somente `docs/F3_ONE_SHOT_VALIDATION.md`: **rear-defrost ON uma vez**, capturar TX/RX e decidir o elo comum. Sem replay, sem frame manual, sem ROM/firmware.
