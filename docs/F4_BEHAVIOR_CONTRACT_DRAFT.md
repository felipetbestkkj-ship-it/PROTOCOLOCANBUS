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

O contrato separa duas perguntas que não podem mais ser misturadas:

```text
1. O protocolo Hiworld sabe representar a função?
2. O veículo-alvo realmente possui essa função?
```

A resposta da primeira não prova a segunda.

### Legenda

- 🟢 **OBSERVED_SINGLE_FIELD** — mudança real observada isoladamente no retorno.
- 🟡 **OBSERVED_COMPOSITE** — campo mudou em runtime, mas junto com outros efeitos.
- ⚪ **NOT_OBSERVED** — sem transição de controle observada; mapeamento vem do código original.
- 🔴 **PHYSICAL_PENDING** — falta o gate físico comum.
- 🚫 **NOT_PRESENT_ON_TARGET** — capacidade existente no protocolo genérico, mas confirmada como ausente no veículo-alvo.

## Perfil físico confirmado do alvo

O proprietário confirmou:

- **desembaçador dianteiro: presente**;
- **desembaçador traseiro: ausente**.

Fonte de máquina: `contracts/hvac_target_profile.json`.

Consequência: o property/bit/subcomando genérico rotulado como `rear_defrost` continua documentado como capacidade do `HdPsaProtocol`, mas não entra como função física do produto para este alvo.

## Matriz funcional do protocolo

| Função/capacidade | Property | TX Hiworld | Retorno `0x31` | Runtime / alvo |
|---|---:|---|---|---|
| HVAC dianteiro liga/desliga | `16385` área `8` | `0x3B` sub 0x01 | `front_power` | 🟡 OBSERVED_COMPOSITE |
| HVAC traseiro liga/desliga | `16385` área `128` | `0x3B` sub 0x11 | `rear_power` | ⚪ presença física no alvo não confirmada |
| A/C liga/desliga | `16386` | `0x3B` sub 0x02 | `ac` | 🟡 OBSERVED_COMPOSITE |
| MAX A/C | `16396` | `0x3B` sub 0x03 | `max_ac` | ⚪ NOT_OBSERVED |
| AUTO | `16395` | `0x3B` sub 0x04 | `auto` | ⚪ NOT_OBSERVED |
| SYNC | `16404` | `0x3B` sub 0x0F | `sync` | ⚪ NOT_OBSERVED |
| Recirculação | `16394` | `0x3B` sub 0x07 | `recirculation` | 🟢 OBSERVED_SINGLE_FIELD / gate atual |
| Recirculação automática | `16393` | `0x3B` sub 0x10 | `auto_recirculation` | ⚪ NOT_OBSERVED |
| Desembaçador dianteiro | `24577` área `1` | `0x3B` sub 0x05 | `front_defrost` | 🟡 OBSERVED_COMPOSITE / presente no alvo |
| `rear_defrost` genérico | `24577` área `2` | `0x3B` sub 0x06 | bit genérico do parser | 🚫 NOT_PRESENT_ON_TARGET |
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
2. **Capacidade do protocolo não vira feature do carro automaticamente.** Antes de expor um controle na UI, ele precisa ser aplicável ao perfil do alvo.
3. **Power e recirculação evitam envio redundante** quando o estado solicitado já coincide com o atual.
4. **Recirculação é invertida no fio:** lógico ON gera valor baixo `0`; lógico OFF gera `1`.
5. **Fan absoluto não é um set direto:** compara alvo com fan atual e emite passos `0x0B` repetidos.
6. **Temperatura absoluta é incremental:** compara alvo com temperatura atual e emite `0x0C/0x0D` para cima/baixo.
7. **Airflow é diferencial por bits:** só subcomandos `0x08/0x09/0x0A` que precisam mudar são emitidos.
8. **Código estático não vira prova física.** O rótulo `PHYSICAL_PENDING` só muda depois do gate físico.

## Gate único que falta

Com recirculação inicialmente OFF, a UI original deve gerar:

`5A A5 02 3B 07 00 43`

e o retorno deve mudar somente `0x31 payload[1] bit4` de `0 → 1` no caso escolhido.

Se esse elo passar, a F4 pode promover o contrato comum sem pedir validação manual função por função. Se não passar, uma única captura volta para análise offline.

## Fonte executável

- catálogo genérico: `contracts/hvac_behavior_contract.json`;
- perfil do alvo: `contracts/hvac_target_profile.json`;
- validador do catálogo: `scripts/validate_hvac_behavior_contract.py`;
- validador do alvo: `scripts/validate_hvac_target_profile.py`;
- testes: `tests/test_hvac_behavior_contract.py` + `tests/test_hvac_target_profile.py`;
- gêmeo digital: `scripts/hiworld_hvac_digital_twin.py`;
- gate físico: `docs/F3_ONE_SHOT_VALIDATION.md`.
