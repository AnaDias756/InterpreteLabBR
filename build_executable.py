#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para gerar executável do InterpreteLab BR
Opções: PyInstaller, auto-py-to-exe, Nuitka
"""

import os
import sys
import subprocess
from pathlib import Path

def check_pyinstaller():
    """Verifica se PyInstaller está instalado"""
    try:
        import PyInstaller
        return True
    except ImportError:
        return False

def install_pyinstaller():
    """Instala PyInstaller"""
    print("📦 Instalando PyInstaller...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("✅ PyInstaller instalado com sucesso!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Erro ao instalar PyInstaller")
        return False

def build_with_pyinstaller():
    """Gera executável com PyInstaller"""
    print("🔨 Gerando executável com PyInstaller...")
    
    # Comando PyInstaller
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name", "InterpretadorLaudos",
        "--add-data", "data;data",
        "--hidden-import", "requests",
        "--hidden-import", "PySide6",
        "--hidden-import", "pandas",
        "frontend/main.py"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("✅ Executável gerado com sucesso!")
        print("📁 Localização: dist/InterpretadorLaudos.exe")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao gerar executável: {e}")
        return False

def show_alternatives():
    """Mostra alternativas de distribuição"""
    print("\n🔧 ALTERNATIVAS DE DISTRIBUIÇÃO:")
    print("\n1️⃣ AUTO-PY-TO-EXE (Recomendado):")
    print("   pip install auto-py-to-exe")
    print("   auto-py-to-exe")
    print("   Configurações:")
    print("   - Script Location: frontend/main.py")
    print("   - Onefile: Yes")
    print("   - Window Based: Yes")
    print("   - Additional Files: data (folder)")
    
    print("\n2️⃣ NUITKA:")
    print("   pip install nuitka")
    print("   python -m nuitka --onefile --windows-disable-console frontend/main.py")
    
    print("\n3️⃣ DISTRIBUIÇÃO SIMPLES:")
    print("   - Copiar pasta completa do projeto")
    print("   - Incluir executar.bat")
    print("   - Usuário executa: executar.bat")
    
    print("\n4️⃣ MANUAL PYINSTALLER:")
    print("   pyinstaller --onefile --windowed --name InterpretadorLaudos --add-data \"data;data\" frontend/main.py")

def main():
    print("🩺 InterpreteLab BR - Gerador de Executável")
    print("=" * 50)
    
    # Verificar se está no diretório correto
    if not Path("frontend/main.py").exists():
        print("❌ Erro: Execute este script na raiz do projeto")
        return
    
    # Verificar PyInstaller
    if not check_pyinstaller():
        print("⚠️ PyInstaller não encontrado")
        if input("Deseja instalar? (s/n): ").lower() == 's':
            if not install_pyinstaller():
                show_alternatives()
                return
        else:
            show_alternatives()
            return
    
    # Tentar gerar executável
    if not build_with_pyinstaller():
        print("\n⚠️ Falha no PyInstaller. Veja as alternativas:")
        show_alternatives()
    else:
        print("\n📋 PRÓXIMOS PASSOS:")
        print("1. Copie o arquivo dist/InterpretadorLaudos.exe")
        print("2. Copie a pasta data/ junto com o executável")
        print("3. Distribua ambos para os usuários")
        print("\n💡 DICA: Teste o executável antes de distribuir!")

if __name__ == "__main__":
    main()
    input("\nPressione Enter para sair...")