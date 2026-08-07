# PROTOCOLOCANBUS — Política de Operação Remota

## Regra principal

O projeto trabalha com **estado remoto como fonte oficial**.

A sequência operacional obrigatória é:

1. **Notion** — entender missão, fase, bloco ativo/planejado, decisões e aprendizados.
2. **Codex Engineering Guardrails** — carregar o modo aplicável e definir o método de execução.
3. **GitHub Connector** — confirmar repositório, linha de trabalho autorizada, commit/SHA, arquivos, diffs, CI e estado técnico real.
4. Executar o bloco autorizado.
5. Confirmar o novo estado no GitHub remoto.
6. Sincronizar Notion com resultado, evidência e próximo passo.

## GitHub Connector obrigatório no preflight

Para fato técnico mutável, o chat deve consultar o GitHub remoto pelo conector. Não é válido substituir essa leitura por:

- memória do chat;
- arquivo copiado para a conversa;
- clone local antigo;
- pasta de trabalho local;
- suposição sobre branch ou commit.

Se o GitHub Connector não estiver disponível para confirmar o estado técnico do bloco, esse bloco não pode receber `PASS`.

## Ambiente local

Ambiente local pode ser usado apenas como ferramenta auxiliar temporária quando uma análise, build ou teste exigir execução fora do conector.

O estado local nunca é permitido como:

- fonte de verdade;
- origem de decisão sobre branch/commit oficial;
- substituto do GitHub remoto;
- referência de versão consolidada;
- prova final de que uma alteração existe no projeto.

Qualquer resultado local que importe ao projeto deve voltar ao fluxo remoto: ser registrado/versionado quando aplicável e associado a um commit/SHA ou evidência oficial antes do fechamento.

## Identidade entre sessões

Sem branch explicitamente autorizada, a fotografia técnica de um bloco é definida por:

`repositório + main + commit/SHA + arquivos versionados + evidência registrada`

Se existir branch explicitamente autorizada para um objetivo, ela é uma linha temporária de trabalho; a `main` continua sendo o estado consolidado até a integração.

Dois chats diferentes devem chegar à mesma fotografia ao ler o mesmo Notion e o mesmo SHA remoto aplicável.

## Sincronização obrigatória

Antes de qualquer `PASS`:

- GitHub deve refletir o estado final pretendido na linha autorizada do bloco;
- commit/SHA de saída deve ser identificado;
- Notion deve registrar o resultado do bloco e o próximo passo;
- divergências entre Notion e GitHub devem ser corrigidas ou explicitamente registradas.

Uma branch autorizada pode concluir seu objetivo técnico sem ser confundida com estado consolidado; integração/merge continua fronteira material própria quando não incluída na autorização.

## Política de branches por risco

A política detalhada fica em `docs/BRANCH_POLICY.md`, `AGENTS.md` e `WORKFLOWS.md`.

Regra curta: **`main` é o padrão. Branch só deve ser recomendada quando isolamento reduzir um risco técnico concreto melhor do que `main + commits + testes + fresh-read + serialização`.**

Mesmo quando houver benefício, criar ou usar qualquer branch diferente de `main` continua exigindo autorização clara e explícita do proprietário para aquele objetivo.

Após a autorização, a operação reversível dentro da branch — commits, testes, correções e documentação — segue com a mesma autonomia normal do bloco. A autorização da branch não autoriza automaticamente merge/release/publicação.

Na descoberta/investigação atual, o gate continua resultando em `main` única. Se houver concorrência de escrita, o trabalho posterior aguarda ou para, relê a `main` quando ela estiver livre e continua sobre o novo HEAD; não abrir branch automaticamente como mecanismo de paralelismo.

## Regra de divergência

Se Notion, GitHub e memória do chat divergirem:

- GitHub/evidência resolvem fatos técnicos;
- Notion resolve intenção, bloco e histórico operacional;
- memória do chat não desempata nada;
- a divergência deve ser registrada e corrigida.

Nunca escolher silenciosamente uma fonte.
