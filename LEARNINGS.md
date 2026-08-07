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

## L-003 — Paralelismo não justifica branch durante descoberta

**Estado:** Fechado  
**Observação:** branches temporárias dispersaram conhecimento que deveria ter sido imediatamente acumulado na `main`.  
**Causa:** a disponibilidade de `work/*`/`lab/*` e a existência de trabalho paralelo foram tratadas como motivo suficiente para separar linhas de conhecimento.  
**Prevenção:** durante descoberta, usar somente `main`; se outra escrita estiver em andamento, aguardar ou parar, fazer fresh-read do novo HEAD e continuar de forma serial.  
**Regra:** nenhuma branch pode ser criada ou usada sem autorização clara e explícita do proprietário. Paralelismo é resolvido por espera/serialização, não por branch.

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

## L-006 — Reservar ID de aprendizado somente após leitura fresca

**Estado:** Fechado  
**Observação:** durante a reconciliação do banco Aprendizados, outro bloco/agente criou o `L-003` entre a leitura inicial e a escrita, produzindo temporariamente dois registros com o mesmo ID.  
**Causa:** o próximo identificador foi escolhido a partir de uma fotografia que deixou de ser atual antes da criação do registro.  
**Prevenção:** em ambiente com possíveis escritores concorrentes, consultar novamente o banco imediatamente antes de criar aprendizado numerado; se houver colisão, preservar um canônico e marcar o duplicado como descartado.  
**Regra:** antes de criar `L-NNN`: fresh-read dos IDs → escolher próximo livre → criar → reconsultar e verificar unicidade.  
**Promoção:** candidato a `skills/reusable-engineering-learning/SKILL.md`.

## L-007 — Protocolo CANBOX serial não é CAN bruto do veículo

**Estado:** Fechado  
**Observação:** os `candata_*` foram tratados informalmente como logs da rede CAN, mas a F3 provou que o framing `5A A5` pertence ao enlace serial Android/Car Info ↔ CANBOX Hiworld; a CAN veicular fica abaixo da CANBOX.  
**Causa:** a camada e o transporte não estavam rotulados antes da interpretação dos IDs, permitindo confundir command IDs do gateway com arbitration IDs CAN do Peugeot.  
**Prevenção:** em toda captura, identificar primeiro framing, direção, transporte e camada; só depois atribuir semântica ao ID.  
**Regra:** para este equipamento, `candata = protocolo Hiworld serial em /dev/ttyS5 @ 38400`; `0x31`, `0x3B`, `0x6A` e `0xFF` são IDs/comandos da CANBOX, não CAN IDs veiculares comprovados.  
**Promoção:** candidato a refinamento de `skills/can-frame-differential-analysis/SKILL.md`.