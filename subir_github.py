#!/usr/bin/env python3
"""
AUTO-SUBIDA A GITHUB para VECTA 12D
Sube automáticamente todo tu proyecto
"""

import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

def subir_github_auto():
    """Sube automáticamente VECTA a GitHub"""
    
    print("="*60)
    print("🚀 AUTO-SUBIDA VECTA 12D A GITHUB")
    print("="*60)
    
    # Ruta del proyecto
    proyecto_path = Path.cwd()
    print(f"📁 Proyecto: {proyecto_path}")
    
    # Verificar si es un repositorio git
    if not (proyecto_path / ".git").exists():
        print("❌ No es un repositorio Git")
        print("   Ejecutando: git init")
        subprocess.run(["git", "init"], check=True)
    
    # 1. Añadir TODO
    print("\n1. 📦 Añadiendo archivos...")
    resultado = subprocess.run(["git", "add", "--all"], 
                             capture_output=True, text=True)
    
    if resultado.returncode != 0:
        print(f"❌ Error añadiendo: {resultado.stderr}")
        return False
    
    print("✅ Archivos añadidos")
    
    # 2. Crear commit
    print("\n2. 📝 Creando commit...")
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
    mensaje = f"Auto-update VECTA 12D - {fecha}"
    
    resultado = subprocess.run(["git", "commit", "-m", mensaje],
                             capture_output=True, text=True)
    
    if resultado.returncode != 0:
        print(f"⚠️  Commit no creado (posiblemente sin cambios): {resultado.stderr[:100]}")
        print("   Continuando de todos modos...")
    
    print(f"✅ Commit creado: {mensaje}")
    
    # 3. Subir a GitHub
    print("\n3. ☁️  Subiendo a GitHub...")
    
    # Intentar diferentes nombres de rama
    ramas = ["main", "master"]
    
    for rama in ramas:
        print(f"   Intentando rama: {rama}")
        resultado = subprocess.run(["git", "push", "-u", "origin", rama],
                                 capture_output=True, text=True)
        
        if resultado.returncode == 0:
            print(f"✅ ¡Subido exitosamente a rama {rama}!")
            break
        else:
            print(f"   ❌ Falló en {rama}: {resultado.stderr[:100]}")
    
    # 4. Mostrar resultado
    print("\n" + "="*60)
    print("📊 RESULTADO DE SUBIDA:")
    
    # Verificar estado
    resultado = subprocess.run(["git", "status"], 
                             capture_output=True, text=True)
    print(resultado.stdout[:500])
    
    print("\n🔍 Verifica en: https://github.com/porleyrafael/VECTA-12D-Automatico")
    print("   Deberías ver los cambios recientes.")
    
    # 5. Opción para configurar si hay errores
    print("\n" + "="*60)
    print("⚙️  SI HUBO ERRORES, CONFIGURA:")
    
    configurar = input("¿Configurar usuario/email de Git? (s/n): ").strip().lower()
    
    if configurar == 's':
        email = input("Tu email de GitHub: ").strip()
        nombre = input("Tu nombre: ").strip()
        
        subprocess.run(["git", "config", "--global", "user.email", email])
        subprocess.run(["git", "config", "--global", "user.name", nombre])
        
        print("✅ Configurado. Intenta subir de nuevo.")
    
    return True

if __name__ == "__main__":
    try:
        subir_github_auto()
        input("\nPresiona ENTER para salir...")
    except KeyboardInterrupt:
        print("\n\n❌ Cancelado por usuario")
    except Exception as e:
        print(f"\n💥 Error crítico: {e}")
        print("\n💡 SOLUCIÓN ALTERNATIVA:")
        print("1. Usa el método manual por la web")
        print("2. O ejecuta estos comandos en PowerShell:")
        print("   git add --all")
        print("   git commit -m 'Update'")
        print("   git push origin main")