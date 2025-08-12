import re
import csv
import io
import os
import glob
from PyPDF2 import PdfReader

# Importar a função de OCR do parser principal
try:
    from backend.services.pdf_parser import extract_text_with_ocr
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    print("⚠️ OCR não disponível")

def debug_pdf_extraction(pdf_path=None):
    print("🔍 DIAGNÓSTICO DE EXTRAÇÃO DE PDF")
    print("=" * 50)
    
    # Se não foi especificado um PDF, procurar na pasta atual
    if pdf_path is None:
        pdf_files = glob.glob("*.pdf")
        if not pdf_files:
            print("❌ Nenhum arquivo PDF encontrado na pasta atual")
            return
        
        pdf_path = pdf_files[0]
        print(f"📁 Usando arquivo: {pdf_path}")
    
    # 1. Extrair texto completo
    try:
        with open(pdf_path, 'rb') as file:
            reader = PdfReader(file)
            full_text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
        
        print(f"📄 Extração padrão: {len(full_text)} caracteres")
        
        # Se pouco texto e OCR disponível, tentar OCR
        if len(full_text.strip()) < 50 and OCR_AVAILABLE:
            print("🔍 Texto insuficiente, tentando OCR...")
            ocr_text = extract_text_with_ocr(pdf_path)
            if len(ocr_text.strip()) > len(full_text.strip()):
                full_text = ocr_text
                print(f"✅ OCR extraiu {len(full_text)} caracteres")
        
        print("✅ PDF lido com sucesso!")
        print(f"📄 Texto extraído ({len(full_text)} caracteres):")
        print("-" * 30)
        print(full_text[:800] + "..." if len(full_text) > 800 else full_text)
        print("-" * 30)
        
    except Exception as e:
        print(f"❌ Erro ao ler PDF: {e}")
        return
    
    # 2. Testar padrões atualizados baseados no PDF mostrado
    patterns = [
        ("hemacias", r"(?:Eritrócitos|Hemácias)\s+([0-9]+,[0-9]+)"),
        ("hemoglobina", r"Hemoglobina\s+([0-9]+,[0-9]+)"),
        ("hematocrito", r"Hemat[óo]crito\s+([0-9]+,[0-9]+)"),
        ("vcm", r"V\.?C\.?M\.?\s+([0-9]+,[0-9]+)"),
        ("hcm", r"H\.?C\.?M\.?\s+([0-9]+,[0-9]+)"),
        ("chcm", r"C\.?H\.?C\.?M\.?\s+([0-9]+,[0-9]+)"),
        ("rdw", r"R\.?D\.?W\.?\s+([0-9]+,[0-9]+)"),
        ("leucocitos", r"Leucó[cç]itos\s+([0-9]+\.?[0-9]*(?:,[0-9]+)?)(?:\s|/|$)"),
        # Padrões alternativos mais flexíveis
        ("hemacias_alt", r"Hemácias\s+([0-9]+,[0-9]+)\s+milhões"),
        ("hemoglobina_alt", r"Hemoglobina\s+([0-9]+,[0-9]+)\s+g/dL"),
        ("leucocitos_alt", r"Leucócitos\s+([0-9]+\.[0-9]+)\s+/mm"),
    ]
    
    print("\n🧪 TESTANDO PADRÕES:")
    print("=" * 30)
    
    resultados = []
    for analito, pattern in patterns:
        try:
            match = re.search(pattern, full_text, re.IGNORECASE | re.DOTALL)
            if match:
                valor = match.group(1)
                print(f"✅ {analito}: {valor}")
                resultados.append((analito, valor))
            else:
                print(f"❌ {analito}: NÃO ENCONTRADO")
                # Buscar variações próximas
                palavras_chave = {
                    "hemacias": ["hemácias", "eritrócitos", "hemacias"],
                    "hemoglobina": ["hemoglobina", "hb"],
                    "hematocrito": ["hematócrito", "hematocrito", "ht"],
                    "vcm": ["vcm", "v.c.m", "v c m"],
                    "hcm": ["hcm", "h.c.m", "h c m"],
                    "chcm": ["chcm", "c.h.c.m", "c h c m"],
                    "rdw": ["rdw", "r.d.w", "r d w"],
                    "leucocitos": ["leucócitos", "leucocitos", "leuco"]
                }
                
                base_analito = analito.replace('_alt', '')
                for palavra in palavras_chave.get(base_analito, []):
                    if palavra.lower() in full_text.lower():
                        # Encontrar contexto
                        idx = full_text.lower().find(palavra.lower())
                        contexto = full_text[max(0, idx-30):idx+80]
                        print(f"   💡 Encontrado '{palavra}' em: ...{contexto}...")
                        break
        except Exception as e:
            print(f"⚠️ {analito}: ERRO no padrão - {e}")
    
    print(f"\n📊 RESUMO: {len(resultados)} analitos extraídos de {len(patterns)} testados")
    
    if len(resultados) == 0:
        print("\n🚨 NENHUM VALOR EXTRAÍDO!")
        print("💡 Possíveis causas:")
        print("   1. Formato do PDF diferente do esperado")
        print("   2. Texto não está sendo extraído corretamente")
        print("   3. Padrões regex precisam ser ajustados")
        
        # Análise linha por linha
        print("\n🔍 ANÁLISE LINHA POR LINHA:")
        linhas = full_text.split('\n')
        for i, linha in enumerate(linhas):
            linha_clean = linha.strip()
            if linha_clean and any(palavra in linha_clean.lower() for palavra in 
                                 ['hemácias', 'hemoglobina', 'leucócitos', 'hematócrito', 'vcm', 'hcm', 'rdw']):
                print(f"   Linha {i+1}: {linha_clean}")
    
    return resultados

if __name__ == "__main__":
    # Usar o arquivo de exemplo específico
    debug_pdf_extraction("tests/exemplos/Laudo_Exemplo.pdf")