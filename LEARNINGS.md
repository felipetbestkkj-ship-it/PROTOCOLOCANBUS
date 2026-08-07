# LEARNINGS

Aprendizados fechados e pendentes. O banco completo fica no Notion.

## L-001 — Confirmar autoridade GitHub antes de declarar publicação

**Estado:** Fechado  
**Observação:** repositório acessível não implica permissão de escrita.  
**Causa:** conector desta sessão autenticado em conta sem `push` no repo alvo.  
**Prevenção:** em bloco que dependa de escrita remota, confirmar repo + usuário autenticado + permissão de push em uma única checagem.  
**Regra:** nunca declarar commit/publicação sem retorno fresco da operação de escrita.
