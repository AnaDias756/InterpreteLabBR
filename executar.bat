@echo off
chcp 65001 >nul
echo 🩺 Interpretador de Laudos Laboratoriais
echo 📦 Verificando dependências...

:: Instalar dependências se necessário
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Erro ao instalar dependências
    pause
    exit /b 1
)

echo ✅ Dependências instaladas!
echo.
echo 🚀 Iniciando aplicação...
echo.

:: Executar a aplicação
python frontend/main.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ Erro ao executar a aplicação
    echo 💡 Verifique se o Python está instalado corretamente
    pause
    exit /b 1
)

echo.
echo ✅ Aplicação finalizada
pause