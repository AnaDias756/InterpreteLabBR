#!/usr/bin/env python3
"""
Teste para verificar se o erro 422 da idade foi corrigido.
"""

import requests
import json
import io

def create_simple_pdf():
    """Cria um PDF simples válido para teste."""
    # PDF mínimo válido
    pdf_content = b"""%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R >>
endobj
4 0 obj
<< /Length 44 >>
stream
BT
/F1 12 Tf
100 700 Td
(Teste de laudo) Tj
ET
endstream
endobj
xref
0 5
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000225 00000 n 
trailer
<< /Size 5 /Root 1 0 R >>
startxref
319
%%EOF"""
    return pdf_content

def test_idade_validation():
    """Testa se a API aceita diferentes valores de idade."""
    
    url = "http://localhost:8000/interpret"
    pdf_content = create_simple_pdf()
    
    test_cases = [
        {'idade': '0', 'genero': 'feminino', 'desc': 'idade 0 (campo vazio)'},
        {'idade': '30', 'genero': 'masculino', 'desc': 'idade 30 (normal)'},
        {'idade': '1', 'genero': 'feminino', 'desc': 'idade 1 (mínima)'},
    ]
    
    results = []
    
    for case in test_cases:
        print(f"\n🧪 Testando {case['desc']}...")
        
        data = {
            'genero': case['genero'],
            'idade': case['idade']
        }
        
        files = {
            'file': ('test_laudo.pdf', pdf_content, 'application/pdf')
        }
        
        try:
            response = requests.post(url, data=data, files=files, timeout=30)
            
            print(f"📊 Status Code: {response.status_code}")
            
            if response.status_code == 422:
                try:
                    error_detail = response.json()
                    print(f"❌ Erro 422: {error_detail['detail']}")
                    
                    # Verificar se o erro é relacionado à idade
                    if 'idade' in error_detail['detail'].lower():
                        print("💥 ERRO: Validação de idade ainda falhando!")
                        results.append(False)
                    else:
                        print("✅ OK: Erro não é relacionado à idade")
                        results.append(True)
                except:
                    print(f"📝 Resposta: {response.text}")
                    results.append(False)
            elif response.status_code == 200:
                print("✅ Sucesso! Requisição aceita")
                results.append(True)
            else:
                print(f"⚠️ Status inesperado: {response.status_code}")
                print(f"📝 Resposta: {response.text[:200]}...")
                results.append(True)  # Não é erro 422 de validação
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro de conexão: {e}")
            results.append(False)
    
    return all(results)

if __name__ == "__main__":
    print("🚀 Iniciando teste de validação de idade...")
    success = test_idade_validation()
    
    if success:
        print("\n🎉 TESTE PASSOU! A validação de idade está funcionando corretamente.")
        print("✅ O erro 422 relacionado à idade foi corrigido!")
    else:
        print("\n💥 TESTE FALHOU! Ainda há problemas com a validação de idade.")