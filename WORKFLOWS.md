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

- qual commit/SHA gerou o arquivo;
- qual finalidade do APK;
- se é laboratório, teste ou versão consolidada;
- o próximo passo humano em linguagem simples.

Durante a fase de descoberta, a origem normal é sempre a `main`.

Nunca entregar um arquivo chamado apenas `app-debug.apk` ou `build.apk` como artefato principal para o proprietário.

## 3. Política de branches durante a descoberta

### Regra principal

**Durante a fase de descoberta/investigação, existe uma única linha técnica ativa: `main`.**

Todo conhecimento, evidência, documentação, aprendizado, skill, script auxiliar e estado consolidável deve ir para a `main`.

Nenhuma `work/*`, `lab/*`, `develop` ou outra branch pode ser criada ou usada para trabalho sem **autorização clara e explícita do proprietário** para aquele objetivo.

### Concorrência

Se outro trabalho ou agente estiver escrevendo no projeto:

1. não criar branch para escapar da concorrência;
2. aguardar ou parar a escrita atual;
3. reler o HEAD da `main` quando a outra escrita terminar;
4. reconciliar o que mudou;
5. continuar na própria `main`.

**Trabalho paralelo não justifica dispersar conhecimento.**

### Branch autorizada no futuro

Se o proprietário autorizar explicitamente uma branch para um objetivo concreto, essa autorização deve ser registrada no Notion antes da criação. A branch deve existir somente pelo tempo necessário ao objetivo autorizado e o conhecimento útil deve voltar à `main` ao final.

Sem essa autorização explícita, a resposta correta é **não criar branch**.

### Refs históricas

Refs antigas que existam de fases anteriores não são linhas de trabalho. Devem permanecer sem commits exclusivos e ser removidas quando a ferramenta disponível permitir. Sua existência física não autoriza novos trabalhos nelas.

## 4. Operação remota

O GitHub remoto é a fotografia técnica oficial.

Fluxo obrigatório:

`Notion → Codex Engineering Guardrails → GitHub Connector → execução → GitHub atualizado → Notion sincronizado`

Uma cópia local pode existir apenas como ferramenta temporária. Ela não define branch, versão, commit, estado, decisão ou resultado oficial.
