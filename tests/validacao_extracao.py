#!/usr/bin/env python3
"""
Harness de Validação da Extração (Frente A do TCC)
==================================================

Mede a acurácia da extração automática de valores laboratoriais a partir de
laudos em PDF, comparando o que o sistema extrai com um GABARITO conferido
manualmente.

Uso:
    python tests/validacao_extracao.py
    python tests/validacao_extracao.py --gabarito tests/gabarito_exemplo.json \
                                       --laudos tests/exemplos \
                                       --relatorio relatorio_extracao.csv

Formato do gabarito (JSON): mapeia o nome do arquivo PDF para os valores
verdadeiros de cada analito (use os nomes-base: hemacias, hemoglobina,
hematocrito, vcm, hcm, chcm, rdw, leucocitos, neutrofilos, eosinofilos,
basofilos, linfocitos, monocitos, plaquetas).

    {
      "hemograma_tabela.pdf": {
        "hemacias": 4.43, "hemoglobina": 14.6, "leucocitos": 6970, ...
      }
    }

PRIVACIDADE/LGPD: laudos reais com dados pessoais NÃO devem ser versionados.
Coloque-os em uma pasta ignorada pelo Git (ex.: tests/laudos/) e aponte o
parâmetro --laudos para ela. O exemplo sintético (tests/exemplos) não contém
dados pessoais e serve para demonstrar o método.
"""
import argparse
import csv
import json
import os
import sys

# Permite importar os serviços do backend
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(THIS_DIR)
sys.path.insert(0, os.path.join(PROJECT_ROOT, "backend"))

from services.pdf_parser import extract_lab_values, normalize_analito_name  # noqa: E402
from services.rule_engine import get_display_name  # noqa: E402


def valores_proximos(extraido: float, esperado: float) -> bool:
    """Compara dois valores com tolerância (absoluta e relativa)."""
    return abs(extraido - esperado) <= max(0.01, abs(esperado) * 0.001)


def extrair_dict(caminho_pdf: str) -> dict:
    """Roda a extração e retorna {analito_base: valor}."""
    with open(caminho_pdf, "rb") as f:
        conteudo = f.read()
    resultados = extract_lab_values(conteudo)
    saida = {}
    for r in resultados:
        base = normalize_analito_name(r["analito"])
        # mantém o primeiro valor caso haja duplicidade após normalização
        saida.setdefault(base, r["valor"])
    return saida


def avaliar_laudo(nome: str, esperado: dict, extraido: dict) -> dict:
    """Compara esperado x extraído para um laudo. Retorna métricas e detalhes."""
    detalhes = []
    corretos = ausentes = incorretos = 0

    for analito, val_esperado in esperado.items():
        base = normalize_analito_name(analito)
        if base not in extraido:
            status = "AUSENTE"
            ausentes += 1
            val_extraido = None
        elif valores_proximos(extraido[base], float(val_esperado)):
            status = "OK"
            corretos += 1
            val_extraido = extraido[base]
        else:
            status = "INCORRETO"
            incorretos += 1
            val_extraido = extraido[base]
        detalhes.append({
            "laudo": nome,
            "analito": get_display_name(base),
            "esperado": val_esperado,
            "extraido": val_extraido,
            "status": status,
        })

    # Analitos extraídos que não constam no gabarito (falsos positivos)
    esperado_bases = {normalize_analito_name(a) for a in esperado}
    falsos_positivos = [b for b in extraido if b not in esperado_bases]
    for b in falsos_positivos:
        detalhes.append({
            "laudo": nome,
            "analito": get_display_name(b),
            "esperado": None,
            "extraido": extraido[b],
            "status": "FALSO_POSITIVO",
        })

    total = len(esperado)
    return {
        "total": total,
        "corretos": corretos,
        "ausentes": ausentes,
        "incorretos": incorretos,
        "falsos_positivos": len(falsos_positivos),
        "detalhes": detalhes,
    }


