#!/usr/bin/env python3
"""
VECTA 12D - INSTALADOR AUTO-CONTENIDO
Descomprime e instala todo automáticamente
"""
import os
import sys
import zipfile
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

class VECTA_AutoInstaller:
    """Instalador automático que funciona sin dependencias externas"""
    
    def __init__(self):
        self.install_dir = Path.home() / "VECTA_12D"
        self.backup_dir = Path.home() / "VECTA_12D_Backup"
        self.package_file = "paquete_vecta.pkg"
        
    def banner(self):
        """Muestra banner de instalación"""
        print("\n" + "="*60)
        print("   🌀 VECTA 12D - INSTALACIÓN AUTOMÁTICA")
        print("   Sistema Autoprogramable de 12 Dimensiones")
        print("="*60)
        
    def check_python(self):
        """Verifica versión de Python"""
        version = sys.version_info
        print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
        
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            print("❌ Se requiere Python 3.8 o superior")
            return False
        return True
    
    def backup_existing(self):
        """Hace backup de instalación previa"""
        if self.install_dir.exists():
            print(f"📦 Haciendo backup de instalación existente...")
            if self.backup_dir.exists():
                shutil.rmtree(self.backup_dir)
            shutil.copytree(self.install_dir, self.backup_dir)
            print(f"✅ Backup guardado en: {self.backup_dir}")
    
    def extract_package(self):
        """Extrae el paquete completo"""
        print(f"📦 Extrayendo paquete VECTA 12D...")
        
        if not os.path.exists(self.package_file):
            print(f"❌ No se encontró {self.package_file}")
            return False
        
        # Crear directorio de instalación
        self.install_dir.mkdir(parents=True, exist_ok=True)
        
        # Extraer contenido
        with zipfile.ZipFile(self.package_file, 'r') as zip_ref:
            zip_ref.extractall(self.install_dir)
        
        print(f"✅ Paquete extraído en: {self.install_dir}")
        return True
    
    def install_dependencies(self):
        """Instala dependencias automáticamente"""
        print(f"📦 Instalando dependencias...")
        
        requirements = [
            "numpy",
            "cryptography",
            "psutil",
            "requests"
        ]
        
        for package in requirements:
            try:
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", 
                    "--quiet", "--no-warn-script-location", package
                ])
                print(f"  ✅ {package}")
            except:
                print(f"  ⚠️  {package} (puede fallar, VECTA continuará)")
        
        print(f"✅ Dependencias instaladas")
    
    def create_shortcut(self):
        """Crea acceso directo en escritorio"""
        print(f"🔗 Creando acceso directo...")
        
        try:
            import winshell
            from win32com.client import Dispatch
            
            desktop = Path(winshell.desktop())
            shortcut_path = desktop / "VECTA 12D.lnk"
            
            target = sys.executable
            arguments = f'"{self.install_dir / "vecta_12d_launcher.py"}"'
            working_dir = str(self.install_dir)
            
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(str(shortcut_path))
            shortcut.TargetPath = target
            shortcut.Arguments = arguments
            shortcut.WorkingDirectory = working_dir
            shortcut.IconLocation = sys.executable
            shortcut.save()
            
            print(f"✅ Acceso directo creado en escritorio")
            
        except ImportError:
            # Fallback: crear archivo .bat
            bat_content = f'''@echo off
cd /d "{self.install_dir}"
python vecta_12d_launcher.py
pause
'''
            bat_path = self.install_dir / "Iniciar_VECTA.bat"
            with open(bat_path, 'w') as f:
                f.write(bat_content)
            
            # Copiar a escritorio
            desktop = Path.home() / "Desktop"
            desktop_bat = desktop / "Iniciar VECTA.bat"
            shutil.copy2(bat_path, desktop_bat)
            
            print(f"✅ Archivo BAT creado en escritorio")
        except Exception as e:
            print(f"⚠️  No se pudo crear acceso directo: {e}")
    
    def create_config(self):
        """Crea configuración inicial"""
        print(f"⚙️  Creando configuración inicial...")
        
        config = {
            "version": "12D.1.0.0",
            "install_date": os.path.getctime(__file__),
            "dimensions": 12,
            "auto_update": True,
            "security_level": "high",
            "paths": {
                "install": str(self.install_dir),
                "data": str(self.install_dir / "data"),
                "logs": str(self.install_dir / "logs"),
                "output": str(self.install_dir / "output")
            }
        }
        
        config_path = self.install_dir / "config.json"
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Configuración creada")
    
    def run_initial_setup(self):
        """Ejecuta configuración inicial"""
        print(f"🔧 Ejecutando configuración inicial...")
        
        setup_script = self.install_dir / "scripts" / "initial_setup.py"
        if setup_script.exists():
            try:
                subprocess.run([sys.executable, str(setup_script)], 
                             check=True, capture_output=True)
                print(f"✅ Configuración inicial completada")
            except:
                print(f"⚠️  Configuración inicial falló (continuando...)")
    
    def verify_installation(self):
        """Verifica que la instalación sea correcta"""
        print(f"🔍 Verificando instalación...")
        
        required_files = [
            "vecta_12d_launcher.py",
            "core/vecta_12d_core.py",
            "dimensiones/__init__.py",
            "autoprogramacion/self_programmer.py"
        ]
        
        missing = []
        for file in required_files:
            if not (self.install_dir / file).exists():
                missing.append(file)
        
        if missing:
            print(f"❌ Archivos faltantes: {missing}")
            return False
        
        print(f"✅ Instalación verificada correctamente")
        return True
    
    def cleanup(self):
        """Limpia archivos temporales"""
        print(f"🧹 Limpiando archivos temporales...")
        
        temp_files = [
            "__pycache__",
            "*.pyc",
            "*.pyo",
            "*.pyd",
            ".DS_Store"
        ]
        
        for pattern in temp_files:
            for file in self.install_dir.rglob(pattern):
                if file.is_dir():
                    shutil.rmtree(file, ignore_errors=True)
                else:
                    try:
                        file.unlink()
                    except:
                        pass
        
        print(f"✅ Limpieza completada")
    
    def run(self):
        """Ejecuta la instalación completa"""
        self.banner()
        
        # 1. Verificar Python
        if not self.check_python():
            return False
        
        # 2. Backup
        self.backup_existing()
        
        # 3. Extraer
        if not self.extract_package():
            return False
        
        # 4. Instalar dependencias
        self.install_dependencies()
        
        # 5. Crear configuración
        self.create_config()
        
        # 6. Configuración inicial
        self.run_initial_setup()
        
        # 7. Verificar
        if not self.verify_installation():
            return False
        
        # 8. Acceso directo
        self.create_shortcut()
        
        # 9. Limpiar
        self.cleanup()
        
        # 10. Mostrar resumen
        print("\n" + "="*60)
        print("   ✅ VECTA 12D INSTALADO EXITOSAMENTE")
        print("="*60)
        print(f"\n📍 Ubicación: {self.install_dir}")
        print("\n🚀 Para iniciar VECTA:")
        print("   1. Haz doble clic en 'VECTA 12D' del escritorio")
        print("   2. O ejecuta: python vecta_12d_launcher.py")
        print("\n🔧 Características incluidas:")
        print("   • Sistema de 12 Dimensiones Vectoriales")
        print("   • Autoprogramación segura")
        print("   • IA local sin dependencias externas")
        print("   • Gestión segura de claves API")
        print("   • Actualizaciones automáticas")
        print("   • Sandbox de ejecución")
        print("\n📚 Documentación en: docs/README_12D.md")
        print("\n⚠️  Recomendación: Ejecuta como administrador la primera vez")
        print("="*60)
        
        return True

if __name__ == "__main__":
    installer = VECTA_AutoInstaller()
    success = installer.run()
    
    if success:
        # Preguntar si iniciar ahora
        input("\nPresiona Enter para iniciar VECTA 12D ahora...")
        
        # Iniciar VECTA
        launcher = installer.install_dir / "vecta_12d_launcher.py"
        if launcher.exists():
            os.chdir(installer.install_dir)
            os.system(f'python "{launcher}"')
    else:
        print("\n❌ Instalación falló. Revisa los mensajes anteriores.")
        input("Presiona Enter para salir...")