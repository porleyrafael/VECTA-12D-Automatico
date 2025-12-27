#!/usr/bin/env python3
"""
VECTA 12D - EJECUTOR AUTOMATICO
Ejecuta comandos automaticamente despues de cambios
"""
import os
import sys
import time
from pathlib import Path

def main():
    # Obtener ruta actual
    base_dir = Path.cwd()
    
    print("VECTA 12D - Sistema de Snapshots")
    print("="*50)
    
    # Verificar si existe el sistema
    snapshot_system = base_dir / "vecta_snapshot_system.py"
    if not snapshot_system.exists():
        print("ERROR: Sistema de snapshots no encontrado")
        print("Ejecuta primero: python instalar_sistema_snapshot.py")
        return
    
    # Menu simple
    print("Opciones:")
    print("1. Crear snapshot ahora")
    print("2. Ver snapshots disponibles")
    print("3. Generar reporte para chat")
    print("4. Salir")
    
    try:
        opcion = input("\nSeleccion [1-4]: ").strip()
    except KeyboardInterrupt:
        print("\nSaliendo...")
        return
    
    if opcion == "1":
        razon = input("Razon del snapshot: ").strip()
        if not razon:
            razon = "Snapshot manual"
        
        import subprocess
        subprocess.run([sys.executable, "vecta_snapshot_system.py", "snapshot", razon])
    
    elif opcion == "2":
        import subprocess
        subprocess.run([sys.executable, "vecta_snapshot_system.py", "list"])
    
    elif opcion == "3":
        import subprocess
        result = subprocess.run([sys.executable, "vecta_snapshot_system.py", "report"], 
                              capture_output=True, text=True)
        print(result.stdout)
        
        # Preguntar si quiere guardar a archivo
        guardar = input("\n¿Guardar reporte en archivo? (s/n): ").lower()
        if guardar == 's':
            with open("reporte_vecta.txt", 'w', encoding='utf-8') as f:
                f.write(result.stdout)
            print("Reporte guardado como: reporte_vecta.txt")
    
    elif opcion == "4":
        print("Saliendo...")
    
    else:
        print("Opcion no valida")

if __name__ == "__main__":
    main()
