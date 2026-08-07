# PROJECT STATE

**Projeto:** PROTOCOLOCANBUS  
**Repositório:** `felipetbestkkj-ship-it/PROTOCOLOCANBUS`  
**Visibilidade:** pública por decisão explícita do proprietário  
**Linha consolidada:** `main`; qualquer outra branch exige autorização explícita  
**F0:** PASS  
**F1:** PASS — triagem Car Info/HVAC  
**F2:** PASS — cadeia HVAC original  
**F3:** ATIVA / PARTIAL — investigação offline e prontidão para implementação concluídas; resta um único gate físico  
**Última atualização:** 2026-08-07

## Em linguagem simples

```text
Car Info deixou de ser uma caixa-preta
        ↓
controle HVAC foi mapeado
        ↓
protocolo e retorno foram reconstruídos
        ↓
gêmeo digital testa sem carro
        ↓
18 operações agora têm contrato executável
        ↓
arquitetura futura já tem candidato líder
        ↓
resta 1 confirmação física antes de congelar F4/F5
```

## Estado operacional

- ordem obrigatória: `Notion → Codex Engineering Guardrails → GitHub Connector → execução → GitHub atualizado → Notion sincronizado`;
- `main` é o estado consolidado;
- alvo real, transmissão CAN, replay, instalação, ROM/firmware/root exigem fronteira própria;
- D-013: descoberta material vive em detalhe versionado no GitHub + mapa humano no Notion;
- detalhes de governança: `AGENTS.md`, `REMOTE_OPERATION_POLICY.md`, `WORKFLOWS.md`, `docs/BRANCH_POLICY.md`.

## F1 — o que já sabemos do Car Info

Relatório: `docs/F1_CARINFO_HVAC_TRIAGEM.md`.

- alvo: `Car Info / com.can.activity`;
- v3854 fornecida é byte a byte o APK registrado na baseline como instalado;
- contexto observado: `versionCode=3854`, shared UID `android.uid.system/1000`, app persistente/sistema;
- mudanças HVAC relevantes entre original e v3854 concentram-se em recursos visuais; o núcleo `HvacActivity/HvacFragment/HvacModel` inspecionado permaneceu igual;
- crash loop relacionado a `sourceDir/base.apk` antigo continua L-004, causa ainda pendente.

## F2 — caminho original de controle

Relatório: `docs/F2_HVAC_ORIGINAL_CHAIN.md`.

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

- configuração sustentada: `Hiworld-Peugeot-208-2023~Present（Brazil）-All`;
- TX HVAC construído como `5A A5 02 3B <subcomando> <valor> <checksum>`;
- RX `0x31` é estado HVAC e retorna por `HvacInfo` à UI;
- fan/temperatura/airflow possuem regras dependentes do estado atual, portanto a futura UI não deve conhecer bytes nem assumir sucesso local.

## F3 — runtime, protocolo e gêmeo digital

Relatórios principais:

- `docs/F3_CAN_RUNTIME_EVIDENCE_DEEP_DIVE.md`;
- `docs/F3_PASSIVE_CONTINUATION_TX_COVERAGE.md`;
- `docs/F3_HVAC_DIGITAL_TWIN.md`;
- `docs/F3_IMPLEMENTATION_READINESS.md`;
- `docs/F3_ONE_SHOT_VALIDATION.md`.

Ferramentas:

- `scripts/analyze_hiword_candata.py`;
- `scripts/hiworld_hvac_digital_twin.py`;
- `scripts/validate_hvac_behavior_contract.py`.

### Protocolo confirmado

- `candata_*` é serial Hiworld/Jancar Android ↔ CANBOX, não CAN bruto do Peugeot;
- caminho observado: `Car Info/Jancar → /dev/ttyS5 @ 38400 → CANBOX Hiworld → CAN veicular`;
- framing: `5A A5 <LEN> <CMD> <DATA...> <CHECKSUM>`;
- `candata_8`: 821 frames reconstruídos, 821/821 checksums válidos;
- TX observado completo: `0xFF` ACK, `0xCB` hora/data, `0x6A` polling, `0xA1/0xA4` mídia; `0x3B=0` naquela captura;
- 8 estados lógicos `0x31`; 1 solicitado e 7 não solicitados pelo polling conhecido;
- logger cobre o caminho TX normal da UI; keycode-mode também foi eliminado para a configuração Peugeot ativa.

### Gêmeo digital

O laboratório offline reproduz:

