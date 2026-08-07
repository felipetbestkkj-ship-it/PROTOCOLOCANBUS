# F5 — Prontidão arquitetural (recomendação preliminar)

> **Status:** PRELIMINAR. Não promove F5 antes do fechamento da F3/F4. O objetivo é evitar chegar à escolha arquitetural sem uma direção técnica.

## Resumo visual

```text
OPÇÃO A — redesenhar dentro do Car Info
[ nossa UI ] → código interno Car Info → Binder/service → CANBOX
      🟡 viável, mas acopla produto ao APK original

OPÇÃO B — app/frontend próprio usando o Binder do Car Info
[ nossa UI + widget ] → ICanUI/ICanBus → serviço Car Info → CANBOX
      🟢 CANDIDATO PREFERIDO

OPÇÃO C — app próprio falando direto /dev/ttyS5
[ nossa UI ] → protocolo Hiworld próprio → serial → CANBOX
      🔴 fallback; duplica transporte/ACK/timing e exige mais privilégio
```

## Nova evidência estática que melhora a decisão

A análise dirigida do `CARINFO.apk` mostrou:

- manifesto: package `com.can.activity`, `targetSdkVersion=27`, shared UID `android.uid.system`;
- serviço `com.can.ui.CanPopWind` possui intent filters `autoai.intent.action.CANBUS_SERVICE`, `yecon.intent.CanService` e `com.jancar.canservice`;
- o manifesto inspecionado não declara `android:permission` nesse serviço;
- o `dumpsys package` da captura runtime lista `CanPopWind` na **Service Resolver Table** para as três actions, confirmando que o PackageManager desta unidade resolve esse serviço;
- `CanBusManager` conecta explicitamente a `com.can.activity/com.can.ui.CanPopWind`;
- ao conectar, chama `ICanUI.getCanService("CanBusManager")`;
- `CanBusService.onBind()` retorna o Binder `ICanUI` diretamente;
- `ICanUI.getCanService("CanBusManager")` retorna `mCanBusBinder`;
- no código inspecionado de `CanBusService`, não foi localizado `Binder.getCallingUid`, `checkCallingPermission`, `enforceCallingPermission` ou gate equivalente antes desse acesso;
- `ICanBus` expõe diretamente as operações de interesse:
  - `registerListener` — transaction 1;
  - `setHvacProperty(CarPropertyValue)` — transaction 7;
  - `getHvacInfo()` — transaction 13;
  - `getPropertyList(String)` — transaction 26;
- `ICanBusListener.onHvacInfoChanged(HvacInfo)` é transaction 1;
- `CarPropertyValue` e `HvacInfo` são `Parcelable`; sua ordem de serialização foi decompilada e é tecnicamente reproduzível.

**Interpretação correta:** isso torna um frontend separado via Binder **fortemente plausível**, mas ainda não prova que um APK externo não-assinado consegue bindar e trocar todos os Parcelables na multimídia real. Esse ponto vira um probe controlado futuro, não uma suposição.

Contrato estático/runtime dessa superfície: `contracts/carinfo_hvac_binder_contract.json`.

## Ranking preliminar

| Opção | Controle | Dependência do Car Info | Complexidade | Risco de privilégio | UI/widget próprios | Nota preliminar |
|---|---|---|---|---|---|---:|
| A. Modificar UI dentro do Car Info | alta | muito alta | média | menor | possível, porém acoplado | 7/10 |
| **B. Frontend próprio via Binder** | **alta** | serviço/backend apenas | **média** | **médio, testável** | **excelente** | **9/10** |
| C. Falar direto com `/dev/ttyS5` | máxima | nenhuma | alta | alta | excelente | 5/10 |

## Por que B lidera

Ela preserva justamente a parte do Car Info que já funciona como backend automotivo e substitui a parte que queremos controlar: a experiência.

```text
HOJE
Car Info UI + Car Info backend + Hiworld

ALVO PROVISÓRIO
Nossa UI/widget
       ↓
Nossa camada HVAC
       ↓
Binder ICanBus existente
       ↓
Car Info como backend invisível
       ↓
Hiworld/CANBOX
```

Benefícios:

1. não reimplementar serial, ACK, polling e timing sem necessidade;
2. UI e widget podem usar a mesma camada própria;
3. estado real continua vindo de `getHvacInfo`/listeners;
4. o protocolo `0x3B/0x31` continua útil como oracle/teste, sem obrigar a UI a conhecer bytes;
5. reduz o que precisa ser modificado no APK original.

## O que ainda impede chamar isso de decisão F5

Antes de promover B como arquitetura oficial, provar:

1. **gate físico F3:** o caminho comum UI original → `0x3B` → `0x31`;
2. **contrato F4:** comportamento congelado;
3. **Binder probe:** um cliente separado consegue bindar a `CanPopWind`, obter `ICanBus`, ler `getHvacInfo` e registrar listener sem privilégio/signatura adicional inesperada;
4. só depois testar escrita (`setHvacProperty`) dentro da fronteira de equipamento real autorizada.

Se o Binder probe falhar por permissão/UID/parcel compatibility, a investigação volta para A antes de considerar C. Falar direto com a serial é fallback, não atalho.
