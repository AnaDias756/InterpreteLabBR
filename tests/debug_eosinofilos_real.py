#!/usr/bin/env python3
"""
Teste de debug focado: Eosinófilos com formato real do usuário.
- Gera PDFs contendo linhas específicas de "Eosinófilos" com 3 variações:
  1) "Eosinófilos 11,5 % 802 /µL"
  2) "Eosinófilos 11,5 % 802/µL" (sem espaço antes de /µL)
  3) "Eosinófilos 11,5% 802/µL" (sem espaço entre 11,5 e %)
- Extrai texto cru; aplica regex de data/patterns.csv; imprime matches, grupos e valor capturado.
- Valida se o analito normalizado "eosinofilos" aparece em extract_lab_values com valor ~802.
"""
import os
import sys
from pathlib import Path
import re

# Garantir root no path
sys.path.insert(0, str(Path.cwd()))

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm


def print_header(title: str):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def gerar_pdf_eosinofilos(texto: str, nome_arquivo: str):
    out_dir = os.path.join(os.getcwd(), "tests", "exemplos")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, nome_arquivo)

    c = canvas.Canvas(out_path, pagesize=A4)
    w, h = A4

    c.setFont("Helvetica-Bold", 14)
    c.drawString(20*mm, h - 20*mm, "Hemograma - Debug Eosinófilos")

    c.setFont("Helvetica", 11)
    y = h - 40*mm
    # Simplesmente escreve a linha alvo e algumas linhas de contexto
    c.drawString(20*mm, y, "Série Branca")
    y -= 8*mm
    c.drawString(20*mm, y, "Parâmetro")
    c.drawString(80*mm, y, "RESULTADO")
    y -= 8*mm
    c.drawString(20*mm, y, texto)  # Linha com Eosinófilos

    c.showPage()
    c.save()
    return out_path


def extrair_texto_pypdf2(pdf_path: str) -> str:
    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(pdf_path)
        textos = [page.extract_text() or "" for page in reader.pages]
        textos = [t for t in textos if t]
        return "\n".join(textos)
    except Exception as e:
        print(f"⚠️ Erro PyPDF2: {e}")
        return ""


def carregar_padroes():
    import csv
    patterns_path = Path("data/patterns.csv")
    assert patterns_path.exists(), "Arquivo data/patterns.csv não encontrado"
    patterns = []
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
                "grupo": grupo_idx
            })
    return patterns


def checar_padroes(full_text: str):
    print_header("Checando padrões de Eosinófilos")
    patterns = carregar_padroes()
    eos_patterns = [p for p in patterns if "eosinofilos" in p["analito"].lower()]
    algum_match = False
    for p in eos_patterns:
        try:
            r = re.search(p["pattern"], full_text, re.IGNORECASE | re.DOTALL)
            print(f"- {p['analito']}: encontrado={bool(r)}")
            if r:
                algum_match = True
                valor_str = r.group(p["grupo"]) if r.groups() else None
                print(f"  pattern={p['pattern']}")
                print(f"  grupos={r.groups()}")
                print(f"  valor_str={valor_str}")
                valor_processado = (valor_str or "").replace(",", ".")
                try:
                    valor = float(valor_processado)
                    print(f"  valor_float={valor}")
                except Exception as e:
                    print(f"  erro_float={e}")
        except Exception as e:
            print(f"  ⚠️ erro regex: {e}")
    return algum_match


def validar_extract_lab_values(pdf_path: str):
    print_header("Executando extract_lab_values")
    from backend.services.pdf_parser import extract_lab_values, validate_pdf, extract_text_with_ocr
    is_valid, err = validate_pdf(pdf_path)
    if not is_valid:
        print("PDF inválido:", err)
        return False

    resultados = extract_lab_values(pdf_path)
    for item in resultados:
        print(f"✅ {item['analito']} = {item['valor']}")
    mapa = {i["analito"].lower(): i["valor"] for i in resultados}
    ok = "eosinofilos" in mapa and abs(mapa["eosinofilos"] - 802.0) < 0.1
    print("Presença eosinofilos=", "eosinofilos" in mapa)
    return ok


def debug_variacao(texto: str, nome: str):
    print_header(f"Gerando PDF: {nome}")
    pdf_path = gerar_pdf_eosinofilos(texto, nome)
    print("PDF:", pdf_path)

    txt = extrair_texto_pypdf2(pdf_path)
    if len(txt.strip()) < 50:
        from backend.services.pdf_parser import extract_text_with_ocr
        txt = extract_text_with_ocr(pdf_path)

    print_header("Texto extraído (primeiros 500 chars)")
    print(txt[:500])

    matched = checar_padroes(txt)
    ok = validar_extract_lab_values(pdf_path)

    print_header("Resumo")
    if matched and ok:
        print("✅ Match de padrões e extração normalizada OK para", nome)
    else:
        print("❌ Falha em match ou extração para", nome)


def main():
    # Variação 1: formato exato do usuário
    debug_variacao("Eosinófilos 11,5 % 802 /µL", "eos_exato.pdf")
    # Variação 2: sem espaço antes de /µL
    debug_variacao("Eosinófilos 11,5 % 802/µL", "eos_sem_espaco_unidade.pdf")
    # Variação 3: sem espaço no %
    debug_variacao("Eosinófilos 11,5% 802/µL", "eos_sem_espaco_percentual.pdf")


if __name__ == "__main__":
    main()