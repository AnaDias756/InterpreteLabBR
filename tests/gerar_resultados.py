#!/usr/bin/env python3
"""
Orquestrador dos Resultados (Etapa 4 do TCC)
============================================

Executa, em sequência, todas as frentes de validação e regenera as figuras do
capítulo de Resultados. É o ponto de entrada único: rode este script sempre que
novos dados (laudos reais, respostas SUS) forem adicionados, e as tabelas,
estatísticas e figuras serão recalculadas.

  Frente A (extração) ....... sobre a pasta de laudos informada (ou o exemplo sintético)
  Frente B (classificação) .. concordância motor × PNS manual (sintético, casos de borda)
  PNS × ref. estrangeira ..... comparação analítica das duas referências
  Frente C (usabilidade) ..... escore SUS a partir do CSV de respostas
  Figuras .................... PNG em docs/figuras/

Uso:
    # Demonstração completa (Frente A no exemplo sintético; Frente C no exemplo sintético)
    python tests/gerar_resultados.py

    # Com dados reais:
    python tests/gerar_resultados.py \
        --laudos tests/laudos --gabarito tests/meu_gabarito.json \
        --respostas-sus tests/respostas_sus.csv

Todas as saídas intermediárias vão para tests/saidas/.
"""
import argparse
import os
import subprocess
import sys

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
SAIDAS = os.path.join(THIS_DIR, "saidas")
os.makedirs(SAIDAS, exist_ok=True)
PY = sys.executable


def rodar(titulo, args):
    print("\n" + "#" * 74)
    print(f"# {titulo}")
    print("#" * 74)
    r = subprocess.run([PY] + args)
    if r.returncode != 0:
        print(f"[!] '{titulo}' terminou com código {r.returncode} (seguindo adiante).")
    return r.returncode


def main():
    p = argparse.ArgumentParser(description="Orquestrador dos resultados (Etapa 4).")
    p.add_argument("--laudos", default=os.path.join(THIS_DIR, "exemplos"),
                   help="Pasta de PDFs para a Frente A (padrão: exemplo sintético).")
    p.add_argument("--gabarito", default=os.path.join(THIS_DIR, "gabarito_exemplo.json"),
                   help="Gabarito JSON para a Frente A.")
    p.add_argument("--respostas-sus", default=os.path.join(THIS_DIR, "respostas_sus_exemplo.csv"),
                   help="CSV de respostas SUS para a Frente C (padrão: exemplo sintético).")
    args = p.parse_args()

    # Frente A — extração
    rodar("Frente A — Validação da extração", [
        os.path.join(THIS_DIR, "validacao_extracao.py"),
        "--laudos", args.laudos, "--gabarito", args.gabarito,
        "--relatorio", os.path.join(SAIDAS, "extracao_frente_a.csv"),
    ])

    # Frente B — classificação (motor × PNS manual)
    rodar("Frente B — Validação da classificação", [
        os.path.join(THIS_DIR, "validacao_classificacao.py"),
        "--relatorio-csv", os.path.join(SAIDAS, "classificacao.csv"),
        "--resumo-json", os.path.join(SAIDAS, "classificacao_resumo.json"),
    ])

    # Comparação analítica PNS × referência estrangeira
    rodar("Comparação PNS × referência estrangeira", [
        os.path.join(THIS_DIR, "comparacao_referencias.py"),
        "--relatorio", os.path.join(SAIDAS, "comparacao_referencias.csv"),
    ])

    # Frente C — usabilidade (SUS)
    if os.path.exists(args.respostas_sus):
        rodar("Frente C — Pontuação SUS", [
            os.path.join(THIS_DIR, "pontuacao_sus.py"),
            "--respostas", args.respostas_sus,
            "--relatorio-csv", os.path.join(SAIDAS, "sus_por_participante.csv"),
            "--resumo-json", os.path.join(SAIDAS, "sus_resumo.json"),
        ])
    else:
        print(f"\n[i] Frente C pulada: {args.respostas_sus} não encontrado.")

    # Figuras
    rodar("Geração de figuras", [os.path.join(THIS_DIR, "gerar_graficos.py")])

    print("\n" + "=" * 74)
    print("PRONTO. Saídas em tests/saidas/ e figuras em docs/figuras/.")
    print("=" * 74)


if __name__ == "__main__":
    main()
