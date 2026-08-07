# L-011 — Capacidade do protocolo não prova feature no veículo-alvo

## Observação

O `HdPsaProtocol` expõe property, subcomando e bit rotulados como `rear_defrost`. A captura também mostra esse bit alternando. Isso foi interpretado como se o veículo-alvo possuísse desembaçador traseiro.

O proprietário corrigiu o fato físico: **o veículo-alvo possui apenas desembaçador dianteiro; não possui desembaçador traseiro**.

## Causa

A engenharia misturou duas camadas diferentes:

`capacidade genérica do protocolo` → `feature física disponível no alvo`

O manager/protocolo Hiworld atende múltiplas configurações e pode carregar campos que não correspondem a hardware existente em cada veículo específico.

## Correção

- preservar `rear_defrost` como semântica/capacidade do parser e builder genéricos;
- não atribuir a transição observada daquele bit a atuação física no alvo;
- manter um `hvac_target_profile.json` separado do catálogo genérico;
- trocar o gate físico único para **recirculação OFF→ON**, que é aplicável ao alvo e possui transição isolada observada.

## Prevenção

Antes de promover qualquer property/bit/subcomando para UI, contrato do produto ou teste físico:

1. provar o protocolo/capacidade;
2. verificar aplicabilidade ao alvo;
3. somente então tratar como feature do veículo.

## Regra

**Capacidade do protocolo ≠ capacidade física do alvo.**

Quando um protocolo for multi-veículo/configurável, manter explicitamente uma camada de `target profile` e usar `NOT_APPLICABLE_TARGET` para capacidades genéricas ausentes no alvo.

## Promoção

Regra incorporada à skill `protocol-digital-twin-inference`.
