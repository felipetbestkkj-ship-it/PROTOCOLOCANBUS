# PROTOCOLOCANBUS — Índice de Skills

Este arquivo é o catálogo técnico canônico das skills próprias do projeto. O conteúdo completo de cada skill vive no GitHub em `skills/<nome>/SKILL.md`.

## Regra de uso

1. Fazer o preflight obrigatório: `Notion → Codex Engineering Guardrails → GitHub Connector`.
2. Ler este índice antes de uma execução especializada.
3. Selecionar automaticamente apenas as skills úteis à pergunta atual. Normalmente 1–3 skills são suficientes.
4. Não pedir autorização para carregar ou aplicar uma skill quando o objetivo do bloco já cobre a ação.
5. Skills são aceleradores de método, **não gates de permissão**. Ausência ou inaplicabilidade de uma skill não bloqueia o bloco; Guardrails + governança do repositório continuam suficientes.
6. Nenhuma skill amplia autoridade: instalação em alvo real, transmissão CAN ativa, root/ROM/firmware, merge/release e outras fronteiras materiais continuam seguindo `AGENTS.md`.
7. Não carregar todas as skills por padrão. Contexto desnecessário também é ruído.

## Skills ativas

| Skill | Use quando | Resultado esperado |
|---|---|---|
| `reusable-engineering-learning` | fechamento de bloco ou marco relevante | destilar experiência operacional, registrar aprendizado e promover método maduro sem guardar transcript |
| `artifact-forensics` | um artefato novo entra na investigação | identidade, hash, tipo real, proveniência e extração não destrutiva |
| `android-apk-differential-triage` | comparar APK original/baseline/candidato | reduzir diferenças a manifest, assinatura, componentes, recursos, DEX e dependências relevantes |
| `runtime-static-correlation` | cruzar código estático com runtime | linha temporal de ação/log/processo/IPC/TX/RX/estado com níveis de confiança |
| `cross-source-state-reconciliation` | Notion, GitHub e evidência parecem divergir | identificar qual fonte governa cada fato, corrigir o estado obsoleto e registrar a reconciliação |
| `can-frame-differential-analysis` | analisar logs/frames CAN de forma passiva | framing, agrupamento, periodicidade, request/response, diferenças de payload e hipóteses explicitamente marcadas |
| `evidence-narrowing` | investigação está ampla ou ruidosa | reduzir superfície pela evidência com maior poder discriminatório e manter lacunas explícitas |

## Combinações típicas

- **Novo APK:** `artifact-forensics` → `android-apk-differential-triage` → `evidence-narrowing`.
- **Entender uma ação HVAC:** `evidence-narrowing` → `runtime-static-correlation`; adicionar `can-frame-differential-analysis` quando houver frames relevantes.
- **Comparar logs CAN:** `artifact-forensics` quando o arquivo for novo → `can-frame-differential-analysis` → `runtime-static-correlation` se houver ação/tempo observável.
- **Divergência de estado:** `cross-source-state-reconciliation`.
- **Fechamento de bloco:** `reusable-engineering-learning` depois da verificação técnica.

## Hierarquia

`Pedido do proprietário / segurança → Notion → Guardrails → GitHub/AGENTS → skill aplicável → execução`

Uma skill nunca contradiz nem substitui uma camada acima.

## Promoção de novos métodos

O sistema de promoção está documentado em `docs/LEARNING_SYSTEM.md`. Em resumo, execução gera conhecimento técnico e experiência operacional; experiência útil vai para `LEARNINGS.md`; somente método suficientemente repetível/provado vira nova skill.

Evitar proliferação: um novo nome de skill só entra quando não cabe com clareza em uma skill existente e existe benefício repetível demonstrável.