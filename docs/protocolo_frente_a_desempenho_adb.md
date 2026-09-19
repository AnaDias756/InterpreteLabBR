# Protocolo de Coleta — Frente A: Desempenho Comparativo (ADB)

**Projeto:** InterpreteLabBR — Migração PWA → Aplicativo Móvel
**Método:** Experimentação controlada com Android Debug Bridge (ADB)
**Objetivo:** Comparar o desempenho do cliente **PWA** (executado no navegador)
e do cliente **móvel** (React Native/Expo, renderização nativa) sobre as mesmas
tarefas, no **mesmo dispositivo**, quantificando tempo de resposta, uso de CPU,
memória, taxa de quadros (FPS) e consumo energético estimado.

> Protocolo inspirado em Oliveira et al. (2023) sobre *overhead* de recursos em
> *frameworks* móveis. Todas as medições usam ferramentas gratuitas (ADB e
> `dumpsys`), garantindo reprodutibilidade.

---

## 1. Materiais

| Item | Especificação |
|---|---|
| Dispositivo | `[modelo Android de entrada — ex.: Motorola Moto G, Android XX]` |
| Cliente PWA | `[URL do PWA]`, executado no Chrome `[versão]` |
| Cliente Móvel | APK release do app (`eas build`) — `[versão]` |
| Backend | Mesmo serviço FastAPI para ambos (`[URL]`) |
| Rede | Mesma rede Wi-Fi para todas as execuções (`[SSID/faixa]`) |
| Host | PC com ADB (`platform-tools [versão]`) conectado via USB |

> **Justificativa do dispositivo único:** elimina a heterogeneidade de
> *hardware* entre execuções; o custo é restringir a generalização das métricas
> absolutas a esse perfil de aparelho (ver Metodologia, Seção de validade).

---

## 2. Tarefas (idênticas nos dois clientes)

| ID | Tarefa | Métricas principais |
|----|--------|---------------------|
| **T1** | Inicialização (*cold start*) até a tela pronta | tempo (ms), RAM |
| **T2** | Submissão de um laudo em PDF e retorno do resultado | tempo (ms), CPU, RAM |
| **T3** | Rolagem da listagem de analitos/resultados | **FPS**, CPU, energia |
| **T4** | Renderização da tabela de comparação de referências | tempo (ms), CPU |

- Use o **laudo sintético** do projeto (`generate_sample_pdf.py`) em T2 — sem
  dados pessoais.
- **10 execuções por tarefa e por cliente** (Oliveira et al., 2023), alternando
  os clientes entre execuções para diluir efeitos térmicos e de processos
  concorrentes.

---

## 3. Controles experimentais (antes de cada execução)

1. Fechar apps em segundo plano; ativar **Modo avião + Wi-Fi** (só a rede do teste).
2. Brilho fixo, sem rotação automática, sem economia de bateria.
3. Bateria entre 40–90% (evita *throttling* térmico e limites de energia).
4. Aguardar o dispositivo esfriar entre blocos (evitar *thermal throttling*).
5. Para *cold start*: encerrar o app/aba e limpar da memória antes de medir.

---

## 4. Comandos ADB de coleta

> Substitua `PKG_APP` pelo pacote do app (ex.: `com.anadias.interpretelabbr`) e
> `PKG_PWA` pelo pacote do navegador/PWA (Chrome: `com.android.chrome`; PWA
> instalada como WebAPK tem pacote próprio `org.chromium.webapk.*`).

**Tempo de inicialização (app nativo, cold start):**
```bash
adb shell am force-stop PKG_APP
adb shell am start -W -n PKG_APP/.MainActivity   # usa TotalTime/WaitTime (ms)
```
Para o **PWA**, o `am start -W` não reflete o tempo até interativo; meça via
`performance.timing`/`PerformanceNavigationTiming` no console do Chrome
(`chrome://inspect`) ou via Lighthouse (*Time to Interactive*). Registre a
assimetria no relatório.

