import re
import csv
import io
from PyPDF2 import PdfReader
from typing import List, Union

def extract_lab_values(pdf_content: Union[str, bytes], patterns_path: str = "data/patterns.csv") -> List[dict]:
    # Extrai texto do PDF
    if isinstance(pdf_content, bytes):
        reader = PdfReader(io.BytesIO(pdf_content))
    else:
        reader = PdfReader(pdf_content)
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
            valor_str = match.group(item["grupo"])
            
            # Para série branca (leucócitos, neutrófilos, linfócitos) com valores decimais
            # Se o valor tem ponto e é menor que 100.000, trata como separador decimal
            if "." in valor_str and item["analito"].lower() in ["leucocitos", "neutrófilos", "linfócitos"]:
                # Verifica se é um valor decimal (ex: 9.480) vs milhares (ex: 9.480.100,0)
                partes = valor_str.split(".")
                # Se tem apenas um ponto, 3 dígitos após o ponto, e valor antes do ponto < 100
                if len(partes) == 2 and len(partes[1]) == 3 and int(partes[0]) < 100 and "," not in valor_str:
                    # Provavelmente é decimal (ex: 9.480), converte ponto para vírgula
                    valor_str = valor_str.replace(".", ",")
            
            # Processamento padrão: remove pontos (separadores de milhares) e converte vírgulas para pontos decimais
            valor_processado = valor_str.replace(".", "").replace(",", ".")
            
            try:
                valor = float(valor_processado)
                resultados.append({
                    "analito": item["analito"],
                    "valor": valor
                })
            except ValueError:
                pass  # ignora se não conseguir converter

    return resultados