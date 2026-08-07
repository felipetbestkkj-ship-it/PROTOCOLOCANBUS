# PROTOCOLOCANBUS — contrato operacional

## 1. Escopo

Este repositório nasceu do zero. Não copiar código, governança, decisões, arquitetura ou dependências de repositórios/projetos anteriores. Repositórios semelhantes não são fonte técnica deste projeto.

Materiais anexados pelo proprietário são evidências locais e podem ser analisados. Ferramentas genéricas podem ser usadas, mas só resultados verificados contra evidência local viram conhecimento do projeto.

## 2. Tríade obrigatória

Toda operação técnica usa, obrigatoriamente:

1. **Notion** como norte operacional para missão, fase, bloco ativo, decisões, aprendizados e handoff;
2. **Codex Engineering Guardrails** no modo aplicável para método, escopo, risco, evidência e fechamento;
3. **GitHub Connector** como fonte técnica remota para confirmar repositório, branches existentes, `main`, commits, arquivos, diffs, CI e estado real.

Use `code-verification` para análise, diagnóstico, revisão e teste sem mudança de produção. Use `code-work` para criação ou alteração de código, scripts, testes, documentação operacional ou governança.

Memória do chat e estado local não substituem fonte oficial.

## 3. Preflight obrigatório — gate de entrada

**Nenhum bloco técnico pode começar sem este preflight.** Antes da primeira ação técnica do bloco, o agente deve:

1. ler no Notion a Central Oficial, o Estado Oficial e o bloco ativo/planejado;
2. carregar **Codex Engineering Guardrails** no modo aplicável;
3. confirmar pelo **GitHub Connector** o repositório `felipetbestkkj-ship-it/PROTOCOLOCANBUS`, as branches remotas existentes, a `main` e o commit real;
4. ler `AGENTS.md`, `PROJECT_STATE.md`, `REMOTE_OPERATION_POLICY.md`, `WORKFLOWS.md` e o trecho aplicável de `ROADMAP.md`;
5. consultar decisões/aprendizados relacionados quando existirem;
6. registrar no bloco ativo do Notion o modo Guardrails usado (`code-verification` ou `code-work`), `main`/commit de entrada e marcar `Preflight` somente depois dessas leituras;
7. definir objetivo observável, escopo e evidência necessária para encerrar;
8. só então executar.

A primeira atualização de progresso de um bloco técnico deve deixar visível, de forma curta: **modo Guardrails + main/commit + objetivo do bloco**. Isso é comprovante operacional, não pedido de permissão.

Se Guardrails, Notion ou GitHub Connector não puderem ser usados para cumprir o preflight, o bloco técnico **não pode ser declarado iniciado nem concluído como PASS**. Registrar `BLOCKED` ou `INCONCLUSIVE` conforme o caso, sem substituir essas fontes por memória ou cópia local.

## 4. Operação remote-first

O estado técnico oficial vive no GitHub remoto.

- usar o GitHub Connector para leitura e escrita remota sempre que tecnicamente disponível;
- confirmar SHA remoto antes de alterar e SHA remoto depois de alterar;
- uma cópia local pode ser usada somente como ferramenta auxiliar temporária de análise/build/teste quando necessária;
- nenhum resultado local é considerado oficial enquanto não estiver refletido na `main` remota e identificado por commit/SHA;
- não tomar decisão de estado com base em clone local, pasta local ou memória do chat;
- ao fechar o bloco, GitHub e Notion devem estar sincronizados sobre fase, resultado e próximo passo.

A meta é que dois chats distintos, lendo Notion e o mesmo SHA remoto da `main`, reconstruam a mesma fotografia do projeto.

## 5. Autonomia por bloco

**Autorize objetivos; a engenharia decide os passos.**

Quando um objetivo está autorizado, o agente executa sem microautorizações as operações previsíveis, necessárias e reversíveis do mesmo bloco, incluindo:

