# DECISIONS

Decisões vigentes de direção. Detalhes/histórico ficam no banco Decisões do Notion.

## D-001 — Projeto novo e isolado
Usar somente `felipetbestkkj-ship-it/PROTOCOLOCANBUS` como repositório técnico do novo projeto. Não herdar código/governança de projetos anteriores.

## D-002 — Tríade operacional e ordem de entrada
A ordem operacional é `Notion → Codex Engineering Guardrails → GitHub Connector → execução`. Notion define o norte e o bloco; Guardrails define o método; GitHub remoto confirma o estado técnico real.

## D-003 — Autonomia por bloco
Microautorizações para passos técnicos já cobertos pelo objetivo são evitadas.

## D-004 — Repositório público por decisão do proprietário
Não criar gates de confidencialidade para material do projeto. Credenciais ativas/tokens/chaves de acesso não são versionados.

## D-005 — Engenharia reversa profunda começa após a fundação
F1 inicia por triagem dirigida e cruza evidência estática, baseline e runtime; não desmontar tudo indiscriminadamente.

## D-006 — Operação remote-first
O GitHub remoto é a fotografia técnica oficial. Ambiente local é somente ferramenta auxiliar temporária e nunca substitui branch, commit/SHA, arquivos ou estado remoto. Um bloco não recebe `PASS` se a mudança relevante não estiver refletida no GitHub e o Notion não estiver sincronizado.

## D-007 — Política antiga de até 3 branches — SUBSTITUÍDA
A regra anterior que permitia `main + work/* + lab/*` como estrutura normal foi substituída pela D-011 e refinada de forma permanente pela D-012. Ela permanece registrada apenas como histórico.

## D-008 — GitHub Actions em linguagem humana
O nome visível de workflow e o artefato entregue ao proprietário devem dizer o resultado esperado. Evitar `CI`, `Build`, `APK Build`, `Release` e equivalentes como nomes principais. Quando houver build Android, usar nome como `📱 GERAR APK PARA INSTALAR` e artefato autoexplicativo como `INSTALAR-ESTE-APK_<versao-ou-fase>_<sha-curto>.apk`.

## D-009 — Skills são técnicas versionadas e não bloqueantes
O texto canônico das skills próprias vive no GitHub em `skills/<nome>/SKILL.md`, indexado por `SKILLS_INDEX.md`. O Notion mantém catálogo/status, sem duplicar a skill integral. Skills aceleram o método, mas não são gates de autorização: o agente seleciona autonomamente as relevantes e continua pelo Guardrails quando nenhuma se aplica.

## D-010 — Learning Distiller e promoção controlada
Blocos materiais destilam experiência operacional em fatos, aprendizados, candidatos a skill e hipóteses. Não preservar transcript como aprendizado. Um método só vira/refina skill quando não duplica outra, tem procedimento/saída/limites claros e cumpre o gate de repetição, prevenção de falha material ou procedimento especializado determinístico definido em `docs/LEARNING_SYSTEM.md`.

## D-011 — Main única durante a fase de descoberta
Enquanto o projeto estiver na fase de descoberta/investigação e não houver uma exceção de risco explicitamente autorizada, `main` é a única linha técnica ativa e o único destino oficial para conhecimento, evidência, documentação, decisões e aprendizados.

Se houver trabalho paralelo ou outra escrita em andamento, o trabalho posterior **aguarda ou para** e revalida a `main` antes de continuar; não cria branch automaticamente como solução para concorrência.

## D-012 — Branch somente por benefício de isolamento + autorização explícita
`main` é o padrão permanente. Uma branch só deve ser recomendada quando a engenharia conseguir demonstrar um risco concreto que o isolamento reduz melhor do que `main + commits + testes + fresh-read + serialização`, como preservar executável conhecido como bom, isolar mudança potencialmente quebrável, comparar implementações independentes, permitir paralelismo de código não serializável de forma razoável ou separar hotfix/release.

Documentação, evidência, aprendizado, início de fase, outro agente trabalhando, mudança pequena ou hábito de Git Flow não justificam branch por si só.

**Mesmo quando o gate de risco indicar benefício, criar ou usar qualquer branch diferente de `main` continua exigindo autorização clara e explícita do proprietário para aquele objetivo.** Após essa autorização, a autonomia normal do bloco permanece: commits, testes, correções, documentação e demais operações reversíveis dentro da linha autorizada não exigem microautorizações. Merge/release/publicação permanecem fronteiras separadas, salvo se a autorização original as incluir.

Sem autorização, somente `main`. Com autorização normal, o padrão é `main` + uma branch temporária; uma segunda branch simultânea exige justificativa própria e nova autorização. Política detalhada: `docs/BRANCH_POLICY.md`.

## D-013 — Conhecimento técnico em duas camadas: resumo + detalhe anti-retrabalho
Toda descoberta técnica material deve ser preservada em duas camadas complementares:

1. **Detalhe reproduzível/versionado na linha GitHub autorizada:** relatório, evidência, hashes, scripts e tabelas técnicas necessários para verificar a conclusão.
2. **Mapa humano no Notion:** resumo no topo e detalhe suficiente para consulta sem redescoberta. Para protocolos/binários, preservar framing, offsets, bits, IDs/subcomandos, exemplos, contagens, confiança, hipóteses descartadas e lacunas.

O `PROJECT_STATE.md` e o Estado Oficial do Notion permanecem resumidos: registram fatos promovidos, fase e próximo passo, sem virar dump técnico.

**Teste anti-retrabalho:** um agente novo deve conseguir identificar o que foi descoberto, onde está o byte/campo, qual fonte sustenta a conclusão, se foi observado ou apenas construído estaticamente e o que ainda falta provar sem repetir a engenharia reversa original.