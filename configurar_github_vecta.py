#!/usr/bin/env python3
"""
CONFIGURADOR GITHUB VECTA - VERSIÓN SIMPLE
"""

import os
import subprocess
import webbrowser
from datetime import datetime

print("="*50)
print("CONFIGURADOR GITHUB VECTA 12D")
print("="*50)

# 1. Verificar Git
try:
    subprocess.run(["git", "--version"], check=True, capture_output=True)
    print("✓ Git encontrado")
except:
    print("✗ Git no encontrado")
    print("Descarga desde: https://git-scm.com/download/win")
    webbrowser.open("https://git-scm.com/download/win")
    input("Presiona Enter después de instalar Git...")
    exit()

# 2. Inicializar repositorio
print("\n1. Inicializando repositorio Git...")
subprocess.run(["git", "init"], capture_output=True)
subprocess.run(["git", "add", "."], capture_output=True)

# 3. Crear .gitignore
with open(".gitignore", "w") as f:
    f.write("__pycache__/\n*.pyc\n*.pyo\n*.pyd\n.DS_Store\n")

# 4. Crear README
print("2. Creando README...")
readme = f"""# VECTA 12D
Creado: {datetime.now().strftime("%Y-%m-%d")}
Proyecto de 12 dimensiones vectoriales.
"""
with open("README.md", "w") as f:
    f.write(readme)

# 5. Primer commit
subprocess.run(["git", "add", "."], capture_output=True)
subprocess.run(["git", "commit", "-m", "Primer commit VECTA 12D"], capture_output=True)
print("✓ Primer commit realizado")

# 6. Crear script de ayuda
print("3. Creando script de ayuda...")
batch = """@echo off
echo.
echo =================================
echo GESTOR GITHUB VECTA 12D
echo =================================
echo.
echo 1. Ver estado actual (git status)
echo 2. Añadir todos los cambios (git add .)
echo 3. Hacer commit
echo 4. Subir a GitHub (git push)
echo 5. Abrir GitHub para crear repositorio
echo 6. Salir
echo.
set /p op=Elije opción (1-6): 

if "%op%"=="1" goto op1
if "%op%"=="2" goto op2
if "%op%"=="3" goto op3
if "%op%"=="4" goto op4
if "%op%"=="5" goto op5
if "%op%"=="6" exit

:op1
git status
pause
goto menu

:op2
git add .
echo ✓ Todos los archivos añadidos
pause
goto menu

:op3
set /p msg="Mensaje del commit: "
git commit -m "%msg%"
echo ✓ Commit realizado
pause
goto menu

:op4
git push
pause
goto menu

:op5
start https://github.com/new
echo ✓ Abre GitHub y crea repositorio "VECTA-12D-Automatico"
echo.
echo LUEGO EJECUTA ESTOS COMANDOS EN LA TERMINAL:
echo git remote add origin https://github.com/TU-USUARIO/VECTA-12D-Automatico.git
echo git branch -M main
echo git push -u origin main
pause
goto menu

:menu
git_help.bat
"""

with open("git_help.bat", "w") as f:
    f.write(batch)

print("\n" + "="*50)
print("✅ CONFIGURACIÓN COMPLETADA")
print("="*50)
print("\n📋 SIGUE ESTOS PASOS:")
print("\nA. CREA CUENTA EN GITHUB (si no tienes):")
print("   1. Ve a https://github.com")
print("   2. Regístrate (gratis)")
print("\nB. CREA REPOSITORIO:")
print("   1. Haz clic en '+' arriba derecha")
print("   2. 'New repository'")
print("   3. Nombre: VECTA-12D-Automatico")
print("   4. Marca 'Public'")
print("   5. NO marques 'Initialize with README'")
print("   6. 'Create repository'")
print("\nC. SUBE TU CÓDIGO:")
print("   En la página que aparece, copia estos 3 comandos")
print("   y ejecútalos UNO POR UNO en tu terminal:")
print("   ------------------------------------")
print("   git remote add origin https://github.com/TU-USUARIO/VECTA-12D-Automatico.git")
print("   git branch -M main")
print("   git push -u origin main")
print("   ------------------------------------")
print("\nD. COMPARTE EL ENLACE:")
print("   Tu enlace será: https://github.com/TU-USUARIO/VECTA-12D-Automatico")
print("   ¡PÉGALO AQUÍ CUANDO LO TENGAS!")
print("\nE. PARA USO DIARIO:")
print("   Ejecuta 'git_help.bat' para gestionar tu repositorio")
print("="*50)

input("\nPresiona Enter para terminar...")