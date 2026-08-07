# F1 — Triagem orientada e mapa do Car Info/HVAC

## Resultado executivo

A F1 confirma o primeiro mapa técnico verificável do `Car Info / com.can.activity` sem atuar no carro, sem transmitir CAN e sem modificar a multimídia durante este bloco.

A descoberta mais importante é que o arquivo `INSTALAR-v3854-CarInfo-HVAC-Visual-V1.apk` não é apenas um candidato abstrato: seu SHA-256 é idêntico ao APK extraído como **atualmente instalado** dentro da baseline de 06/08/2026.

Também foi possível separar mudança visual de mudança lógica no núcleo HVAC inspecionado: o manifesto muda somente o `versionCode` 3853 → 3854, três classes centrais analisadas mantêm o mesmo código decompilado entre original e v3854, enquanto as diferenças significativas localizadas concentram-se em layouts, cores e novos drawables HVAC.

Há ainda um risco de runtime relevante e não resolvido: a captura posterior mostra `com.can.activity` entrando em ciclo de reinício ao tentar carregar um caminho antigo de `base.apk` que já não existe. O sintoma é comprovado; a causa ainda não é.

## 1. Escopo e método

Pergunta da F1: **quais são os componentes, privilégios, diferenças e dependências relevantes do Car Info/HVAC antes de mapear comando por comando?**

Análise dirigida sobre:

- `CARINFO.apk` — referência original;
- `INSTALAR-v3854-CarInfo-HVAC-Visual-V1.apk` — v3854;
- `CANBOX-Baseline-20260806-104015.zip` — estado instalado/baseline;
- `CANBOX_RUNTIME_CAPTURE_2026-08-06_1201.zip` — runtime posterior;
- `logcat_0.log` e `candata_5.log` a `candata_8.log`;
- JADX anexado, usado somente como ferramenta auxiliar de análise estática.

Não foram usados outros repositórios como fonte técnica. Não houve instalação, root, alteração de ROM/firmware, replay ou transmissão CAN ativa neste bloco.

## 2. Identidade das evidências principais

| Artefato | SHA-256 | Resultado na F1 |
|---|---|---|
| `CARINFO.apk` | `b047b836b1ce62f72a2f7f1f6c83f3da926cfe2362f4b755e9256625d2dc1cf7` | referência original analisada |
| `INSTALAR-v3854-CarInfo-HVAC-Visual-V1.apk` | `d0741a541fc575d3b25bc853a171532b815e8c396451dcc9ebe0f678d1905a50` | v3854 analisado |
| `CANBOX-Baseline-20260806-104015.zip` | `fb409903ac421a05b3fb2da48a7956f84bae1e5e68a969e7b79b92c390c2ccdf` | contém o APK instalado e dados do pacote |
| `CANBOX_RUNTIME_CAPTURE_2026-08-06_1201.zip` | `308177150441e123b9001cd2d4ae9e4112543f01c0e16d1ffc2444c3a65fe567` | evidencia comportamento de runtime posterior |
| `logcat_0.log` | `721ca35ebcfb544695abe09400a274b771b44a5d730f85b9e674fb9898146139` | runtime Car Info/Jancar |
| `candata_8.log` | `f52d1a7dfd936208208ecbfdc79e58a799a2f0fcfb8f2903ffa100dcd8e16211` | tráfego `5A A5` com mudanças de payload |

## 3. Prova de qual APK estava instalado

Dentro da baseline existe:

`CarInfo/CarInfo-atualmente-instalado.apk`

SHA-256 observado:

`d0741a541fc575d3b25bc853a171532b815e8c396451dcc9ebe0f678d1905a50`

Esse valor é **idêntico** ao SHA-256 de:

`INSTALAR-v3854-CarInfo-HVAC-Visual-V1.apk`

A baseline também registra:

- package: `com.can.activity`;
- `versionCode=3854`;
- `versionName=1.0.3853.2026-06-17-09-33.060a51b6e`;
- UID efetivo `1000`;
- shared user `android.uid.system/1000`;
- processo `com.can.activity` dentro do contexto de sistema;
- assinatura reportada pelo Package Manager como identificador `[b1a1812f]`;
- caminho instalado naquele momento em `/data/app/.../com.can.activity-.../base.apk`.

