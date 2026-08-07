---
name: reusable-engineering-learning
description: Destila experiência operacional de blocos concluídos em fatos, aprendizados e procedimentos reutilizáveis, promovendo somente métodos maduros a skills sem criar gates de autorização.
---

# Reusable Engineering Learning

## Use quando

- um bloco técnico/material está sendo encerrado;
- houve erro, retrabalho, redução importante de escopo ou descoberta de método;
- uma técnica existente foi confirmada, refinada ou contradita.

Não precisa de um sub-bloco próprio. Faz parte do fechamento do objetivo autorizado.

## Objetivo

Transformar experiência de execução em conhecimento reutilizável sem armazenar transcript, lista de chamadas de ferramenta ou narrativa completa do chat.

## Procedimento

1. Separe **resultado técnico** de **experiência operacional**.
2. Revise apenas marcos materiais: falhas, correções, narrowing, divergências, verificações decisivas e escolhas de ferramenta que mudaram o resultado.
3. Classifique cada item:
   - `FATO_DO_PROJETO`;
   - `APRENDIZADO_OPERACIONAL`;
   - `CANDIDATO_A_SKILL`;
   - `HIPOTESE`.
4. Registre fatos na evidência/estado apropriados.
5. Para aprendizado operacional, registre `observação → causa (se provada) → prevenção → teste/regra`.
6. **Aplique o gate anti-retrabalho ao conhecimento material:**
   - detalhe reproduzível/versionado na linha GitHub autorizada;
   - mapa humano no Notion com resumo no topo e detalhe suficiente para consulta sem redescoberta;
   - para protocolo/binário, preservar framing, bytes/bits, IDs/subcomandos, exemplos, contagens, confiança, hipóteses descartadas e lacunas.
7. Use o teste: um agente novo consegue responder `o que é → onde está → qual fonte prova → qual classificação de evidência → o que falta provar` sem repetir a análise original?
8. Compare candidato com `SKILLS_INDEX.md` para evitar duplicação.
9. Promova autonomamente somente quando cumprir o gate em `docs/LEARNING_SYSTEM.md`.
10. Se ainda não cumprir, mantenha como candidato; não bloqueie o próximo bloco.

## Registros numerados e concorrência

Quando o projeto usa IDs sequenciais para aprendizados/decisões:

1. faça **fresh-read imediatamente antes** de reservar o próximo ID;
2. escolha o próximo ID livre;
3. grave;
4. reconsulte e confirme unicidade;
5. se houver colisão concorrente, preserve um canônico e marque o duplicado como descartado — não apague silenciosamente a história.

## Gate de promoção resumido

Promover quando houver escopo claro e não duplicado, mais pelo menos um:

- repetição bem-sucedida em dois contextos independentes;
- prevenção de falha material com causa provada;
- procedimento especializado determinístico, verificável e claramente reutilizável.

## Saída mínima

Quando houver material útil:

```text
Fatos novos: ...
Aprendizados úteis: ...
Procedimentos reutilizáveis: ...
Skills promovidas/refinadas: ...
Hipóteses/lacunas: ...
Mapa anti-retrabalho atualizado?: sim/não + onde
```

Não invente contagens. Se 42 passos geraram 2 aprendizados, registre 2 aprendizados.

## Autonomia

- Não pedir ao proprietário quais aprendizados registrar quando a classificação é técnica e reversível.
- Refinar ou promover skill dentro do bloco quando o gate estiver satisfeito e isso não alterar autoridade/safety boundary.
- Se a promoção mudaria segurança, fronteira material ou estratégia pública incompatível, registrar candidato e parar na fronteira correspondente.

## Limites

- não transformar hipótese em regra;
- não copiar o histórico completo do chat;
- não promover fato específico do carro/APK como skill genérica;
- não criar skill nova quando uma existente pode ser refinada;
- não usar esta skill para substituir Codex Engineering Guardrails, Notion ou GitHub Connector.