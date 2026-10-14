# Runbook rápido — Coleta REAL da Frente A (ADB)

Objetivo: obter medições reais de desempenho **hoje**, para preencher a
Tabela da Frente A e a figura com dados verdadeiros (sem fabricar nada).

## 0. Pré-requisitos (cheque antes)

- [ ] Um **celular Android** com **Depuração USB** ativada (Opções do
      desenvolvedor) e cabo USB.
- [ ] Um **PC** com **ADB** instalado (`adb version` responde).
- [ ] O **app móvel** instalado no celular (via Expo Go, APK ou EAS build).
- [ ] A **PWA** acessível pelo Chrome do celular (ex.: a URL do Netlify).
- [ ] `adb devices` lista o aparelho como `device` (autorize no celular se pedir).

> Se faltar o app instalado ou o ADB, me avise: partimos para a entrega
> preliminar honesta (Frente B real + A/C pendentes) — também é defensável.

## 1. Descubra os "pacotes" (package names)

```bash
# App móvel (procure por "interpret" ou o nome do app):
adb shell pm list packages | grep -i -E "interpret|labbr|expo"
# PWA no Chrome:
#   PKG_PWA = com.android.chrome
```
Anote: `PKG_APP` (ex.: `com.anadias.interpretelabbr`) e `PKG_PWA=com.android.chrome`.

## 2. Métricas e comandos (rode para CADA cliente)

> Deixe o app/página EM PRIMEIRO PLANO e na tela certa antes de medir.
> Repita cada medição **10 vezes** (ou, se faltar tempo, **5** — e reporte o n real).

**RAM (MB) — T1/T2:**
```bash
adb shell dumpsys meminfo PKG | grep -i "TOTAL PSS"   # valor em KB; divida por 1024
```

**CPU (%) — T2/T3/T4:** (com a tarefa acontecendo)
```bash
adb shell top -b -n 1 | grep -i PKG      # coluna %CPU
```

**Inicialização (ms) — T1 (app nativo):**
```bash
adb shell am force-stop PKG_APP
adb shell am start -W -n PKG_APP/.MainActivity | grep TotalTime
```
Para a **PWA**, meça o tempo até a tela interativa com **gravação de tela**
(conte os segundos no vídeo) ou Lighthouse — e registre o método usado.

**FPS em rolagem — T3:**
```bash
adb shell dumpsys gfxinfo PKG reset
# role a tela por ~10 segundos agora
adb shell dumpsys gfxinfo PKG | grep -E "Total frames|Janky"
# FPS aprox = (Total frames) / 10
```

**Energia (mAh) — T3 [opcional, pode pular se faltar tempo]:**
```bash
adb shell dumpsys batterystats --reset
# execute a tarefa por ~10 s
adb shell dumpsys batterystats --charged PKG | grep -iE "Computed drain|Estimated power"
```

## 3. (Opção A) Use o coletor pronto, se tiver o repo no PC

```bash
# para cada cliente/tarefa/repetição:
./tests/coletar_desempenho.sh PKG_APP Móvel T1 1 tests/desempenho.csv
./tests/coletar_desempenho.sh com.android.chrome PWA T1 1 tests/desempenho.csv
# ... repita variando tarefa (T1..T4) e repetição (1..10) ...
python tests/analisar_desempenho.py --entrada tests/desempenho.csv \
    --relatorio-json tests/saidas/desempenho_resumo.json
```

## 4. (Opção B — mais simples) Só me mande os números

Anote numa tabelinha e **cole aqui no chat** (eu monto o CSV, calculo as
estatísticas, regenero a figura e preencho a tabela do LaTeX). Formato:

```
cliente, tarefa, metrica, valores (uma lista por repetição)
Móvel, T1, tempo_resposta_ms, 840, 910, 880, ...
PWA,   T1, tempo_resposta_ms, 2300, 2500, 2380, ...
Móvel, T1, ram_mb, 131, 128, 135, ...
PWA,   T1, ram_mb, 210, 205, 219, ...
Móvel, T3, cpu_pct, 38, 41, 36, ...
PWA,   T3, cpu_pct, 70, 66, 72, ...
Móvel, T3, fps, 58, 57, 59, ...
PWA,   T3, fps, 46, 48, 45, ...
```

> Prioridade se o tempo apertar: **RAM, CPU e FPS** (saem limpos pelo ADB nos
> dois clientes). Inicialização e energia são "bônus".

## 5. O que eu faço quando você me mandar os dados

1. Monto `tests/desempenho.csv` e rodo a análise (média, mediana, desvio).
2. Regenero a figura **sem** o aviso de "sintético".
3. Preencho a **Tabela da Frente A** no `InterpreteLabBR_monografia_etapa4.tex`
   com os valores reais e o Δ%.
4. Faço commit e te mando os arquivos atualizados.
