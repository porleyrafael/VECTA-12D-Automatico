@echo off
title VECTA 12D - Instalador
echo ====================================
echo    VECTA 12D - Sistema 12D
echo ====================================
echo.
echo [1/2] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python no encontrado
    echo Instala Python desde python.org
    pause
    exit /b 1
)

echo [2/2] Iniciando VECTA 12D...
echo.
python vecta_launcher.py
pause
