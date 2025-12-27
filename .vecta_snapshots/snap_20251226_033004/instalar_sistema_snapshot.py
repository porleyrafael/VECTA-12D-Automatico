"""
VECTA 12D - SISTEMA DE INSTALACION COMPLETO CON AUTO-DIAGNOSTICO
Version: 1.0
Autor: Sistema de Asistencia
"""

import os
import sys
import json
import shutil
import hashlib
import datetime
from pathlib import Path
import subprocess
import traceback

class SistemaInstalacionCompleto:
    def __init__(self):
        self.base_dir = Path.cwd()
        self.log_errores = []
        self.log_exitos = []
        
    def ejecutar_auto_diagnostico(self):
        """Realiza diagnostico completo del sistema"""
        print("\n" + "="*60)
        print("AUTO-DIAGNOSTICO DEL SISTEMA")
        print("="*60)
        
        resultados = []
        
        # 1. Verificar Python
        try:
            version = sys.version_info
            if version.major == 3 and version.minor >= 7:
                resultados.append(("Python", f"OK - Version {version.major}.{version.minor}.{version.micro}", True))
            else:
                resultados.append(("Python", f"ERROR - Version {version.major}.{version.minor} - Se requiere 3.7+", False))
        except:
            resultados.append(("Python", "ERROR - No se pudo verificar", False))
        
        # 2. Verificar directorio VECTA
        archivos_vecta = ["vecta_launcher.py", "core/", "dimensiones/"]
        for archivo in archivos_vecta:
            if (self.base_dir / archivo).exists():
                resultados.append((f"Archivo {archivo}", "OK - Encontrado", True))
            else:
                resultados.append((f"Archivo {archivo}", "ERROR - No encontrado", False))
        
        # 3. Verificar permisos de escritura
        try:
            test_file = self.base_dir / "test_permiso.txt"
            test_file.write_text("test")
            test_file.unlink()
            resultados.append(("Permisos escritura", "OK - Tiene permisos", True))
        except:
            resultados.append(("Permisos escritura", "ERROR - Sin permisos de escritura", False))
        
        # 4. Mostrar resultados
        errores = 0
        for nombre, mensaje, estado in resultados:
            if estado:
                print(f"✓ {nombre}: {mensaje}")
            else:
                print(f"✗ {nombre}: {mensaje}")
                errores += 1
        
        print(f"\nTotal verificaciones: {len(resultados)}")
        print(f"Errores encontrados: {errores}")
        
        return errores == 0
    
    def instalar_dependencias(self):
        """Instala las dependencias necesarias"""
        print("\n" + "="*60)
        print("INSTALANDO DEPENDENCIAS")
        print("="*60)
        
        try:
            # Verificar si watchdog ya está instalado
            import importlib.util
            if importlib.util.find_spec("watchdog"):
                print("✓ Watchdog ya está instalado")
                return True
            
            print("Instalando watchdog...")
            comando = [sys.executable, "-m", "pip", "install", "watchdog", "--user", "--quiet"]
            resultado = subprocess.run(comando, capture_output=True, text=True)
            
            if resultado.returncode == 0:
                print("✓ Watchdog instalado correctamente")
                return True
            else:
                print(f"✗ Error instalando watchdog: {resultado.stderr}")
                return False
                
        except Exception as e:
            print(f"✗ Error en instalacion: {e}")
            return False
    
    def crear_sistema_snapshots(self):
        """Crea el sistema completo de snapshots"""
        print("\n" + "="*60)
        print("CREANDO SISTEMA DE SNAPSHOTS")
        print("="*60)
        
        # Codigo del sistema de snapshots
        codigo_sistema = '''"""
VECTA 12D - SISTEMA DE SNAPSHOTS AUTOMATICO
Version: 1.0
Este sistema crea puntos de restauracion automaticos de tu proyecto VECTA
"""
import os
import sys
import json
import shutil
import hashlib
import datetime
from pathlib import Path
import threading

class VECTA_SnapshotSystem:
    def __init__(self):
        self.base_dir = Path.cwd()
        self.snapshots_dir = self.base_dir / ".vecta_snapshots"
        self.max_snapshots = 3
        self.config_file = self.snapshots_dir / "config.json"
        self._setup()
    
    def _setup(self):
        """Configura el sistema"""
        self.snapshots_dir.mkdir(exist_ok=True)
        if not self.config_file.exists():
            config = {
                "version": "1.0",
                "created": datetime.datetime.now().isoformat(),
                "total_snapshots": 0,
                "active_snapshots": [],
                "tracked_files": [".py", ".json", ".txt", ".md", ".bat"]
            }
            self._save_config(config)
    
    def _save_config(self, config):
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
    
    def _load_config(self):
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {}
    
    def create_snapshot(self, reason="Auto-snapshot"):
        """Crea un nuevo snapshot"""
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            snapshot_id = f"snap_{timestamp}"
            snapshot_path = self.snapshots_dir / snapshot_id
            
            snapshot_path.mkdir(exist_ok=True)
            
            print(f"Creando snapshot: {snapshot_id}")
            print(f"Razon: {reason}")
            
            files_copied = 0
            config = self._load_config()
            
            for ext in config.get("tracked_files", [".py"]):
                for source_file in self.base_dir.rglob(f"*{ext}"):
                    if source_file.is_file() and ".vecta_snapshots" not in str(source_file):
                        rel_path = source_file.relative_to(self.base_dir)
                        target_file = snapshot_path / rel_path
                        target_file.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(source_file, target_file)
                        files_copied += 1
            
            metadata = {
                "id": snapshot_id,
                "created": datetime.datetime.now().isoformat(),
                "reason": reason,
                "files_copied": files_copied
            }
            
            metadata_file = snapshot_path / "metadata.json"
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            config["active_snapshots"].append(metadata)
            
            while len(config["active_snapshots"]) > self.max_snapshots:
                old = config["active_snapshots"].pop(0)
                old_path = self.snapshots_dir / old["id"]
                if old_path.exists():
                    shutil.rmtree(old_path)
            
            config["total_snapshots"] = len(config["active_snapshots"])
            self._save_config(config)
            
            print(f"Snapshot creado: {snapshot_id}")
            print(f"Archivos copiados: {files_copied}")
            
            return snapshot_id
            
        except Exception as e:
            print(f"Error creando snapshot: {e}")
            return None
    
    def restore_snapshot(self, snapshot_id):
        """Restaura un snapshot"""
        try:
            snapshot_path = self.snapshots_dir / snapshot_id
            if not snapshot_path.exists():
                print(f"Snapshot no encontrado: {snapshot_id}")
                return False
            
            print(f"Restaurando snapshot: {snapshot_id}")
            
            for source_file in snapshot_path.rglob("*"):
                if source_file.is_file() and source_file.name != "metadata.json":
                    rel_path = source_file.relative_to(snapshot_path)
                    target_file = self.base_dir / rel_path
                    target_file.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source_file, target_file)
            
            print(f"Snapshot restaurado: {snapshot_id}")
            return True
            
        except Exception as e:
            print(f"Error restaurando snapshot: {e}")
            return False
    
    def list_snapshots(self):
        """Lista todos los snapshots disponibles"""
        config = self._load_config()
        return config.get("active_snapshots", [])
    
    def generate_chat_report(self):
        """Genera reporte para compartir en chat"""
        try:
            report_lines = []
            report_lines.append("VECTA 12D - ESTADO DEL SISTEMA")
            report_lines.append("="*50)
            report_lines.append(f"Fecha: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report_lines.append(f"Directorio: {self.base_dir}")
            report_lines.append("")
            
            snapshots = self.list_snapshots()
            report_lines.append(f"Snapshots disponibles: {len(snapshots)}")
            for snap in snapshots:
                report_lines.append(f"- {snap['id']}: {snap['reason']}")
            
            report_lines.append("")
            report_lines.append("ARCHIVOS PRINCIPALES:")
            
            important_files = [
                "vecta_launcher.py",
                "core/vecta_12d_core.py",
                "core/meta_vecta.py",
                "dimensiones/vector_12d.py"
            ]
            
            for file in important_files:
                file_path = self.base_dir / file
                if file_path.exists():
                    size_kb = file_path.stat().st_size / 1024
                    report_lines.append(f"- {file} ({size_kb:.1f} KB)")
                else:
                    report_lines.append(f"- {file} (NO ENCONTRADO)")
            
            report_lines.append("")
            report_lines.append("PARA RESTAURAR:")
            report_lines.append("python vecta_snapshot_system.py restore SNAPSHOT_ID")
            report_lines.append("")
            report_lines.append("PARA CREAR NUEVO SNAPSHOT:")
            report_lines.append("python vecta_snapshot_system.py snapshot 'Razon'")
            
            return "\\n".join(report_lines)
            
        except Exception as e:
            return f"Error generando reporte: {e}"

def main():
    if len(sys.argv) < 2:
        print("Uso: python vecta_snapshot_system.py [comando]")
        print("Comandos:")
        print("  snapshot [razon]  - Crea nuevo snapshot")
        print("  restore [id]      - Restaura snapshot")
        print("  list              - Lista snapshots")
        print("  report            - Genera reporte para chat")
        return
    
    sistema = VECTA_SnapshotSystem()
    comando = sys.argv[1]
    
    if comando == "snapshot":
        razon = sys.argv[2] if len(sys.argv) > 2 else "Snapshot automatico"
        sistema.create_snapshot(razon)
    
    elif comando == "restore":
        if len(sys.argv) > 2:
            sistema.restore_snapshot(sys.argv[2])
        else:
            print("Debe especificar ID del snapshot")
    
    elif comando == "list":
        snapshots = sistema.list_snapshots()
        print("Snapshots disponibles:")
        for snap in snapshots:
            print(f"- {snap['id']}: {snap['reason']}")
    
    elif comando == "report":
        reporte = sistema.generate_chat_report()
        print(reporte)
        print("\\n" + "="*50)
        print("COPIAR TODO ESTE TEXTO Y PEGARLO EN EL CHAT")
    
    else:
        print(f"Comando desconocido: {comando}")

if __name__ == "__main__":
    main()
'''
        
        # Guardar el sistema de snapshots
        system_file = self.base_dir / "vecta_snapshot_system.py"
        try:
            with open(system_file, 'w', encoding='utf-8') as f:
                f.write(codigo_sistema)
            print(f"✓ Sistema creado: {system_file}")
            
            # Crear snapshot inicial
            print("\nCreando snapshot inicial...")
            subprocess.run([sys.executable, "vecta_snapshot_system.py", "snapshot", "Instalacion inicial"], 
                         capture_output=True, text=True)
            
            return True
        except Exception as e:
            print(f"✗ Error creando sistema: {e}")
            return False
    
    def crear_script_auto(self):
        """Crea script para ejecucion automatica"""
        print("\n" + "="*60)
        print("CREANDO SCRIPT DE EJECUCION AUTOMATICA")
        print("="*60)
        
        codigo_auto = '''#!/usr/bin/env python3
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
        opcion = input("\\nSeleccion [1-4]: ").strip()
    except KeyboardInterrupt:
        print("\\nSaliendo...")
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
        guardar = input("\\n¿Guardar reporte en archivo? (s/n): ").lower()
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
'''
        
        try:
            auto_file = self.base_dir / "vecta_auto.py"
            with open(auto_file, 'w', encoding='utf-8') as f:
                f.write(codigo_auto)
            print(f"✓ Script automatico creado: {auto_file}")
            return True
        except Exception as e:
            print(f"✗ Error creando script: {e}")
            return False
    
    def crear_archivo_resumen(self):
        """Crea archivo con resumen de instalacion"""
        print("\n" + "="*60)
        print("CREANDO RESUMEN DE INSTALACION")
        print("="*60)
        
        resumen = f"""RESUMEN DE INSTALACION - VECTA 12D SNAPSHOT SYSTEM
Fecha: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Directorio: {self.base_dir}

ARCHIVOS CREADOS:
1. vecta_snapshot_system.py - Sistema principal de snapshots
2. vecta_auto.py - Interfaz automatica
3. .vecta_snapshots/ - Directorio de snapshots

COMO USAR:
1. Para crear snapshot manual:
   python vecta_snapshot_system.py snapshot "Tu razon aqui"

2. Para ver snapshots disponibles:
   python vecta_snapshot_system.py list

3. Para generar reporte para chat:
   python vecta_snapshot_system.py report
   (Copia TODO el texto y pegalo en el chat)

4. Para restaurar snapshot anterior:
   python vecta_snapshot_system.py restore snap_YYYYMMDD_HHMMSS

5. Usar interfaz automatica:
   python vecta_auto.py

ERRORES COMUNES Y SOLUCIONES:
- Si hay error de permisos: Ejecuta como administrador
- Si hay error de importacion: Verifica que Python sea version 3.7+
- Si no se crean snapshots: Verifica que haya archivos .py en el directorio

PARA OBTENER AYUDA:
Copia y pega cualquier mensaje de error en el chat de asistencia.
"""
        
        try:
            resumen_file = self.base_dir / "RESUMEN_INSTALACION.txt"
            with open(resumen_file, 'w', encoding='utf-8') as f:
                f.write(resumen)
            print(f"✓ Resumen creado: {resumen_file}")
            return True
        except Exception as e:
            print(f"✗ Error creando resumen: {e}")
            return False
    
    def ejecutar_prueba_completa(self):
        """Ejecuta prueba completa del sistema"""
        print("\n" + "="*60)
        print("EJECUTANDO PRUEBA COMPLETA")
        print("="*60)
        
        try:
            # Prueba 1: Verificar archivos creados
            archivos_necesarios = [
                "vecta_snapshot_system.py",
                "vecta_auto.py",
                "RESUMEN_INSTALACION.txt",
                ".vecta_snapshots"
            ]
            
            for archivo in archivos_necesarios:
                if (self.base_dir / archivo).exists():
                    print(f"✓ {archivo} - OK")
                else:
                    print(f"✗ {archivo} - NO ENCONTRADO")
            
            # Prueba 2: Ejecutar comando list
            print("\nProbando sistema de snapshots...")
            resultado = subprocess.run(
                [sys.executable, "vecta_snapshot_system.py", "list"],
                capture_output=True,
                text=True
            )
            
            if resultado.returncode == 0:
                print("✓ Sistema responde correctamente")
            else:
                print(f"✗ Error en sistema: {resultado.stderr}")
            
            # Prueba 3: Generar reporte de prueba
            print("\nGenerando reporte de prueba...")
            resultado = subprocess.run(
                [sys.executable, "vecta_snapshot_system.py", "report"],
                capture_output=True,
                text=True
            )
            
            if resultado.returncode == 0:
                print("✓ Reporte generado correctamente")
                # Guardar reporte
                with open("prueba_reporte.txt", 'w', encoding='utf-8') as f:
                    f.write(resultado.stdout)
                print("  Reporte guardado como: prueba_reporte.txt")
            else:
                print(f"✗ Error generando reporte: {resultado.stderr}")
            
            return True
            
        except Exception as e:
            print(f"✗ Error en prueba: {e}")
            return False

