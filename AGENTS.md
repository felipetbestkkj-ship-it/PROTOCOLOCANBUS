# PROTOCOLOCANBUS — contrato operacional

## 1. Escopo

Este repositório nasceu do zero. Não copiar código, governança, decisões, arquitetura ou dependências de repositórios/projetos anteriores. Repositórios semelhantes não são fonte técnica deste projeto.

Materiais anexados pelo proprietário são evidências locais e podem ser analisados. Ferramentas genéricas podem ser usadas, mas só resultados verificados contra evidência local viram conhecimento do projeto.

## 2. Tríade obrigatória

Toda operação técnica usa:

1. **Codex Engineering Guardrails** no modo aplicável;
2. **GitHub** para confirmar repositório, branch, commit, arquivos, diffs, CI e estado técnico;
3. **Notion** para missão, fase, bloco ativo, decisões, aprendizados e handoff.

Use `code-verification` para análise, diagnóstico, revisão e teste sem mudança de produção. Use `code-work` para criação ou alteração de código, scripts, testes, documentação operacional ou governança.

Memória do chat não substitui fonte.

## 3. Ordem de entrada

Antes de uma tarefa não trivial:

1. confirmar `felipetbestkkj-ship-it/PROTOCOLOCANBUS`;
2. confirmar branch e commit afetados;
3. ler este arquivo;
4. ler `PROJECT_STATE.md` e o trecho aplicável de `ROADMAP.md`;
5. ler decisões/aprendizados relacionados;
6. consultar a Central Oficial e o bloco ativo no Notion;
7. carregar o Guardrails aplicável;
8. definir objetivo observável e evidência de saída;
9. executar.

## 4. Autonomia por bloco

**Autorize objetivos; a engenharia decide os passos.**

Quando um objetivo está autorizado, o agente executa sem microautorizações as operações previsíveis, necessárias e reversíveis do mesmo bloco, incluindo:

- leitura, busca, inventário e comparação;
- decompilação e inspeção de artefatos em escopo;
- scripts e ferramentas auxiliares;
- testes focados, negativos, integração e regressão proporcional;
- correções indispensáveis ao mesmo objetivo;
- revisão do estado integrado;
- documentação, estado, evidência e aprendizado;
- commit/push na branch de trabalho do bloco quando tecnicamente disponível.

Teste é responsabilidade da engenharia. Não perguntar ao proprietário se deve testar.

Atualização de progresso informa; não pede permissão.

## 5. Fronteiras materiais

Uma nova autorização objetiva só é necessária quando a ação não estiver incluída no bloco e mudar materialmente:

- objetivo ou alvo;
- branch protegida ou estratégia de integração;
- merge/release/publicação quando não previstos no bloco;
- instalação/modificação no equipamento real;
- transmissão CAN ativa, replay ou atuação física;
- root, partição, ROM, MCU/IAP ou firmware;
- ação destrutiva ou irreversível;
- compatibilidade pública, dados, segurança, legalidade ou custo relevante.

Perguntas técnicas resolvíveis por inspeção, teste seguro ou escolha reversível devem ser resolvidas pela engenharia.

## 6. Repositório público

A visibilidade pública é intencional neste ciclo. Não criar bloqueios de confidencialidade para logs, scripts, documentação, evidências ou artefatos do projeto.

Única exceção operacional: não versionar credenciais ativas, tokens ou chaves privadas que concedam acesso a contas/sistemas.

## 7. Evidência

- preservar evidência original;
- registrar SHA-256 de artefatos materiais;
- separar observação de inferência;
- nome de classe/string/recurso não prova comportamento;
- código estático não prova efeito em runtime;
- UI, interpretação, transmissão e atuação são capacidades distintas;
- afirmação importante deve apontar para evidência reproduzível.

Resultados de bloco usam: `PASS`, `PARTIAL`, `FAIL`, `INCONCLUSIVE`.

## 8. Engenharia reversa dirigida

Não desmontar tudo por disponibilidade. Abrir somente artefatos necessários para responder à pergunta do bloco.

Ordem padrão do primeiro ciclo:

`evidência -> mapa do sistema -> cadeia HVAC -> runtime -> contrato -> escolha arquitetural -> controlador único -> nova UI -> autoridade visual única -> widget -> assinatura/build -> laboratório -> validação integrada -> alvo real autorizado -> generalização`

ROM/firmware são último recurso, não ponto de partida.

## 9. Branches e integração

Evitar proliferação de branches.

- `main` representa estado oficial consolidado.
- F0 pode ser consolidada diretamente em `main` quando a fundação for o próprio objetivo autorizado.
- Mudança técnica relevante usa uma branch de trabalho por bloco/fase, não uma branch por descoberta.
- commit/push na branch de trabalho faz parte do bloco.
- merge em `main` pode fazer parte do mesmo bloco quando estiver explicitamente previsto; caso contrário é uma única fronteira macro, nunca uma sequência de microautorizações.

## 10. Aprendizado fechado

Erro ou descoberta reutilizável segue:

`observação -> causa -> correção -> prevenção/teste/regra -> registro`

Sem causa provada, registrar como pendente. Não transformar hipótese em regra permanente.

## 11. Comunicação

O proprietário é leigo em programação.

- explicar efeito prático antes do jargão;
- definir termos técnicos quando necessários;
- evitar decisões técnicas devolvidas ao proprietário;
- manter atualizações curtas e com evidência nova;
- não repetir pedido já respondido.

## 12. Fechamento obrigatório

Todo bloco técnico termina com:

- modo Guardrails;
- objetivo;
- repo/branch/commit;
- resultado;
- comprovado;
- não comprovado;
- arquivos/artefatos;
- evidência/testes;
- sistemas externos/alvo real alterados?;
- aprendizado;
- próximo passo único.
