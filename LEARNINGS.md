# LEARNINGS

Aprendizados fechados e pendentes. O banco completo fica no Notion.

## L-001 — Confirmar autoridade GitHub antes de declarar publicação

**Estado:** Fechado  
**Observação:** repositório acessível não implica permissão de escrita.  
**Causa:** conector desta sessão autenticado em conta sem `push` no repo alvo.  
**Prevenção:** em bloco que dependa de escrita remota, confirmar repo + usuário autenticado + permissão de push em uma única checagem.  
**Regra:** nunca declarar commit/publicação sem retorno fresco da operação de escrita.

## L-002 — Destilar execução em vez de preservar a trilha inteira

**Estado:** Fechado  
**Observação:** um bloco pode produzir muitas inspeções, buscas e chamadas de ferramenta, mas apenas uma fração altera conhecimento, prevenção ou método reutilizável.  
**Causa:** a trilha de execução mistura orquestração transitória com evidência e decisões; copiá-la integralmente transfere ruído para o próximo agente.  
**Prevenção:** no fechamento material, classificar somente fatos do projeto, aprendizados operacionais, candidatos a skill e hipóteses; registrar apenas itens úteis.  
**Regra:** usar `skills/reusable-engineering-learning/SKILL.md`; transcript/log de ações não é, por si só, aprendizado.

## L-003 — Branch permitida não significa branch necessária

**Estado:** Fechado  
**Observação:** foi criada `lab/f0-learning-system` apenas para isolar uma melhoria paralela enquanto outra `work/*` estava ativa, embora a mudança pudesse aguardar consolidação e não tivesse necessidade técnica concreta de isolamento experimental.  
**Causa:** o limite `main + work/* + lab/*` foi interpretado como estrutura disponível a ocupar, em vez de teto máximo para exceções justificadas.  
**Prevenção:** antes de criar qualquer branch, provar a necessidade: reutilizar a linha ativa quando o objetivo for o mesmo; aguardar consolidação quando a mudança puder esperar; usar `lab/*` somente se houver isolamento técnico real que reduza risco ou permita experimento descartável. Trabalho paralelo de outro agente, sozinho, não basta.  
**Regra:** o menor número de branches é o padrão; **3 é teto, não meta**. Se a nova branch não tiver uma justificativa técnica concreta que possa ser registrada em uma frase, não criar.

## L-004 — Crash loop após mudança de sourceDir do Car Info — causa pendente

**Estado:** Pendente  
**Observação:** a captura runtime posterior mostra `com.can.activity` reiniciando repetidamente e tentando carregar um caminho antigo de `base.apk` inexistente, enquanto a baseline registra a v3854 em outro caminho atual.  
**Causa:** ainda não provada; a hipótese de estado/metadados persistentes após substituição do APK não deve virar regra sem reprodução controlada.  
**Prevenção:** não definir procedimento de instalação/restart como regra antes da reprodução em laboratório ou bloco autorizado.  
**Regra:** comparar `sourceDir` e processo antes/depois da substituição e só fechar este aprendizado quando a causa for demonstrada.

## L-005 — Frame construído estaticamente não equivale a TX observado

**Estado:** Fechado  
**Observação:** a F2 reconstruiu frames HVAC `0x3B` diretamente de `buildHvacPackets`, mas `candata_5..8` não contém TX `0x3B` observado.  
**Causa:** código estático mostra o que a implementação pode construir; runtime mostra o que realmente ocorreu. São evidências complementares, não equivalentes.  
**Prevenção:** rotular frames como `construído estaticamente`, `TX observado`, `RX observado` ou `correlacionado`.  
**Regra:** para promover comando a comportamento comprovado, exigir `ação controlada → timestamp → TX → RX/estado`; ausência de TX permanece lacuna explícita.  
**Promoção:** candidato a `skills/runtime-static-correlation/SKILL.md`.
