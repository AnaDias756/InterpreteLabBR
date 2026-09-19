#!/usr/bin/env python3
"""
Validação da Classificação — Frente B do TCC
============================================

Mede a CONCORDÂNCIA entre a classificação produzida pelo motor de regras do
sistema (`backend/services/rule_engine.apply_rules`) e a aplicação MANUAL das
faixas de referência da PNS (Rosenfeld et al., 2019), analito a analito.

Diferença em relação a `comparacao_referencias.py`: aquele script compara a
referência PNS com a referência estrangeira do laudo (dois padrões distintos);
ESTE script mede a fidelidade do sistema à própria PNS — ou seja, valida se o
software implementa corretamente a tabela de decisão (`guideline_map.csv`).

Como o "gabarito manual" nesta frente é a aplicação determinística das mesmas
faixas por um leitor independente (reimplementado aqui, à parte do motor),
uma concordância perfeita evidencia que o motor reproduz fielmente as regras;
qualquer discordância aponta um defeito de implementação (tipicamente no
tratamento dos LIMITES — os "casos de borda" enfatizados na proposta).

Gera:
  - matriz de confusão {baixo, normal, alto} × {baixo, normal, alto};
  - percentual de concordância global e coeficiente kappa de Cohen;
  - recorte por estrato sexo × faixa etária;
  - lista das discordâncias (para inspeção);
  - resumo em JSON e CSV, consumidos por `gerar_graficos.py`.

Uso:
    python tests/validacao_classificacao.py
    python tests/validacao_classificacao.py --relatorio-csv tests/saidas/classificacao.csv \
                                             --resumo-json tests/saidas/classificacao_resumo.json

Casos de teste: por padrão são SINTÉTICOS e gerados de forma sistemática em
torno de cada limite de referência (bem abaixo, no limite, logo abaixo/acima do
limite, no miolo da faixa, etc.), maximizando a densidade de casos de borda —
que é onde erros de classificação tendem a aparecer. Não há dados pessoais.
"""
import argparse
import csv
import json
import os
import sys
import unicodedata

import pandas as pd

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(THIS_DIR)
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
sys.path.insert(0, os.path.join(PROJECT_ROOT, "backend"))

from services.rule_engine import apply_rules, get_display_name, normalize_analito_name  # noqa: E402

CLASSES = ["baixo", "normal", "alto"]

# Estratos avaliados (a PNS é estratificada por sexo e faixa etária).
ESTRATOS = [
    ("masculino", 30, "M 18–59"),
    ("masculino", 70, "M 60+"),
    ("feminino", 30, "F 18–59"),
    ("feminino", 70, "F 60+"),
]


def _norm(s: str) -> str:
    s = str(s)
    return "".join(c for c in unicodedata.normalize("NFD", s)
                    if unicodedata.category(c) != "Mn").lower().strip()


def carregar_pns() -> pd.DataFrame:
    df = pd.read_csv(os.path.join(DATA_DIR, "guideline_map.csv"), comment="#")
    df["_analito"] = df["analito_id"].apply(_norm)
    df["_sexo"] = df["sexo"].apply(_norm)
    return df


def intervalo_manual(df: pd.DataFrame, analito_id: str, genero: str, idade: int):
    """Leitor MANUAL independente da PNS: retorna (inf, sup) ou None.

    Reproduz a semântica pretendida (regra específica de sexo tem prioridade
    sobre 'Todos'), porém em implementação separada do motor, servindo de
    gabarito para a Frente B.
    """
    sexo_map = {"masculino": "m", "feminino": "f"}
    alvo = _norm(normalize_analito_name(analito_id))
    sexo_n = sexo_map.get(genero.lower(), "todos")
    cand = df[(df["_analito"] == alvo)
              & (df["_sexo"].isin([sexo_n, "todos"]))
              & (df["idade_min"] <= idade)
              & (df["idade_max"] >= idade)]
    if cand.empty:
        return None
    # Prioriza a linha específica de sexo (não-'todos') sobre a genérica.
    especifica = cand[cand["_sexo"] != "todos"]
    linha = (especifica if not especifica.empty else cand).iloc[0]
    return float(linha["limite_inferior"]), float(linha["limite_superior"])


