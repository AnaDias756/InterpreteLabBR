#!/usr/bin/env bash
# =====================================================================
# Coletor de Desempenho via ADB — Frente A do TCC
# ---------------------------------------------------------------------
# Auxilia a coleta das métricas de desempenho (tempo, CPU, RAM, FPS,
# energia) de um cliente instalado, gravando em CSV no formato esperado
# por analisar_desempenho.py.
#
# REQUER: um dispositivo Android conectado via USB com depuração ativada
# (adb devices deve listá-lo). Este script NÃO roda sem um aparelho.
#
# Uso:
#   ./tests/coletar_desempenho.sh <PKG> <cliente> <tarefa> <repeticao> [saida.csv]
# Exemplos:
#   ./tests/coletar_desempenho.sh com.anadias.interpretelabbr Móvel T2 1 tests/desempenho.csv
#   ./tests/coletar_desempenho.sh com.android.chrome PWA T3 1 tests/desempenho.csv
#
# As métricas coletadas dependem da tarefa (T1..T4). Para FPS (T3), role a
# tela DURANTE a janela de coleta quando solicitado.
# =====================================================================
set -euo pipefail

PKG="${1:?informe o pacote (ex.: com.anadias.interpretelabbr)}"
CLIENTE="${2:?informe o cliente (PWA|Móvel)}"
TAREFA="${3:?informe a tarefa (T1..T4)}"
REP="${4:?informe a repetição (1..10)}"
SAIDA="${5:-tests/desempenho.csv}"

if ! command -v adb >/dev/null 2>&1; then
  echo "[!] adb não encontrado no PATH. Instale o Android platform-tools." >&2
  exit 1
fi
if [ -z "$(adb devices | sed '1d' | grep -w device || true)" ]; then
  echo "[!] Nenhum dispositivo conectado/autorizado (verifique 'adb devices')." >&2
  exit 1
fi

mkdir -p "$(dirname "$SAIDA")"
if [ ! -f "$SAIDA" ]; then
  echo "cliente,tarefa,repeticao,metrica,valor,unidade" > "$SAIDA"
fi

registrar() { # metrica valor unidade
  echo "${CLIENTE},${TAREFA},${REP},${1},${2},${3}" >> "$SAIDA"
  echo "  -> ${1}=${2} ${3}"
}

echo "== Coleta ${CLIENTE} / ${TAREFA} / rep ${REP} (pkg=${PKG}) =="

medir_tempo_cold_start() {
  # Apenas app nativo: am start -W devolve TotalTime (ms).
  adb shell am force-stop "$PKG" || true
  sleep 1
  local out total
  out="$(adb shell am start -W -n "${PKG}/.MainActivity" 2>/dev/null || true)"
  total="$(echo "$out" | awk -F': ' '/TotalTime/{print $2}')"
  if [ -n "${total:-}" ]; then
    registrar tempo_resposta_ms "$total" ms
  else
    echo "  [i] TotalTime indisponível (PWA?). Meça o cold start via Lighthouse/Performance API e registre manualmente."
  fi
}

medir_cpu() {
  local cpu
  cpu="$(adb shell top -b -n 1 2>/dev/null | awk -v p="$PKG" 'tolower($0) ~ tolower(p){print $9; exit}')"
  [ -n "${cpu:-}" ] && registrar cpu_pct "${cpu}" pct || echo "  [i] CPU não capturada (app precisa estar em foreground)."
}

medir_ram() {
  local pss
  pss="$(adb shell dumpsys meminfo "$PKG" 2>/dev/null | awk '/TOTAL PSS/{print $3; exit} /TOTAL:/{print $2; exit}')"
  if [ -n "${pss:-}" ]; then
    # pss vem em KB
    registrar ram_mb "$(awk -v k="$pss" 'BEGIN{printf "%.1f", k/1024}')" MB
  else
    echo "  [i] RAM não capturada (app em execução?)."
  fi
}

medir_fps() {
  echo "  Rolagem: zerando gfxinfo; ROLE a tela por ~10s a partir de agora..."
  adb shell dumpsys gfxinfo "$PKG" reset >/dev/null 2>&1 || true
  sleep 10
  local total janky
  total="$(adb shell dumpsys gfxinfo "$PKG" 2>/dev/null | awk -F': ' '/Total frames rendered/{print $2; exit}')"
  janky="$(adb shell dumpsys gfxinfo "$PKG" 2>/dev/null | awk -F': ' '/Janky frames/{print $2; exit}')"
  if [ -n "${total:-}" ]; then
    registrar fps "$(awk -v t="$total" 'BEGIN{printf "%.1f", t/10.0}')" fps
    [ -n "${janky:-}" ] && echo "  [i] Janky frames: ${janky}"
  else
    echo "  [i] gfxinfo sem frames (a view usa aceleração de hardware?)."
  fi
}

medir_energia() {
  echo "  Energia: zerando batterystats; EXECUTE a tarefa por ~10s..."
  adb shell dumpsys batterystats --reset >/dev/null 2>&1 || true
  sleep 10
  local drain
  drain="$(adb shell dumpsys batterystats --charged "$PKG" 2>/dev/null | awk -F': ' '/Computed drain|Estimated power/{print $2; exit}')"
  [ -n "${drain:-}" ] && registrar energia_mah "${drain%% *}" mAh || echo "  [i] Estimativa de energia indisponível neste device/Android."
}

case "$TAREFA" in
  T1) medir_tempo_cold_start; medir_ram ;;
  T2) medir_cpu; medir_ram ;;   # meça o tempo de resposta pela própria UI/log
  T3) medir_fps; medir_cpu; medir_energia ;;
  T4) medir_cpu ;;
  *)  echo "[!] Tarefa desconhecida: $TAREFA" >&2; exit 1 ;;
esac

echo "Registros anexados em: $SAIDA"
