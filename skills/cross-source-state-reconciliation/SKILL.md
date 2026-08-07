---
name: cross-source-state-reconciliation
description: Resolve divergências entre Notion, GitHub remoto, evidência do alvo e memória do chat usando autoridade por tipo de fato, corrigindo a fonte obsoleta sem escolher silenciosamente.
---

# Cross Source State Reconciliation

## Use quando

Duas fontes parecem discordar sobre fase, branch, commit, arquivo, comportamento observado ou decisão vigente.

## Autoridade por tipo

- **pedido explícito recente do proprietário:** objetivo/direção;
- **Notion:** missão, bloco, histórico operacional, decisões e handoff;
- **GitHub remoto:** branch, commit/SHA, arquivo versionado, diff, CI e estado técnico mutável;
- **evidência original/runtime:** comportamento/artefato observado do alvo;
- **memória do chat/local:** contexto auxiliar, nunca desempate final.

## Procedimento

1. Declare exatamente qual fato diverge.
2. Classifique o tipo do fato (intenção, versão, comportamento, evidência, histórico).
3. Consulte a fonte com autoridade sobre esse tipo.
4. Confirme frescor: SHA/data/origem.
5. Determine se existe divergência real ou apenas snapshots de momentos diferentes.
6. Corrija a fonte obsoleta quando a correção estiver dentro do bloco e for reversível.
7. Registre a reconciliação se ela puder afetar outro chat.
8. Continue o objetivo; não transforme a reconciliação em nova rodada de autorização.

## Saída

```text
Fato divergente:
Fonte A:
Fonte B:
Autoridade aplicável:
Estado confirmado:
Fonte corrigida:
Evidência fresca:
Impacto no bloco:
```

## Limites

- não fazer média entre fontes;
- não escolher a versão mais conveniente;
- não usar Notion para sobrescrever fato técnico remoto sem evidência;
- não usar GitHub para sobrescrever decisão operacional explícita do proprietário;
- se a correção exigir merge, release ou outra fronteira material, registrar a divergência e parar nessa fronteira.