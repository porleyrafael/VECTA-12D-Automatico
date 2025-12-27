#!/usr/bin/env python3
"""
VECTA 12D - LANZADOR PRINCIPAL
Sistema de 12 Dimensiones Vectoriales
Versión: 2.0.0
"""
import sys
import os
from pathlib import Path

def main():
    print("\n" + "="*60)
    print("🚀 VECTA 12D - SISTEMA DE 12 DIMENSIONES")
    print("="*60)
    print("Versión: 2.0.0")
    print("Modo: Sistema Vectorial Autoprogramable")
    print("="*60)
    
    # Asegurarnos de que estamos en el directorio correcto
    base_dir = Path(__file__).parent
    os.chdir(base_dir)
    
    # Añadir directorios al path
    sys.path.insert(0, str(base_dir))
    if (base_dir / "dimensiones").exists():
        sys.path.insert(0, str(base_dir / "dimensiones"))
    if (base_dir / "core").exists():
        sys.path.insert(0, str(base_dir / "core"))
    
    try:
        # Intentar cargar el núcleo de VECTA
        print("\n📦 Cargando sistema VECTA 12D...")
        
        # Primero verificar si existen los archivos necesarios
        if not (base_dir / "core" / "vecta_12d_core.py").exists():
            print("❌ Error: No se encontró el núcleo de VECTA")
            print("   Asegúrate de que 'core/vecta_12d_core.py' existe")
            input("\nPresiona Enter para salir...")
            return
        
        # Importar el núcleo
        from core.vecta_12d_core import VECTA_12D_Core
        
        print("✅ Sistema cargado exitosamente")
        print("✅ 12 dimensiones vectoriales activas")
        
        # Crear instancia
        vecta = VECTA_12D_Core()
        
        # Verificar modo de ejecución
        if len(sys.argv) > 1:
            if sys.argv[1] == "--gui":
                print("\n🎨 Iniciando interfaz gráfica...")
                vecta.start_gui()
            elif sys.argv[1] == "--help" or sys.argv[1] == "-h":
                mostrar_ayuda()
            else:
                print(f"\n⚠️  Opción desconocida: {sys.argv[1]}")
                mostrar_ayuda()
        else:
            # Modo por defecto: interfaz de texto
            print("\n💻 Iniciando en modo consola...")
            print("   Escribe 'salir' para terminar")
            print("   Escribe 'estado' para ver información del sistema")
            print("   Escribe 'ayuda' para ver comandos disponibles")
            print("-" * 40)
            vecta.start_text_interface()
            
    except ImportError as e:
        print(f"❌ Error importando módulos: {e}")
        print("\n📋 Solución:")
        print("1. Ejecuta primero: python vecta_corregido.py")
        print("2. O verifica que los directorios 'core/' y 'dimensiones/' existen")
        
        # Mostrar estructura actual
        print("\n📁 Estructura actual:")
        for item in base_dir.iterdir():
            if item.is_dir():
                print(f"  📁 {item.name}/")
            else:
                print(f"  📄 {item.name}")
        
        input("\nPresiona Enter para salir...")
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        input("\nPresiona Enter para salir...")

def mostrar_ayuda():
    """Muestra la ayuda del sistema"""
    print("\n📖 AYUDA VECTA 12D:")
    print("="*40)
    print("Uso: python vecta_launcher.py [OPCIÓN]")
    print("\nOpciones:")
    print("  --gui       Inicia interfaz gráfica")
    print("  --help      Muestra esta ayuda")
    print("  --version   Muestra la versión")
    print("\nSin opciones: Inicia en modo consola")
    print("\nComandos en modo consola:")
    print("  salir       Termina el programa")
    print("  estado      Muestra información del sistema")
    print("  ayuda       Muestra comandos disponibles")
    print("="*40)

def mostrar_version():
    """Muestra la versión del sistema"""
    print("\n📊 VERSIÓN VECTA 12D:")
    print("="*40)
    print("Sistema: VECTA 12D")
    print("Versión: 2.0.0")
    print("Estado: Sistema de 12 Dimensiones Vectoriales")
    print("Autor: Sistema Autoprogramable VECTA")
    print("="*40)

if __name__ == "__main__":
    # Verificar si se solicita ayuda o versión
    if len(sys.argv) > 1:
        if sys.argv[1] == "--version" or sys.argv[1] == "-v":
            mostrar_version()
            sys.exit(0)
        elif sys.argv[1] == "--help" or sys.argv[1] == "-h":
            mostrar_ayuda()
            sys.exit(0)
    
    main()