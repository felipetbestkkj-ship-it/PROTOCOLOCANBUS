# F4 — Contrato de comportamento HVAC (rascunho pré-F4)

> **Status:** DRAFT_PRE_F4. Este arquivo prepara a F4, mas não a declara concluída. O elo físico comum ainda depende do gate único da F3.

## Leitura em 30 segundos

```text
INTENÇÃO DO USUÁRIO
       ↓
CarPropertyValue
       ↓
HdPsaProtocol / TX 0x3B
       ↓
CANBOX / veículo
       ↓
RX 0x31
       ↓
ESTADO REAL NA UI
```

O contrato abaixo congela o que já sabemos nos dois sentidos. O único elo ainda marcado como `PHYSICAL_PENDING` é a aceitação física do caminho comum `0x3B → veículo → 0x31` nesta unidade.

### Legenda

- 🟢 **OBSERVED_SINGLE_FIELD** — mudança real observada isoladamente no retorno.
- 🟡 **OBSERVED_COMPOSITE** — campo mudou em runtime, mas junto com outros efeitos.
- ⚪ **NOT_OBSERVED** — sem transição de controle observada; mapeamento vem do código original.
- 🔴 **PHYSICAL_PENDING** — falta o gate físico comum.

## Matriz funcional

| Função | Property | TX Hiworld | Retorno `0x31` | Runtime atual |
|---|---:|---|---|---|
| HVAC dianteiro liga/desliga | `16385` área `8` | `0x3B` sub 0x01 | `front_power` | 🟡 OBSERVED_COMPOSITE |
| HVAC traseiro liga/desliga | `16385` área `128` | `0x3B` sub 0x11 | `rear_power` | ⚪ NOT_OBSERVED |
| A/C liga/desliga | `16386` | `0x3B` sub 0x02 | `ac` | 🟡 OBSERVED_COMPOSITE |
| MAX A/C | `16396` | `0x3B` sub 0x03 | `max_ac` | ⚪ NOT_OBSERVED |
| AUTO | `16395` | `0x3B` sub 0x04 | `auto` | ⚪ NOT_OBSERVED |
| SYNC | `16404` | `0x3B` sub 0x0F | `sync` | ⚪ NOT_OBSERVED |
| Recirculação | `16394` | `0x3B` sub 0x07 | `recirculation` | 🟢 OBSERVED_SINGLE_FIELD |
| Recirculação automática | `16393` | `0x3B` sub 0x10 | `auto_recirculation` | ⚪ NOT_OBSERVED |
| Desembaçador dianteiro | `24577` área `1` | `0x3B` sub 0x05 | `front_defrost` | 🟡 OBSERVED_COMPOSITE |
| Desembaçador traseiro | `24577` área `2` | `0x3B` sub 0x06 | `rear_defrost` | 🟢 OBSERVED_SINGLE_FIELD |
| Ventilador + / - | `16390` | `0x3B` sub 0x0B | `fan` | 🟡 OBSERVED_COMPOSITE |
| Ventilador absoluto | `16389` | `0x3B` sub 0x0B | `fan` | ⚪ NOT_OBSERVED |
| Temperatura esquerda + / - | `16388` área `left` | `0x3B` sub 0x0C | `left_temperature` | ⚪ NOT_OBSERVED |
| Temperatura direita + / - | `16388` área `4` | `0x3B` sub 0x0D | `right_temperature` | ⚪ NOT_OBSERVED |
| Temperatura esquerda absoluta | `16387` área `left` | `0x3B` sub 0x0C | `left_temperature` | ⚪ NOT_OBSERVED |
| Temperatura direita absoluta | `16387` área `4` | `0x3B` sub 0x0D | `right_temperature` | ⚪ NOT_OBSERVED |
| Direção do ar | `16391` | `0x3B` sub 0x08, 0x09, 0x0A | `airflow` | 🟡 OBSERVED_COMPOSITE |
| Intensidade/modo adicional | `16392` | `0x3B` sub 0x0E | `wind_intensity` | ⚪ NOT_OBSERVED |

## Regras que uma implementação nova não pode quebrar

1. **Estado real manda.** UI não assume sucesso local; deve refletir `0x31/HvacInfo` retornado.
2. **Power e recirculação evitam envio redundante** quando o estado solicitado já coincide com o atual.
3. **Recirculação é invertida no fio:** lógico ON gera valor baixo `0`; lógico OFF gera `1`.
4. **Fan absoluto não é um set direto:** compara alvo com fan atual e emite passos `0x0B` repetidos.
5. **Temperatura absoluta é incremental:** compara alvo com temperatura atual e emite `0x0C/0x0D` para cima/baixo.
6. **Airflow é diferencial por bits:** só subcomandos `0x08/0x09/0x0A` que precisam mudar são emitidos.
7. **Código estático não vira prova física.** O rótulo `PHYSICAL_PENDING` só muda depois do gate físico.

## Gate único que falta

Com rear-defrost inicialmente OFF, a UI original deve gerar:

`5A A5 02 3B 06 01 43`

e o retorno deve mudar somente `0x31 payload[2] bit5` de `0 → 1` no caso escolhido.

Se esse elo passar, a F4 pode promover o contrato comum sem pedir validação manual função por função. Se não passar, uma única captura volta para análise offline.

## Fonte executável

- contrato de máquina: `contracts/hvac_behavior_contract.json`;
- validador: `scripts/validate_hvac_behavior_contract.py`;
- testes: `tests/test_hvac_behavior_contract.py`;
- gêmeo digital: `scripts/hiworld_hvac_digital_twin.py`;
- gate físico: `docs/F3_ONE_SHOT_VALIDATION.md`.