### Classificação

**CONFIRMADO:** a v3854 anexada é byte a byte o APK que a baseline registrou como instalado.

Isso não prova, sozinho, que toda instalação futura será compatível nem revela a chave privada usada para assinatura.

## 4. Manifesto: original x v3854

A comparação do manifesto decodificado encontrou uma mudança material explícita:

- original: `versionCode="3853"`;
- v3854: `versionCode="3854"`.

Nos campos inspecionados, permanecem iguais:

- package `com.can.activity`;
- `android:sharedUserId="android.uid.system"`;
- `minSdkVersion=24`;
- `targetSdkVersion=27`;
- aplicação `com.autoai.platforms.CanApp`;
- `android:persistent="true"`;
- conjunto de Activities/Service/Receiver/Providers observado;
- permissões privilegiadas observadas.

### Privilégios relevantes observados

O manifesto inclui, entre outras:

- `SYSTEM_ALERT_WINDOW`;
- `CHANGE_COMPONENT_ENABLED_STATE`;
- `SYSTEM_OVERLAY_WINDOW`;
- `INSTALL_PACKAGES`;
- `REBOOT`;
- `READ_LOGS`;
- `WRITE_SETTINGS`;
- `DEVICE_POWER`;
- `MOUNT_UNMOUNT_FILESYSTEMS`;
- `RECEIVE_BOOT_COMPLETED`.

Isso demonstra que o Car Info foi desenhado para operar como componente privilegiado/persistente do sistema. Não demonstra que qualquer APK recompilado por nós herdará esses privilégios.

## 5. Componentes Android relevantes

### Activities observadas

- `com.can.ui.CanActivity`
- `com.can.ui.CanSource`
- `com.can.ui.CanPopActivity`
- `com.can.ui.CanInfoActivity`
- `com.can.ui.CanChoose`
- `com.can.ui.CanSyncOnStarActivity`
- `com.can.ui.CarMediaActivity` — `enabled=false`
- `com.can.ui.HvacActivity` — `enabled=false` no manifesto estático
- `com.can.ui.WheelKeyStudyActivity` — exportada
- `com.can.ui.EmptyActivity` — exportada
- `com.autoai.canbus.trumpchi.ui.ScreensaverActivity` — exportada

`HvacActivity` estar `enabled=false` no manifesto estático é um fato. A hipótese de habilitação dinâmica conforme configuração do veículo ainda precisa ser provada.

### Serviço central observado

`com.can.ui.CanPopWind`

Intent actions declaradas incluem:

- `autoai.intent.action.CANBUS_SERVICE`;
- `yecon.intent.CanService`;
- `com.jancar.canservice`.

### Receiver observado

`com.autoai.platforms.BootCompletedReceiver`

Escuta, entre outros:

- `BOOT_COMPLETED`;
- `com.jancar.services.ready`;
- `com.jancar.avm360.ready`.

Isso sustenta uma dependência explícita da inicialização Jancar, mas ainda não mapeia o transporte físico até a CANBOX.

## 6. Diferenças significativas no HVAC visual

Os dois APKs possuem 20 DEX. A comparação bruta de ZIP/DEX gera milhares de diferenças por reempacotamento e alteração de IDs de recursos; portanto, ela não foi usada como prova de mudança funcional.

Na árvore decodificada com nomes HVAC, a v3854 acrescenta três recursos:

- `res/drawable/canbox_hvac_bg_main.xml`;
- `res/drawable/canbox_hvac_bg_panel.xml`;
- `res/drawable/canbox_hvac_pop_bg_main.xml`.

Arquivos HVAC de mesmo caminho com alteração observada:

- `res/color/hvac_setup_selector_btn_text_color.xml`;
- `res/color/hvac_v1_setup_selector_btn_text_color.xml`;
- `res/drawable-1280x720/hover_hvac.png`;
- `res/drawable-mdpi/hover_hvac.png`;
- `res/layout/hvac_pop_window.xml`;
- `res/layout/hvac_setup_fragment_hvac.xml`.

Os PNGs `hover_hvac` decodificados não apresentaram diferença de pixels na comparação; a diferença é de representação do arquivo.

