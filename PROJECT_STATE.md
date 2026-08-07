# PROJECT STATE

**Projeto:** PROTOCOLOCANBUS  
**Repositório:** `felipetbestkkj-ship-it/PROTOCOLOCANBUS`  
**Visibilidade:** pública por decisão explícita do proprietário  
**Fundação F0:** PASS — publicada e verificável  
**Governança F0.1:** PASS — operação remote-first definida  
**Governança F0.2:** PASS — sistema de aprendizado/skills integrado  
**Governança F0.4:** PASS — `main` única durante descoberta  
**Governança F0.5:** PASS — decisão permanente de branch por risco + autorização explícita  
**Fase F1:** PASS — consolidada na `main`  
**Fase F2:** PASS — cadeia HVAC original mapeada  
**Fase atual:** F3 — ATIVA; marco passivo das evidências CANBOX concluído, correlação controlada ainda pendente  
**Última atualização:** 2026-08-07

## Missão atual

Reconstruir de forma dirigida a cadeia Car Info/HVAC a partir das evidências locais, mantendo o projeto autossuficiente e sem herança técnica de repositórios anteriores.

## Ordem de entrada oficial

`Notion → Codex Engineering Guardrails → GitHub Connector → execução → GitHub atualizado → Notion sincronizado`

Estado local nunca substitui o GitHub remoto.

## Política de branch vigente — risco + autorização

**`main` é o padrão permanente. Branch é ferramenta de isolamento de risco, não etapa obrigatória.**

A engenharia pode recomendar uma branch quando provar benefício concreto de isolamento, por exemplo preservar executável conhecido como bom, isolar mudança executável potencialmente quebrável, comparar implementações independentes, permitir paralelismo de código realmente não serializável ou separar hotfix/release.

Mesmo nesses casos, **criar ou usar qualquer branch diferente de `main` exige autorização clara e explícita do proprietário para aquele objetivo**.

Depois da autorização, a autonomia normal do bloco permanece: commits, testes, correções e documentação dentro da linha autorizada não exigem microautorizações. Merge/release/publicação continuam fronteiras separadas, salvo se a autorização original as incluir.

Sem autorização, somente `main`. O padrão autorizado normal é `main` + uma branch temporária; uma segunda branch simultânea exige justificativa própria e nova autorização.

Na descoberta/investigação atual, o gate continua resultando em `main` única. Se houver outra escrita/bloco/agente em andamento, o trabalho posterior aguarda ou para, faz fresh-read da `main`, reconcilia e continua nela.

Política detalhada: `docs/BRANCH_POLICY.md`.

Verificação remota atual: apenas a branch `main` existe.

## F1 — resultado consolidado

Relatório técnico: `docs/F1_CARINFO_HVAC_TRIAGEM.md`

### Comprovado na F1

- `Car Info / com.can.activity` permanece o alvo central do HVAC;
- `INSTALAR-v3854-CarInfo-HVAC-Visual-V1.apk` é byte a byte o APK registrado como instalado na baseline, SHA-256 `d0741a541fc575d3b25bc853a171532b815e8c396451dcc9ebe0f678d1905a50`;
- baseline: `versionCode=3854`, shared user `android.uid.system/1000`, contexto privilegiado/persistente;
- manifesto original → v3854 altera `versionCode` 3853 → 3854; package/shared UID/componentes inspecionados permanecem iguais;
- `HvacActivity`, `HvacFragment` e `HvacModel` apresentam código decompilado idêntico entre original e v3854;
- mudança significativa observada na superfície HVAC da v3854 concentra-se em layouts, cores e novos drawables;
- cadeia estática alcança `HvacFragment → HvacViewModel/HvacModel → CanBusManager → CanPopWind → ICanUI/ICanBus`;
- runtime confirma Car Info/Jancar, enquadramento `5A A5` e identificador Hiworld `H1H2PAF23A-240409`;
- captura runtime posterior contém crash/restart loop de `com.can.activity` tentando carregar caminho antigo de `base.apk` inexistente.

## F2 — cadeia HVAC original

Relatório técnico: `docs/F2_HVAC_ORIGINAL_CHAIN.md`

### Comprovado na F2

- UI envia `CarPropertyValue`, não bytes CAN diretamente;
- cadeia de controle chega a `CanBusService.setHvacProperty → mObjProtocol.buildHvacPackets → CanProxy/CanSender → CanRxTx.sendData`;
- `PeugeotHiworldManager` aponta a família inspecionada para `HdPsaProtocol`;
- runtime identifica `Hiworld-Peugeot-208-2023~Present（Brazil）-All`;
- `HdPsaProtocol` traduz propriedades HVAC para `5A A5 02 3B <subcomando> <valor> <checksum>`;
- `rxAirInfoCmdId = 0x31`; `HdPsaProtocol` decodifica `0x31` para power, A/C, MAX A/C, AUTO, SYNC, recirculação, desembaçadores, fan, direção e temperaturas;
- retorno percorre `CanPopWind/ICanBus → HvacModel/ViewModel → HvacFragment.setHvacInfo`.

