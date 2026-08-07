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

- `✅ VERIFICAR SE O PROJETO ESTÁ ORGANIZADO` — confere governança, branches e regras básicas;
- `📱 GERAR APK PARA INSTALAR` — quando existir build Android, gera um APK pronto para o proprietário baixar e instalar;
- `🧪 TESTAR APK SEM MEXER NO CARRO` — quando houver laboratório/simulador, executa validações sem atuar no equipamento real;
- `🚀 PREPARAR VERSÃO FINAL` — somente quando existir uma etapa real de consolidação/release.

Não criar workflow só para ocupar espaço. Um workflow novo só entra quando existir uma ação real e repetível que o projeto já saiba executar.

## 2. Nome do APK/artefato

Quando a geração de APK existir, o arquivo entregue ao proprietário deve ser autoexplicativo.

Formato preferido:

`INSTALAR-ESTE-APK_<versao-ou-fase>_<sha-curto>.apk`

O resumo do workflow deve informar sempre:

- qual branch gerou o arquivo;
- qual commit/SHA gerou o arquivo;
- qual finalidade do APK;
- se é laboratório, teste ou versão consolidada;
- o próximo passo humano em linguagem simples.

Nunca entregar um arquivo chamado apenas `app-debug.apk` ou `build.apk` como artefato principal para o proprietário.

## 3. Política anti-proliferação de branches

O projeto é curto e deve permanecer simples.

### Princípio principal

**O menor número de branches é o padrão. O limite de 3 é teto de segurança, não meta de ocupação.**

Antes de criar uma branch nova, deve existir uma justificativa técnica concreta que possa ser registrada em uma frase. A mera existência de outro agente/bloco em andamento **não** justifica uma nova branch por si só.

Preferir, nesta ordem:

1. reutilizar a `work/*` atual quando o objetivo técnico for o mesmo;
2. aguardar a consolidação quando a melhoria puder esperar sem risco;
3. criar `lab/*` somente quando isolamento real for necessário para experimento, comparação ou risco técnico específico.

Se não houver uma razão técnica clara para isolamento, não criar branch.

### Limite normal

Máximo de **3 branches remotas ativas ao mesmo tempo**:

1. `main` — estado oficial consolidado;
2. uma única `work/*` — trabalho técnico atual;
3. uma única `lab/*` — investigação temporária, somente quando realmente necessária.

Não existe branch `develop` por padrão.

### Nomenclatura

Branch de trabalho:

`work/f<fase>-<objetivo-curto>`

Exemplo:

`work/f1-hvac-mapeamento`

Branch de laboratório:

`lab/f<fase>-<pergunta-curta>`

Exemplo:

`lab/f1-comparar-apks`

### Regras

- não criar branch por correção pequena;
- não criar `v2`, `v3`, `final`, `final2`;
- um bloco/fase reutiliza a mesma `work/*` enquanto o objetivo permanecer o mesmo;
- `lab/*` só existe quando a investigação precisa de isolamento real;
- “há outro agente trabalhando” não é justificativa suficiente para `lab/*`;
- antes de criar nova branch, consultar as branches remotas existentes;
- branch concluída/abandonada deve ser removida depois de confirmar que não contém trabalho único necessário;
- se já existirem 3 branches remotas, uma nova só pode nascer depois de consolidar ou remover uma das temporárias.

## 4. Operação remota

O GitHub remoto é a fotografia técnica oficial.

Fluxo obrigatório:

`Notion → Codex Engineering Guardrails → GitHub Connector → execução → GitHub atualizado → Notion sincronizado`

Uma cópia local pode existir apenas como ferramenta temporária. Ela não define branch, versão, commit, estado, decisão ou resultado oficial.
