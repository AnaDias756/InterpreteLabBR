#!/usr/bin/env python3
"""
Teste de debug: verifica extração de PDF real do usuário.
- Gera o PDF de exemplo com 'Eosinófilos 11,5 % 802 /µL'.
- Lê e imprime o texto cru extraído do PDF.
- Aplica os padrões e imprime matches detalhados, especialmente para Eosinófilos.
- Verifica encoding e caracteres especiais como 'µ', 'ó'.
"""
import sys
import os
from pathlib import Path
import re

# Garantir root no path
sys.path.insert(0, str(Path.cwd()))


def print_header(title: str):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def main():
    # 1) Gerar PDF com formato exato
    from generate_sample_pdf import main as gerar_pdf
    gerar_pdf()
    pdf_arg = sys.argv[1] if len(sys.argv) > 1 else None
    pdf_path = Path(pdf_arg) if pdf_arg else Path("tests/exemplos/hemograma_tabela.pdf")
    assert pdf_path.exists(), f"PDF não encontrado/gerado: {pdf_path}"

    # 2) Extrair texto cru usando o parser internamente
    from backend.services.pdf_parser import extract_lab_values, validate_pdf, extract_text_with_ocr
    is_valid, err = validate_pdf(str(pdf_path))
    if not is_valid:
        print_header("PDF inválido")
        print(err)
        raise SystemExit(1)

    # Vamos tentar extrair texto via PyPDF2 diretamente
    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(str(pdf_path))
        full_text = "\n".join(filter(None, (page.extract_text() or "") for page in reader.pages))
    except Exception as e:
        print_header("Erro PyPDF2")
        print(e)
        full_text = ""

    if len(full_text.strip()) < 50:
        # fallback OCR
        full_text = extract_text_with_ocr(str(pdf_path))

    print_header("Texto extraído (primeiros 800 chars)")
    print(full_text[:800])

    # 3) Carregar padrões e checar matches
    patterns_csv = Path("data/patterns.csv")
    assert patterns_csv.exists(), "Arquivo data/patterns.csv não encontrado"

    import csv
    patterns = []
    with open(patterns_csv, newline="", encoding="utf-8") as f:
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
                "grupo": grupo_idx
            })

    print_header("Checando padrão específico de Eosinófilos")
    eos_patterns = [p for p in patterns if "eosinofilos" in p["analito"].lower()]
    for p in eos_patterns:
        try:
            r = re.search(p["pattern"], full_text, re.IGNORECASE | re.DOTALL)
            print(f"- {p['analito']}: encontrado={bool(r)}")
            if r:
                valor_str = r.group(p["grupo"]) if r.groups() else None
                print(f"  pattern={p['pattern']}")
                print(f"  grupos={r.groups()}")
                print(f"  valor_str={valor_str}")
                # Conversão semelhante ao parser
                valor_processado = (valor_str or "").replace(",", ".")
                try:
                    valor = float(valor_processado)
                    print(f"  valor_float={valor}")
                except Exception as e:
                    print(f"  erro_float={e}")
        except Exception as e:
            print(f"  ⚠️ erro regex: {e}")

    print_header("Executando extract_lab_values")
    resultados = extract_lab_values(str(pdf_path))
    for item in resultados:
        print(f"✅ {item['analito']} = {item['valor']}")

    # 4) Verificações de presença e encoding
    print_header("Verificações de encoding e termos")
    checks = [
        "Eosinófilos", "eosinofilos", "µL", "/µL", "%", "11,5", "802"
    ]
    for chk in checks:
        print(f"- contém '{chk}': {chk in full_text}")

    # 5) Assegurar que eosinofilos normalizado aparece
    mapa = {i["analito"].lower(): i["valor"] for i in resultados}
    ok = "eosinofilos" in mapa and abs(mapa["eosinofilos"] - 802.0) < 0.1
    print_header("Resumo")
    if ok:
        print("✅ Eosinófilos extraídos e normalizados: 802 /µL")
        return
    else:
        print("❌ Eosinófilos não normalizado/extraído. Veja logs acima.")
        raise SystemExit(1)


if __name__ == "__main__":
    main()