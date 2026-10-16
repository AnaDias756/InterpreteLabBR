@echo off
REM ============================================================
REM  Coleta de FPS/jank + CPU em ROLAGEM (Frente A) - Windows
REM  Rola a tela automaticamente e mede gfxinfo e CPU.
REM  Salve em D:\platform-tools e de 2 cliques (tablet conectado).
REM  Gera: coleta_fps.txt  (envie no chat ao terminar)
REM ============================================================
cd /d "%~dp0"
setlocal enabledelayedexpansion
set OUT=coleta_fps.txt
set APP=com.anadias.interpretelabbr
set ACT=com.anadias.interpretelabbr/.MainActivity
set PWA=com.android.chrome
set URL=https://interpretlabbr.netlify.app
set N=10

REM --- descobrir tamanho da tela e calcular os pontos do swipe ---
for /f "tokens=3" %%s in ('adb shell wm size') do set SIZE=%%s
for /f "tokens=1,2 delims=x" %%a in ("!SIZE!") do (set W=%%a & set H=%%b)
set /a CX=W/2
set /a Y1=H*75/100
set /a Y2=H*25/100

echo ====== COLETA FPS/CPU EM ROLAGEM ======> %OUT%
echo Tela: !W!x!H!  swipe (!CX!,!Y1!)-^>(!CX!,!Y2!)>> %OUT%
echo Tela detectada: !W!x!H!

echo.
echo === FASE 1/2: APP - %N% repeticoes de rolagem ===
echo O script abre o app e rola sozinho. Nao mexa no tablet.
for /L %%i in (1,1,%N%) do (
  echo   [APP] rep %%i de %N% ...
  adb shell am force-stop %APP%
  adb shell am start -n %ACT% >nul
  timeout /t 3 /nobreak >nul
  adb shell dumpsys gfxinfo %APP% reset >nul
  adb shell dumpsys cpuinfo >nul
  for /L %%k in (1,1,12) do adb shell input swipe !CX! !Y1! !CX! !Y2! 250 >nul
  echo --- APP rep %%i gfxinfo --->> %OUT%
  adb shell "dumpsys gfxinfo %APP% | grep -E 'Total frames|Janky|percentile'" >> %OUT%
  echo --- APP rep %%i cpu --->> %OUT%
  adb shell "dumpsys cpuinfo | grep interprete" >> %OUT%
)

echo.
echo === FASE 2/2: PWA (Chrome) - %N% repeticoes de rolagem ===
echo O script abre a pagina no Chrome e rola sozinho.
for /L %%i in (1,1,%N%) do (
  echo   [PWA] rep %%i de %N% ...
  adb shell am start -a android.intent.action.VIEW -d "%URL%" %PWA% >nul
  timeout /t 5 /nobreak >nul
  adb shell dumpsys gfxinfo %PWA% reset >nul
  adb shell dumpsys cpuinfo >nul
  for /L %%k in (1,1,12) do adb shell input swipe !CX! !Y1! !CX! !Y2! 250 >nul
  echo --- PWA rep %%i gfxinfo --->> %OUT%
  adb shell "dumpsys gfxinfo %PWA% | grep -E 'Total frames|Janky|percentile'" >> %OUT%
  echo --- PWA rep %%i cpu --->> %OUT%
  adb shell "dumpsys cpuinfo | grep chrome" >> %OUT%
)

echo.
echo ====== PRONTO! Arquivo: %CD%\%OUT% ======
echo Envie o arquivo coleta_fps.txt no chat.
pause
endlocal