### Mudanças de layout observadas

`hvac_setup_fragment_hvac.xml`:

- fundo principal passa para `@drawable/canbox_hvac_bg_main`;
- adiciona `padding=16dp`;
- barra de status usa `canbox_hvac_bg_panel`;
- área inferior de ações usa `canbox_hvac_bg_panel`.

`hvac_pop_window.xml`:

- popup passa a usar `canbox_hvac_pop_bg_main`;
- margens do painel superior passam de 10dp para 16dp.

Cores do seletor foram ajustadas, incluindo destaque azulado para estados pressionado/selecionado/checked.

### Classificação

**FORTEMENTE SUSTENTADO para a superfície inspecionada:** a v3854 concentra a mudança observável do HVAC em recursos visuais, não em uma nova arquitetura de controle.

Não se declara que todo o código dos 20 DEX é idêntico; isso não foi provado.

## 7. Núcleo HVAC estático inspecionado

Três classes centrais foram decompiladas e comparadas entre `CARINFO.apk` e v3854. O texto decompilado foi idêntico nas três:

- `com.can.ui.HvacActivity`;
- `com.autoai.canbus.ui.hvac.fragment.HvacFragment`;
- `com.autoai.canbus.ui.hvac.mvvm.HvacModel`.

### Cadeia estática observada

`HvacActivity`

→ carrega `R.layout.hvac_setup_activity`

→ `HvacFragment`

→ `HvacViewModel` / `HvacModel`

→ `CanBusManager`

→ bind explícito em `com.can.activity/com.can.ui.CanPopWind`

→ `ICanUI.Stub.asInterface(...)`

→ `getCanService("CanBusManager")`

→ interface `ICanBus`

→ operações de alto nível como `getHvacInfo()`, `getPropertyList("hvac")` e `setHvacProperty(...)`.

### O que o fragmento faz

O `HvacFragment` observado:

- recebe configuração de propriedades HVAC;
- observa `HvacInfo`;
- atualiza temperatura, fan e modos a partir do estado recebido;
- usa `CarPropertyValue` para enviar mudanças;
- encaminha propriedades de power, temperatura, fan, modo automático e posição do ar ao ViewModel/Model.

### Impacto prático

A UI original já possui uma separação útil entre **controle visual** e uma **API de propriedades HVAC**. Isso é uma pista arquitetural forte, mas a F1 não escolhe ainda como a nova UI será construída. A decisão arquitetural continua reservada para depois das Fases 2–4.

## 8. Runtime Car Info/Jancar

O `logcat_0.log` registra em runtime:

- `CanPopWind.onReceive(...)`;
- `JancarRx.checkDuplicateData(...)` recebendo dados `5A A5 ...`;
- `Carinfo.sendSpeedAndRotation2Launcher(...)`;
- `CustomSettingFragment.sendData(...)`;
- configuração `Hiworld-Peugeot-208-2023~Present（Brazil）-All`.

Isso liga, em runtime, o processo Car Info a componentes Jancar e à configuração Hiworld observada.

### Tráfego

Os logs `candata_*` confirmam enquadramento recorrente `5A A5` e repetem o identificador ASCII:

`H1H2PAF23A-240409`

Em `candata_8.log`, mensagens com identificador `0x31` mudam de payload durante a captura, por exemplo entre estados que contêm sequências como:

- `45 10 00 01 06 04 ...`;
- `45 10 10 01 0b 07 ...`;
- `45 10 30 01 0b 07 ...`;
- `45 00 20 01 06 04 ...`;
- `45 00 00 01 06 04 ...`.

**Não foi provado na F1 que `0x31` corresponde a uma função HVAC específica.** Essa correlação pertence às Fases 2–3.

## 9. Instabilidade observada na captura posterior

A captura runtime de 12:01 registra o pacote atual apontando para o caminho instalado da v3854, coerente com a baseline.

Entretanto, durante a inicialização do processo, o Android tenta repetidamente abrir outro caminho antigo de `base.apk`, inexistente naquele momento.

O log mostra em sequência:

