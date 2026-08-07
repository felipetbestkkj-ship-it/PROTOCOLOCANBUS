# PROTOCOLOCANBUS — Workflows e branches em linguagem simples

Este arquivo existe para que qualquer pessoa consiga olhar o GitHub e entender **o que cada botão/rotina faz** sem precisar conhecer termos de DevOps.

## 1. Regra de nomes visíveis no GitHub Actions

O nome exibido no GitHub Actions deve dizer **qual resultado o proprietário obterá**.

Evitar nomes isolados como:

- `CI`;
- `Build`;
- `APK Build`;
- `Release`;
- `Pipeline`.

Preferir nomes como:

- `✅ VERIFICAR SE O PROJETO ESTÁ ORGANIZADO` — confere governança e regras básicas;
- `📱 GERAR APK PARA INSTALAR` — quando existir build Android, gera um APK pronto para o proprietário baixar e instalar;
- `🧪 TESTAR APK SEM MEXER NO CARRO` — quando houver laboratório/simulador, executa validações sem atuar no equipamento real;
- `🚀 PREPARAR VERSÃO FINAL` — somente quando existir uma etapa real de consolidação/release.

Não criar workflow só para ocupar espaço. Um workflow novo só entra quando existir uma ação real e repetível que o projeto já saiba executar.

## 2. Nome do APK/artefato

Quando a geração de APK existir, o arquivo entregue ao proprietário deve ser autoexplicativo.

Formato preferido:

`INSTALAR-ESTE-APK_<versao-ou-fase>_<sha-curto>.apk`

O resumo do workflow deve informar sempre:

- qual linha/branch autorizada gerou o arquivo;
- qual commit/SHA gerou o arquivo;
- qual finalidade do APK;
- se é laboratório, teste ou versão consolidada;
- o próximo passo humano em linguagem simples.

Sem branch explicitamente autorizada, a origem é a `main`.

Nunca entregar um arquivo chamado apenas `app-debug.apk` ou `build.apk` como artefato principal para o proprietário.

## 3. Política de branches — efeito prático

A regra completa está em `docs/BRANCH_POLICY.md`.

### Regra principal

**`main` é o padrão. Branch só faz sentido quando isola um risco real.**

Antes de sugerir uma branch, a engenharia deve conseguir responder:

`qual risco existe → como a branch isola esse risco → por que main + commits + testes + fresh-read não bastam → benefício supera o custo?`

Exemplos em que branch pode comprar segurança:

- manter um APK/build funcional intacto enquanto outro é alterado;
- desenvolver mudança executável que pode quebrar build/empacotamento/assinatura antes da validação;
- comparar duas implementações reais independentes;
- permitir paralelismo de código realmente necessário quando serializar causaria bloqueio material;
- isolar hotfix/release de código executável ainda em desenvolvimento.

Não são motivo suficiente sozinhos:

- documentação/evidência/aprendizado/skill;
- outro agente estar trabalhando;
- mudança pequena;
- início de fase;
- hábito de Git Flow;
- simplesmente começar a gerar APK, se não houver risco de perder uma versão conhecida como boa.

### Autorização obrigatória

Mesmo quando a engenharia conclui que branch seria útil, **ela não cria nem usa a branch sem autorização clara e explícita do proprietário para aquele objetivo**.

O pedido deve ser único e objetivo: explicar risco, benefício, finalidade e duração esperada.

Depois da autorização, não surgem microautorizações novas. Dentro da branch autorizada, a engenharia pode autonomamente commitar, testar, corrigir, documentar e executar os passos reversíveis necessários ao objetivo.

Merge/release/publicação continuam separados, salvo se a autorização os incluir explicitamente.

### Quantidade

Sem autorização: somente `main`.

Com autorização normal: `main` + uma branch temporária.

Uma segunda branch simultânea precisa de motivo próprio e nova autorização explícita. Não existe `develop` permanente por padrão.

### Situação atual

Na descoberta/investigação atual, o gate de risco continua resultando em **`main` única**. Se outro agente estiver escrevendo, aguardar/serializar, reler o HEAD e continuar; não criar branch automaticamente para paralelizar.

## 4. Operação remota

O GitHub remoto é a fotografia técnica oficial.

Fluxo obrigatório:

`Notion → Codex Engineering Guardrails → GitHub Connector → execução → GitHub atualizado → Notion sincronizado`

Uma cópia local pode existir apenas como ferramenta temporária. Ela não define branch, versão, commit, estado, decisão ou resultado oficial.