def classificar_manual(valor: float, intervalo) -> str:
    inf, sup = intervalo
    if valor < inf:
        return "baixo"
    if valor > sup:
        return "alto"
    return "normal"


def classificar_sistema(analito_id: str, valor: float, genero: str, idade: int) -> str:
    """Extrai a classificação do MOTOR do sistema para um único analito.

    `apply_rules` só devolve achados ANORMAIS; portanto, se o analito não
    aparece na saída (mas possui regra aplicável), o motor o considerou normal.
    """
    achados = apply_rules([{"analito": analito_id, "valor": valor}], genero, idade)
    display = get_display_name(analito_id)
    for a in achados:
        if a["analito"] == display:
            return a["resultado"]  # 'baixo' ou 'alto'
    return "normal"


def gerar_casos(inf: float, sup: float):
    """Gera valores de teste em torno de um intervalo, com foco nas bordas.

    Retorna lista de (valor, rotulo_do_caso). 'delta' é um passo pequeno,
    proporcional à largura da faixa, para sondar o comportamento logo
    abaixo/acima de cada limite (zona de borda).
    """
    largura = max(sup - inf, 1e-6)
    delta = max(largura * 0.01, 1e-6)  # 1% da faixa
    casos = [
        (max(inf - largura * 0.5, 0.0), "bem_abaixo"),
        (inf - delta, "logo_abaixo_do_inferior"),
        (inf, "no_limite_inferior"),
        (inf + delta, "logo_acima_do_inferior"),
        ((inf + sup) / 2.0, "miolo"),
        (sup - delta, "logo_abaixo_do_superior"),
        (sup, "no_limite_superior"),
        (sup + delta, "logo_acima_do_superior"),
        (sup + largura * 0.5, "bem_acima"),
    ]
    # Remove eventuais negativos (analitos como eosinófilos têm inf=0).
    return [(round(v, 6), rot) for v, rot in casos if v >= 0]


def cohen_kappa(matriz) -> float:
    n = sum(sum(l) for l in matriz)
    if n == 0:
        return float("nan")
    k = len(CLASSES)
    po = sum(matriz[i][i] for i in range(k)) / n
    lin = [sum(matriz[i]) / n for i in range(k)]
    col = [sum(matriz[i][j] for i in range(k)) / n for j in range(k)]
    pe = sum(lin[i] * col[i] for i in range(k))
    if pe == 1:
        return 1.0
    return (po - pe) / (1 - pe)


def eh_borda(rotulo: str) -> bool:
    return rotulo.startswith("logo_") or rotulo.startswith("no_limite")


