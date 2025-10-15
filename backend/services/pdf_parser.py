import re
import csv
import io
import os
import logging
import unicodedata
from PyPDF2 import PdfReader
from PyPDF2.errors import PdfReadError
from typing import List, Union

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Tentar importar dependências de OCR
try:
    import fitz  # PyMuPDF
    from PIL import Image, ImageEnhance, ImageFilter, ImageOps
    import pytesseract
    import numpy as np
    import cv2
    OCR_AVAILABLE = True
    logger.info("✅ Dependências OCR carregadas com sucesso")
except ImportError as e:
    OCR_AVAILABLE = False
    logger.warning(f"⚠️ OCR não disponível: {e}. Instale: pip install PyMuPDF pillow pytesseract opencv-python numpy")

# Configurar caminho do Tesseract no Windows
if OCR_AVAILABLE:
    tesseract_paths = [
        r'C:\Program Files\Tesseract-OCR\tesseract.exe',
        r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
        'tesseract'  # Para sistemas com tesseract no PATH
    ]
    
    tesseract_found = False
    for path in tesseract_paths:
        if os.path.exists(path) or path == 'tesseract':
            try:
                pytesseract.pytesseract.tesseract_cmd = path
                # Teste rápido
                pytesseract.get_tesseract_version()
                tesseract_found = True
                logger.info(f"✅ Tesseract configurado: {path}")
                break
            except Exception:
                continue
    
    if not tesseract_found:
        OCR_AVAILABLE = False
        logger.warning("⚠️ Tesseract não encontrado. OCR desabilitado.")

def validate_pdf(pdf_content: Union[str, bytes]) -> tuple[bool, str]:
    """
    Valida se o PDF é válido e pode ser processado
    Retorna: (is_valid, error_message)
    """
    try:
        if isinstance(pdf_content, bytes):
            if len(pdf_content) < 100:
                return False, "Arquivo muito pequeno para ser um PDF válido"
            
            # Verificar assinatura PDF
            if not pdf_content.startswith(b'%PDF-'):
                return False, "Arquivo não possui assinatura PDF válida"
            
            reader = PdfReader(io.BytesIO(pdf_content))
        else:
            if not os.path.exists(pdf_content):
                return False, "Arquivo não encontrado"
            
            reader = PdfReader(pdf_content)
        
        # Verificar se o PDF está protegido
        if reader.is_encrypted:
            return False, "PDF protegido por senha. Remova a proteção antes de enviar."
        
        # Verificar se tem páginas
        if len(reader.pages) == 0:
            return False, "PDF não contém páginas"
        
        # Tentar acessar a primeira página
        try:
            first_page = reader.pages[0]
            first_page.extract_text()
        except Exception as e:
            return False, f"Erro ao acessar conteúdo do PDF: {str(e)}"
        
        logger.info(f"✅ PDF válido com {len(reader.pages)} página(s)")
        return True, ""
        
    except PdfReadError as e:
        return False, f"PDF corrompido ou inválido: {str(e)}"
    except Exception as e:
        return False, f"Erro inesperado na validação: {str(e)}"

def normalize_analito_name(analito: str) -> str:
    """Normaliza nomes de analitos para deduplicação"""
    analito_lower = analito.lower()
    
    # Mapeamento de nomes alternativos para nomes padrão
    mapeamento = {
        'plaquetas_alt': 'plaquetas',
        'plaquetas_alt2': 'plaquetas',
        'plaquetas_ponto': 'plaquetas',
        'plaquetas_ponto_alt': 'plaquetas',
        'plaquetas_formato_exato': 'plaquetas',
        'hemacias_alt': 'hemacias',
        'leucocitos_novo': 'leucocitos',
        'neutrofilos_novo': 'neutrofilos',
        'eosinofilos_novo': 'eosinofilos',
        'eosinofilos_formato_exato': 'eosinofilos',
        'eosinofilos_compacto': 'eosinofilos',
        'eosinofilos_spaced': 'eosinofilos',
        'eosinofilos_fragmentado': 'eosinofilos',
        'eosinofilos_space_tolerant': 'eosinofilos',
         'eosinofilos_reverse': 'eosinofilos',
         'eosinofilos_flex': 'eosinofilos',
         'eosinofilos_percent_only': 'eosinofilos',
         'eosinofilos_percent_fragmentado': 'eosinofilos',
        'basofilos_novo': 'basofilos',
        'linfocitos_novo': 'linfocitos',
        'monocitos_novo': 'monocitos',
        'leucocitos_hemograma': 'leucocitos',
        'neutrofilos_hemograma': 'neutrofilos',
        'eosinofilos_hemograma': 'eosinofilos',
        'eosinofilos_hemograma_alt': 'eosinofilos',
        'basofilos_hemograma': 'basofilos',
        'linfocitos_hemograma': 'linfocitos',
        'monocitos_hemograma': 'monocitos'
    }
    
    return mapeamento.get(analito_lower, analito_lower)

