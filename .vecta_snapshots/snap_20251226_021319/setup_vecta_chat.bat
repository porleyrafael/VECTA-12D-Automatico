@echo off
echo ========================================
echo  VECTA AI CHAT - INSTALADOR AUTOMÁTICO
echo ========================================
echo.

echo Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no encontrado
    echo Instala Python 3.8+ desde python.org
    pause
    exit /b 1
)

echo ✅ Python encontrado

echo.
echo Verificando directorio VECTA...
if not exist "core\vecta_12d_core.py" (
    echo ERROR: No se encuentra VECTA 12D
    echo Ejecuta desde el directorio de VECTA 12D
    pause
    exit /b 1
)

echo ✅ VECTA 12D encontrado

echo.
echo Instalando VECTA AI Chat...
python vecta_ai_chat.py --install

echo.
if errorlevel 1 (
    echo ❌ Error en la instalación
    pause
    exit /b 1
)

echo.
echo ========================================
echo  INSTALACIÓN COMPLETADA EXITOSAMENTE
echo ========================================
echo.
echo ✅ VECTA AI Chat instalado
echo ✅ Acceso directo creado en el escritorio
echo ✅ Sistema listo para usar
echo.
echo Para iniciar:
echo   1. Busca "VECTA AI Chat" en el escritorio
echo   2. O ejecuta: python vecta_ai_chat.py
echo.
echo ¡Habla con VECTA en lenguaje natural!
echo.
pause