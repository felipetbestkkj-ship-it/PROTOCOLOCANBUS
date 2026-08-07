---
name: runtime-static-correlation
description: Correlaciona ação observável, código estático, processos, intents/IPC, logs, TX/RX e estado em uma linha temporal, sem confundir proximidade temporal com causalidade.
---

# Runtime Static Correlation

## Use quando

For necessário ligar uma ação/UI/componente estático ao que realmente ocorreu em runtime.

## Procedimento

1. Defina o evento-alvo e a janela temporal.
2. Identifique o ponto estático candidato: Activity/Fragment/ViewModel/Model/service/receiver/método.
3. Monte uma timeline com fontes disponíveis:
   - ação/touch/estado de UI;
   - lifecycle/process/window;
   - logcat;
   - intent/broadcast/Binder/IPC;
   - chamadas Jancar/CanBusManager quando observadas;
   - TX/RX;
   - retorno/estado posterior.
4. Normalize timestamps e deixe incerteza explícita quando relógios/fontes diferirem.
5. Procure repetição: mesma ação produz o mesmo encadeamento?
6. Procure controles negativos: o evento ocorre também sem a ação?
7. Diferencie `correlacionado`, `fortemente correlacionado` e `causalidade ainda não provada`.
8. Use `evidence-narrowing` para decidir o próximo elo que falta.

## Matriz mínima

| Tempo | Ação/estado | Código/componente | IPC/log | TX/RX | Retorno | Confiança |
|---|---|---|---|---|---|---|

## Regras de confiança

- **confirmado:** evidência direta/repetível liga o elo declarado;
- **provável:** múltiplas evidências convergem, mas falta um elo direto;
- **inconclusivo:** alternativas relevantes continuam abertas.

Proximidade temporal sozinha não prova causalidade.

## Limites

Passiva por padrão. Esta skill não autoriza gerar ações no equipamento real nem transmitir CAN. Quando uma correlação exigir estímulo ativo, parar na fronteira material prevista em `AGENTS.md`.