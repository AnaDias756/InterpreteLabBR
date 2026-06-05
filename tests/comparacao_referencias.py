#!/usr/bin/env python3
"""
Comparação de Referências — Frente B do TCC
===========================================

Compara, analito a analito, a classificação baseada nos valores de
referência da **PNS** (população adulta brasileira; Rosenfeld et al., 2019)
com a referência **clássica/laboratorial** impressa no laudo do SUS
(fontes citadas no laudo: Wintrobe e Dacie & Lewis — livros-texto
estrangeiros).

Para cada analito × sexo × faixa etária, calcula:
  - os dois intervalos de referência e suas diferenças (Δ limite inferior/superior);
  - qual referência é mais "restritiva" em cada extremo;
  - as ZONAS DE DISCORDÂNCIA (faixas de valor em que a classificação muda);
  - a taxa de discordância e o coeficiente kappa sob amostragem uniforme.

Uso:
    python tests/comparacao_referencias.py
    python tests/comparacao_referencias.py --relatorio comparacao.csv
"""
import argparse
import csv
import os
import unicodedata

import pandas as pd

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(THIS_DIR)
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

CLASSES = ["baixo", "normal", "alto"]


def norm(s: str) -> str:
    s = str(s)
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn").lower().strip()


def carregar(caminho: str) -> pd.DataFrame:
    df = pd.read_csv(caminho, comment="#")
    df["_analito"] = df["analito_id"].apply(norm)
    df["_sexo"] = df["sexo"].apply(norm)
    return df


def get_intervalo(df: pd.DataFrame, analito: str, sexo: str, idade: int):
    """Retorna (inf, sup) do analito para o sexo/idade, ou None."""
    alvo = norm(analito)
    sexo_n = norm(sexo)
    cand = df[(df["_analito"] == alvo)
              & (df["_sexo"].isin([sexo_n, "todos"]))
              & (df["idade_min"] <= idade)
              & (df["idade_max"] >= idade)]
    if cand.empty:
        return None
    linha = cand.iloc[0]
    return float(linha["limite_inferior"]), float(linha["limite_superior"])


def classificar(valor: float, intervalo) -> str:
    inf, sup = intervalo
    if valor < inf:
        return "baixo"
    if valor > sup:
        return "alto"
    return "normal"


def cohen_kappa(rotulos_a, rotulos_b) -> float:
    """Coeficiente kappa de Cohen para duas listas de rótulos categóricos."""
    n = len(rotulos_a)
    if n == 0:
        return float("nan")
    idx = {c: i for i, c in enumerate(CLASSES)}
    conf = [[0] * len(CLASSES) for _ in CLASSES]
    for a, b in zip(rotulos_a, rotulos_b):
        conf[idx[a]][idx[b]] += 1
    po = sum(conf[i][i] for i in range(len(CLASSES))) / n
    lin = [sum(conf[i]) / n for i in range(len(CLASSES))]
    col = [sum(conf[i][j] for i in range(len(CLASSES))) / n for j in range(len(CLASSES))]
    pe = sum(lin[i] * col[i] for i in range(len(CLASSES)))
    if pe == 1:
        return 1.0
    return (po - pe) / (1 - pe)


def amostrar_discordancia(int_pns, int_lab, n=4000):
    """Amostra valores uniformemente e mede discordância e kappa."""
    inf = min(int_pns[0], int_lab[0])
    sup = max(int_pns[1], int_lab[1])
    span = sup - inf
    lo = max(0.0, inf - 0.5 * span)
    hi = sup + 0.5 * span
    passo = (hi - lo) / n
    rot_pns, rot_lab = [], []
    discordantes = 0
    for k in range(n):
        v = lo + k * passo
        cp = classificar(v, int_pns)
        cl = classificar(v, int_lab)
        rot_pns.append(cp)
        rot_lab.append(cl)
        if cp != cl:
            discordantes += 1
    return discordantes / n, cohen_kappa(rot_pns, rot_lab), (lo, hi)


def descreve_zona(lim_pns, lim_lab, extremo: str) -> str:
    """Descreve a direção da discordância em um extremo (inferior/superior)."""
    if abs(lim_pns - lim_lab) < 1e-9:
        return "—"
    if extremo == "inferior":
        if lim_pns < lim_lab:
            return f"PNS normal / Lab baixo em [{lim_pns:g}, {lim_lab:g}] (PNS menos sensível a valores baixos)"
        return f"PNS baixo / Lab normal em [{lim_lab:g}, {lim_pns:g}] (PNS mais sensível a valores baixos)"
    else:
        if lim_pns > lim_lab:
            return f"PNS normal / Lab alto em [{lim_lab:g}, {lim_pns:g}] (PNS menos sensível a valores altos)"
        return f"PNS alto / Lab normal em [{lim_pns:g}, {lim_lab:g}] (PNS mais sensível a valores altos)"


