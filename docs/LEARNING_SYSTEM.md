# PROTOCOLOCANBUS — Sistema de Aprendizado Reutilizável

## Objetivo

Fazer cada bloco deixar o próximo agente melhor preparado sem transformar histórico de execução em burocracia ou contexto infinito.

O sistema preserva duas coisas diferentes:

1. **conhecimento do projeto** — fatos técnicos, evidências, decisões e estado;
2. **método reutilizável** — formas de investigar/testar que evitaram erro ou reduziram trabalho.

## Fluxo

```text
EXECUÇÃO
   ↓
resultado técnico + experiência operacional
   ↓
LEARNING DISTILLER
   ↓
┌────────────────────────┬────────────────────────┐
│ conhecimento do projeto│ método de engenharia  │
│ evidência/estado/docs   │ LEARNINGS.md / Notion │
└────────────────────────┴─────────────┬──────────┘
                                      ↓
                              repetível/provado?
                                ↓          ↓
                               não        sim
                                ↓          ↓
                             guardar      SKILL
                                           ↓
                                  próximo agente
                                           ↓
                                     execução melhor
                                           ↓
                                        aprende
```

O alvo não é conservar uma lista de tudo que o chat fez. Um bloco pode executar dezenas de passos e produzir poucos aprendizados realmente úteis:

```text
42 passos executados
      ↓
5 aprendizados úteis
      ↓
2 procedimentos reutilizáveis
      ↓
talvez 1 nova skill
```

Os números são ilustrativos; a regra é **destilar, não transcrever**.

## Classificação no fechamento

Ao fechar um bloco material, classificar descobertas em quatro caixas:

### A. Fato do projeto

Exemplos: hash de APK, componente confirmado, versão, relação observada, resultado de teste.

Destino: `EVIDENCE_INDEX.md`, documento técnico da fase, `PROJECT_STATE.md` quando consolidado e Notion quando operacionalmente relevante.

### B. Aprendizado operacional

Exemplos: uma ordem de investigação reduziu ruído; uma checagem evitou trabalhar sobre SHA obsoleto; uma ferramenta falhou de modo reproduzível.

Destino: `LEARNINGS.md` + banco Aprendizados do Notion quando material/reutilizável.

### C. Procedimento candidato a skill

Método especializado que pode ser repetido em outros blocos, mas ainda não atingiu o gate de promoção.

Destino: aprendizado com estado/promoção explícitos; não criar skill prematuramente.

### D. Hipótese

Inferência ainda sem evidência suficiente.

Destino: lacuna/pergunta pendente. Hipótese não vira regra, aprendizado fechado ou skill.

## Gate de promoção para skill

Uma aprendizagem pode ser promovida autonomamente a skill quando:

- não duplica uma skill existente; e
- tem escopo claro, entrada, procedimento, saída e limites; e
- cumpre pelo menos um dos critérios abaixo:
  1. funcionou em dois ou mais blocos/contextos independentes; ou
  2. previne recorrência de falha material cuja causa foi provada; ou
  3. é procedimento especializado determinístico, verificável e claramente repetível nas fases seguintes.

Não promover:

- fato específico do projeto;
- estado mutável;
- preferência isolada;
- hipótese;
- conselho genérico;
- uma sequência que só funcionou uma vez sem explicação de por que funcionou;
- nova skill cujo conteúdo cabe claramente em outra existente.

## Autonomia e não-bloqueio

Este sistema **não adiciona checkpoints de autorização**.

Dentro de um objetivo autorizado, a engenharia pode autonomamente:

- escolher skills aplicáveis;
- registrar aprendizado;
- refinar uma skill existente;
- promover candidato que satisfaça o gate;
- criar teste/regra de prevenção correspondente.

Só parar quando a própria mudança atravessar uma fronteira material de `AGENTS.md`, por exemplo alterar autoridade, segurança, integração protegida ou alvo real.

Skills não são pré-condição para trabalhar. Se uma skill faltar, estiver incompleta ou não se aplicar, executar pelo Guardrails e pelas regras do repositório, registrar a lacuna e seguir.

## Seleção enxuta de skills

Após o preflight, consultar `SKILLS_INDEX.md` e selecionar o menor conjunto útil. Normalmente 1–3.

Evitar carregar todas as skills porque:

- aumenta ruído;
- cria instruções concorrentes;
- gasta contexto sem melhorar evidência.

Skills podem chamar conceitualmente outras skills relacionadas, mas o agente continua responsável por manter um único plano coerente.

## Evidência de aprendizado

Uma afirmação como “este método é melhor” precisa indicar o que melhorou de forma observável, por exemplo:

- superfície de investigação reduzida;
- hipótese eliminada por evidência discriminatória;
- erro recorrente prevenido;
- etapa redundante removida;
- diferença entre fontes reconciliada;
- teste/checagem passou a detectar um defeito real.

Não exigir métricas artificiais quando não existem; registrar comparação qualitativa verificável é suficiente.

## Relação GitHub × Notion

### GitHub — canônico técnico

- `skills/<nome>/SKILL.md`: conteúdo completo da skill;
- `SKILLS_INDEX.md`: catálogo e seleção;
- `LEARNINGS.md`: espelho compacto dos aprendizados reutilizáveis;
- documentos/evidências da fase: fatos técnicos.

### Notion — operação e memória

- página de Skills: catálogo humano, status e hierarquia;
- banco Aprendizados: erro/descoberta, causa, prevenção, promoção;
- Estado/Blocos: onde o projeto está e qual o próximo passo.

O Notion não deve duplicar o texto integral das skills. Assim não surgem duas versões concorrentes.

## Revisão de skills

Uma skill deve ser alterada quando evidência real mostrar que:

- o procedimento causa ruído recorrente;
- uma etapa é desnecessária;
- falta um caso negativo importante;
- o escopo está amplo demais;
- uma fronteira de segurança precisa ser mais clara.

A revisão acontece no mesmo ciclo `observação → causa → correção → prevenção → registro`.

## Anti-padrões

- salvar transcript completo como “aprendizado”;
- criar uma skill para cada descoberta;
- transformar skill em nova camada de autorização;
- fazer o proprietário decidir quais ferramentas técnicas usar dentro do bloco;
- transformar uma hipótese em procedimento obrigatório;
- duplicar skill completa no Notion/instrução personalizada;
- usar skill como justificativa para ignorar Guardrails ou `AGENTS.md`.