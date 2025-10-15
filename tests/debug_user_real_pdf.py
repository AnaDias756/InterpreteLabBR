#!/usr/bin/env python3
"""
Debug do PDF real do usuário para Eosinófilos.

Uso:
  python tests/debug_user_real_pdf.py "caminho/para/laudo.pdf"

O script:
- Extrai texto com PyPDF2 e, se necessário, com OCR do backend
- Busca por "Eosinófilos" e mostra contexto
- Testa TODOS os padrões de Eosinófilos de data/patterns.csv
- Executa extract_lab_values para ver o valor normalizado
"""
import sys
import os
from pathlib import Path
import re
import csv

# Garantir root no path
sys.path.insert(0, str(Path.cwd()))

from typing import List, Dict, Tuple


def print_header(title: str):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def extract_text_pypdf2(pdf_path: str) -> str:
    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(pdf_path)
        texts = []
        for page in reader.pages:
            t = page.extract_text() or ""
            if t:
                texts.append(t)
        return "\n".join(texts)
    except Exception as e:
        print(f"⚠️ Erro PyPDF2: {e}")
        return ""


def extract_text_backend_ocr(pdf_path: str) -> str:
    try:
        from backend.services.pdf_parser import extract_text_with_ocr
        return extract_text_with_ocr(pdf_path)
    except Exception as e:
        print(f"⚠️ Erro OCR: {e}")
        return ""


def load_patterns() -> List[Dict[str, str]]:
    patterns_path = Path("data/patterns.csv")
    assert patterns_path.exists(), f"Arquivo não encontrado: {patterns_path}"
    patterns: List[Dict[str, str]] = []
    with open(patterns_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            grupo = row.get("grupo_decimal") or row.get("grupo") or "1"
            try:
                grupo_idx = int(grupo)
            except Exception:
                grupo_idx = 1
            patterns.append({
                "analito": row["analito"],
                "pattern": row["pattern"],
                "grupo": grupo_idx,
            })
    return patterns


def check_eos_patterns(full_text: str) -> List[Tuple[str, bool, Tuple[str, ...], str, float]]:
    """Retorna lista com detalhes de (analito, encontrado, grupos, valor_str, valor_float|nan)."""
    results = []
    for p in load_patterns():
        if "eosinofilos" not in p["analito"].lower():
            continue
        try:
            r = re.search(p["pattern"], full_text, re.IGNORECASE | re.DOTALL)
            if r:
                valor_str = r.group(p["grupo"]) if r.groups() else None
                valor_proc = (valor_str or "").replace(",", ".")
                try:
                    valor_float = float(valor_proc)
                except Exception:
                    valor_float = float("nan")
                results.append((p["analito"], True, r.groups(), valor_str or "", valor_float))
            else:
                results.append((p["analito"], False, tuple(), "", float("nan")))
        except Exception as e:
            print(f"  ⚠️ erro regex em {p['analito']}: {e}")
    return results


def show_context(full_text: str, needle: str, radius: int = 120) -> str:
    idx = full_text.lower().find(needle.lower())
    if idx == -1:
        return "(termo não encontrado no texto)"
    start = max(0, idx - radius)
    end = min(len(full_text), idx + len(needle) + radius)
    return full_text[start:end]


def run_extract_lab_values(pdf_path: str):
    from backend.services.pdf_parser import extract_lab_values, validate_pdf
    is_valid, err = validate_pdf(pdf_path)
    if not is_valid:
        print("PDF inválido:", err)
        return []
    return extract_lab_values(pdf_path)


def main():
    if len(sys.argv) < 2:
        print("Uso: python tests/debug_user_real_pdf.py \"caminho/para/laudo.pdf\"")
        sys.exit(1)

    pdf_path = sys.argv[1]
    if not os.path.exists(pdf_path):
        print(f"❌ Arquivo não encontrado: {pdf_path}")
        sys.exit(2)

    print_header("Extração de texto (PyPDF2)")
    text = extract_text_pypdf2(pdf_path)
    if len(text.strip()) < 60:
        print("Texto muito curto, tentando OCR do backend...")
        text = extract_text_backend_ocr(pdf_path)

    print(text[:500])

    print_header("Presença de termos")
    termos = ["Eosinófilos", "eosinofilos", "µL", "/µL", "%", "11,5", "802"]
    for t in termos:
        print(f"- contém '{t}':", t in text)

    print_header("Contexto onde aparece 'Eosinófilos'")
    print(show_context(text, "Eosinófilos"))

    print_header("Testando padrões de Eosinófilos (data/patterns.csv)")
    detalhados = check_eos_patterns(text)
    algum_match = False
    for analito, ok, groups, valor_str, valor_float in detalhados:
        print(f"- {analito}: encontrado={ok}")
        if ok:
            algum_match = True
            print(f"  grupos={groups}")
            print(f"  valor_str={valor_str}")
            print(f"  valor_float={valor_float}")

    print_header("Executando extract_lab_values do backend")
    resultados = run_extract_lab_values(pdf_path)
    mapa = {i["analito"].lower(): i["valor"] for i in resultados}
    for item in resultados:
        print(f"✅ {item['analito']} = {item['valor']}")
    print("Presença eosinofilos=", "eosinofilos" in mapa)

    print_header("Resumo")
    if "eosinofilos" in mapa:
        print("✅ Eosinófilos extraídos e normalizados:", mapa["eosinofilos"])
    elif algum_match:
        print("⚠️ Há match de padrões, mas não houve normalização/extract final. Verificar normalizador.")
    else:
        print("❌ Nenhum match de padrão para Eosinófilos. Precisamos ajustar regex conforme texto real.")


if __name__ == "__main__":
    main()