- leitura, busca, inventário e comparação;
- decompilação e inspeção de artefatos em escopo;
- scripts e ferramentas auxiliares;
- testes focados, negativos, integração e regressão proporcional;
- correções indispensáveis ao mesmo objetivo;
- revisão do estado integrado;
- documentação, estado, evidência e aprendizado;
- seleção/aplicação de skills úteis ao objetivo;
- refinamento de aprendizado/skill quando coberto pelo sistema de promoção;
- commit/push diretamente na `main` durante a fase de descoberta, após fresh-read do HEAD remoto.

Teste é responsabilidade da engenharia. Não perguntar ao proprietário se deve testar, qual ferramenta técnica previsível deve usar ou qual skill aplicável deve carregar.

Atualização de progresso informa; não pede permissão.

## 6. Fronteiras materiais

Uma nova autorização objetiva só é necessária quando a ação não estiver incluída no bloco e mudar materialmente:

- objetivo ou alvo;
- **criação ou uso de qualquer branch diferente de `main`**;
- estratégia de integração, merge/release/publicação quando não previstos no bloco;
- instalação/modificação no equipamento real;
- transmissão CAN ativa, replay ou atuação física;
- root, partição, ROM, MCU/IAP ou firmware;
- ação destrutiva ou irreversível;
- compatibilidade pública, dados, segurança, legalidade ou custo relevante.

Perguntas técnicas resolvíveis por inspeção, teste seguro ou escolha reversível devem ser resolvidas pela engenharia.

## 7. Repositório público

A visibilidade pública é intencional neste ciclo. Não criar bloqueios de confidencialidade para logs, scripts, documentação, evidências ou artefatos do projeto.

Única exceção operacional: não versionar credenciais ativas, tokens ou chaves privadas que concedam acesso a contas/sistemas.

## 8. Evidência

- preservar evidência original;
- registrar SHA-256 de artefatos materiais;
- separar observação de inferência;
- nome de classe/string/recurso não prova comportamento;
- código estático não prova efeito em runtime;
- UI, interpretação, transmissão e atuação são capacidades distintas;
- afirmação importante deve apontar para evidência reproduzível.

Resultados de bloco usam: `PASS`, `PARTIAL`, `FAIL`, `INCONCLUSIVE`.

## 9. Engenharia reversa dirigida

Não desmontar tudo por disponibilidade. Abrir somente artefatos necessários para responder à pergunta do bloco.

Ordem padrão do primeiro ciclo:

`evidência -> mapa do sistema -> cadeia HVAC -> runtime -> contrato -> escolha arquitetural -> controlador único -> nova UI -> autoridade visual única -> widget -> assinatura/build -> laboratório -> validação integrada -> alvo real autorizado -> generalização`

ROM/firmware são último recurso, não ponto de partida.

## 10. Branches — main única durante descoberta

### Regra obrigatória atual

**Enquanto o projeto estiver em fase de descoberta/investigação, `main` é a única linha técnica ativa e o único destino oficial de conhecimento.**

Tudo que for comprovado ou útil ao projeto — evidência, documentação, decisões, aprendizados, skills, scripts, correções e estado — deve ser consolidado diretamente na `main`.

### Criação ou uso de branch

Nenhuma `work/*`, `lab/*`, `develop` ou outra branch pode ser criada **ou usada para novo trabalho** sem autorização clara e explícita do proprietário para aquele objetivo.

A existência de uma ref antiga não concede autorização para usá-la.

### Trabalho paralelo

Se outra escrita/bloco/agente estiver atuando no repositório:

1. não abrir branch para trabalhar em paralelo;
2. aguardar ou parar a escrita posterior;
3. quando a escrita anterior terminar, consultar novamente a `main` e o HEAD remoto;
4. reconciliar as mudanças;
5. continuar na `main`.

**Concorrência é resolvida por serialização e fresh-read, não por dispersão em branches.**

