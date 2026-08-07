# ROADMAP

Cada fase possui saída verificável. Fases podem ser curtas; não servem para burocracia.

## F0 — Fundação limpa
Governança, estado, roadmap, evidência e aprendizado autossuficientes.

**Gate:** novo chat consegue continuar por Notion + GitHub sem contexto externo.

## F1 — Triagem dirigida do Car Info/HVAC
Comparar original/candidato, baseline e runtime; mapear package, versões, manifesto, Activities/Fragments, recursos, serviços/receivers, privilégios e dependências observadas.

**Gate:** mapa verificável de componentes + perguntas prioritárias.

## F2 — Cadeia HVAC original
Mapear ação de UI -> método -> controlador/serviço -> mensagem -> retorno -> estado.

**Gate:** matriz por função com lacunas explícitas.

## F3 — Correlação runtime
Correlacionar ação, logcat, TX/RX, retorno e estado.

**Gate:** hipóteses promovidas ou descartadas por evidência dinâmica.

## F4 — Contrato de comportamento
Congelar estados/transições relevantes do original.

**Gate:** regressões podem ser detectadas.

## F5 — Escolha arquitetural
Decidir por prova entre adaptar UI original, frontend próprio sobre API/IPC existente ou reimplementação mais profunda.

## F6 — Camada única de controle HVAC
Encapsular operações e estado; UI/widget não conhecem protocolo diretamente.

## F7 — Nova UI HVAC
UX automotiva com controles grandes, leitura rápida, estado evidente e comportamento preservado.

## F8 — Autoridade visual única
Resolver overlays/popups antigos.

## F9 — Widget
Usar a mesma camada da tela e refletir estado real.

## F10 — Assinatura, privilégios e instalação
Provar certificado, UID/shared UID, permissões e estratégia de instalação.

## F11 — Build reproduzível e CI
Build -> hash -> testes -> relatório, sem passos manuais obscuros.

## F12 — Laboratório/simulador
Parser/fake/simulador somente quando a gramática necessária estiver comprovada.

## F13 — Validação integrada
Cobrir comandos, estados, reinício, background, atrasos, falha de resposta, reconexão e overlay.

## F14 — Equipamento real
Instalação/atuação somente em bloco que inclua essa fronteira, com rollback.

## F15 — Generalização
Reutilizar arquitetura e aprendizado em outros recursos automotivos.

## Linha paralela: desempenho/ROM

`medir -> classificar -> desativar reversivelmente -> medir novamente -> considerar remoção/ROM somente se justificado`
