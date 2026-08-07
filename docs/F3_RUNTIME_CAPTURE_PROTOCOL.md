# F3 — Protocolo de captura controlada HVAC

## Objetivo

Executar, **somente quando houver autorização material para interação no equipamento real**, uma sessão que produza evidência suficiente para ligar:

`ação conhecida → timestamp → TX observado/ausente → RX 0x31 → estado retornado → latência → efeito físico`

Este documento prepara a coleta. Ele **não autoriza** tocar controles HVAC, transmitir frames manualmente, replayar CAN, instalar APK, alterar ROM/firmware ou modificar o veículo.

## 1. O mecanismo nativo de captura já está provado

O Car Info possui `DbgAssist` para a porta CANBOX/Hiworld.

### Como o overlay é habilitado internamente

- `CustomInfo.POPUP_DBG_ASSIST = 14`;
- `CustomInfo.ITEM_VALUES[14] = "dbg_assist"`;
- `CustomSettingFragment` inclui a propriedade 14 (`custom_str_popup_dbg_assist`);
- quando `CanPopWind.onCustomChanged(14, 1)` ocorre, ele:
  1. instancia `DbgAssist` para a porta principal;
  2. chama `registerDbgRxTx(mDbgAssist)`;
  3. chama `mDbgAssist.setVisibility(true)`.

Ao mostrar o overlay, `DbgAssist.show()` marca o toggle `start_stop` como ativo. RX e TX são `true` por padrão.

### O que entra no log

`DbgAssist.txData(...)` e `rxData(...)` usam `LogDataInfo`.

Cada entrada recebe o horário por:

`System.currentTimeMillis() → SimpleDateFormat("HH:mm:ss.SSS")`

Assim, o `candata` usa o relógio do próprio Android e resolução nominal de milissegundos.

### Como salvar

`DbgAssist.saveData2Files()` cria `ThSaveDataFiles`.

O diretório é:

`Environment.getExternalStorageDirectory()/canlog`

No equipamento observado isso corresponde a:

`/sdcard/canlog/`

O nome é:

`candata_<index>.log`

O formato de cada linha é:

`HH:mm:ss.SSS RX:[hex...]`

ou

`HH:mm:ss.SSS TX:[hex...]`

### Gesto de salvar

No overlay:

- **toque curto em Clear**: limpa a lista em memória;
- **toque longo em Clear**: salva a lista atual em `/sdcard/canlog/candata_<n>.log` e dispara `LogcatAssist.ACTION_START_UPLOAD_LOG`;
- toggle `start_stop`: habilita/desabilita a acumulação de RX/TX;
- toque longo em `start_stop`: fecha o overlay;
- checkboxes RX/TX: habilitam os respectivos sentidos;
- filtro padrão: `PROTOCOL`.

Para F3, manter **RX e TX habilitados** e não usar filtro que esconda comandos.

## 2. Preparação da sessão

Antes de qualquer ação HVAC real:

1. confirmar que o equipamento está em condição segura e estacionado;
2. confirmar que a sessão está autorizada para **uso da UI original do HVAC**; isso não inclui replay nem frame manual;
3. abrir o `DbgAssist` da porta principal pelo ajuste original `dbg_assist`/property 14;
4. confirmar RX=ON e TX=ON;
5. preferir filtro `PROTOCOL` ou `ALL` somente se a finalidade exigir; não usar `SELECTED` para a sessão principal;
6. tocar **Clear uma vez** para remover tráfego anterior;
7. iniciar captura de `logcat` em paralelo quando ADB estiver disponível;
8. aguardar alguns segundos sem tocar no HVAC para formar controle negativo/baseline.

## 3. Logcat paralelo via ADB

O runtime anterior comprova ADB ativo no equipamento, mas estes comandos devem ser executados no host apenas durante a sessão autorizada.

Exemplo de captura passiva:

```sh
adb logcat -c
adb logcat -v threadtime -b all > logcat_F3.txt
```

Parar ao final com `Ctrl+C`.

Antes de confiar em marcadores enviados pelo host, verificar se o binário `log` existe:

```sh
adb shell 'command -v log'
```