def deduplicate_analitos(resultados: List[dict]) -> List[dict]:
    """Remove analitos duplicados, mantendo apenas um por tipo normalizado"""
    analitos_unicos = {}
    
    for resultado in resultados:
        analito_original = resultado['analito']
        analito_normalizado = normalize_analito_name(analito_original)
        valor = resultado['valor']
        
        # Se é o primeiro deste tipo normalizado, adiciona
        if analito_normalizado not in analitos_unicos:
            analitos_unicos[analito_normalizado] = {
                'analito': analito_normalizado,  # Usar nome normalizado
                'valor': valor
            }
        else:
            # Se já existe, verifica se é o mesmo valor
            valor_existente = analitos_unicos[analito_normalizado]['valor']
            if abs(valor - valor_existente) > 0.01:  # Valores diferentes
                logger.warning(f"⚠️ Valores diferentes para {analito_normalizado}: {valor_existente} vs {valor}")
                # Manter o primeiro valor encontrado
            # Se mesmo valor, ignora a duplicata
    
    return list(analitos_unicos.values())

def extract_lab_values(pdf_content: Union[str, bytes], patterns_path: str = None) -> List[dict]:
    # Determinar caminho absoluto do arquivo patterns.csv
    if patterns_path is None:
        import os
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        patterns_path = os.path.join(project_root, "data", "patterns.csv")
    logger.info("🔍 Iniciando extração de valores laboratoriais")
    
    # Validar PDF primeiro
    is_valid, error_msg = validate_pdf(pdf_content)
    if not is_valid:
        logger.error(f"❌ Validação falhou: {error_msg}")
        raise Exception(f"Erro na validação do PDF: {error_msg}")
    
    # Tentativa 1: Extração padrão com PyPDF2
    try:
        if isinstance(pdf_content, bytes):
            reader = PdfReader(io.BytesIO(pdf_content))
        else:
            reader = PdfReader(pdf_content)
        
        full_text = ""
        for i, page in enumerate(reader.pages):
            try:
                page_text = page.extract_text()
                if page_text:
                    full_text += page_text + "\n"
                    logger.info(f"📄 Página {i+1}: {len(page_text)} caracteres extraídos")
                else:
                    logger.warning(f"⚠️ Página {i+1}: Nenhum texto extraído")
            except Exception as e:
                logger.warning(f"⚠️ Erro na página {i+1}: {e}")
                continue
        
        logger.info(f"📝 Total de texto extraído: {len(full_text)} caracteres")
        
    except Exception as e:
        logger.error(f"❌ Erro na extração com PyPDF2: {e}")
        full_text = ""
    
    # Se não conseguiu extrair texto suficiente, tenta OCR
    if len(full_text.strip()) < 50:
        logger.warning("⚠️ Texto insuficiente com PyPDF2")
        if OCR_AVAILABLE:
            logger.info("🔍 Tentando extração com OCR...")
            ocr_text = extract_text_with_ocr(pdf_content)
            if len(ocr_text.strip()) > len(full_text.strip()):
                full_text = ocr_text
                logger.info(f"✅ OCR extraiu {len(full_text)} caracteres")
            else:
                logger.warning("⚠️ OCR não melhorou a extração")
        else:
            logger.error("❌ OCR não disponível para fallback")
    
    if len(full_text.strip()) == 0:
        raise Exception("Não foi possível extrair texto do PDF. Possíveis causas: PDF baseado em imagens sem OCR disponível, arquivo corrompido, ou formato não suportado.")
    
    # Sanitização unicode para normalizar acentos e remover espaços invisíveis
    full_text = sanitize_unicode_text(full_text)
    # Normalização de termos fragmentados antes de aplicar regex
    full_text = normalize_fragmented_terms(full_text)

    # Lê os padrões do CSV
    try:
        patterns = []
        with open(patterns_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                patterns.append({
                    "analito": row["analito"],
                    "pattern": row["pattern"],
                    "grupo": int(row["grupo_decimal"])
                })
        logger.info(f"📋 Carregados {len(patterns)} padrões de análise")
    except FileNotFoundError:
        logger.error(f"❌ Arquivo de padrões não encontrado: {patterns_path}")
        raise Exception(f"Arquivo de configuração não encontrado: {patterns_path}")
    except Exception as e:
        logger.error(f"❌ Erro ao carregar padrões: {e}")
        raise Exception(f"Erro ao carregar configurações: {e}")

    # Aplica os padrões
    resultados = []
    matches_found = 0
    patterns_not_found = []
    
    for item in patterns:
        try:
            match = re.search(item["pattern"], full_text, re.IGNORECASE | re.DOTALL)
            if match:
                matches_found += 1
                valor_str = match.group(item["grupo"])
                logger.debug(f"🎯 {item['analito']}: valor bruto '{valor_str}'")
                
                # Processamento inteligente de separadores de milhares vs decimais
                normalized_name = normalize_analito_name(item["analito"])  # usa mapeamento interno
                if "." in valor_str:
                    partes = valor_str.split(".")
                    if len(partes) == 2 and len(partes[1]) == 3:  # formato X.XXX = separador de milhares
                        # Para leucócitos, neutrófilos, linfócitos, plaquetas: ponto é separador de milhares
                        if normalized_name in ["leucocitos", "neutrofilos", "linfocitos", "plaquetas"]:
                            valor_str = valor_str.replace(".", "")  # 7.010 → 7010, 282.000 → 282000
                
                # Para plaquetas, vírgula é sempre separador de milhares
                if "," in valor_str and normalized_name == "plaquetas":
                    valor_str = valor_str.replace(",", "")  # 282,000 → 282000
                
                # Processamento padrão (agora sem conversão desnecessária)
                valor_processado = valor_str.replace(",", ".")  # Apenas vírgula → ponto para decimais
                
                try:
                    valor = float(valor_processado)
                    resultados.append({
                        "analito": item["analito"],
                        "valor": valor
                    })
                    logger.info(f"✅ Analito encontrado: {item['analito']} = {valor}")
                except ValueError as e:
                    logger.warning(f"⚠️ Erro ao converter '{valor_processado}' para {item['analito']}: {e}")
                    continue
            else:
                # Padrão não encontrou match
                patterns_not_found.append(item['analito'])
                logger.debug(f"❌ Padrão não encontrou match para: {item['analito']} - Pattern: {item['pattern'][:100]}...")
        except Exception as e:
            logger.warning(f"⚠️ Erro ao processar padrão para {item['analito']}: {e}")
            continue
    
    logger.info(f"🎯 Encontrados {matches_found} matches, {len(resultados)} valores válidos extraídos")
    
    # Log dos padrões que não encontraram match
    if patterns_not_found:
        logger.warning(f"❌ Padrões sem match ({len(patterns_not_found)}): {', '.join(patterns_not_found)}")
    
    # Log detalhado do texto extraído para debug (sempre mostrar quando há padrões não encontrados)
    if patterns_not_found or len(resultados) == 0:
        # Mostrar o texto completo para análise
        logger.info(f"📝 Texto extraído COMPLETO para análise ({len(full_text)} chars):\n{full_text}")
        logger.info("="*80)
        
        # Procurar especificamente por termos da série branca no texto
        serie_branca_terms = ['basófilo', 'eosinófilo', 'linfócito', 'monócito', 'neutrófilos']
        found_terms = []
        for term in serie_branca_terms:
            if term.lower() in full_text.lower():
                found_terms.append(term)
        
        if found_terms:
            logger.info(f"🔍 Termos da série branca encontrados no texto: {', '.join(found_terms)}")
        else:
            logger.warning("❌ Nenhum termo da série branca encontrado no texto extraído")
    
    if len(resultados) == 0:
        logger.warning("⚠️ Nenhum valor laboratorial encontrado no PDF")
    
    # Deduplicar analitos com mesmo valor normalizado
    resultados_deduplificados = deduplicate_analitos(resultados)
    logger.info(f"🔄 Deduplicação: {len(resultados)} → {len(resultados_deduplificados)} analitos únicos")
    
    return resultados_deduplificados

def preprocess_image_for_ocr(img: Image.Image) -> Image.Image:
    """
    Aplica pré-processamento avançado na imagem para melhorar OCR
    """
    try:
        # Converter para numpy array para processamento com OpenCV
        img_array = np.array(img)
        
        # Converter para escala de cinza se necessário
        if len(img_array.shape) == 3:
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_array
        
        # 1. Denoising (remoção de ruído)
        denoised = cv2.fastNlMeansDenoising(gray)
        
        # 2. Melhorar contraste com CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(denoised)
        
        # 3. Binarização adaptativa (melhor para documentos escaneados)
        binary = cv2.adaptiveThreshold(
            enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        
        # 4. Morfologia para limpar a imagem
        kernel = np.ones((1,1), np.uint8)
        cleaned = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        
        # Converter de volta para PIL Image
        processed_img = Image.fromarray(cleaned)
        
        logger.debug("✅ Pré-processamento de imagem concluído")
        return processed_img
        
    except Exception as e:
        logger.warning(f"⚠️ Erro no pré-processamento: {e}, usando imagem original")
        return img

def detect_and_correct_orientation(img: Image.Image) -> Image.Image:
    """
    Detecta e corrige a orientação da imagem
    """
    try:
        # Usar Tesseract para detectar orientação
        osd = pytesseract.image_to_osd(img, output_type=pytesseract.Output.DICT)
        angle = osd['rotate']
        
        if angle != 0:
            logger.info(f"🔄 Corrigindo rotação: {angle} graus")
            img = img.rotate(-angle, expand=True, fillcolor='white')
        
        return img
    except Exception as e:
        logger.debug(f"⚠️ Não foi possível detectar orientação: {e}")
        return img

def detect_medical_document_type(img: Image.Image) -> str:
    """
    Detecta o tipo de documento médico para aplicar processamento específico
    """
    try:
        # Fazer OCR rápido para detectar palavras-chave
        quick_text = pytesseract.image_to_string(img, lang='por', config='--psm 6 --oem 3').lower()
        
        # Palavras-chave para diferentes tipos de exames
        if any(word in quick_text for word in ['hemograma', 'hemacias', 'leucocitos', 'plaquetas', 'serie']):
            return 'hemograma'
        elif any(word in quick_text for word in ['bioquimica', 'glicose', 'colesterol', 'triglicerides']):
            return 'bioquimica'
        elif any(word in quick_text for word in ['urina', 'eas', 'sedimento']):
            return 'urina'
        else:
            return 'geral'
            
    except Exception:
        return 'geral'

def extract_text_with_medical_ocr(img: Image.Image, page_num: int) -> str:
    """
    Extrai texto usando OCR otimizado para documentos médicos
    """
    # Detectar tipo de documento
    doc_type = detect_medical_document_type(img)
    logger.debug(f"📋 Página {page_num+1}: Detectado como documento tipo '{doc_type}'")
    
    best_text = ""
    best_confidence = 0
    
    # Configurações PSM específicas para documentos médicos
    if doc_type == 'hemograma':
        # Hemogramas geralmente têm layout tabular
        psm_configs = [
            ('--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789.,ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÀÁÂÃÇÉÊÍÓÔÕÚÜàáâãçéêíóôõúü%/³²μ ', 'Hemograma com caracteres específicos'),
            ('--psm 7 --oem 3', 'Linha única para valores'),
            ('--psm 8 --oem 3', 'Palavra única para analitos'),
            ('--psm 11 --oem 3', 'Texto esparso para tabelas')
        ]
    else:
        # Configurações gerais para outros documentos
        psm_configs = [
            ('--psm 6 --oem 3', 'Bloco uniforme de texto'),
            ('--psm 7 --oem 3', 'Linha única de texto'),
            ('--psm 8 --oem 3', 'Palavra única'),
            ('--psm 11 --oem 3', 'Texto esparso'),
            ('--psm 12 --oem 3', 'Texto esparso com OSD'),
            ('--psm 13 --oem 3', 'Linha crua - bypass de heurísticas')
        ]
    
    # Idiomas para tentar (português primeiro para documentos médicos brasileiros)
    languages = ['por', 'por+eng', 'eng']
    
    for lang in languages:
        for config, description in psm_configs:
            try:
                # Extrair texto com configuração específica
                text = pytesseract.image_to_string(img, lang=lang, config=config)
                
                # Pós-processamento específico para documentos médicos
                text = post_process_medical_text(text, doc_type)
                
                # Calcular confiança (aproximada pelo comprimento e caracteres válidos)
                confidence = calculate_medical_text_confidence(text, doc_type)
                
                if confidence > best_confidence and len(text.strip()) > 10:
                    best_text = text
                    best_confidence = confidence
                    logger.debug(f"✅ Página {page_num+1}: Melhor resultado com {lang} + {description} (confiança: {confidence:.2f})")
                    
            except Exception as e:
                logger.debug(f"⚠️ Erro com {lang} + {config}: {e}")
                continue
    
    return best_text

def sanitize_unicode_text(text: str) -> str:
    """Normaliza acentos (NFKC) e remove caracteres invisíveis/controle que atrapalham regex."""
    if not text:
        return text
    normalized = unicodedata.normalize('NFKC', text)
    for ch in ("\u200B","\u200C","\u200D","\u2060","\u00A0"):
        normalized = normalized.replace(ch, " ")
    import re
    normalized = re.sub(r"\s{2,}", " ", normalized)
    return normalized


def post_process_medical_text(text: str, doc_type: str) -> str:
    """
    Aplica pós-processamento específico para texto médico
    """
    if not text:
        return text
    
    # Correções comuns em OCR de documentos médicos
    corrections = {
        # Correções de caracteres comuns
        'O': '0',  # O maiúsculo por zero
        'l': '1',  # l minúsculo por 1
        'I': '1',  # I maiúsculo por 1
        'S': '5',  # S por 5 em contextos numéricos
        'B': '8',  # B por 8 em contextos numéricos
        
        # Correções específicas para termos médicos
        'Hemacias': 'Hemácias',
        'Leucocitos': 'Leucócitos',
        'Neutrofilos': 'Neutrófilos',
        'Linfocitos': 'Linfócitos',
        'Monocitos': 'Monócitos',
        'Eosinofilos': 'Eosinófilos',
        'Basofilos': 'Basófilos',
    }
    
    processed_text = text
    
    # Aplicar correções específicas para hemogramas
    if doc_type == 'hemograma':
        # Corrigir valores numéricos mal interpretados
        import re
        
        # Padrão para encontrar valores numéricos seguidos de unidades
        number_pattern = r'([O|l|I|S|B])(\d+[.,]?\d*)'
        processed_text = re.sub(number_pattern, lambda m: corrections.get(m.group(1), m.group(1)) + m.group(2), processed_text)
        
        # Corrigir termos médicos
        for wrong, correct in corrections.items():
            if wrong in ['Hemacias', 'Leucocitos', 'Neutrofilos', 'Linfocitos', 'Monocitos', 'Eosinofilos', 'Basofilos']:
                processed_text = processed_text.replace(wrong, correct)
    
    return processed_text

# Normalização de termos com espaçamento interno incomum
def normalize_fragmented_terms(text: str) -> str:
    """Normaliza termos e tokens numéricos fragmentados (ex.: 'E o s i n ó f i l o s', '5 , 0 %', 'μ L')."""
    import re
    processed = text
    # 1) Termos médicos com letras separadas por espaços
    label_patterns = [
        r"(?i)E\s*o\s*s\s*i\s*n\s*[óo]\s*f\s*i\s*l\s*o\s*s",
        r"(?i)N\s*e\s*u\s*t\s*r\s*[óo]\s*f\s*i\s*l\s*o\s*s",
        r"(?i)L\s*i\s*n\s*f\s*[óo]\s*c\s*i\s*t\s*o\s*s",
        r"(?i)M\s*o\s*n\s*[óo]\s*c\s*i\s*t\s*o\s*s",
        r"(?i)B\s*a\s*s\s*[óo]\s*f\s*i\s*l\s*o\s*s",
        r"(?i)H\s*e\s*m\s*[áa]\s*c\s*i\s*a\s*s",
        r"(?i)L\s*e\s*u\s*c\s*[óo]\s*c\s*i\s*t\s*o\s*s",
        r"(?i)P\s*l\s*a\s*q\s*u\s*e\s*t\s*a\s*s",
    ]
    replacements = [
        "Eosinófilos", "Neutrófilos", "Linfócitos", "Monócitos", "Basófilos",
        "Hemácias", "Leucócitos", "Plaquetas"
    ]
    for pat, rep in zip(label_patterns, replacements):
        processed = re.sub(pat, rep, processed)

    # 2) Colapsar espaços em números e símbolos (vírgula, ponto, porcento)
    # Ex.: '5 , 0' -> '5,0', '7 . 010' -> '7.010', '3 5' -> '35'
    processed = re.sub(r"(\d)\s*,\s*(\d)", r"\1,\2", processed)
    processed = re.sub(r"(\d)\s*\.\s*(\d{3})", r"\1.\2", processed)
    processed = re.sub(r"(\d)\s+([\d]{1,3})(?=[^\d])", r"\1\2", processed)
    processed = re.sub(r"(\d)\s*%", r"\1%", processed)

    # 3) Colapsar espaços em unidades comuns
    processed = re.sub(r"μ\s*L", "μL", processed)
    processed = re.sub(r"mm\s*3", "mm3", processed)
    processed = re.sub(r"/\s*μ\s*L", "/μL", processed)

    return processed

def calculate_medical_text_confidence(text: str, doc_type: str) -> float:
    """
    Calcula confiança específica para texto médico
    """
    if not text.strip():
        return 0.0
    
    base_confidence = calculate_text_confidence(text)
    
    # Bônus para termos médicos específicos
    medical_terms_bonus = 0.0
    
    if doc_type == 'hemograma':
        hemograma_terms = [
            'hemácias', 'hemacias', 'leucócitos', 'leucocitos', 'plaquetas',
            'neutrófilos', 'neutrofilos', 'linfócitos', 'linfocitos',
            'monócitos', 'monocitos', 'eosinófilos', 'eosinofilos',
            'basófilos', 'basofilos', 'hematócrito', 'hemoglobina',
            'série', 'serie', 'vermelha', 'branca', 'plaquetária'
        ]
        
        text_lower = text.lower()
        found_terms = sum(1 for term in hemograma_terms if term in text_lower)
        medical_terms_bonus = min(0.3, found_terms * 0.05)  # Máximo 30% de bônus
    
    # Bônus para valores numéricos (importantes em exames)
    import re
    numeric_values = re.findall(r'\d+[.,]?\d*', text)
    numeric_bonus = min(0.2, len(numeric_values) * 0.02)  # Máximo 20% de bônus
    
    final_confidence = base_confidence + medical_terms_bonus + numeric_bonus
    return max(0.0, min(1.0, final_confidence))

def extract_text_with_advanced_ocr(img: Image.Image, page_num: int) -> str:
    """
    Extrai texto usando OCR avançado com múltiplas configurações
    """
    # Usar OCR médico especializado
    return extract_text_with_medical_ocr(img, page_num)

def calculate_text_confidence(text: str) -> float:
    """
    Calcula uma pontuação de confiança aproximada para o texto extraído
    """
    if not text.strip():
        return 0.0
    
    # Fatores que indicam boa extração
    total_chars = len(text)
    alpha_chars = sum(1 for c in text if c.isalpha())
    digit_chars = sum(1 for c in text if c.isdigit())
    space_chars = sum(1 for c in text if c.isspace())
    
    # Penalizar caracteres estranhos
    weird_chars = sum(1 for c in text if not (c.isalnum() or c.isspace() or c in '.,;:!?()[]{}"\'-+=/\n\r'))
    
    if total_chars == 0:
        return 0.0
    
    # Calcular pontuação
    alpha_ratio = alpha_chars / total_chars
    digit_ratio = digit_chars / total_chars
    space_ratio = space_chars / total_chars
    weird_ratio = weird_chars / total_chars
    
    # Pontuação baseada em características de texto médico/laboratorial
    confidence = (alpha_ratio * 0.4 + digit_ratio * 0.3 + space_ratio * 0.2) - (weird_ratio * 0.5)
    
    return max(0.0, min(1.0, confidence))

def extract_text_with_ocr(pdf_content: Union[str, bytes]) -> str:
    """
    Extrai texto usando OCR avançado como fallback
    """
    if not OCR_AVAILABLE:
        logger.warning("⚠️ OCR não disponível")
        return ""
    
    try:
        if isinstance(pdf_content, bytes):
            doc = fitz.open(stream=pdf_content, filetype="pdf")
        else:
            doc = fitz.open(pdf_content)
        
        full_text = ""
        ocr_pages = 0
        
        for page_num in range(len(doc)):
            try:
                page = doc.load_page(page_num)
                
                # Tenta extrair texto primeiro com PyMuPDF
                page_text = page.get_text()
                if len(page_text.strip()) > 50:  # Aumentei o threshold
                    full_text += page_text + "\n"
                    logger.debug(f"📄 Página {page_num+1}: Texto extraído diretamente")
                else:
                    # OCR avançado como último recurso
                    logger.info(f"🔍 Página {page_num+1}: Aplicando OCR avançado...")
                    
                    # Tentar múltiplas resoluções
                    resolutions = [2, 3, 4]  # 2x, 3x, 4x zoom
                    best_page_text = ""
                    
                    for resolution in resolutions:
                        try:
                            # Extrair imagem com resolução específica
                            matrix = fitz.Matrix(resolution, resolution)
                            pix = page.get_pixmap(matrix=matrix)
                            img_data = pix.tobytes("ppm")
                            img = Image.open(io.BytesIO(img_data))
                            
                            # Detectar e corrigir orientação
                            img = detect_and_correct_orientation(img)
                            
                            # Pré-processar imagem
                            processed_img = preprocess_image_for_ocr(img)
                            
                            # Extrair texto com OCR avançado
                            ocr_text = extract_text_with_advanced_ocr(processed_img, page_num)
                            
                            # Usar o melhor resultado
                            if len(ocr_text.strip()) > len(best_page_text.strip()):
                                best_page_text = ocr_text
                                logger.debug(f"✅ Melhor resultado com resolução {resolution}x")
                                
                        except Exception as res_error:
                            logger.debug(f"⚠️ Erro com resolução {resolution}x: {res_error}")
                            continue
                    
                    full_text += best_page_text + "\n"
                    ocr_pages += 1
                    
            except Exception as page_error:
                logger.warning(f"⚠️ Erro na página {page_num+1}: {page_error}")
                continue
        
        doc.close()
        logger.info(f"🔍 OCR avançado aplicado em {ocr_pages} página(s), {len(full_text)} caracteres extraídos")
        return full_text
        
    except Exception as e:
        logger.error(f"❌ Erro no OCR avançado: {e}")
        return ""