#!/usr/bin/env python3
"""
Teste automatizado: extração de PDF em formato de tabela (Hemograma).
Gera um PDF com cabeçalhos 'Série Vermelha' e 'Série Branca', com colunas
'Parâmetro', 'RESULTADO', 'INTERVALO DE REFERÊNCIA', e valida a extração
pelos padrões existentes no sistema.
"""
import sys
import os
from pathlib import Path


def main():
    # Garantir que o diretório raiz esteja no path
    sys.path.insert(0, str(Path.cwd()))

    # Gerar o PDF tabular de exemplo
    from generate_sample_pdf import main as gerar_pdf
    gerar_pdf()

    pdf_path = Path("tests/exemplos/hemograma_tabela.pdf")
    assert pdf_path.exists(), f"PDF não foi gerado: {pdf_path}"

    # Importar parser e extrair valores
    from backend.services.pdf_parser import extract_lab_values
    resultados = extract_lab_values(str(pdf_path))

    # Mapear analitos para valores
    mapa = {item["analito"]: item["valor"] for item in resultados}

    # Esperados com base no PDF gerado
    esperados = {
        "eosinofilos": 802.0,
        "linfocitos": 2216.0,
        "neutrofilos": 3548.0,
        "plaquetas": 282000.0,
        "leucocitos": 6970.0,
        "rdw": 11.8,
    }

    faltando = []
    divergencias = []

    for analito, valor_esp in esperados.items():
        if analito not in mapa:
            faltando.append(analito)
        else:
            valor = mapa[analito]
            # Tolerância mínima para floats
            if abs(valor - valor_esp) > 0.05:
                divergencias.append((analito, valor, valor_esp))

    if faltando:
        print(f"❌ Analitos não extraídos: {', '.join(faltando)}")
        raise SystemExit(1)

    if divergencias:
        print("❌ Valores divergentes:")
        for a, v, e in divergencias:
            print(f"- {a}: extraído={v} esperado={e}")
        raise SystemExit(1)

    print("✅ Extração OK: todos os analitos e valores conferem.")


if __name__ == "__main__":
    main()

