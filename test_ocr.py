import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import io

# Configurar caminho do Tesseract no Windows
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def test_ocr_direct():
    print("🔍 TESTE DIRETO DE OCR")
    print("=" * 30)
    
    try:
        # Testar se o Tesseract está no PATH
        print("📍 Testando Tesseract...")
        version = pytesseract.get_tesseract_version()
        print(f"✅ Tesseract versão: {version}")
        
        # Abrir PDF com PyMuPDF
        print("📄 Abrindo PDF...")
        doc = fitz.open("tests/exemplos/Laudo_Exemplo.pdf")  # Mudança aqui
        print(f"✅ PDF aberto: {len(doc)} páginas")
        
        # Processar primeira página
        page = doc.load_page(0)
        print("🖼️ Convertendo página para imagem...")
        
        # Renderizar em alta resolução
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        img_data = pix.tobytes("ppm")
        img = Image.open(io.BytesIO(img_data))
        print(f"✅ Imagem criada: {img.size}")
        
        # OCR
        print("🔍 Executando OCR...")
        ocr_text = pytesseract.image_to_string(img, lang='eng')  # Mudança: 'por' para 'eng'
        print(f"✅ OCR concluído: {len(ocr_text)} caracteres")
        
        print("📄 Texto extraído:")
        print("-" * 30)
        print(ocr_text[:500])
        print("-" * 30)
        
        doc.close()
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        print("💡 Possíveis soluções:")
        print("   1. Tesseract não está no PATH")
        print("   2. Configurar: pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'")
        print("   3. Reinstalar Tesseract")

if __name__ == "__main__":
    test_ocr_direct()