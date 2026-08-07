---
name: android-apk-differential-triage
description: Compara APK baseline/original/candidato de forma dirigida, reduzindo a superfície antes de decompilação profunda e separando identidade, privilégios, componentes, recursos e código.
---

# Android APK Differential Triage

## Use quando

- houver dois ou mais APKs relacionados;
- for preciso descobrir o que realmente mudou;
- a investigação estiver prestes a decompilar tudo sem uma pergunta discriminatória.

## Dependências conceituais

Use `artifact-forensics` para identidade/hashes e `evidence-narrowing` para reduzir a superfície quando necessário.

## Ordem padrão

1. Confirme hash, tamanho e papel de cada APK.
2. Compare identidade Android:
   - package;
   - versionCode/versionName;
   - certificado/assinatura quando acessível;
   - sharedUserId/UID relevante;
   - min/target SDK quando relevante.
3. Compare manifesto:
   - permissions;
   - activities;
   - services;
   - receivers;
   - providers;
   - exported/process/persistent/privileged signals.
4. Compare estrutura do pacote:
   - resources/layouts/drawables/values;
   - assets;
   - native libs;
   - DEX/classes.
5. Faça primeiro diff estrutural/quantitativo; só depois abra código das áreas que diferem ou participam da pergunta.
6. Cruze diferenças com runtime/baseline antes de declarar efeito funcional.
7. Registre também **o que permaneceu idêntico**, pois isso elimina hipóteses.

## Saída

```text
APK A / papel / hash:
APK B / papel / hash:
Identidade:
Manifesto:
Privilégios:
Recursos diferentes:
Código/classes diferentes:
Dependências relevantes:
Superfície reduzida para:
Confirmado:
Provável:
Inconclusivo:
Próxima pergunta de maior poder discriminatório:
```

## Regras de evidência

- nome `HvacActivity` não prova controle físico;
- recurso alterado não prova lógica alterada;
- código estático idêntico em uma classe é evidência forte de que a diferença procurada está em outra superfície, mas não prova comportamento de runtime completo;
- versão maior não significa automaticamente mais compatibilidade;
- assinatura/shared UID são relevantes para instalação/privilégio, não para provar semântica HVAC.

## Limites

Não instalar APK nem modificar alvo real. Não escolher arquitetura final só com diff estático.