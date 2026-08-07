---
name: evidence-narrowing
description: Reduz investigações amplas para a menor superfície capaz de responder à pergunta, priorizando evidência discriminatória sem esconder lacunas ou alternativas materiais.
---

# Evidence Narrowing

## Use quando

- há muitos arquivos/classes/logs/caminhos possíveis;
- a investigação está consumindo contexto sem aumentar confiança;
- é preciso decidir qual evidência abrir a seguir.

## Princípio

Não analisar tudo só porque está disponível. Escolher a próxima evidência pelo **poder de eliminar hipóteses**.

## Procedimento

1. Escreva a pergunta de decisão em uma frase.
2. Liste as hipóteses relevantes e o que distinguiria uma da outra.
3. Liste fontes candidatas.
4. Priorize cada fonte por:
   - proximidade com o comportamento alvo;
   - poder discriminatório;
   - custo/tempo;
   - invasividade/risco;
   - independência da evidência já usada.
5. Inspecione primeiro a fonte de maior valor líquido.
6. Reduza a superfície somente quando o descarte estiver sustentado.
7. Mantenha ao menos um controle negativo/alternativa relevante para evitar confirmação prematura.
8. Pare quando:
   - a pergunta estiver respondida com evidência suficiente; ou
   - a próxima evidência necessária estiver indisponível/for uma fronteira material.

## Exemplo de redução

```text
classes candidatas
   ↓ filtro por referência HVAC
subconjunto
   ↓ diff entre APKs
subconjunto menor
   ↓ presença no runtime/cadeia
poucos candidatos decisivos
```

Não invente números se não foram medidos.

## Saída

```text
Pergunta:
Hipóteses:
Superfície inicial:
Evidência escolhida e por quê:
O que foi eliminado:
Superfície restante:
Controle negativo:
Resposta atual / lacuna:
Próxima evidência de maior valor:
```

## Limites

- narrowing não autoriza ignorar evidência contraditória;
- não descartar safety/security boundary por conveniência;
- não confundir ausência em uma busca com ausência no sistema inteiro;
- quando o custo de narrowing superar o custo da inspeção direta, fazer a inspeção direta.