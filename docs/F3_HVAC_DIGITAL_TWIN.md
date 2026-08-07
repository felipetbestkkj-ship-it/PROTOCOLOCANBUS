# F3 — Gêmeo digital offline do HVAC Hiworld/Peugeot

## Resultado executivo

Este bloco foi criado para reduzir a dependência do carro a **uma validação final discriminatória**, em vez de uma sessão de tentativa e erro.

O trabalho combina três fontes:

1. **código original decompilado** do Car Info/HdPsaProtocol;
2. **runtime real já capturado** em `candata_8.log`;
3. métodos genéricos de engenharia reversa de protocolo absorvidos de referências públicas, principalmente `wshobson/agents` (`protocol-reverse-engineering` e `binary-analysis-patterns`): reconstruir vocabulário, gramática/state machine, implementar parser/generator e validar a compreensão por replay/simulação.

Nenhuma conclusão de projeto foi importada dessas referências externas. O método foi aplicado e verificado contra as evidências do PROTOCOLOCANBUS.

## 1. Pergunta que o gêmeo digital precisa responder

Antes deste bloco restava a dúvida:

> Se não existe `TX 0x3B` na captura, será que a UI HVAC do Car Info poderia estar usando um caminho alternativo por keycodes?

A resposta estática agora é **não para a configuração Peugeot/Hiworld ativa**.

### Prova

`HvacFragment.customizeView(...)` inicia:

- `mCmdMode = true`;
- fan/temp/airflow controllers em command-mode.

A tela só troca para keycode-mode quando a lista de propriedades contém IDs especiais `> 61440`, por exemplo:

- `61697` HVAC power keycode;
- `61699/61700` temp +/-;
- `61701/61702` fan +/-;
- `61703..61715` airflow;
- `61729` automatic mode 2.

`CanBusManager.HvacPropId.isKeyCode(id)` retorna `id > 61440`.

A lista `mHvacPropConfigs` da classe-base nasce vazia. `HdPsaProtocol.initHvacPropertyList()` adiciona somente propriedades normais do HVAC, como `16385`, `16386`, `16388`, `16390`, `16391`, `16392`, `16393`, `16394`, `16395`, `16396`, `16400`, `16401`, `16404` e `24577`. Não existe ID keycode nessa lista.

A mutação posterior localizada em `CanPopWind` substitui apenas a configuração de temperatura `16400` para conversão de unidade e não injeta keycodes.

### Consequência

Para esta configuração:

`HvacFragment → property normal → HvacModel → setHvacProperty → HdPsaProtocol.buildHvacPackets → 0x3B`

é o caminho previsto da UI original.

Portanto, a ausência de `0x3B` durante os sete pushes HVAC de `candata_8` **não pode ser explicada por um keycode-mode oculto da própria tela Peugeot**.

Ela continua permitindo apenas uma classe residual de alternativas: estado/controle originado do lado veículo/CANBOX ou algum produtor externo que bypassasse o fluxo conhecido do Car Info.

## 2. Vocabulário do protocolo modelado

O gêmeo implementa o framing comprovado:

`5A A5 <LEN> <CMD> <DATA...> <CHECKSUM>`

Checksum:

`(sum(bytes de LEN até último DATA) - 1) & 0xFF`

O formato foi validado contra todos os 821 frames de `candata_8`, todos com checksum válido.

### Controle HVAC

`0x3B`:

`5A A5 02 3B <SUBCOMANDO> <VALOR> <CHECKSUM>`

O gêmeo replica o comportamento de `HdPsaProtocol.buildHvacPackets(...)`, incluindo:

- power dianteiro com supressão redundante;
- A/C;
- MAX A/C;
- AUTO;
- front/rear defrost;
- recirculação com inversão do valor no fio;
- airflow por bits `0x08/0x09/0x0A`;
- fan relativo e fan absoluto expandido em passos;
- temp +/-;
- temperatura absoluta expandida em passos conforme `frontTempUnit`;
- wind intensity;
- SYNC;
- auto recirculation.

### Estado HVAC

`0x31` é decodificado e novamente codificado byte a byte. Os oito frames lógicos observados fazem round-trip exato:

`frame real → HvacState → frame gerado == frame real`

## 3. Gramática/state machine aprendida da captura

Os 16 registros RX `0x31` de `candata_8` colapsam em oito estados lógicos.

O solver diferencial compara cada estado com o próximo e produz a sequência semântica mais simples que explica as transições:

| passo | inferência | confiança | motivo principal | TX estático previsto se a ação viesse da UI Car Info |
|---:|---|---:|---|---|
| 1 | `FRONT_DEFROST_ON` | 0,90 | front-defrost muda junto a fan/airflow/temp como macro | `5A A5 02 3B 05 01 42` |
| 2 | `REAR_DEFROST_ON` | 0,999 | **único campo alterado** | `5A A5 02 3B 06 01 43` |
| 3 | `FRONT_DEFROST_OFF` | 0,86 | front-defrost volta e macro fan/airflow/temp é revertida | `5A A5 02 3B 05 00 41` |
| 4 | `REAR_DEFROST_OFF` | 0,999 | **único campo alterado** | `5A A5 02 3B 06 00 42` |
| 5 | `RECIRCULATION_ON` | 0,995 | **único campo alterado** | `5A A5 02 3B 07 00 43` |
| 6 | `HVAC_POWER_OFF` | 0,98 | power muda com efeitos coerentes em A/C e fan | `5A A5 02 3B 01 00 3D` |
| 7 | `HVAC_POWER_ON` | 0,98 | retorno exato ao estado-base | `5A A5 02 3B 01 01 3E` |