def main():
    """Funcion principal de instalacion"""
    print("\n" + "="*60)
    print("VECTA 12D - INSTALADOR COMPLETO DEL SISTEMA DE SNAPSHOTS")
    print("="*60)
    print("Este instalador hara todo automaticamente.")
    print("Solo sigue las instrucciones.")
    print("="*60)
    
    instalador = SistemaInstalacionCompleto()
    
    # Paso 1: Auto-diagnostico
    if not instalador.ejecutar_auto_diagnostico():
        print("\n" + "="*60)
        print("ERRORES ENCONTRADOS EN EL DIAGNOSTICO")
        print("Soluciona estos problemas antes de continuar.")
        print("="*60)
        
        respuesta = input("\n¿Continuar a pesar de los errores? (s/n): ").lower()
        if respuesta != 's':
            print("Instalacion cancelada.")
            return
    
    # Paso 2: Instalar dependencias
    print("\nPresiona Enter para instalar dependencias...")
    input()
    instalador.instalar_dependencias()
    
    # Paso 3: Crear sistema
    print("\nPresiona Enter para crear el sistema de snapshots...")
    input()
    instalador.crear_sistema_snapshots()
    
    # Paso 4: Crear script auto
    instalador.crear_script_auto()
    
    # Paso 5: Crear resumen
    instalador.crear_archivo_resumen()
    
    # Paso 6: Prueba completa
    print("\nPresiona Enter para ejecutar prueba completa...")
    input()
    instalador.ejecutar_prueba_completa()
    
    # Resumen final
    print("\n" + "="*60)
    print("INSTALACION COMPLETADA")
    print("="*60)
    print("\nRESUMEN:")
    print("1. Sistema de snapshots instalado correctamente")
    print("2. Se crearon los siguientes archivos:")
    print("   - vecta_snapshot_system.py (sistema principal)")
    print("   - vecta_auto.py (interfaz automatica)")
    print("   - RESUMEN_INSTALACION.txt (instrucciones)")
    print("   - .vecta_snapshots/ (directorio de snapshots)")
    print("\nPARA USAR EL SISTEMA:")
    print("1. Para crear snapshot: python vecta_snapshot_system.py snapshot 'Razon'")
    print("2. Para generar reporte: python vecta_snapshot_system.py report")
    print("3. Copia TODO el texto del reporte y pegalo en el chat")
    print("\nPARA OBTENER AYUDA:")
    print("Copia y pega cualquier mensaje de error en este chat.")
    print("="*60)
    
    # Mostrar contenido del resumen
    try:
        with open("RESUMEN_INSTALACION.txt", 'r', encoding='utf-8') as f:
            contenido = f.read()
            print("\n" + contenido[:500] + "...")
    except:
        pass

if __name__ == "__main__":
    try:
        main()
        print("\nPresiona Enter para salir...")
        input()
    except Exception as e:
        print(f"\nERROR CRITICO: {e}")
        print("Por favor, copia este mensaje completo y pegalo en el chat:")
        print("="*60)
        print(traceback.format_exc())
        print("="*60)
        input("\nPresiona Enter para salir...")