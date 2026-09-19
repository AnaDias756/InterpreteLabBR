#!/usr/bin/env python3
"""
Geração de Figuras do Capítulo de Resultados
=============================================

Lê as saídas das frentes de validação (em `tests/saidas/`) e produz as figuras
estáticas (PNG) do capítulo de Resultados, em `docs/figuras/`.

Figuras geradas (quando os insumos existem):
  - fig_frente_a_acuracia.png ....... acurácia de extração por analito (Frente A)
  - fig_frente_b_matriz.png ......... matriz de confusão sistema × PNS (Frente B)
  - fig_pns_vs_lab_discordancia.png . discordância PNS × ref. estrangeira (Frente B analítica)
  - fig_frente_c_sus.png ............ escore SUS por participante (Frente C)

Paleta e princípios seguem a skill de dataviz (paleta validada para daltonismo;
uma matiz por magnitude; marcas finas; grade recessiva; rótulos diretos).

Uso:
    python tests/gerar_graficos.py
"""
import csv
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(THIS_DIR)
SAIDAS = os.path.join(THIS_DIR, "saidas")
FIGS = os.path.join(PROJECT_ROOT, "docs", "figuras")
os.makedirs(FIGS, exist_ok=True)

# ---- Paleta (validada para CVD; ver skill dataviz / references/palette.md) ----
AZUL = "#2a78d6"      # magnitude / série 1
LARANJA = "#eb6834"   # série 2
CINZA = "#52514e"     # texto secundário / linhas de referência
GRADE = "#e6e6e3"
SURF = "#fcfcfb"
AZUL_RAMP = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#104281"]

plt.rcParams.update({
    "figure.facecolor": SURF, "axes.facecolor": SURF,
    "savefig.facecolor": SURF, "font.size": 10,
    "axes.edgecolor": CINZA, "axes.labelcolor": "#0b0b0b",
    "xtick.color": CINZA, "ytick.color": CINZA, "text.color": "#0b0b0b",
})


def _grade(ax, eixo="y"):
    ax.grid(axis=eixo, color=GRADE, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)