Se existir, cada ação pode receber um marcador imediatamente antes do toque:

```sh
adb shell log -t F3MARK 'ACTION=AC_ON'
```

O marcador é apenas uma linha de logcat; **não envia CAN**.

Se `log` não existir, não inventar substituto silencioso. Usar uma planilha/ledger de ação e preservar a incerteza de timestamp.

## 4. Matriz de ações — uma por vez

A execução real deve usar **somente controles originais**, nunca frames construídos manualmente.

Ordem sugerida para reduzir ambiguidade:

1. baseline sem ação;
2. HVAC power OFF → ON;
3. A/C OFF → ON;
4. fan + → fan -;
5. front defrost ON → OFF;
6. rear defrost ON → OFF;
7. recirculação alternar e retornar;
8. AUTO alternar e retornar;
9. SYNC alternar e retornar;
10. airflow/modo — uma mudança por vez;
11. temperatura esquerda + → -;
12. temperatura direita + → -.

Entre ações, deixar intervalo suficiente para o estado estabilizar e para evitar sobreposição na timeline. O intervalo exato deve ser registrado na sessão; não assumir causalidade apenas porque dois eventos ocorreram próximos.

## 5. Registro obrigatório por ação

Para cada ação, preencher:

| Campo | Conteúdo |
|---|---|
| ação | ex. `AC_ON` |
| hora/marcador | timestamp da ação ou marcador F3MARK |
| estado anterior | leitura física/UI imediatamente antes |
| TX observado | frame(s) TX dentro da janela, ou `AUSENTE` |
| classificação TX | `TX_OBSERVADO` / `AUSENTE` / `INDETERMINADO` |
| RX 0x31 | primeiro estado coerente posterior |
| proveniência RX | solicitada / não solicitada / indeterminada |
| latência | ação→TX, TX→RX e/ou ação→RX quando mensurável |
| efeito físico | o que realmente mudou no HVAC |
| repetição | número da repetição da mesma ação |
| confiança | confirmado / provável / inconclusivo |

Cada função importante deve ser repetida quando necessário para excluir coincidência temporal.

## 6. Encerramento e salvamento

Ao terminar as ações:

1. aguardar alguns segundos de baseline final;
2. usar **toque longo em Clear** no `DbgAssist` para salvar o `candata`;
3. parar o logcat do host;
4. listar os arquivos novos:

```sh
adb shell ls -lt /sdcard/canlog/
```

5. copiar de forma somente-leitura para o host:

```sh
adb pull /sdcard/canlog/ .
```

6. não apagar arquivos do equipamento durante a sessão de evidência;
7. calcular SHA-256 dos arquivos que entrarem no projeto;
8. analisar o novo `candata` com:

```sh
python scripts/analyze_hiword_candata.py candata_N.log
```

ou JSON:

```sh
python scripts/analyze_hiword_candata.py --json candata_N.log
```

## 7. Referência de regressão do analisador

Para o `candata_8.log` existente, `scripts/analyze_hiword_candata.py` deve continuar produzindo:

- 821 frames reconstruídos;
- 821 checksums válidos;
- 0 checksums inválidos;
- TX `0x3B` = 0;
- 8 eventos lógicos `RX 0x31`;
- 1 `RESPOSTA_SOLICITADA`;
- 7 `RX_NAO_SOLICITADO`.

`--self-test` deve retornar `SELF-TEST PASS`.

## 8. Critério para fechar F3

F3 não exige que todas as ações obrigatoriamente produzam `0x3B`; ela exige descobrir **o caminho real**.

Exemplos de resultados válidos:

- UI original → TX `0x3B` repetível → RX `0x31` → efeito físico;
- controle físico do carro → nenhum TX Android → RX `0x31` → efeito físico;
- UI original → nenhum TX `0x3B`, mas outro caminho repetível e identificado → RX/efeito;
- ausência de correlação suficiente → F3 permanece `INCONCLUSIVE/PARTIAL` e a próxima evidência discriminatória é explicitada.

O objetivo é provar o comportamento, não forçar a hipótese `0x3B` a ser verdadeira.
