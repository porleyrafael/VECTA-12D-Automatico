@echo off
echo ========================================
echo 🧹 LIMPIADOR VECTA 12D - EJECUCIÓN RÁPIDA
echo ========================================
echo.

cd /d "C:\Users\Rafael\Desktop\VECTA 12D Automatico"

if exist "limpiador_vecta.py" (
    python limpiador_vecta.py
) else (
    echo ❌ Error: No se encuentra limpiador_vecta.py
    echo.
    echo Creando limpiador básico...
    echo import os, glob, shutil > limpiador_basico.py
    echo for f in glob.glob("**/__pycache__", recursive=True): shutil.rmtree(f, ignore_errors=True) >> limpiador_basico.py
    echo for f in glob.glob("**/*.pyc", recursive=True): os.remove(f) >> limpiador_basico.py
    echo print("✅ Limpieza básica completada") >> limpiador_basico.py
    python limpiador_basico.py
    del limpiador_basico.py
)

echo.
pause