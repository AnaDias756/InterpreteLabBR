import re
import csv
import io
from PyPDF2 import PdfReader
from typing import List, Union

# Tentar importar dependências de OCR
try:
    import fitz  # PyMuPDF
    from PIL import Image
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    print("⚠️ OCR não disponível. Instale: pip install PyMuPDF pillow pytesseract")

# Configurar caminho do Tesseract no Windows
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_lab_values(pdf_content: Union[str, bytes], patterns_path: str = "data/patterns.csv") -> List[dict]:
    # Tentativa 1: Extração padrão
    if isinstance(pdf_content, bytes):
        reader = PdfReader(io.BytesIO(pdf_content))
    else:
        reader = PdfReader(pdf_content)
    
    full_text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
    
    # Se não conseguiu extrair texto suficiente, tenta OCR
    if len(full_text.strip()) < 50 and OCR_AVAILABLE:
        print("🔍 Texto insuficiente, tentando OCR...")
        full_text = extract_text_with_ocr(pdf_content)
    
    if len(full_text.strip()) == 0:
        raise Exception("Não foi possível extrair texto do PDF. Verifique se o arquivo não está corrompido ou protegido.")
    
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
            if "." in valor_str and item["analito"].lower() in ["leucocitos", "neutrófilos", "linfócitos"]:
                partes = valor_str.split(".")
                if len(partes) == 2 and len(partes[1]) == 3 and int(partes[0]) < 100 and "," not in valor_str:
                    # Para leucócitos, ponto é separador de milhares, não decimal
                    valor_str = valor_str.replace(".", "")  # 9.480 → 9480 (valor correto)
            
            # Para plaquetas, vírgula é sempre separador de milhares
            if "," in valor_str and item["analito"].lower() == "plaquetas":
                valor_str = valor_str.replace(",", "")
            
            # Para plaquetas, ponto também pode ser separador de milhares
            if "." in valor_str and item["analito"].lower() == "plaquetas":
                partes = valor_str.split(".")
                if len(partes) == 2 and len(partes[1]) == 3:  # formato xxx.xxx
                    valor_str = valor_str.replace(".", "")  # 256.108 → 256108
            
            # Processamento padrão (agora sem conversão desnecessária)
            valor_processado = valor_str.replace(",", ".")  # Apenas vírgula → ponto para decimais
            
            try:
                valor = float(valor_processado)
                resultados.append({
                    "analito": item["analito"],
                    "valor": valor
                })
            except ValueError:
                pass

    return resultados

def extract_text_with_ocr(pdf_content: Union[str, bytes]) -> str:
    """
    Extrai texto usando OCR como fallback
    """
    if not OCR_AVAILABLE:
        return ""
    
    try:
        if isinstance(pdf_content, bytes):
            doc = fitz.open(stream=pdf_content, filetype="pdf")
        else:
            doc = fitz.open(pdf_content)
        
        full_text = ""
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            
            # Tenta extrair texto primeiro
            page_text = page.get_text()
            if len(page_text.strip()) > 10:
                full_text += page_text + "\n"
            else:
                # OCR como último recurso
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                img_data = pix.tobytes("ppm")
                img = Image.open(io.BytesIO(img_data))
                ocr_text = pytesseract.image_to_string(img, lang='eng')  # Mudança: 'por' para 'eng'
                full_text += ocr_text + "\n"
        
        doc.close()
        return full_text
        
    except Exception as e:
        print(f"Erro no OCR: {e}")
        return ""