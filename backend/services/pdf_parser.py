import re
import csv
from PyPDF2 import PdfReader
from typing import List

def extract_lab_values(pdf_path: str, patterns_path: str = "data/patterns.csv") -> List[dict]:
    # Extrai texto do PDF
    reader = PdfReader(pdf_path)
    full_text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())

    # Lê os padrões do CSV
    patterns = []
    with open(patterns_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            patterns.append({
                "analito": row["analito"],
                "pattern": row["pattern"],
                "grupo": int(row["grupo_decimal"])
            })

    # Aplica os padrões
    resultados = []
    for item in patterns:
        match = re.search(item["pattern"], full_text, re.IGNORECASE | re.DOTALL)
        if match:
            valor_str = match.group(item["grupo"]).replace(".", "").replace(",", ".")
            try:
                valor = float(valor_str)
                resultados.append({
                    "analito": item["analito"],
                    "valor": valor
                })
            except ValueError:
                pass  # ignora se não conseguir converter

    return resultados