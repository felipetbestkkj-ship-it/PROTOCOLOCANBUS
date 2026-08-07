---
name: artifact-forensics
description: Faz triagem passiva e reprodutível de APKs, archives, logs, firmware containers e outros artefatos preservando original, hash, tipo real e proveniência.
---

# Artifact Forensics

## Use quando

Um arquivo novo entra na investigação ou quando há dúvida sobre identidade, formato, integridade, versão ou relação entre artefatos.

## Procedimento

1. Preserve o original; não sobrescreva.
2. Registre nome, tamanho e SHA-256.
3. Identifique o **tipo real** por assinatura/magic/estrutura, não só por extensão.
4. Para multipart, confirme presença/coerência das partes antes de declarar incompleto/corrompido.
5. Extraia metadados de forma não destrutiva.
6. Separe `original` de `derivado` (extração, decompilação, relatório, conversão).
7. Registre ferramenta/versão quando o resultado depender dela.
8. Só execute binário anexado se houver necessidade e inspeção proporcional; prefira ferramentas conhecidas já disponíveis.
9. Encaminhe para skill especializada quando o tipo estiver confirmado.

## Saída

```text
Artefato:
SHA-256:
Tamanho:
Tipo real:
Proveniência:
Estrutura/metadata relevante:
Derivados gerados:
Ferramenta/versão:
Estado: confirmado | provável | inconclusivo
Próxima pergunta:
```

## Evidência

- extensão ou nome não prova formato;
- arquivo que não abre como ZIP não deve ser chamado de corrompido antes de identificar o formato real;
- igualdade de SHA-256 prova igualdade byte a byte entre os arquivos comparados;
- diferença de hash não explica sozinha a natureza da diferença.

## Limites

Esta skill é passiva. Não instala APK, não executa firmware, não transmite CAN e não modifica equipamento real. Não amplia autoridade do bloco.