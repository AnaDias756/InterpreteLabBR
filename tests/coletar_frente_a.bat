@echo off
REM ============================================================
REM  Coleta automatica da Frente A (InterpreteLabBR) - Windows
REM  COMO USAR:
REM   1. Salve este arquivo na pasta  D:\platform-tools
REM   2. Garanta que o tablet esta conectado (adb devices = device)
REM   3. De 2 cliques no arquivo (ou rode: coletar_frente_a.bat)
REM  Gera: coleta_frente_a.txt  (envie no chat ao terminar)
REM ============================================================
cd /d "%~dp0"
setlocal
set OUT=coleta_frente_a.txt
set APP=com.anadias.interpretelabbr
set ACT=com.anadias.interpretelabbr/.MainActivity
set PWA=com.android.chrome

echo ====== COLETA FRENTE A ======> %OUT%
echo Data: %date% %time%>> %OUT%

echo.
echo === FASE 1/2: APP (inicializacao + RAM) - 10 repeticoes ===
echo O script abre e fecha o app sozinho. Nao mexa no tablet.
echo.
for /L %%i in (1,1,10) do (
  echo   [APP] repeticao %%i de 10...
  echo --- APP rep %%i --->> %OUT%
  adb shell am force-stop %APP%
  timeout /t 2 /nobreak >nul
  adb shell am start -W -n %ACT% >> %OUT%
  timeout /t 4 /nobreak >nul
  adb shell "dumpsys meminfo %APP% | grep 'TOTAL PSS'" >> %OUT%
)

echo.
echo === FASE 2/2: PWA (RAM) - 10 repeticoes ===
echo No TABLET: abra o Chrome em  https://interpretlabbr.netlify.app
echo Espere a pagina carregar e deixe-a na frente.
echo Depois volte aqui e tecle qualquer coisa para continuar.
pause
echo.
for /L %%i in (1,1,10) do (
  echo   [PWA] repeticao %%i de 10...
  echo --- PWA rep %%i --->> %OUT%
  adb shell "dumpsys meminfo %PWA% | grep 'TOTAL PSS'" >> %OUT%
  timeout /t 2 /nobreak >nul
)

echo.
echo ====== PRONTO! ======
echo Arquivo gerado: %CD%\%OUT%
echo Envie o arquivo coleta_frente_a.txt no chat.
echo.
pause
endlocal
