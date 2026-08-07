# PROJECT STATE

**Projeto:** PROTOCOLOCANBUS  
**Repositório:** `felipetbestkkj-ship-it/PROTOCOLOCANBUS`  
**Visibilidade:** pública por decisão explícita do proprietário  
**Fundação F0:** PASS — publicada e verificável  
**Governança F0.1:** PASS — operação remote-first definida  
**Governança F0.2:** PASS — sistema de aprendizado/skills integrado  
**Governança F0.4:** regra vigente — `main` única durante descoberta  
**Fase F1:** PASS — consolidada na `main`  
**Fase F2:** PASS — cadeia HVAC original mapeada  
**Fase atual:** F3 — pronta para correlação runtime controlada  
**Última atualização:** 2026-08-07

## Missão atual

Reconstruir de forma dirigida a cadeia Car Info/HVAC a partir das evidências locais, mantendo o projeto autossuficiente e sem herança técnica de repositórios anteriores.

## Ordem de entrada oficial

`Notion → Codex Engineering Guardrails → GitHub Connector → execução → GitHub atualizado → Notion sincronizado`

Estado local nunca substitui o GitHub remoto.

## Política de branch vigente — fase de descoberta

**`main` é a única linha técnica ativa e o único destino de conhecimento durante descoberta/investigação.**

- toda evidência, documentação, aprendizado, skill, script e estado útil deve ser consolidado na `main`;
- nenhuma branch nova pode ser criada ou usada sem autorização clara e explícita do proprietário;
- existência de ref histórica não autoriza trabalho nela;
- se houver outra escrita/bloco/agente em andamento, o trabalho posterior aguarda ou para;
- quando a escrita anterior terminar, fazer fresh-read da `main`, reconciliar e continuar nela;
- paralelismo não é motivo para dispersar conhecimento.

Refs históricas `work/*`/`lab/*` que ainda existam devem permanecer sem commits exclusivos e sem uso técnico até poderem ser removidas.

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
- temperatura/fan absolutos e posição do ar dependem do `HvacInfo` atual;
- `rxAirInfoCmdId = 0x31`; `HdPsaProtocol` decodifica `0x31` para power, A/C, MAX A/C, AUTO, SYNC, recirculação, desembaçadores, fan, direção e temperaturas;
- logs existentes contêm RX reais `5A A5 0C 31 ...` com checksum válido;
- retorno percorre `CanPopWind/ICanBus → HvacModel/ViewModel → HvacFragment.setHvacInfo`.

### Lacunas mantidas após F2

- TX `0x3B` ainda não observado diretamente nos `candata_5..8`;
- toque específico → TX → RX → estado ainda não correlacionado por timestamp;
- efeito físico de cada subcomando permanece para prova dinâmica;
- causa raiz do crash loop de `sourceDir` continua pendente;
- assinatura/instalação privilegiada continua fora deste estágio.

## Próximo bloco

**F3 — Correlação runtime.**

Objetivo:

`ação controlada → timestamp → logcat → TX 0x3B → RX 0x31 → HvacInfo/estado`

A F3 deve priorizar observação e correlação. Não construir nem transmitir frames manualmente por hipótese. Qualquer interação com o equipamento real precisa permanecer dentro da fronteira explicitamente autorizada.

## Sistema de aprendizado

- `SKILLS_INDEX.md`, `docs/LEARNING_SYSTEM.md` e skills próprias estão integrados na `main`;
- `LEARNINGS.md` é resumo versionado; banco Aprendizados do Notion mantém histórico/status;
- durante descoberta, novos aprendizados são registrados diretamente na `main`, nunca isolados em branch de aprendizado.

## Invariantes

- projeto novo e isolado;
- Notion + Guardrails + GitHub Connector no topo;
- `main` como única linha técnica ativa durante descoberta;
- branch somente com autorização explícita do proprietário;
- concorrência serializada por espera/fresh-read;
- autonomia por bloco sem microautorizações técnicas;
- evidência original preservada;
- código estático não prova efeito físico;
- UI/widget futuros compartilham uma única camada de controle;
- ROM/firmware somente se camadas superiores forem insuficientes;
- alvo real só é modificado dentro de bloco que inclua explicitamente essa fronteira.