def main():
    parser = argparse.ArgumentParser(description="Validação da classificação (Frente B).")
    parser.add_argument("--relatorio-csv", default=None,
                        help="(Opcional) CSV com todos os casos avaliados.")
    parser.add_argument("--resumo-json", default=None,
                        help="(Opcional) JSON com o resumo agregado (para gráficos).")
    args = parser.parse_args()

    pns = carregar_pns()
    analitos = sorted(pns["analito_id"].unique(), key=lambda a: a.lower())

    idx = {c: i for i, c in enumerate(CLASSES)}
    matriz = [[0] * len(CLASSES) for _ in CLASSES]
    matriz_borda = [[0] * len(CLASSES) for _ in CLASSES]
    por_estrato = {lbl: {"total": 0, "concordantes": 0} for _, _, lbl in ESTRATOS}
    por_analito = {}
    linhas = []
    discordancias = []
    total = concordantes = total_borda = concordantes_borda = 0

    print("=" * 74)
    print("VALIDAÇÃO DA CLASSIFICAÇÃO — Frente B (motor × aplicação manual da PNS)")
    print("=" * 74)

    for genero, idade, estrato_lbl in ESTRATOS:
        for analito in analitos:
            intervalo = intervalo_manual(pns, analito, genero, idade)
            if intervalo is None:
                continue
            display = get_display_name(analito)
            a_stat = por_analito.setdefault(display, {"total": 0, "concordantes": 0})
            for valor, caso in gerar_casos(*intervalo):
                manual = classificar_manual(valor, intervalo)
                sistema = classificar_sistema(analito, valor, genero, idade)
                concorda = manual == sistema

                matriz[idx[manual]][idx[sistema]] += 1
                total += 1
                por_estrato[estrato_lbl]["total"] += 1
                a_stat["total"] += 1
                if concorda:
                    concordantes += 1
                    por_estrato[estrato_lbl]["concordantes"] += 1
                    a_stat["concordantes"] += 1

                if eh_borda(caso):
                    total_borda += 1
                    matriz_borda[idx[manual]][idx[sistema]] += 1
                    if concorda:
                        concordantes_borda += 1

                linha = {
                    "estrato": estrato_lbl, "analito": display, "valor": valor,
                    "caso": caso, "manual_pns": manual, "sistema": sistema,
                    "concorda": concorda, "borda": eh_borda(caso),
                }
                linhas.append(linha)
                if not concorda:
                    discordancias.append(linha)

    # ---------------- Síntese ----------------
    perc = concordantes / total * 100 if total else 0
    perc_borda = concordantes_borda / total_borda * 100 if total_borda else 0
    kappa = cohen_kappa(matriz)
    kappa_borda = cohen_kappa(matriz_borda)

    print(f"\nCasos avaliados...............: {total} "
          f"({total_borda} em zona de borda)")
    print(f"Concordância global...........: {concordantes}/{total} ({perc:.1f}%)")
    print(f"Concordância em bordas........: {concordantes_borda}/{total_borda} ({perc_borda:.1f}%)")
    print(f"Kappa de Cohen (global).......: {kappa:.3f}")
    print(f"Kappa de Cohen (bordas).......: {kappa_borda:.3f}")

    print("\nMatriz de confusão (linhas = manual PNS, colunas = sistema):")
    print(f"  {'':>10}" + "".join(f"{c:>10}" for c in CLASSES))
    for i, c in enumerate(CLASSES):
        print(f"  {c:>10}" + "".join(f"{matriz[i][j]:>10}" for j in range(len(CLASSES))))

    print("\nConcordância por estrato:")
    for _, _, lbl in ESTRATOS:
        e = por_estrato[lbl]
        p = e["concordantes"] / e["total"] * 100 if e["total"] else 0
        print(f"  {lbl:<10} {e['concordantes']}/{e['total']} ({p:.1f}%)")

    if discordancias:
        print(f"\n[!] {len(discordancias)} discordância(s) encontrada(s):")
        for d in discordancias[:30]:
            print(f"  [{d['estrato']}] {d['analito']} = {d['valor']} "
                  f"({d['caso']}): manual={d['manual_pns']} × sistema={d['sistema']}")
    else:
        print("\n[OK] Nenhuma discordância: o motor reproduz fielmente as faixas da PNS.")

    # ---------------- Saídas ----------------
    if args.relatorio_csv:
        os.makedirs(os.path.dirname(os.path.abspath(args.relatorio_csv)), exist_ok=True)
        with open(args.relatorio_csv, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["estrato", "analito", "valor", "caso",
                                              "manual_pns", "sistema", "concorda", "borda"])
            w.writeheader()
            w.writerows(linhas)
        print(f"\nRelatório detalhado salvo em: {args.relatorio_csv}")

    resumo = {
        "frente": "B — Classificação (motor × PNS manual)",
        "natureza_dos_dados": "sintético (casos de borda gerados sistematicamente)",
        "total_casos": total,
        "concordancia_global_pct": round(perc, 2),
        "concordancia_bordas_pct": round(perc_borda, 2),
        "kappa_global": round(kappa, 4),
        "kappa_bordas": round(kappa_borda, 4),
        "matriz_confusao": {"classes": CLASSES, "valores": matriz},
        "por_estrato": {lbl: {
            "total": por_estrato[lbl]["total"],
            "concordantes": por_estrato[lbl]["concordantes"],
            "pct": round(por_estrato[lbl]["concordantes"] / por_estrato[lbl]["total"] * 100, 2)
            if por_estrato[lbl]["total"] else 0,
        } for _, _, lbl in ESTRATOS},
        "n_discordancias": len(discordancias),
    }
    if args.resumo_json:
        os.makedirs(os.path.dirname(os.path.abspath(args.resumo_json)), exist_ok=True)
        with open(args.resumo_json, "w", encoding="utf-8") as f:
            json.dump(resumo, f, ensure_ascii=False, indent=2)
        print(f"Resumo (JSON) salvo em: {args.resumo_json}")


if __name__ == "__main__":
    main()
