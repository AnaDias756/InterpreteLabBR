import os
from backend.services.pdf_parser import extract_lab_values

def test_extract_lab_values():
    caminho_pdf = "tests/exemplos/Laudo_Exemplo.pdf"
    if not os.path.exists(caminho_pdf):
        print(f"⚠️ Arquivo de teste não encontrado: {caminho_pdf}")
        return

    resultados = extract_lab_values(caminho_pdf)
    assert isinstance(resultados, list)
    assert any(r["analito"] == "Hemoglobina" for r in resultados)
    print("✅ Teste de extração executado com sucesso! Resultados:", resultados)