1. tentativa de iniciar `com.can.activity`;
2. falha de `ziparchive`/ResourcesManager ao abrir o `base.apk` antigo;
3. falha fatal durante o bind do processo;
4. morte do processo;
5. `ActivityManager` agendando reinício de `com.can.activity/com.can.ui.CanPopWind` por ser persistente;
6. repetição do ciclo.

### Classificação

**CONFIRMADO:** existe um crash/restart loop de `com.can.activity` nessa captura e o processo tenta resolver um caminho antigo de APK inexistente.

**NÃO CONFIRMADO:** a causa raiz.

Hipótese de trabalho, ainda não promovida a fato: a substituição/atualização de um aplicativo persistente com UID de sistema pode ter deixado metadados/processo em memória referenciando o `sourceDir` anterior até uma reinicialização adequada. Isso precisa de teste controlado em fase compatível antes de virar regra.

## 10. Mapa F1 consolidado

```text
HvacActivity
    │
    ▼
Layouts/recursos HVAC
    │
    ▼
HvacFragment
    │
    ▼
HvacViewModel / HvacModel
    │
    ▼
CanBusManager
    │
    ├── getHvacInfo()
    ├── getPropertyList("hvac")
    └── setHvacProperty(CarPropertyValue)
    │
    ▼
CanPopWind (serviço explícito do com.can.activity)
    │
    ▼
ICanUI / ICanBus (Binder)
    │
    ▼
[backend Jancar/Hiworld ainda a mapear]
    │
    ▼
tráfego observado 5A A5
    │
    ▼
H1H2PAF23A-240409 / veículo
```

A ligação final entre cada `HvacPropId` e mensagem física específica ainda está aberta.

## 11. Matriz de confiança

| Afirmação | Estado |
|---|---|
| `com.can.activity` é o Car Info analisado | CONFIRMADO |
| v3854 anexada é o APK presente na baseline | CONFIRMADO por SHA-256 |
| v3854 mantém package/shared UID e componentes manifestos inspecionados | CONFIRMADO |
| manifesto original → v3854 muda `versionCode` 3853 → 3854 | CONFIRMADO |
| classes `HvacActivity`, `HvacFragment`, `HvacModel` inspecionadas têm código decompilado idêntico | CONFIRMADO |
| mudanças HVAC localizadas incluem layouts/cores/drawables | CONFIRMADO |
| UI chega a `CanPopWind`/Binder por `CanBusManager` | CONFIRMADO estaticamente |
| runtime usa componentes Jancar e enquadramento `5A A5` | CONFIRMADO |
| `0x31` é especificamente HVAC | NÃO PROVADO |
| cada botão HVAC já está ligado a um frame físico conhecido | NÃO PROVADO |
| `HvacActivity` é habilitada dinamicamente conforme veículo | HIPÓTESE |
| causa do crash loop após troca de caminho do APK | NÃO PROVADA |
| nova UI pode ser instalada com privilégios de sistema usando qualquer assinatura | NÃO PROVADO |

## 12. Perguntas prioritárias para F2/F3

1. Qual mecanismo efetivamente habilita/abre `HvacActivity` e/ou o popup HVAC para esta configuração Peugeot/Hiworld?
2. Para cada `HvacPropId` usado pelo `HvacFragment`, qual caminho exato segue dentro do serviço até a mensagem enviada?
3. Qual retorno atualiza `HvacInfo` depois de uma alteração e como é correlacionado temporalmente com a ação?
4. Quais mensagens `5A A5` pertencem de fato ao HVAC e qual é o significado de cada byte necessário?
5. O crash loop é consequência direta do procedimento de substituição do APK persistente ou de outro estado do sistema? Qual sequência de instalação/restart é segura e reproduzível?

## 13. Gate F1

A F1 entrega:

- identificação original/v3854;
- versões e identidade do APK instalado;
- manifesto, privilégios e componentes relevantes;
- diferenças visuais significativas;
- cadeia estática principal da UI até Binder/CanPopWind;
- cruzamento com baseline e runtime;
- risco de runtime explicitamente registrado;
- lacunas e perguntas prioritárias sem converter hipótese em fato.

**Resultado técnico proposto: PASS para F1.**

Isso não significa que o controle físico HVAC já foi reconstruído. Significa que existe um mapa verificável suficiente para iniciar a F2 sem desmontagem aleatória nem atuação no carro.
