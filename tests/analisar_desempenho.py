#!/usr/bin/env python3
"""
Análise do Desempenho (ADB) — Frente A do TCC
=============================================

Lê as medições de desempenho coletadas por `coletar_desempenho.sh` (ou
preenchidas manualmente) e calcula estatística descritiva (média, mediana,
desvio-padrão) por cliente × tarefa × métrica, comparando PWA e Móvel.

CSV de entrada (colunas):
    cliente,tarefa,repeticao,metrica,valor,unidade
- cliente : "PWA" ou "Móvel"
- tarefa  : "T1".."T4"
- metrica : tempo_resposta_ms | cpu_pct | ram_mb | fps | energia_mah
- valor   : número

Uso:
    python tests/analisar_desempenho.py --entrada tests/desempenho.csv \
        --relatorio-json tests/saidas/desempenho_resumo.json
"""
import argparse
import csv
import json
import os
import statistics
from collections import defaultdict

CLIENTES = ["PWA", "Móvel"]

# Metadados das métricas: unidade e direção (menor ou maior é melhor).
METRICAS = {
    "tempo_resposta_ms": {"unidade": "ms", "direcao": "menor_melhor", "rotulo": "Tempo de resposta"},
    "cpu_pct":           {"unidade": "%",  "direcao": "menor_melhor", "rotulo": "Uso de CPU"},
    "ram_mb":            {"unidade": "MB", "direcao": "menor_melhor", "rotulo": "Memória (RAM)"},
    "fps":               {"unidade": "fps","direcao": "maior_melhor", "rotulo": "Taxa de quadros"},
    "energia_mah":       {"unidade": "mAh","direcao": "menor_melhor", "rotulo": "Energia estimada"},
}


def _norm_cliente(v: str) -> str:
    v = (v or "").strip().lower()
    if v.startswith("pwa") or v.startswith("web"):
        return "PWA"
    if v.startswith("mó") or v.startswith("mo") or v.startswith("app") or v.startswith("mobile"):
        return "Móvel"
    return v


def _stats(vals):
    return {
        "n": len(vals),
        "media": round(statistics.mean(vals), 2) if vals else None,
        "mediana": round(statistics.median(vals), 2) if vals else None,
        "dp": round(statistics.stdev(vals), 2) if len(vals) > 1 else 0.0,
    }


def main():
    p = argparse.ArgumentParser(description="Análise de desempenho ADB (Frente A).")
    p.add_argument("--entrada", required=True, help="CSV de medições.")
    p.add_argument("--relatorio-json", default=None, help="(Opcional) resumo JSON para gráficos.")
    p.add_argument("--natureza", default="real", choices=["real", "sintético"],
                   help="Marca a origem dos dados (rotula o gráfico quando sintético).")
    args = p.parse_args()

    if not os.path.exists(args.entrada):
        print(f"[!] Arquivo não encontrado: {args.entrada}")
        print("    Colete as medições com tests/coletar_desempenho.sh (ou preencha")
        print("    tests/desempenho_modelo.csv) e rode novamente.")
        raise SystemExit(1)

    # dados[metrica][tarefa][cliente] = [valores]
    dados = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    with open(args.entrada, encoding="utf-8") as f:
        for l in csv.DictReader(f):
            try:
                valor = float(str(l["valor"]).replace(",", "."))
            except (ValueError, KeyError, TypeError):
                continue
            metrica = (l.get("metrica") or "").strip()
            tarefa = (l.get("tarefa") or "").strip()
            cliente = _norm_cliente(l.get("cliente", ""))
            if metrica not in METRICAS or cliente not in CLIENTES:
                continue
            dados[metrica][tarefa][cliente].append(valor)

    print("=" * 72)
    print("ANÁLISE DE DESEMPENHO (ADB) — Frente A")
    print("=" * 72)

    resumo_metricas = {}
    for metrica, meta in METRICAS.items():
        if metrica not in dados:
            continue
        seta = "↓ menor é melhor" if meta["direcao"] == "menor_melhor" else "↑ maior é melhor"
        print(f"\n{meta['rotulo']} ({meta['unidade']}) — {seta}")
        print(f"  {'Tarefa':<8}{'PWA (méd±dp)':>20}{'Móvel (méd±dp)':>20}{'Δ%':>10}")
        por_tarefa = {}
        for tarefa in sorted(dados[metrica]):
            spwa = _stats(dados[metrica][tarefa].get("PWA", []))
            smov = _stats(dados[metrica][tarefa].get("Móvel", []))
            delta = ""
            if spwa["media"] not in (None, 0) and smov["media"] is not None:
                d = (smov["media"] - spwa["media"]) / spwa["media"] * 100
                delta = f"{d:+.0f}%"
            pwa_s = f"{spwa['media']}±{spwa['dp']}" if spwa["media"] is not None else "—"
            mov_s = f"{smov['media']}±{smov['dp']}" if smov["media"] is not None else "—"
            print(f"  {tarefa:<8}{pwa_s:>20}{mov_s:>20}{delta:>10}")
            por_tarefa[tarefa] = {"PWA": spwa, "Móvel": smov}
        resumo_metricas[metrica] = {
            "unidade": meta["unidade"], "direcao": meta["direcao"],
            "rotulo": meta["rotulo"], "por_tarefa": por_tarefa,
        }

    resumo = {"frente": "A — Desempenho (ADB)", "natureza": args.natureza,
              "clientes": CLIENTES, "metricas": resumo_metricas}
    if args.relatorio_json:
        os.makedirs(os.path.dirname(os.path.abspath(args.relatorio_json)), exist_ok=True)
        with open(args.relatorio_json, "w", encoding="utf-8") as f:
            json.dump(resumo, f, ensure_ascii=False, indent=2)
        print(f"\nResumo (JSON) salvo em: {args.relatorio_json}")


if __name__ == "__main__":
    main()
