# PROTOCOLOCANBUS — Política de Operação Remota

## Regra principal

O projeto trabalha com **estado remoto como fonte oficial**.

A sequência operacional obrigatória é:

1. **Notion** — entender missão, fase, bloco ativo, decisões e aprendizados.
2. **Codex Engineering Guardrails** — carregar o modo aplicável e definir o método de execução.
3. **GitHub Connector** — confirmar repositório, branch, commit, arquivos e estado técnico real.
4. Executar o bloco autorizado.

## Ambiente local

Ambiente local pode ser usado apenas como ferramenta auxiliar temporária.

Não é permitido usar estado local como:

- fonte de verdade;
- origem de decisões técnicas;
- substituto do GitHub remoto;
- referência de versão oficial.

## Sincronização obrigatória

Antes de qualquer conclusão:

- GitHub deve refletir o estado final;
- commit/SHA deve ser identificado;
- Notion deve registrar estado, evidência e próximo passo.

A meta é manter o projeto reproduzível e idêntico entre sessões, evitando divergência entre máquina local, chat e repositório.

## Regra de divergência

Se Notion, GitHub e memória do chat divergirem:

- GitHub/evidência resolvem fatos técnicos;
- Notion resolve intenção e histórico operacional;
- a divergência deve ser registrada e corrigida.

Nunca escolher silenciosamente uma fonte.