**CPU (amostra durante a tarefa):**
```bash
adb shell top -b -n 1 | grep -i PKG_APP        # coluna %CPU
# alternativa acumulada:
adb shell dumpsys cpuinfo | grep -i PKG_APP
```

**Memória (PSS total, em MB):**
```bash
adb shell dumpsys meminfo PKG_APP | grep -i "TOTAL PSS"
```

**FPS / jank (rolagem — T3):**
```bash
adb shell dumpsys gfxinfo PKG_APP reset          # zera antes da rolagem
# ... executar a rolagem por ~10 s ...
adb shell dumpsys gfxinfo PKG_APP | grep -E "Total frames|Janky frames|50th|90th|95th|99th"
```
FPS aproximado = frames renderizados / duração da coleta; reporte também a
**porcentagem de *janky frames*** (quadros com atraso).

**Energia estimada (bateria):**
```bash
adb shell dumpsys batterystats --reset
# ... executar a tarefa ...
adb shell dumpsys batterystats --charged PKG_APP | grep -iE "Estimated power|Computed drain"
```

---

## 5. Formato de registro dos dados

Preencha `tests/desempenho_modelo.csv` (uma linha por medição):

```
cliente,tarefa,repeticao,metrica,valor,unidade
Móvel,T1,1,tempo_resposta_ms,842,ms
Móvel,T1,1,ram_mb,131,MB
PWA,T1,1,tempo_resposta_ms,2380,ms
...
```

- `cliente`: `PWA` ou `Móvel`
- `tarefa`: `T1`–`T4`
- `metrica`: `tempo_resposta_ms`, `cpu_pct`, `ram_mb`, `fps`, `energia_mah`
- `repeticao`: 1–10

O script `tests/analisar_desempenho.py` calcula média, mediana e desvio-padrão
por (cliente × tarefa × métrica) e gera as figuras comparativas.

---

## 6. Análise

```bash
python tests/analisar_desempenho.py --entrada tests/desempenho.csv \
    --relatorio-json tests/saidas/desempenho_resumo.json
python tests/gerar_graficos.py     # inclui as figuras da Frente A (ADB)
```

**Tabela-síntese a preencher no capítulo de Resultados** (média ± desvio-padrão):

| Métrica | PWA | Móvel | Δ |
|---|---|---|---|
| Tempo de inicialização (ms) | `[PENDENTE]` | `[PENDENTE]` | |
| CPU em rolagem (%) | `[PENDENTE]` | `[PENDENTE]` | |
| RAM (MB) | `[PENDENTE]` | `[PENDENTE]` | |
| FPS em rolagem | `[PENDENTE]` | `[PENDENTE]` | |
| Energia estimada (mAh) | `[PENDENTE]` | `[PENDENTE]` | |

> **Direção das métricas:** menor é melhor para tempo, CPU, RAM e energia; maior
> é melhor para FPS. **Não** combine métricas de escalas/direções diferentes em
> um mesmo eixo — cada métrica tem seu próprio gráfico.

---

## 7. Ameaças à validade (a reportar)

- **Assimetria de medição PWA × nativo:** o *cold start* e o FPS são medidos por
  mecanismos distintos em cada cliente; descreva o método usado em cada caso.
- **Dispositivo único e 10 repetições:** limita a generalização das métricas
  absolutas; os resultados relativos (sentido e magnitude aproximada da
  diferença) são o objeto de interesse.
- ***Thermal throttling*** e processos de fundo do Android: mitigados pelos
  controles da Seção 3 e pela execução alternada entre clientes.

---

## 8. Referências

- OLIVEIRA, W. et al. `[completar]` — *overhead* de recursos em *frameworks* de
  desenvolvimento móvel, 2023. `[confirmar no padrão ABNT/SBC]`
- Documentação do Android Debug Bridge (ADB) e `dumpsys` (Android Open Source
  Project). `[confirmar formato de citação]`
