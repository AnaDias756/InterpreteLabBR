#!/usr/bin/env python3
"""
Consolidação da Inspeção Heurística — Frente C do TCC
=====================================================

Consolida os formulários de inspeção heurística (um por avaliador, unificados
em um único CSV) e calcula as métricas comparativas entre os clientes PWA e
Móvel, alimentando o capítulo de Resultados.

CSV de entrada (colunas):
    avaliador,cliente,cenario,tela,heuristica,severidade,descricao,recomendacao
- `cliente`   : "PWA" ou "Móvel"
- `heuristica`: H1..H10
- `severidade`: inteiro 0–4 (Nielsen). Linhas com severidade 0 são ignoradas
                (não constituem problema de usabilidade).

Métricas geradas por cliente:
  - número de problemas registrados;
  - índice médio de severidade;
  - nº de problemas de severidade alta (3–4);
  - distribuição de problemas por heurística;
  - taxa de detecção por avaliador (nº de problemas por avaliador).

Uso:
    python tests/consolidar_inspecao.py --entrada tests/inspecao_heuristica.csv \
        --relatorio-json tests/saidas/inspecao_resumo.json

PRIVACIDADE: use identificadores anonimizados de avaliador (A1..A5).
"""
import argparse
import csv
import json
import os
import statistics
from collections import defaultdict

HEURISTICAS = [f"H{i}" for i in range(1, 11)]
CLIENTES = ["PWA", "Móvel"]


def _norm_cliente(v: str) -> str:
    v = (v or "").strip().lower()
    if v.startswith("pwa") or v.startswith("web"):
        return "PWA"
    if v.startswith("mó") or v.startswith("mo") or v.startswith("app") or v.startswith("mobile"):
        return "Móvel"
    return v


def main():
    p = argparse.ArgumentParser(description="Consolidação da inspeção heurística (Frente C).")
    p.add_argument("--entrada", required=True, help="CSV unificado dos avaliadores.")
    p.add_argument("--relatorio-json", default=None, help="(Opcional) resumo JSON para gráficos.")
    args = p.parse_args()

    if not os.path.exists(args.entrada):
        print(f"[!] Arquivo não encontrado: {args.entrada}")
        print("    Preencha tests/inspecao_heuristica_modelo.csv com os registros")
        print("    dos 5 avaliadores e rode novamente.")
        raise SystemExit(1)

    with open(args.entrada, encoding="utf-8") as f:
        linhas = [l for l in csv.DictReader(f)]

    # Estruturas de agregação
    por_cliente = {c: {"n": 0, "sev": [], "alta": 0} for c in CLIENTES}
    por_heur = {c: defaultdict(int) for c in CLIENTES}
    por_avaliador = defaultdict(lambda: defaultdict(int))  # avaliador -> cliente -> n

    for l in linhas:
        try:
            sev = int(str(l.get("severidade", "")).strip())
        except (ValueError, TypeError):
            continue
        if sev <= 0:
            continue  # 0 = não é problema
        cliente = _norm_cliente(l.get("cliente", ""))
        if cliente not in CLIENTES:
            continue
        heur = (l.get("heuristica", "") or "").strip().upper()
        por_cliente[cliente]["n"] += 1
        por_cliente[cliente]["sev"].append(sev)
        if sev >= 3:
            por_cliente[cliente]["alta"] += 1
        if heur in HEURISTICAS:
            por_heur[cliente][heur] += 1
        por_avaliador[(l.get("avaliador", "") or "?").strip()][cliente] += 1

    print("=" * 62)
    print("CONSOLIDAÇÃO DA INSPEÇÃO HEURÍSTICA — Frente C")
    print("=" * 62)
    print(f"{'Métrica':<34}{'PWA':>12}{'Móvel':>12}")
    print("-" * 62)

    def media(c):
        s = por_cliente[c]["sev"]
        return statistics.mean(s) if s else 0.0

    print(f"{'Problemas registrados':<34}"
          f"{por_cliente['PWA']['n']:>12}{por_cliente['Móvel']['n']:>12}")
    print(f"{'Índice médio de severidade':<34}"
          f"{media('PWA'):>12.2f}{media('Móvel'):>12.2f}")
    print(f"{'Problemas de severidade 3–4':<34}"
          f"{por_cliente['PWA']['alta']:>12}{por_cliente['Móvel']['alta']:>12}")

    print("\nDistribuição por heurística (PWA / Móvel):")
    for h in HEURISTICAS:
        print(f"  {h:<4} {por_heur['PWA'][h]:>3}  /  {por_heur['Móvel'][h]:>3}")

    print("\nProblemas por avaliador:")
    for a in sorted(por_avaliador):
        d = por_avaliador[a]
        print(f"  {a:<6} PWA={d.get('PWA', 0):>2}  Móvel={d.get('Móvel', 0):>2}")

    resumo = {
        "frente": "C — Usabilidade (inspeção heurística)",
        "clientes": CLIENTES,
        "por_cliente": {c: {
            "problemas": por_cliente[c]["n"],
            "severidade_media": round(media(c), 2),
            "severidade_alta_3_4": por_cliente[c]["alta"],
        } for c in CLIENTES},
        "por_heuristica": {c: {h: por_heur[c][h] for h in HEURISTICAS} for c in CLIENTES},
        "n_avaliadores": len(por_avaliador),
    }
    if args.relatorio_json:
        os.makedirs(os.path.dirname(os.path.abspath(args.relatorio_json)), exist_ok=True)
        with open(args.relatorio_json, "w", encoding="utf-8") as f:
            json.dump(resumo, f, ensure_ascii=False, indent=2)
        print(f"\nResumo (JSON) salvo em: {args.relatorio_json}")


if __name__ == "__main__":
    main()