def main():
    parser = argparse.ArgumentParser(description="Validação da extração de hemogramas (Frente A).")
    parser.add_argument("--gabarito", default=os.path.join(THIS_DIR, "gabarito_exemplo.json"),
                        help="Arquivo JSON com os valores verdadeiros por laudo.")
    parser.add_argument("--laudos", default=os.path.join(THIS_DIR, "exemplos"),
                        help="Pasta onde estão os PDFs dos laudos.")
    parser.add_argument("--relatorio", default=None,
                        help="(Opcional) Caminho para salvar um relatório CSV detalhado.")
    args = parser.parse_args()

    with open(args.gabarito, encoding="utf-8") as f:
        gabarito = json.load(f)

    # Gera o exemplo sintético automaticamente se ele não existir (não é versionado)
    exemplo = os.path.join(THIS_DIR, "exemplos", "hemograma_tabela.pdf")
    if args.laudos == os.path.join(THIS_DIR, "exemplos") and not os.path.exists(exemplo):
        try:
            sys.path.insert(0, PROJECT_ROOT)
            import generate_sample_pdf
            generate_sample_pdf.main()
        except Exception as e:
            print(f"[!] Não foi possível gerar o exemplo sintético: {e}")

    todos_detalhes = []
    tot = dict(total=0, corretos=0, ausentes=0, incorretos=0, falsos_positivos=0)
    # Métricas por analito (para identificar os mais problemáticos)
    por_analito = {}

    print("=" * 64)
    print("VALIDAÇÃO DA EXTRAÇÃO — Frente A")
    print("=" * 64)

    for nome, esperado in gabarito.items():
        caminho = os.path.join(args.laudos, nome)
        if not os.path.exists(caminho):
            print(f"\n[!] Laudo não encontrado: {caminho} (pulando)")
            continue

        try:
            extraido = extrair_dict(caminho)
        except Exception as e:
            print(f"\n[!] Erro ao processar {nome}: {e}")
            continue

        res = avaliar_laudo(nome, esperado, extraido)
        todos_detalhes.extend(res["detalhes"])
        for k in tot:
            tot[k] += res[k]

        print(f"\nLaudo: {nome}")
        print(f"  {'Analito':<14}{'Esperado':>12}{'Extraído':>12}   Status")
        print(f"  {'-'*14}{'-'*12:>12}{'-'*12:>12}   {'-'*13}")
        for d in res["detalhes"]:
            ext = "—" if d["extraido"] is None else d["extraido"]
            esp = "—" if d["esperado"] is None else d["esperado"]
            print(f"  {d['analito']:<14}{str(esp):>12}{str(ext):>12}   {d['status']}")
            # acumula por analito
            a = por_analito.setdefault(d["analito"], {"ok": 0, "total": 0})
            if d["status"] != "FALSO_POSITIVO":
                a["total"] += 1
                if d["status"] == "OK":
                    a["ok"] += 1
        acc = res["corretos"] / res["total"] * 100 if res["total"] else 0
        print(f"  -> {res['corretos']}/{res['total']} corretos ({acc:.0f}%) | "
              f"ausentes: {res['ausentes']} | incorretos: {res['incorretos']} | "
              f"falsos+: {res['falsos_positivos']}")

    # --- Agregado ---
    print("\n" + "=" * 64)
    print("RESUMO AGREGADO")
    print("=" * 64)
    total = tot["total"]
    corretos = tot["corretos"]
    acuracia = corretos / total * 100 if total else 0
    # Precisão = corretos / (corretos + incorretos + falsos+); Recall = corretos / esperados
    denom_prec = corretos + tot["incorretos"] + tot["falsos_positivos"]
    precisao = corretos / denom_prec if denom_prec else 0
    recall = corretos / total if total else 0
    f1 = (2 * precisao * recall / (precisao + recall)) if (precisao + recall) else 0

    print(f"Laudos avaliados......: {len(gabarito)}")
    print(f"Analitos esperados....: {total}")
    print(f"Acurácia de extração..: {corretos}/{total} ({acuracia:.1f}%)")
    print(f"Precisão..............: {precisao:.3f}")
    print(f"Recall................: {recall:.3f}")
    print(f"F1....................: {f1:.3f}")
    print(f"Ausentes..............: {tot['ausentes']}")
    print(f"Incorretos............: {tot['incorretos']}")
    print(f"Falsos positivos......: {tot['falsos_positivos']}")

    print("\nDesempenho por analito (acertos/total):")
    for analito, a in sorted(por_analito.items()):
        taxa = a["ok"] / a["total"] * 100 if a["total"] else 0
        print(f"  {analito:<14} {a['ok']}/{a['total']} ({taxa:.0f}%)")

    if args.relatorio:
        with open(args.relatorio, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["laudo", "analito", "esperado", "extraido", "status"])
            writer.writeheader()
            writer.writerows(todos_detalhes)
        print(f"\nRelatório detalhado salvo em: {args.relatorio}")


if __name__ == "__main__":
    main()
