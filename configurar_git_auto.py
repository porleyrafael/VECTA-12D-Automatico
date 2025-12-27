#!/usr/bin/env python3
"""
CONFIGURADOR AUTOMÁTICO GIT + GITHUB
Solo ejecútalo y sigue las instrucciones
"""

import os
import sys
import subprocess
import webbrowser

def ejecutar_comando(comando):
    """Ejecuta un comando y muestra el resultado"""
    print(f"▶ Ejecutando: {comando}")
    resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
    if resultado.returncode == 0:
        print(f"✓ Éxito: {resultado.stdout}")
        return True
    else:
        print(f"✗ Error: {resultado.stderr}")
        return False

def main():
    print("="*60)
    print("CONFIGURADOR GIT AUTOMÁTICO")
    print("="*60)
    
    # 1. Verificar Git
    print("\n🔍 Verificando Git...")
    if not ejecutar_comando("git --version"):
        print("\n❌ Git no encontrado. Instálalo desde:")
        print("   https://git-scm.com/download/win")
        webbrowser.open("https://git-scm.com/download/win")
        return
    
    # 2. Pedir datos al usuario
    print("\n📝 CONFIGURACIÓN DE IDENTIDAD")
    print("   (Usa los mismos datos que en GitHub)")
    
    nombre = input("   Tu nombre completo: ")
    email = input("   Tu email (usado en GitHub): ")
    
    # 3. Configurar Git
    print("\n⚙️ Configurando Git...")
    ejecutar_comando(f'git config --global user.name "{nombre}"')
    ejecutar_comando(f'git config --global user.email "{email}"')
    
    # 4. Verificar configuración
    print("\n✅ Configuración guardada:")
    ejecutar_comando("git config --global user.name")
    ejecutar_comando("git config --global user.email")
    
    # 5. Inicializar repositorio (si no existe)
    print("\n📁 Configurando repositorio...")
    if not os.path.exists(".git"):
        ejecutar_comando("git init")
    
    # 6. Añadir todo
    ejecutar_comando("git add .")
    
    # 7. Commit
    ejecutar_comando('git commit -m "Subida automática VECTA 12D"')
    
    # 8. Configurar remote
    print("\n🌐 Configurando conexión con GitHub...")
    ejecutar_comando("git remote remove origin 2>nul")
    ejecutar_comando("git remote add origin https://github.com/porleyrafael/VECTA-12D-Automatico.git")
    
    # 9. Crear y subir rama main
    print("\n🚀 Subiendo a GitHub...")
    ejecutar_comando("git branch -M main")
    
    if ejecutar_comando("git push -u origin main"):
        print("\n" + "="*60)
        print("🎉 ¡ÉXITO TOTAL!")
        print("="*60)
        print(f"\n✅ Tu código está ahora en:")
        print("   https://github.com/porleyrafael/VECTA-12D-Automatico")
        print("\n📊 Puedes verlo en tu navegador.")
        print("🔗 Comparte ese enlace conmigo para ayudarte.")
        
        # Abrir el repositorio
        webbrowser.open("https://github.com/porleyrafael/VECTA-12D-Automatico")
    else:
        print("\n⚠️  Hubo un error al subir.")
        print("   Intenta estos comandos manualmente:")
        print("   1. git push -u origin main")
        print("   2. Si falla: git pull origin main --allow-unrelated-histories")
        print("   3. Luego: git push -u origin main")
    
    print("\n💡 Presiona Enter para salir...")
    input()

if __name__ == "__main__":
    main()