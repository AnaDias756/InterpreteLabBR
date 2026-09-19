#!/usr/bin/env python3
"""
Pontuação da Usabilidade (SUS) — Frente C do TCC
================================================

Calcula o escore da System Usability Scale (SUS; Brooke, 1996) a partir das
respostas dos participantes ao questionário de 10 itens (escala Likert 1–5).

Regra de pontuação (Brooke, 1996):
  - itens ÍMPARES (1,3,5,7,9): contribuição = (resposta − 1)
  - itens PARES  (2,4,6,8,10): contribuição = (5 − resposta)
  - escore individual = soma das 10 contribuições × 2,5   →  intervalo 0–100

Reporta, além do escore médio e do desvio-padrão, a classificação adjetiva de
Bangor et al. (2009) e a faixa aproximada de percentil (referência prática:
média ~68 = "OK"; ≥80,3 costuma corresponder a percentil > 90 / "A").

Uso:
    python tests/pontuacao_sus.py --respostas tests/respostas_sus_exemplo.csv
    python tests/pontuacao_sus.py --respostas tests/respostas_sus.csv \
        --relatorio-csv tests/saidas/sus_por_participante.csv \
        --resumo-json tests/saidas/sus_resumo.json

Formato do CSV de respostas (uma linha por participante):
    participante,q1,q2,q3,q4,q5,q6,q7,q8,q9,q10
    P01,4,2,5,1,4,2,5,1,4,2
    ...
Cada q* é um inteiro de 1 (Discordo totalmente) a 5 (Concordo totalmente).

PRIVACIDADE/LGPD: use identificadores anonimizados (P01, P02, ...). Não inclua
nome, e-mail ou qualquer dado pessoal do participante.
"""
import argparse
import csv
import json
import os
import statistics

ITENS = [f"q{i}" for i in range(1, 11)]
IMPARES = {1, 3, 5, 7, 9}


def classificacao_adjetiva(score: float) -> str:
    """Escala adjetiva de Bangor et al. (2009)."""
    if score >= 90:
        return "Melhor imaginável"
    if score >= 80.3:
        return "Excelente"
    if score >= 68:
        return "Bom"
    if score >= 51:
        return "OK / Aceitável (limítrofe)"
    return "Pobre"


def faixa_percentil(score: float) -> str:
    """Faixa aproximada de percentil / nota (referência prática de mercado)."""
    if score >= 80.3:
        return "A (percentil ~90+)"
    if score >= 74:
        return "B (percentil ~70–89)"
    if score >= 68:
        return "C (percentil ~50–69) — média de mercado ≈ 68"
    if score >= 51:
        return "D (percentil ~15–49)"
    return "F (percentil < 15)"


def score_participante(respostas: dict) -> float:
    total = 0.0
    for i in range(1, 11):
        r = int(respostas[f"q{i}"])
        if not 1 <= r <= 5:
            raise ValueError(f"Resposta fora de 1–5 em q{i}: {r}")
        total += (r - 1) if i in IMPARES else (5 - r)
    return total * 2.5


def main():
    parser = argparse.ArgumentParser(description="Pontuação SUS (Frente C).")
    parser.add_argument("--respostas", required=True,
                        help="CSV de respostas (participante,q1..q10).")
    parser.add_argument("--relatorio-csv", default=None,
                        help="(Opcional) CSV com o escore por participante.")
    parser.add_argument("--resumo-json", default=None,
                        help="(Opcional) JSON com o resumo agregado (para gráficos).")
    args = parser.parse_args()

    if not os.path.exists(args.respostas):
        print(f"[!] Arquivo de respostas não encontrado: {args.respostas}")
        print("    Preencha o modelo (tests/respostas_sus_modelo.csv) com as")
        print("    respostas reais dos participantes e rode novamente.")
        raise SystemExit(1)

    with open(args.respostas, encoding="utf-8") as f:
        leitor = csv.DictReader(f)
        faltando = [c for c in (["participante"] + ITENS) if c not in leitor.fieldnames]
        if faltando:
            raise SystemExit(f"[!] Colunas ausentes no CSV: {faltando}")
        linhas = [l for l in leitor if l.get("participante", "").strip()]

    if not linhas:
        print("[!] Nenhuma resposta encontrada no arquivo (apenas cabeçalho?).")
        print("    A Frente C só produz resultados após a coleta com usuários reais.")
        raise SystemExit(1)

    resultados = []
    for l in linhas:
        s = score_participante(l)
        resultados.append({
            "participante": l["participante"].strip(),
            "sus_score": round(s, 1),
            "classificacao": classificacao_adjetiva(s),
        })

    escores = [r["sus_score"] for r in resultados]
    n = len(escores)
    media = statistics.mean(escores)
    dp = statistics.stdev(escores) if n > 1 else 0.0
    mediana = statistics.median(escores)

    print("=" * 60)
    print("PONTUAÇÃO DE USABILIDADE (SUS) — Frente C")
    print("=" * 60)
    print(f"Participantes.........: {n}")
    print(f"Escore médio (SUS)....: {media:.1f}  (0–100)")
    print(f"Desvio-padrão.........: {dp:.1f}")
    print(f"Mediana...............: {mediana:.1f}")
    print(f"Mínimo / Máximo.......: {min(escores):.1f} / {max(escores):.1f}")
    print(f"Classificação (média).: {classificacao_adjetiva(media)}")
    print(f"Faixa de percentil....: {faixa_percentil(media)}")
    print("\nPor participante:")
    for r in resultados:
        print(f"  {r['participante']:<8} {r['sus_score']:>6.1f}  ({r['classificacao']})")

    if args.relatorio_csv:
        os.makedirs(os.path.dirname(os.path.abspath(args.relatorio_csv)), exist_ok=True)
        with open(args.relatorio_csv, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["participante", "sus_score", "classificacao"])
            w.writeheader()
            w.writerows(resultados)
        print(f"\nRelatório por participante salvo em: {args.relatorio_csv}")

    resumo = {
        "frente": "C — Usabilidade (SUS)",
        "n_participantes": n,
        "sus_medio": round(media, 1),
        "desvio_padrao": round(dp, 1),
        "mediana": round(mediana, 1),
        "minimo": round(min(escores), 1),
        "maximo": round(max(escores), 1),
        "classificacao_media": classificacao_adjetiva(media),
        "faixa_percentil": faixa_percentil(media),
        "escores": escores,
    }
    if args.resumo_json:
        os.makedirs(os.path.dirname(os.path.abspath(args.resumo_json)), exist_ok=True)
        with open(args.resumo_json, "w", encoding="utf-8") as f:
            json.dump(resumo, f, ensure_ascii=False, indent=2)
        print(f"Resumo (JSON) salvo em: {args.resumo_json}")


if __name__ == "__main__":
    main()
