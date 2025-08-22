#!/usr/bin/env python3
"""
Script para testar o backend localmente antes do deploy no Render.
Este script verifica se todas as dependências estão funcionando corretamente.
"""

import sys
import os
import traceback
import requests
import time
import subprocess
from pathlib import Path

def test_imports():
    """Testa se todos os imports críticos funcionam."""
    print("🔍 Testando imports...")
    
    try:
        # Adicionar o diretório raiz ao Python path
        sys.path.insert(0, str(Path.cwd()))
        
        from backend.services.pdf_parser import extract_lab_values
        from backend.services.rule_engine import apply_rules
        from backend.services.specialty_selector import select_specialties
        from backend.services.nlg import build_briefing
        
        print("✅ Todos os imports funcionando")
        return True
        
    except Exception as e:
        print(f"❌ Erro nos imports: {e}")
        print(f"📍 Traceback: {traceback.format_exc()}")
        return False

def test_data_files():
    """Verifica se os arquivos de dados existem."""
    print("\n📁 Verificando arquivos de dados...")
    
    data_files = [
        'data/patterns.csv',
        'data/guideline_map.csv'
    ]
    
    all_exist = True
    for file_path in data_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} encontrado")
        else:
            print(f"❌ {file_path} NÃO encontrado")
            all_exist = False
    
    return all_exist

def test_dependencies():
    """Testa se todas as dependências estão instaladas."""
    print("\n📦 Verificando dependências...")
    
    required_packages = [
        'fastapi',
        'uvicorn',
        'pandas',
        'pdfplumber',
        'psutil',
        'pydantic'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} instalado")
        except ImportError:
            print(f"❌ {package} NÃO instalado")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️ Pacotes faltando: {', '.join(missing_packages)}")
        print("Execute: pip install -r requirements-backend.txt")
        return False
    
    return True

def start_server_test():
    """Inicia o servidor para teste."""
    print("\n🚀 Iniciando servidor de teste...")
    
    try:
        # Iniciar servidor em background
        process = subprocess.Popen([
            sys.executable, '-m', 'uvicorn', 
            'backend.main:app', 
            '--host', '0.0.0.0', 
            '--port', '8000',
            '--timeout-keep-alive', '300'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Aguardar um pouco para o servidor inicializar
        print("⏳ Aguardando servidor inicializar...")
        time.sleep(5)
        
        # Testar health check
        try:
            response = requests.get('http://localhost:8000/health', timeout=10)
            if response.status_code == 200:
                print("✅ Health check funcionando")
                print(f"📊 Resposta: {response.json()}")
                
                # Testar debug endpoint
                debug_response = requests.get('http://localhost:8000/debug', timeout=10)
                if debug_response.status_code == 200:
                    print("✅ Debug endpoint funcionando")
                    debug_data = debug_response.json()
                    print(f"📊 Working directory: {debug_data.get('working_directory')}")
                    print(f"📊 Files exist: {debug_data.get('files_exist')}")
                else:
                    print(f"⚠️ Debug endpoint retornou: {debug_response.status_code}")
                
                return True, process
            else:
                print(f"❌ Health check falhou: {response.status_code}")
                return False, process
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro ao conectar com servidor: {e}")
            return False, process
            
    except Exception as e:
        print(f"❌ Erro ao iniciar servidor: {e}")
        return False, None

def main():
    """Função principal de teste."""
    print("🧪 Testando Backend do Interpretador de Laudos")
    print("=" * 50)
    
    # Verificar diretório atual
    print(f"📂 Diretório atual: {os.getcwd()}")
    
    # Executar testes
    tests_passed = 0
    total_tests = 3
    
    if test_dependencies():
        tests_passed += 1
    
    if test_data_files():
        tests_passed += 1
    
    if test_imports():
        tests_passed += 1
    
    print(f"\n📊 Resultado dos testes: {tests_passed}/{total_tests} passaram")
    
    if tests_passed == total_tests:
        print("\n🎉 Todos os testes básicos passaram!")
        print("🚀 Testando servidor...")
        
        server_ok, process = start_server_test()
        
        if server_ok:
            print("\n✅ Servidor funcionando corretamente!")
            print("🌐 Acesse: http://localhost:8000/health")
            print("🔧 Debug: http://localhost:8000/debug")
            print("\n⚠️ Pressione Ctrl+C para parar o servidor")
            
            try:
                process.wait()
            except KeyboardInterrupt:
                print("\n🛑 Parando servidor...")
                process.terminate()
                process.wait()
                print("👋 Servidor parado")
        else:
            print("\n❌ Servidor não funcionou corretamente")
            if process:
                process.terminate()
                process.wait()
            return False
    else:
        print("\n❌ Alguns testes falharam. Corrija os problemas antes do deploy.")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)