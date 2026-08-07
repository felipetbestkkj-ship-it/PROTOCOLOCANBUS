# PROJECT STATE

**Projeto:** PROTOCOLOCANBUS  
**Repositório:** `felipetbestkkj-ship-it/PROTOCOLOCANBUS`  
**Visibilidade:** pública por decisão explícita do proprietário  
**Fundação F0:** PASS — publicada e verificável  
**Governança F0.1:** PASS — operação remote-first, branches e workflows definidos  
**Fase F1:** PASS na branch `work/f1-hvac-mapeamento`  
**Fase atual:** F2 — pronta para iniciar após fechamento/sincronização operacional da F1  
**Última atualização:** 2026-08-06

## Missão atual

Reconstruir de forma dirigida a cadeia Car Info/HVAC a partir das evidências locais, mantendo o projeto autossuficiente e sem herança técnica de repositórios anteriores.

## Fundação concluída

A fundação estabeleceu no próprio repositório:

- `README.md` como porta de entrada técnica;
- `AGENTS.md` como contrato operacional;
- `PROJECT_STATE.md` como fotografia técnica mutável;
- `ROADMAP.md` como sequência de fases e gates;
- `EVIDENCE_INDEX.md` como inventário inicial com SHA-256;
- `DECISIONS.md` como decisões vigentes;
- `LEARNINGS.md` como aprendizado fechado;
- `REMOTE_OPERATION_POLICY.md` como contrato remote-first;
- `WORKFLOWS.md` como política didática de branches, Actions e artefatos;
- `scripts/check_governance.py` como verificador mínimo;
- `.github/workflows/governance.yml` como checagem automática com nome humano e controle de branches.

O Notion permanece como primeiro norte operacional. Codex Engineering Guardrails é carregado depois do contexto do Notion e antes da primeira ação técnica. O GitHub Connector confirma a fotografia técnica remota antes da execução.

## Ordem de entrada oficial

`Notion → Codex Engineering Guardrails → GitHub Connector → execução → GitHub atualizado → Notion sincronizado`

Estado local nunca substitui o GitHub remoto.

## Política de branches vigente

Máximo normal de **3 branches remotas ativas**:

1. `main` — estado oficial consolidado;
2. uma única `work/*` — trabalho técnico atual;
3. uma única `lab/*` — investigação temporária somente quando necessária.

Nomes:

- `work/f<fase>-<objetivo-curto>`;
- `lab/f<fase>-<pergunta-curta>`.

Não existe `develop` por padrão e não se cria branch por correção pequena.

## F1 — resultado consolidado

Relatório técnico:

`docs/F1_CARINFO_HVAC_TRIAGEM.md`

### Comprovado na F1

- `Car Info / com.can.activity` permanece o alvo central do HVAC.
- `INSTALAR-v3854-CarInfo-HVAC-Visual-V1.apk` é byte a byte o APK registrado como instalado na baseline, por SHA-256 `d0741a541fc575d3b25bc853a171532b815e8c396451dcc9ebe0f678d1905a50`.
- A baseline registra `versionCode=3854`, shared user `android.uid.system/1000` e contexto privilegiado/persistente.
- No manifesto decodificado, original → v3854 altera `versionCode` 3853 → 3854; package, shared UID e componentes inspecionados permanecem iguais.
- As classes centrais inspecionadas `HvacActivity`, `HvacFragment` e `HvacModel` apresentam código decompilado idêntico entre original e v3854.
- A mudança significativa observada na superfície HVAC da v3854 está concentrada em layouts, cores e novos drawables.
- A cadeia estática alcança `HvacFragment → HvacViewModel/HvacModel → CanBusManager → CanPopWind → ICanUI/ICanBus`.
- Runtime confirma componentes Car Info/Jancar, enquadramento `5A A5` e identificador Hiworld `H1H2PAF23A-240409`.
- A captura runtime posterior contém crash/restart loop de `com.can.activity` tentando carregar um caminho antigo de `base.apk` inexistente.

### Lacunas mantidas explicitamente

- significado HVAC específico de mensagens como `0x31` ainda não está provado;
- ação física de cada botão ainda não está mapeada até frame/retorno;
- mecanismo que habilita/abre `HvacActivity` para esta configuração ainda precisa ser provado;
- causa raiz do crash loop após mudança de caminho do APK não está provada;
- estratégia futura de assinatura/instalação privilegiada não foi decidida nem provada.

## Próximo bloco

**F2 — Cadeia HVAC original.**

Objetivo: mapear cada função relevante como:

`ação de UI → propriedade/método → controlador/serviço → mensagem → retorno → estado`

Começar pelas propriedades já usadas pelo `HvacFragment` e seguir somente as dependências necessárias até o backend, sem transmissão CAN por hipótese e sem modificar o equipamento real.

### Gate de saída de F2

Entregar matriz por função com evidência e lacunas explícitas para temperatura, fan, power/A/C/AUTO/modos e demais controles encontrados, sem declarar efeito físico apenas por nome de classe, recurso ou propriedade.

## Workflows em linguagem simples

O GitHub Actions deve mostrar resultados compreensíveis ao proprietário.

Workflow atual:

- `✅ VERIFICAR SE O PROJETO ESTÁ ORGANIZADO`.

Nomes reservados quando essas capacidades realmente existirem:

- `📱 GERAR APK PARA INSTALAR`;
- `🧪 TESTAR APK SEM MEXER NO CARRO`;
- `🚀 PREPARAR VERSÃO FINAL`.

Quando houver APK instalável, o artefato principal deve ser autoexplicativo, preferencialmente `INSTALAR-ESTE-APK_<versao-ou-fase>_<sha-curto>.apk`.

## Invariantes

- projeto novo e isolado;
- Notion + Guardrails + GitHub Connector no topo, nessa ordem operacional;
- estado oficial remoto;
- autonomia por bloco;
- sem microautorizações;
- poucas branches remotas;
- workflows/artefatos autoexplicativos;
- evidência original preservada;
- nenhuma capacidade de controle é declarada por nome/string apenas;
- UI/widget futuros compartilham uma única camada de controle;
- ROM/firmware somente se camadas superiores forem insuficientes;
- alvo real só é modificado dentro de bloco que inclua explicitamente essa fronteira.

## Não fazer sem evidência ou fronteira autorizada

- não importar código/governança de outro repo;
- não escolher arquitetura final de UI antes do mapa F1–F4;
- não transmitir CAN por hipótese;
- não mexer em ROM/firmware;
- não declarar assinatura/instalação compatível sem prova;
- não instalar ou modificar o equipamento real fora de bloco que inclua explicitamente essa fronteira.