### Exceção futura

Uma branch só pode nascer após autorização explícita do proprietário. Essa autorização deve registrar objetivo e motivo no Notion. Encerrado o objetivo autorizado, todo conhecimento útil volta à `main` e a branch deve ser removida.

### Refs históricas

Refs antigas que ainda existam devem permanecer sem commits exclusivos e sem uso técnico. Removê-las quando a ferramenta disponível permitir. Até lá, a `main` continua sendo a única fonte e linha ativa.

## 11. Workflows e artefatos em linguagem humana

Os nomes visíveis no GitHub Actions devem dizer **o que o proprietário deve esperar**, não expor jargão interno.

Exemplos oficiais:

- `✅ VERIFICAR SE O PROJETO ESTÁ ORGANIZADO`;
- `📱 GERAR APK PARA INSTALAR`;
- `🧪 TESTAR APK SEM MEXER NO CARRO`;
- `🚀 PREPARAR VERSÃO FINAL`.

Evitar como nome principal: `CI`, `Build`, `APK Build`, `Release`, `Pipeline`.

Quando existir geração de APK, o artefato principal entregue ao proprietário deve seguir formato autoexplicativo, preferencialmente:

`INSTALAR-ESTE-APK_<versao-ou-fase>_<sha-curto>.apk`

Detalhes e convenções ficam em `WORKFLOWS.md`.

## 12. Aprendizado fechado

Erro ou descoberta reutilizável segue:

`observação -> causa -> correção -> prevenção/teste/regra -> registro`

Sem causa provada, registrar como pendente. Não transformar hipótese em regra permanente.

## 13. Skills e aprendizado reutilizável

O conteúdo técnico canônico das skills vive no GitHub. Consultar `SKILLS_INDEX.md` depois do preflight e antes de execução especializada.

### Seleção

- selecionar autonomamente apenas as skills relevantes ao objetivo; normalmente 1–3;
- não carregar todas por padrão;
- não pedir autorização para usar skill quando a ação já está dentro do bloco;
- ausência/inaplicabilidade de skill **não bloqueia**: Guardrails + este contrato continuam suficientes;
- skill nunca amplia autoridade nem reduz fronteira material.

### Learning Distiller

No fechamento de bloco material, usar `skills/reusable-engineering-learning/SKILL.md` para destilar:

`execução -> resultado técnico + experiência operacional -> fato / aprendizado / candidato a skill / hipótese`

Não armazenar transcript de execução como aprendizado. Muitas ações podem gerar poucos aprendizados e talvez nenhuma nova skill.

### Promoção

Método pode virar/refinar skill autonomamente quando não duplicar outra skill, tiver procedimento/saída/limites claros e cumprir o gate de `docs/LEARNING_SYSTEM.md`.

Fato específico, estado mutável, hipótese ou conselho genérico não viram skill.

Notion mantém catálogo/status/promoção; GitHub mantém o texto canônico. Não duplicar a skill integral na instrução personalizada ou Notion.

## 14. Comunicação

O proprietário é leigo em programação.

- explicar efeito prático antes do jargão;
- definir termos técnicos quando necessários;
- evitar decisões técnicas devolvidas ao proprietário;
- manter atualizações curtas e com evidência nova;
- não repetir pedido já respondido.

## 15. Fechamento obrigatório

Todo bloco técnico termina com:

- modo Guardrails efetivamente carregado;
- Notion consultado e sincronizado?;
- objetivo;
- repo/main/commit de entrada e saída;
- resultado;
- comprovado;
- não comprovado;
- arquivos/artefatos;
- evidência/testes;
- aprendizado destilado (quando houver) e eventual skill refinada/promovida;
- sistemas externos/alvo real alterados?;
- próximo passo único.

Um bloco não pode receber `PASS` se não houver registro do modo Guardrails usado, preflight no Notion e fotografia remota de `main`/commit.