Estas etiquetas são **INFERRED**, não `CORRELATED`. O dado observado é a transição `0x31`; a associação com a intenção humana ainda é inferência.

O ponto importante é que o caminho forma uma sequência semanticamente consistente, incluindo pares ON/OFF e retorno exato ao estado inicial.

## 4. Endpoint fake CANBOX

`scripts/hiworld_hvac_digital_twin.py` contém `FakeCanbox`.

Ele trabalha na fronteira Android ↔ CANBOX e nunca acessa dispositivo.

Entrada:

`0x3B`

Saída:

`0x31` previsto.

Regra:

1. se existe uma transição empírica exatamente observada para aquele estado/ação, o fake usa a assinatura real;
2. caso contrário aplica somente o menor efeito sustentado pelo builder/parser estático;
3. efeitos físicos não observados não são inventados;
4. temperatura relativa, por exemplo, é reconhecida como comando, mas o delta exato do byte de retorno não é inventado sem evidência.

Assim, simulação e fato ficam separados.

## 5. Evidência de validação do laboratório

Testes locais executados antes da consolidação:

- `python scripts/hiworld_hvac_digital_twin.py --self-test` → `PASS`;
- `python -m unittest discover -s tests -v` → **11/11 PASS**;
- contra o `candata_8.log` original:
  - 821 frames válidos;
  - 8 estados lógicos `0x31`;
  - 0 TX `0x3B`;
  - caminho observado corresponde byte a byte ao vetor de regressão incorporado;
  - inferência produz a sequência de sete ações acima.

Os testes cobrem:

- vetores conhecidos de checksum/`0x3B`;
- round-trip exato `0x31`;
- supressão redundante de power;
- inversão de recirculação;
- fan absoluto → passos relativos;
- airflow → somente bits modificados e na ordem do builder original;
- temperatura absoluta → quantidade de passos do original;
- replay completo da state machine;
- endpoint fake para rear defrost.

## 6. O que agora está decidido sem usar o carro

### Confirmado

- a UI Peugeot não entra em keycode-mode com a property list do `HdPsaProtocol` ativo;
- o caminho previsto da UI normal termina no builder `0x3B`;
- o protocolo/framing/checksum está modelado;
- o builder HVAC está reproduzido offline;
- o parser/encoder `0x31` está reproduzido byte a byte;
- os oito estados reais formam uma state machine reexecutável;
- rear-defrost ON/OFF e a mudança de recirculação são transições particularmente fortes porque alteram um único campo;
- os sete pushes existentes não foram produzidos pelo caminho HVAC normal da UI Car Info durante aquela captura.

### Ainda não confirmado

A única lacuna relevante para confiar no envio pelo Android é:

> um `0x3B` construído pelo caminho original é realmente aceito pela CANBOX/veículo nesta unidade física e provoca o `0x31` correspondente?

Todo o restante da cadeia até a fronteira serial já está fechado por estático + logs + simulação.

## 7. Experimento físico único de maior informação

Se uma validação no carro ainda for exigida antes de F4/F5, ela não deve ser uma bateria de testes.

O melhor experimento é **um único rear-defrost ON pela UI original do Car Info, partindo de rear-defrost OFF**, com DbgAssist já capturando RX/TX.

Previsão exata:

`TX esperado: 5A A5 02 3B 06 01 43`

Retorno esperado:

- próximo estado `0x31` muda o bit de rear defrost (`payload[2] bit5`) de 0 para 1;
- na assinatura real já observada, nenhum outro campo muda nessa transição.

### Por que este é o melhor teste

- um único botão;
- um único subcomando;
- uma única mudança de estado observada;
- sem macro de fan/airflow como front defrost;
- elimina de uma vez a dúvida “builder estático funciona no fio nesta unidade?”;
- confirma TX, aceitação da CANBOX e retorno de estado no mesmo evento;
- se passar, não há motivo técnico para pedir ao proprietário que repita manualmente cada função: os demais comandos continuam cobertos pelo mesmo builder/framing e pelo contrato estático.

Este teste continua sendo fronteira material e **não foi executado**.

## 8. Método externo absorvido

Foram consultadas referências públicas de skills no GitHub, em especial:

- `wshobson/agents/plugins/reverse-engineering/skills/protocol-reverse-engineering/SKILL.md`;
- `wshobson/agents/plugins/reverse-engineering/skills/binary-analysis-patterns/SKILL.md`.

O procedimento reaproveitado foi:

`captura → boundaries → campos → vocabulário → gramática/state machine → parser/generator → replay → simulação → experimento discriminatório`

A parte de binary analysis reforçou a reconstrução do `customizeView(...)` parcialmente mal decompilado por JADX, permitindo recuperar o switch que ativa/desativa command-mode.

Esse método foi adaptado para uma skill própria do projeto, sem copiar código externo nem importar conclusões de outro projeto.
