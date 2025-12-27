#!/usr/bin/env python3

import os
import subprocess

print("="*50)
print("CONFIGURACIÓN GITHUB PARA VECTA 12D")
print("="*50)

# Inicializar repositorio Git
print("\n1. Inicializando repositorio Git...")
os.system("git init")
os.system("git add .")

# Crear .gitignore
with open(".gitignore", "w") as f:
    f.write("__pycache__/\n*.pyc\n")

# Crear README básico
with open("README.md", "w") as f:
    f.write("# VECTA 12D\nProyecto de dimensiones vectoriales.")

# Primer commit
os.system('git commit -m "Primer commit VECTA 12D"')

print("\n✅ REPOSITORIO LOCAL CREADO")
print("\n📋 AHORA HAZ ESTO:")
print("1. Ve a https://github.com y crea cuenta (si no tienes)")
print("2. Crea nuevo repositorio llamado: VECTA-12D-Automatico")
print("3. Sigue las instrucciones de GitHub para subir tu código")
print("\n🔗 Cuando tengas el enlace, pégamelo aquí.")
print("="*50)