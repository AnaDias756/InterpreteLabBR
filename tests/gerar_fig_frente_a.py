#!/usr/bin/env python3
"""Figura 6 (Frente A) com DOIS painéis: Memória (RAM) e Fluidez (FPS),
ambos como comparação de 2 barras (PWA x Móvel). Resolve o comentário do
orientador (nada de gráfico com um ponto só) e incorpora a medição real de
FPS do PWA via Chrome DevTools (Frame Rate meter) remoto por ADB.
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)))

AZUL = "#2a78d6"      # PWA
LARANJA = "#eb6834"   # Móvel
CINZA = "#52514e"
GRADE = "#e6e6e3"
SURF = "#fcfcfb"

plt.rcParams.update({
    "figure.facecolor": SURF, "axes.facecolor": SURF,
    "savefig.facecolor": SURF, "font.size": 10,
    "axes.edgecolor": CINZA, "axes.labelcolor": "#0b0b0b",
    "xtick.color": CINZA, "ytick.color": CINZA, "text.color": "#0b0b0b",
})


def _grade(ax):
    ax.grid(axis="y", color=GRADE, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.0, 3.6))

# -------- Painel 1: Memória (RAM) — menor melhor --------
larg = 0.42
ax1.bar([-larg/2], [235.0], larg, yerr=[18.7], capsize=4, color=AZUL, zorder=3,
        label="PWA", error_kw={"elinewidth": 1, "ecolor": CINZA})
ax1.bar([larg/2], [84.9], larg, yerr=[0.2], capsize=4, color=LARANJA, zorder=3,
        label="Móvel", error_kw={"elinewidth": 1, "ecolor": CINZA})
for x, v, e in [(-larg/2, 235.0, 18.7), (larg/2, 84.9, 0.2)]:
    ax1.text(x, v + e + 9, f"{v:.1f}", ha="center", va="bottom", fontsize=9, color=CINZA, zorder=4)
_grade(ax1)
ax1.set_xticks([0]); ax1.set_xticklabels(["App carregado"], fontsize=9)
ax1.set_ylim(0, 300)
ax1.set_title("Memória (RAM) (MB) · ↓ menor melhor", fontsize=10, fontweight="bold", loc="left")
ax1.legend(frameon=False, fontsize=8.5, loc="upper right")

# -------- Painel 2: Fluidez na rolagem (FPS) — maior melhor --------
ax2.bar([-larg/2], [60], larg, color=AZUL, zorder=3)
ax2.bar([larg/2], [60], larg, color=LARANJA, zorder=3)
for x in (-larg/2, larg/2):
    ax2.text(x, 61.5, "~60", ha="center", va="bottom", fontsize=9, color=CINZA, zorder=4)
_grade(ax2)
ax2.set_xticks([0]); ax2.set_xticklabels(["Rolagem"], fontsize=9)
ax2.set_ylim(0, 75)
ax2.axhline(60, color=CINZA, linewidth=0.9, linestyle=(0, (4, 3)), zorder=2)
ax2.set_title("Fluidez na rolagem (FPS) · ↑ maior melhor", fontsize=10, fontweight="bold", loc="left")

fig.suptitle("Frente A — Desempenho PWA × Móvel (ADB)",
             fontweight="bold", x=0.01, ha="left", fontsize=12)
fig.text(0.01, -0.03,
         "Galaxy Tab S9 FE, Android 16. RAM: média ± desvio-padrão, 10 repetições. "
         "FPS: medido no PWA via Chrome DevTools (Frame Rate meter) por ADB (~60 fps, sem quedas); "
         "nativo via gfxinfo (0,2% de quadros lentos, ~60 fps).",
         fontsize=7.6, color=CINZA)
fig.tight_layout(rect=[0, 0.02, 1, 0.94])
caminho = os.path.join(OUT, "fig_frente_a_desempenho_adb.png")
fig.savefig(caminho, dpi=150, bbox_inches="tight")
print("salvo:", caminho)
