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

## D-007 — Poucas branches remotas
Máximo normal de 3 branches remotas ativas: `main`, uma `work/*` e, quando necessário, uma `lab/*`. Não existe `develop` por padrão. Não criar branch por microcorreção ou tentativa. Nomes: `work/f<fase>-<objetivo-curto>` e `lab/f<fase>-<pergunta-curta>`.

## D-008 — GitHub Actions em linguagem humana
O nome visível de workflow e o artefato entregue ao proprietário devem dizer o resultado esperado. Evitar `CI`, `Build`, `APK Build`, `Release` e equivalentes como nomes principais. Quando houver build Android, usar nome como `📱 GERAR APK PARA INSTALAR` e artefato autoexplicativo como `INSTALAR-ESTE-APK_<versao-ou-fase>_<sha-curto>.apk`.