- framing/checksum;
- builder `0x3B`;
- parser/encoder `0x31`;
- oito estados reais;
- state machine empírica;
- fake CANBOX `0x3B → 0x31` sem I/O de dispositivo.

Regressão anterior consolidada: self-test PASS, 11/11 testes do gêmeo PASS e replay exato dos estados reais.

## F3.1 — prontidão para implementação

Este marco transforma conhecimento em contrato executável.

### Contrato HVAC

- `contracts/hvac_behavior_contract.json` — **18 operações** catalogadas;
- **14** possuem vetores estáticos completos de frame;
- **2** possuem transição runtime de campo único (`rear_defrost`, `recirculation`);
- **5** aparecem em transições runtime compostas;
- **11** ainda não possuem transição de controle isolada observada;
- todas continuam `PHYSICAL_PENDING` no mesmo elo físico comum; isso **não significa 18 testes no carro**.

Contrato humano preparatório: `docs/F4_BEHAVIOR_CONTRACT_DRAFT.md` — permanece `DRAFT_PRE_F4`, não promove F4 antecipadamente.

### Superfície Binder do Car Info

Contrato: `contracts/carinfo_hvac_binder_contract.json`.

Evidência atual:

- serviço: `com.can.activity/com.can.ui.CanPopWind`;
- resolvido no runtime pelas actions CANBUS conhecidas;
- `ICanUI.getCanService("CanBusManager")` entrega `ICanBus` no fluxo original;
- operações relevantes congeladas: `registerListener`, `setHvacProperty`, `getHvacInfo`, `getPropertyList`;
- callback `ICanBusListener.onHvacInfoChanged(HvacInfo)` mapeado;
- `CarPropertyValue` e `HvacInfo` são Parcelables reproduzíveis;
- no serviço inspecionado não foi localizado gate explícito por calling UID/permissão antes desse acesso.

**Ainda não provado:** um APK externo separado consegue bindar e trocar esses Parcelables na unidade real. Esse será probe futuro; escrita só entra com autorização de alvo real.

### Arquitetura F5 — recomendação preliminar

Documento: `docs/F5_ARCHITECTURE_READINESS_DRAFT.md`.

Ranking atual, ainda não promovido a decisão F5:

1. **Frontend/app próprio → Binder do Car Info → Hiworld/CANBOX** — candidato líder;
2. modificar a UI dentro do próprio Car Info — fallback próximo;
3. falar direto em `/dev/ttyS5` — fallback profundo, evita dependência mas duplica transporte/ACK/polling/timing e aumenta risco de privilégio.

A opção Binder lidera porque permite trocar a experiência visual mantendo o Car Info temporariamente como backend automotivo invisível.

## Laboratório automático no GitHub

Workflow ativo: `.github/workflows/offline-hvac-lab.yml`

Nome visível: **`🧪 TESTAR HVAC SEM MEXER NO CARRO`**.

Ele executa parser self-test, gêmeo digital self-test, validação do contrato e suíte `unittest`. A presença do workflow não significa F11 concluída; ele é uma automação antecipada do laboratório já reproduzível.

O conector não retornou status/check de Actions para o SHA consultado, portanto ausência de status não é tratada como PASS de CI.

## Único gate físico que resta na F3

Documento: `docs/F3_ONE_SHOT_VALIDATION.md`.

Quando houver autorização material:

> com rear defrost OFF, tocar rear defrost ON **uma única vez** na UI original com RX/TX capturados.

Previsão congelada:

- TX: `5A A5 02 3B 06 01 43`;
- ACK normal;
- RX `0x31`: `rear_defrost` / payload[2] bit5 `0 → 1`;
- efeito físico coerente.

Se passar, fechar o elo comum e seguir F4/F5 sem bateria função-por-função. Se divergir, preservar somente essa captura e voltar offline.

## Lacunas secundárias — não bloqueiam o próximo gate

- origem material dos 7 pushes `RX_NAO_SOLICITADO` antigos;
- arbitration IDs/payloads abaixo da CANBOX;
- IAP exato `PAF23A-240409`;
- `0x1A data[9:10]` permanece hipótese forte de RPM;
- causa raiz do crash `sourceDir`.

Essas lacunas não justificam atrasar indefinidamente o primeiro ciclo HVAC se deixarem de ser dependência real da arquitetura escolhida.

## Próximo passo único

**Fechar F3 com o gate físico único de rear-defrost quando o proprietário autorizar essa interação real.** Até essa fronteira, não executar tentativa e erro nem transmissão manual/replay.
