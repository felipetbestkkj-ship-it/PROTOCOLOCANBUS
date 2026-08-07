# Contratos HVAC — como ler sem confundir protocolo com veículo

Há duas camadas intencionais:

1. `hvac_behavior_contract.json` — **catálogo genérico do protocolo `HdPsaProtocol`**. Preserva properties, bits, subcomandos e exemplos que o protocolo sabe representar.
2. `hvac_target_profile.json` — **perfil autoritativo do veículo-alvo**. Diz quais capacidades são realmente aplicáveis ao carro e qual é o gate físico vigente.

## Regra de precedência

Quando houver conflito entre um rótulo/capacidade do contrato genérico e o perfil do alvo:

**o perfil do alvo vence para UI, produto e teste físico.**

## Correção conhecida

O contrato genérico histórico ainda contém no campo `common_physical_link` a antiga escolha `rear_defrost_on`. Esse campo é **legado e não autoritativo** após a correção de 07/08/2026.

O veículo-alvo possui somente desembaçador dianteiro. `rear_defrost` continua preservado apenas como capacidade/semântica do protocolo genérico.

Gate físico correto da F3, definido em `hvac_target_profile.json` e `docs/F3_ONE_SHOT_VALIDATION.md`:

- ação: recirculação OFF→ON;
- TX previsto: `5A A5 02 3B 07 00 43`;
- RX previsto: `0x31 payload[1] bit4: 0 → 1`.

O validador genérico não usa mais o gate histórico como verdade do alvo; o workflow também executa `validate_hvac_target_profile.py`.