## F3 — marco passivo das evidências CANBOX/runtime

Relatório técnico: `docs/F3_CAN_RUNTIME_EVIDENCE_DEEP_DIVE.md`

### Hierarquia das fontes confirmada

- `candata_5 → candata_6 → candata_7 → candata_8` são snapshots progressivos por prefixo exato; `candata_8` é a captura canônica mais completa;
- `CANBOX_RUNTIME_CAPTURE_2026-08-06_1201 (2).zip` contém os 15 arquivos centrais do ZIP menor byte a byte idênticos e acrescenta 76 diagnósticos;
- `Engenharia-Reversa-CANBOX.zip` é artefato derivado com diretório central/EOCD ausente, mas 4.122 entradas recuperáveis por cabeçalhos locais.

### Camada e transporte confirmados

- os `candata_*` **não são CAN bruto do Peugeot**; registram o protocolo serial Hiworld/Jancar no limite Android/Car Info ↔ CANBOX;
- no RK3326 observado, o caminho sustentado é `Car Info/Jancar → /dev/ttyS5 @ 38400 → CANBOX Hiworld → CAN veicular`;
- a configuração converge para `Hiworld-Peugeot-208-2023~Present（Brazil）-All`;
- `0x31`, `0x3B`, `0x6A` e `0xFF` são IDs/comandos do protocolo CANBOX, não arbitration IDs CAN veiculares comprovados.

### Protocolo/runtime confirmados

- framing: `5A A5 <len> <cmd> <data...> <checksum>`;
- `candata_8` contém 821 frames reconstruídos e 821/821 checksums aditivos válidos;
- `0xFF`/`0xFE` são ACKs;
- `TX 0x6A` é o mecanismo de consulta: a captura mostra pedidos `0x11, 0x31, 0x94, 0x71, 0x72, 0x76, 0x79, 0xF0` seguidos dos relatórios correspondentes;
- portanto parte dos `RX 0x31` é estado HVAC **solicitado pelo app**, não prova de toque HVAC;
- `RX 0x31` mostra transições de power, A/C, recirculação, front/rear defrost, fan e airflow;
- continua havendo **zero TX `0x3B`** em `candata_5..8`;
- a origem das transições `0x31` permanece não provada;
- `0x1A` é o grupo mais variável, mas não é registrado/decodificado pelo `HdPsaProtocol`; nessa implementação o ID de 360/parking é `0xE8`, logo `0x1A` permanece sem semântica promovida.

### Firmware CANBOX

- `RX 0xF0` em runtime reporta `H1H2PAF23A-240409`;
- o IAP fornecido `H1H2PAF23A-230802` pertence à mesma família PAF23A, porém é mais antigo e não prova a imagem exata instalada;
- os quatro IAPs fornecidos compartilham 13 bytes iniciais e depois divergem; não há base para afirmar criptografia ou compressão.

### Aprendizado promovido

- `L-007 — Protocolo CANBOX serial não é CAN bruto do veículo`;
- regra: **primeiro provar a camada/transporte; depois interpretar o ID**.

### F3 ainda não comprovou

- ação/touch original → TX `0x3B` → ACK → RX `0x31` → efeito físico;
- origem de cada transição HVAC já capturada;
- arbitration IDs e payloads da CAN veicular abaixo da CANBOX;
- imagem IAP exata `PAF23A-240409`;
- semântica de `0x1A`;
- causa raiz do crash loop de `sourceDir`.

## Próximo passo técnico da F3

Executar somente após autorização material de interação real uma sessão sincronizada e controlada:

`ação na UI original → timestamp → TX 0x3B → ACK → RX 0x31 → HvacInfo/estado → latência → efeito físico`

Priorizar uma ação por vez: power, A/C, fan, temperatura, AUTO, SYNC, recirculação, airflow e defrost.

Não construir nem transmitir frames manualmente por hipótese e não usar replay.

## Sistema de aprendizado

- `SKILLS_INDEX.md`, `docs/LEARNING_SYSTEM.md` e skills próprias estão integrados na `main`;
- `LEARNINGS.md` é resumo versionado; banco Aprendizados do Notion mantém histórico/status;
- novos aprendizados são registrados na linha de trabalho autorizada e consolidados na `main` quando aplicável;
- `L-007` está registrado como candidato a refinamento da skill `can-frame-differential-analysis`.

## Invariantes

- projeto novo e isolado;
- Notion + Guardrails + GitHub Connector no topo;
- `main` é o padrão e estado consolidado;
- branch só por risco demonstrável **e** autorização explícita do proprietário;
- autorização de branch não reduz autonomia técnica dentro do objetivo autorizado;
- concorrência atual é serializada por espera/fresh-read quando não há branch autorizada;
- autonomia por bloco sem microautorizações técnicas;
- evidência original preservada;
- **camada/transporte devem ser provados antes de interpretar IDs de protocolo**;
- código estático não prova efeito físico;
- UI/widget futuros compartilham uma única camada de controle;
- ROM/firmware somente se camadas superiores forem insuficientes;
- alvo real só é modificado dentro de bloco que inclua explicitamente essa fronteira.