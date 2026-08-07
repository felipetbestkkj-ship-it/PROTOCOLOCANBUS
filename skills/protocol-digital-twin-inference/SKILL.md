---
name: protocol-digital-twin-inference
description: Constrói um gêmeo digital passivo de protocolo quando formato, código estático e traces existem, reduzindo validação cara no hardware a um experimento final de máxima informação.
---

# Protocol Digital Twin Inference

## Use quando

- o protocolo é proprietário e parcialmente reconstruído;
- há código/decompilação + traces reais;
- interação com o equipamento real é cara, demorada ou uma fronteira material;
- a pergunta é “quanto conseguimos provar/simular antes de tocar o hardware?”.

## Princípio

Separar duas coisas:

1. **vocabulário** — framing, campos, comandos, checksum, parser/generator;
2. **gramática** — quais estados/transições ocorrem e sob quais ações/eventos.

O gêmeo deve reproduzir o que já foi observado e deixar explícito quando está fazendo uma previsão contra-factual.

## Procedimento

1. Faça o preflight normal e prove camada/transporte antes de interpretar IDs.
2. Use `evidence-narrowing` para definir a menor pergunta ainda aberta.
3. Recupere o **vocabulário** por fontes independentes quando possível:
   - parser original;
   - builder original;
   - traces reais;
   - checksum/framing validado.
4. Recupere a **gramática**:
   - normalize estados;
   - deduplicate cópias de logger;
   - calcule deltas consecutivos;
   - identifique pares reversíveis e transições de campo único;
   - classifique polling vs push/evento.
5. Classifique toda peça do modelo como:
   - `STATIC` — código/configuração;
   - `OBSERVED` — trace real;
   - `SIMULATED` — produzido pelo gêmeo;
   - `INFERRED` — melhor explicação ainda não correlacionada.
6. Implemente parser + generator e exija round-trip exato para mensagens observadas quando o formato permitir.
7. Reimplemente apenas a lógica necessária do builder; preserve edge cases e supressões observadas no código original.
8. Construa uma state machine empírica com as transições reais. Não generalize uma macro além do estado em que foi observada sem marcar a extrapolação.
9. Crie um endpoint fake na fronteira já comprovada. Ele pode:
   - usar transição empírica quando houver match exato;
   - aplicar efeito mínimo sustentado por estático quando não houver;
   - nunca inventar efeito físico desconhecido.
10. Rode regressões:
    - checksum/framing;
    - vetores estáticos;
    - trace replay;
    - invariantes do builder;
    - controle negativo para hipótese alternativa.
11. Procure caminhos alternativos no software antes de atribuir ausência de TX ao hardware (ex.: keycode-mode, IPC alternativo, segunda porta, outro processo).
12. Quando restar hardware, ranqueie experimentos por:
    - poder discriminatório;
    - número de variáveis alteradas;
    - reversibilidade/risco;
    - tempo do proprietário.
13. Escolha **um único experimento de máxima informação** quando ele puder fechar o elo comum. Não peça validação função-por-função se um teste de infraestrutura + estático cobre o restante.

## Saída mínima

```text
Pergunta residual:
Vocabulário confirmado:
Gramática observada:
Modelo/fake implementado:
Regressões:
Hipóteses eliminadas:
Inferências preservadas:
Lacuna física residual:
Experimento único de maior informação:
```

## Regras de evidência

- replay exato prova fidelidade ao trace, não causalidade física;
- builder reproduzido prova equivalência estática, não aceitação no fio;
- state transition observada não prova qual ator a causou;
- “não houve TX” só exclui caminhos cobertos pelo ponto de logging provado;
- gêmeo não pode converter `INFERRED` em `OBSERVED`;
- uma transição de campo único tem alto poder discriminatório, mas ainda precisa do rótulo correto de evidência.

## Limites

Esta skill é **offline/passiva por padrão**.

Ela não autoriza:
- transmissão CAN;
- replay em equipamento;
- ação física;
- instalação/modificação do alvo;
- ROM/firmware/root.

Quando o experimento final exigir o equipamento real, parar na fronteira material de `AGENTS.md`.

## Origem metodológica

Método adaptado e validado no projeto a partir de práticas públicas de protocol reverse engineering e binary analysis, incluindo as skills `protocol-reverse-engineering` e `binary-analysis-patterns` do repositório público `wshobson/agents`. Nenhuma conclusão técnica externa é importada como verdade do projeto.