def _salvar(fig, nome):
    caminho = os.path.join(FIGS, nome)
    fig.savefig(caminho, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  figura salva: {os.path.relpath(caminho, PROJECT_ROOT)}")


# --------------------------------------------------------------------------- #
def fig_frente_a():
    """Acurácia de extração por analito (a partir do CSV detalhado da Frente A)."""
    caminho = os.path.join(SAIDAS, "extracao_frente_a.csv")
    if not os.path.exists(caminho):
        print("  [pulado] Frente A: tests/saidas/extracao_frente_a.csv ausente.")
        return
    stats = {}
    with open(caminho, encoding="utf-8") as f:
        for l in csv.DictReader(f):
            if l["status"] == "FALSO_POSITIVO":
                continue
            s = stats.setdefault(l["analito"], {"ok": 0, "tot": 0})
            s["tot"] += 1
            if l["status"] == "OK":
                s["ok"] += 1
    if not stats:
        print("  [pulado] Frente A: sem linhas no relatório.")
        return
    itens = sorted(stats.items(), key=lambda kv: (kv[1]["ok"] / kv[1]["tot"], kv[0]))
    nomes = [k for k, _ in itens]
    acc = [v["ok"] / v["tot"] * 100 for _, v in itens]

    fig, ax = plt.subplots(figsize=(7.2, 5.2))
    _grade(ax, "x")
    y = range(len(nomes))
    ax.barh(list(y), acc, color=AZUL, height=0.62, zorder=3)
    for i, a in zip(y, acc):
        ax.text(a - 1.5 if a > 12 else a + 1.5, i, f"{a:.0f}%",
                va="center", ha="right" if a > 12 else "left",
                color="white" if a > 12 else CINZA, fontsize=8.5, zorder=4)
    ax.set_yticks(list(y)); ax.set_yticklabels(nomes)
    ax.set_xlim(0, 100); ax.xaxis.set_major_formatter(PercentFormatter())
    ax.set_xlabel("Acurácia de extração")
    ax.set_title("Frente A — Acurácia de extração por analito", fontweight="bold", loc="left")
    total_analitos = sum(v["tot"] for _, v in itens)
    fig.text(0.01, -0.02,
             f"Cada barra: acertos / ocorrências no gabarito. Total de {total_analitos} ocorrências avaliadas.",
             fontsize=8, color=CINZA)
    _salvar(fig, "fig_frente_a_acuracia.png")


# --------------------------------------------------------------------------- #
def fig_frente_b_matriz():
    """Matriz de confusão sistema × PNS manual (Frente B)."""
    caminho = os.path.join(SAIDAS, "classificacao_resumo.json")
    if not os.path.exists(caminho):
        print("  [pulado] Frente B: classificacao_resumo.json ausente.")
        return
    with open(caminho, encoding="utf-8") as f:
        resumo = json.load(f)
    classes = resumo["matriz_confusao"]["classes"]
    M = resumo["matriz_confusao"]["valores"]
    vmax = max(max(l) for l in M) or 1

    fig, ax = plt.subplots(figsize=(5.6, 5.0))
    for i in range(len(classes)):
        for j in range(len(classes)):
            v = M[i][j]
            intensidade = v / vmax
            # célula diagonal: azul cheio; fora da diagonal: laranja se houver erro
            if i == j:
                cor = AZUL_RAMP[min(int(intensidade * (len(AZUL_RAMP) - 1)), len(AZUL_RAMP) - 1)]
            else:
                cor = "#f6cbb9" if v > 0 else SURF
            ax.add_patch(plt.Rectangle((j, len(classes) - 1 - i), 1, 1,
                                       facecolor=cor, edgecolor=SURF, linewidth=2, zorder=2))
            texto_claro = (i == j and intensidade > 0.55)
            ax.text(j + 0.5, len(classes) - 1 - i + 0.5, str(v),
                    ha="center", va="center", zorder=3,
                    color="white" if texto_claro else "#0b0b0b",
                    fontsize=12, fontweight="bold")
    ax.set_xlim(0, len(classes)); ax.set_ylim(0, len(classes))
    ax.set_xticks([c + 0.5 for c in range(len(classes))]); ax.set_xticklabels(classes)
    ax.set_yticks([c + 0.5 for c in range(len(classes))])
    ax.set_yticklabels(list(reversed(classes)))
    ax.set_xlabel("Classificação do sistema"); ax.set_ylabel("Aplicação manual da PNS")
    ax.set_aspect("equal")
    for lado in ("top", "right", "left", "bottom"):
        ax.spines[lado].set_visible(False)
    ax.tick_params(length=0)
    kappa = resumo["kappa_global"]; pct = resumo["concordancia_global_pct"]
    ax.set_title(f"Frente B — Concordância {pct:.0f}%  ·  κ = {kappa:.2f}",
                 fontweight="bold", loc="left")
    fig.text(0.01, -0.02,
             f"{resumo['total_casos']} casos sintéticos; diagonal = concordância. "
             f"Dados: {resumo['natureza_dos_dados']}.", fontsize=8, color=CINZA)
    _salvar(fig, "fig_frente_b_matriz.png")


# --------------------------------------------------------------------------- #
def fig_pns_vs_lab():
    """Discordância PNS × referência estrangeira, por analito (Frente B analítica)."""
    caminho = os.path.join(SAIDAS, "comparacao_referencias.csv")
    if not os.path.exists(caminho):
        print("  [pulado] PNS×Lab: comparacao_referencias.csv ausente.")
        return
    # média da taxa de discordância por analito (agrega estratos sexo×idade)
    corrige = {"leucocitos": "Leucócitos"}
    acc = {}
    with open(caminho, encoding="utf-8") as f:
        for l in csv.DictReader(f):
            nome = corrige.get(l["analito"], l["analito"])
            a = acc.setdefault(nome, [])
            a.append(float(l["taxa_discordancia"]) * 100)
    itens = sorted(((k, sum(v) / len(v)) for k, v in acc.items()), key=lambda kv: kv[1])
    nomes = [k for k, _ in itens]; taxas = [v for _, v in itens]

    fig, ax = plt.subplots(figsize=(7.2, 5.6))
    _grade(ax, "x")
    y = range(len(nomes))
    ax.barh(list(y), taxas, color=LARANJA, height=0.62, zorder=3)
    for i, t in zip(y, taxas):
        ax.text(t + 0.6, i, f"{t:.1f}%", va="center", ha="left", color=CINZA, fontsize=8.5, zorder=4)
    ax.set_yticks(list(y)); ax.set_yticklabels(nomes)
    ax.set_xlim(0, max(taxas) * 1.18 if taxas else 1)
    ax.xaxis.set_major_formatter(PercentFormatter())
    ax.set_xlabel("Taxa de discordância (amostragem uniforme)")
    ax.set_title("PNS × referência estrangeira do laudo — discordância por analito",
                 fontweight="bold", loc="left")
    fig.text(0.01, -0.02,
             "Faixa de valores em que as duas referências classificam de modo diferente. "
             "Média dos estratos sexo × idade.", fontsize=8, color=CINZA)
    _salvar(fig, "fig_pns_vs_lab_discordancia.png")


# --------------------------------------------------------------------------- #
def fig_frente_c():
    """Escore SUS por participante, com média e referência de mercado (68)."""
    caminho = os.path.join(SAIDAS, "sus_por_participante.csv")
    resumo_p = os.path.join(SAIDAS, "sus_resumo.json")
    if not (os.path.exists(caminho) and os.path.exists(resumo_p)):
        print("  [pulado] Frente C: saídas SUS ausentes.")
        return
    with open(resumo_p, encoding="utf-8") as f:
        resumo = json.load(f)
    linhas = []
    with open(caminho, encoding="utf-8") as f:
        for l in csv.DictReader(f):
            linhas.append((l["participante"], float(l["sus_score"])))
    linhas.sort(key=lambda t: t[1])
    nomes = [p for p, _ in linhas]; escores = [s for _, s in linhas]
    media = resumo["sus_medio"]

    fig, ax = plt.subplots(figsize=(7.6, 4.6))
    _grade(ax, "y")
    x = range(len(nomes))
    ax.bar(list(x), escores, color=AZUL, width=0.66, zorder=3)
    for i, s in zip(x, escores):
        ax.text(i, s + 1.2, f"{s:.0f}", ha="center", va="bottom", color=CINZA, fontsize=8, zorder=4)
    # linhas de referência
    ax.axhline(media, color=LARANJA, linewidth=2, zorder=5)
    ax.text(len(nomes) - 0.4, media + 1.2, f"média {media:.1f}", color=LARANJA,
            ha="right", va="bottom", fontsize=8.5, fontweight="bold")
    ax.axhline(68, color=CINZA, linewidth=1.2, linestyle=(0, (4, 3)), zorder=5)
    ax.text(len(nomes) - 0.4, 68 - 3.2, "média de mercado ≈ 68", color=CINZA,
            ha="right", va="top", fontsize=8)
    ax.set_xticks(list(x)); ax.set_xticklabels(nomes, rotation=45, ha="right", fontsize=8)
    ax.set_ylim(0, 100); ax.set_ylabel("Escore SUS (0–100)")
    ax.set_title(f"Frente C — Usabilidade (SUS)  ·  n = {resumo['n_participantes']}",
                 fontweight="bold", loc="left")
    fig.text(0.01, -0.04,
             "ATENÇÃO: dados ILUSTRATIVOS/SINTÉTICOS — substituir pelas respostas reais dos participantes.",
             fontsize=8, color=LARANJA, fontweight="bold")
    _salvar(fig, "fig_frente_c_sus.png")


# --------------------------------------------------------------------------- #
def fig_inspecao_heuristica():
    """Problemas por heurística, PWA × Móvel (Frente C — inspeção heurística)."""
    caminho = os.path.join(SAIDAS, "inspecao_resumo.json")
    if not os.path.exists(caminho):
        print("  [pulado] Inspeção heurística: inspecao_resumo.json ausente.")
        return
    with open(caminho, encoding="utf-8") as f:
        resumo = json.load(f)
    heurs = [f"H{i}" for i in range(1, 11)]
    pwa = [resumo["por_heuristica"]["PWA"].get(h, 0) for h in heurs]
    mob = [resumo["por_heuristica"]["Móvel"].get(h, 0) for h in heurs]

    fig, ax = plt.subplots(figsize=(8.0, 4.8))
    _grade(ax, "y")
    x = range(len(heurs))
    larg = 0.38
    ax.bar([i - larg / 2 for i in x], pwa, larg, color=AZUL, zorder=3, label="PWA")
    ax.bar([i + larg / 2 for i in x], mob, larg, color=LARANJA, zorder=3, label="Móvel")
    for i, v in zip(x, pwa):
        if v:
            ax.text(i - larg / 2, v + 0.1, str(v), ha="center", va="bottom", fontsize=7.5, color=CINZA)
    for i, v in zip(x, mob):
        if v:
            ax.text(i + larg / 2, v + 0.1, str(v), ha="center", va="bottom", fontsize=7.5, color=CINZA)
    ax.set_xticks(list(x)); ax.set_xticklabels(heurs)
    ax.set_ylabel("Problemas registrados")
    ax.set_xlabel("Heurística de Nielsen")
    ax.legend(frameon=False, loc="upper right")
    pc = resumo["por_cliente"]
    ax.set_title("Frente C — Problemas por heurística (PWA × Móvel)", fontweight="bold", loc="left")
    fig.text(0.01, -0.04,
             f"PWA: {pc['PWA']['problemas']} problemas (sev. média {pc['PWA']['severidade_media']}) · "
             f"Móvel: {pc['Móvel']['problemas']} (sev. média {pc['Móvel']['severidade_media']}). "
             f"ILUSTRATIVO/SINTÉTICO — substituir pelos dados reais.",
             fontsize=7.5, color=LARANJA, fontweight="bold")
    _salvar(fig, "fig_frente_c_inspecao_heuristica.png")


def main():
    print("Gerando figuras em docs/figuras/ ...")
    fig_frente_a()
    fig_frente_b_matriz()
    fig_pns_vs_lab()
    fig_frente_c()
    fig_inspecao_heuristica()
    print("Concluído.")


if __name__ == "__main__":
    main()