def main():
    parser = argparse.ArgumentParser(description="Comparação PNS × referência laboratorial (Frente B).")
    parser.add_argument("--pns", default=os.path.join(DATA_DIR, "guideline_map.csv"))
    parser.add_argument("--lab", default=os.path.join(DATA_DIR, "lab_reference.csv"))
    parser.add_argument("--relatorio", default=None, help="(Opcional) salva CSV detalhado.")
    args = parser.parse_args()

    pns = carregar(args.pns)
    lab = carregar(args.lab)

    analitos = ["Hemácias", "Hemoglobina", "Hematócrito", "VCM", "HCM", "CHCM", "RDW",
                "leucocitos", "Neutrófilos", "Eosinófilos", "Basófilos",
                "Linfócitos", "Monócitos", "Plaquetas"]
    sexos = [("F", "Feminino"), ("M", "Masculino")]
    faixas = [(30, "18–59"), (70, "60–120")]

    linhas_csv = []
    kappas = []
    taxas = []
    pns_menos_sensivel_baixo = 0
    comparacoes = 0

    print("=" * 78)
    print("COMPARAÇÃO DE REFERÊNCIAS — PNS × Laboratorial (Frente B)")
    print("=" * 78)

    for sexo, sexo_lbl in sexos:
        print(f"\n################  SEXO: {sexo_lbl}  ################")
        for idade, faixa_lbl in faixas:
            print(f"\n----- Faixa etária {faixa_lbl} anos -----")
            print(f"{'Analito':<13}{'PNS (inf–sup)':>20}{'Lab (inf–sup)':>20}{'Δinf':>10}{'Δsup':>10}{'discord.':>10}{'kappa':>8}")
            for analito in analitos:
                ip = get_intervalo(pns, analito, sexo, idade)
                il = get_intervalo(lab, analito, sexo, idade)
                if ip is None or il is None:
                    continue
                comparacoes += 1
                d_inf = ip[0] - il[0]
                d_sup = ip[1] - il[1]
                taxa, kappa, _ = amostrar_discordancia(ip, il)
                taxas.append(taxa)
                kappas.append(kappa)
                if ip[0] < il[0]:
                    pns_menos_sensivel_baixo += 1

                print(f"{analito:<13}"
                      f"{f'{ip[0]:g}–{ip[1]:g}':>20}"
                      f"{f'{il[0]:g}–{il[1]:g}':>20}"
                      f"{d_inf:>10.4g}{d_sup:>10.4g}{taxa*100:>9.1f}%{kappa:>8.2f}")

                linhas_csv.append({
                    "analito": analito, "sexo": sexo_lbl, "faixa_etaria": faixa_lbl,
                    "pns_inf": ip[0], "pns_sup": ip[1], "lab_inf": il[0], "lab_sup": il[1],
                    "delta_inf": d_inf, "delta_sup": d_sup,
                    "taxa_discordancia": round(taxa, 4), "kappa": round(kappa, 4),
                    "zona_inferior": descreve_zona(ip[0], il[0], "inferior"),
                    "zona_superior": descreve_zona(ip[1], il[1], "superior"),
                })

    # ----- Síntese -----
    print("\n" + "=" * 78)
    print("SÍNTESE")
    print("=" * 78)
    media_taxa = sum(taxas) / len(taxas) if taxas else 0
    media_kappa = sum(kappas) / len(kappas) if kappas else 0
    print(f"Comparações realizadas........: {comparacoes}")
    print(f"Taxa média de discordância....: {media_taxa*100:.1f}% (sob amostragem uniforme)")
    print(f"Kappa médio (concordância)....: {media_kappa:.2f}")
    print(f"Analitos em que a PNS é menos sensível a valores BAIXOS")
    print(f"  (limite inferior PNS < limite inferior do laudo): {pns_menos_sensivel_baixo}/{comparacoes}")

    print("\nPrincipais zonas de discordância (limite inferior):")
    for l in linhas_csv:
        if l["zona_inferior"] != "—":
            print(f"  [{l['sexo'][:3]} {l['faixa_etaria']}] {l['analito']}: {l['zona_inferior']}")

    if args.relatorio:
        with open(args.relatorio, "w", newline="", encoding="utf-8") as f:
            campos = ["analito", "sexo", "faixa_etaria", "pns_inf", "pns_sup",
                      "lab_inf", "lab_sup", "delta_inf", "delta_sup",
                      "taxa_discordancia", "kappa", "zona_inferior", "zona_superior"]
            w = csv.DictWriter(f, fieldnames=campos)
            w.writeheader()
            w.writerows(linhas_csv)
        print(f"\nRelatório detalhado salvo em: {args.relatorio}")


if __name__ == "__main__":
    main()
