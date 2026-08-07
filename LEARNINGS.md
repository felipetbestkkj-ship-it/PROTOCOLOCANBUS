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