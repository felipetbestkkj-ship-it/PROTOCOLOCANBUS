# PROTOCOLOCANBUS — Política de Branches por Risco

## Princípio permanente

**`main` é o padrão. Branch é uma ferramenta de isolamento de risco, não uma etapa obrigatória do processo.**

Não criar branch porque uma fase começou, porque outro agente está trabalhando, porque “é boa prática”, porque existe uma vaga `work/*`/`lab/*` ou simplesmente porque haverá muitas alterações.

Uma branch só deve ser proposta quando o isolamento comprar um benefício concreto que commits, fresh-read, testes e serialização na `main` não entreguem com simplicidade suficiente.

## Gate de benefício

A engenharia avalia autonomamente se há motivo técnico para **recomendar** uma branch. Há benefício real quando pelo menos um risco material está presente, por exemplo:

1. **Preservar um executável conhecido como bom:** existe APK/build/versão funcional que deve continuar intacta enquanto outra implementação potencialmente quebrável é desenvolvida.
2. **Mudança executável com risco de quebrar a linha principal:** código, build, empacotamento, assinatura, instalação ou migração podem deixar temporariamente o projeto sem build utilizável antes da validação.
3. **Comparação de implementações independentes:** duas soluções reais precisam coexistir temporariamente para teste, medição ou descarte sem misturar seus estados.
4. **Paralelismo de código que não pode ser serializado de forma razoável:** trabalhos independentes precisam avançar ao mesmo tempo e a espera/fresh-read causaria bloqueio material; as superfícies de escrita devem estar claramente separadas.
5. **Release/hotfix isolado:** uma correção ou preparação de versão precisa ser validada sem incorporar trabalho executável ainda não consolidado.

A presença de um critério não autoriza branch automaticamente. Ela apenas demonstra que existe razão técnica para pedir autorização.

## O que NÃO justifica branch por si só

- documentação, evidência, decisão, aprendizado ou skill;
- outro agente/chat estar trabalhando;
- mudança pequena e reversível;
- início de nova fase do roadmap;
- desejo de “organizar melhor” sem risco observável;
- costume de Git Flow;
- disponibilidade de um nome `work/*` ou `lab/*`;
- geração de APK por si só, se a `main` continuar segura e validável.

## Autorização obrigatória

**Criar ou usar qualquer branch diferente de `main` exige autorização clara e explícita do proprietário para aquele objetivo.**

Fluxo:

1. a engenharia identifica o risco concreto e conclui que branch traria isolamento útil;
2. informa em linguagem simples: risco, benefício, nome/finalidade proposta e quando a branch deve morrer;
3. pede **uma única autorização objetiva** para criar/usar a branch;
4. somente após a autorização, registra objetivo/motivo no Notion e cria a branch a partir de um HEAD fresco da `main`;
5. dentro do objetivo autorizado, a engenharia mantém a autonomia normal: pesquisar, editar, commitar, testar, corrigir, documentar e atualizar estado sem microautorizações;
6. merge/release/publicação continuam fronteiras materiais separadas, salvo quando a autorização original as incluir explicitamente;
7. encerrado o motivo de isolamento, conhecimento útil é consolidado e a branch é removida quando seguro.

## Topologia padrão

Sem autorização específica:

```text
main
```

Quando uma branch foi explicitamente autorizada:

```text
main
└── uma branch temporária autorizada
```

O padrão normal é **no máximo uma branch temporária além da `main`**. Uma segunda branch simultânea precisa de justificativa técnica própria e nova autorização explícita; não nasce por inferência da primeira.

Não existe `develop` permanente por padrão.

## Nomenclatura quando autorizada

- `work/<objetivo-curto>` — implementação que deve retornar à `main` após validação;
- `lab/<pergunta-curta>` — experimento realmente descartável/comparativo.

O nome é consequência do objetivo, não justificativa para criar a branch.

## Aplicação ao estágio atual

Na descoberta/investigação atual, evidência, documentação, scripts auxiliares, decisões, aprendizados e correlações passivas não apresentam por si só necessidade de isolamento executável. Portanto, **a aplicação atual deste gate continua sendo `main` única**.

Quando o projeto entrar em código Android executável, nova UI, controlador, build, APK, assinatura ou testes de regressão, o gate deve ser reavaliado. Branch pode passar a comprar segurança — mas continua dependendo de autorização explícita do proprietário.

## Regra anti-viés

A decisão não deve ser “gosto/não gosto de branches”. Deve responder:

`qual risco concreto existe → que isolamento a branch oferece → por que main + commits + testes + serialização não bastam → qual o custo da branch → benefício supera custo?`

Se essa cadeia não puder ser respondida com evidência e efeito prático, permanecer na `main`.
