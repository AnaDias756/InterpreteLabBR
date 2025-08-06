#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de inicialização para a aplicação desktop
Interpretador de Laudos Laboratoriais
"""

import sys
import os
import subprocess
import time
from pathlib import Path

def check_backend_running():
    """Verificar se o backend está rodando"""
    try:
        import requests
        response = requests.get("http://localhost:8000/health", timeout=2)
        return response.status_code == 200
    except:
        return False

def start_backend():
    """Iniciar o backend se não estiver rodando"""
    if not check_backend_running():
        print("🚀 Iniciando servidor backend...")
        backend_cmd = [
            sys.executable, "-m", "uvicorn", 
            "backend.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000"
        ]
        
        # Iniciar backend em processo separado
        subprocess.Popen(
            backend_cmd,
            cwd=Path(__file__).parent,
            creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0
        )
        
        # Aguardar backend inicializar
        print("⏳ Aguardando backend inicializar...")
        for i in range(30):  # Aguardar até 30 segundos
            if check_backend_running():
                print("✅ Backend iniciado com sucesso!")
                break
            time.sleep(1)
            print(f"   Tentativa {i+1}/30...")
        else:
            print("❌ Erro: Backend não iniciou. Verifique as dependências.")
            return False
    else:
        print("✅ Backend já está rodando!")
    
    return True

def start_frontend():
    """Iniciar a interface desktop"""
    print("🖥️ Iniciando interface desktop...")
    
    # Adicionar diretório atual ao Python path
    current_dir = Path(__file__).parent
    if str(current_dir) not in sys.path:
        sys.path.insert(0, str(current_dir))
    
    # Importar e executar aplicação
    try:
        from frontend.main import main
        main()
    except ImportError as e:
        print(f"❌ Erro ao importar frontend: {e}")
        print("Verifique se o PySide6 está instalado: pip install PySide6")
        return False
    except Exception as e:
        print(f"❌ Erro ao executar frontend: {e}")
        return False
    
    return True

def main():
    """Função principal"""
    print("🩺 Interpretador de Laudos Laboratoriais")
    print("=" * 50)
    
    # Verificar se estamos no diretório correto
    if not Path("backend/main.py").exists():
        print("❌ Erro: Execute este script no diretório raiz do projeto.")
        sys.exit(1)
    
    # Iniciar backend
    if not start_backend():
        print("❌ Falha ao iniciar backend. Encerrando.")
        sys.exit(1)
    
    # Pequena pausa antes de iniciar frontend
    time.sleep(2)
    
    # Iniciar frontend
    if not start_frontend():
        print("❌ Falha ao iniciar frontend. Encerrando.")
        sys.exit(1)

if __name__ == "__main__":
    main()