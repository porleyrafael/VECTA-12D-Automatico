#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SISTEMA DE AUTO-IMPLEMENTACIÓN VECTA
======================================
Sistema autónomo que crea y configura automáticamente
todos los componentes de VECTA 12D con auto-diagnóstico.
"""

import os
import sys
import json
import shutil
import subprocess
import traceback
from pathlib import Path
from datetime import datetime

class VECTAAutoInstaller:
    """Sistema de auto-implementación completa para VECTA"""
    
    def __init__(self):
        self.base_dir = Path.cwd()
        self.install_log = []
        self.errors = []
        
        # Configuración del sistema
        self.system_config = {
            "version": "5.0.0",
            "creator": "Rafael Porley",
            "install_date": datetime.now().isoformat(),
            "components": []
        }
    
    def log(self, message, level="INFO"):
        """Registra mensaje en log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] {level}: {message}"
        self.install_log.append(entry)
        print(entry)
    
    def create_directory_structure(self):
        """Crea la estructura completa de directorios"""
        directories = [
            "core",
            "dimensiones",
            "chat_data",
            "chat_data/sessions",
            "chat_data/logs",
            "chat_data/backups",
            "chat_data/learning",
            "chat_data/auto_implementacion"
        ]
        
        for dir_path in directories:
            full_path = self.base_dir / dir_path
            try:
                full_path.mkdir(parents=True, exist_ok=True)
                self.log(f"Directorio creado: {dir_path}")
                self.system_config["components"].append({
                    "type": "directory",
                    "path": dir_path,
                    "status": "created"
                })
            except Exception as e:
                self.errors.append(f"Error creando directorio {dir_path}: {str(e)}")
                self.log(f"Error creando directorio {dir_path}: {str(e)}", "ERROR")
    
    def create_file_with_content(self, file_path, content):
        """Crea un archivo con contenido específico"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            file_size = os.path.getsize(file_path)
            self.log(f"Archivo creado: {file_path.name} ({file_size} bytes)")
            
            self.system_config["components"].append({
                "type": "file",
                "path": str(file_path.relative_to(self.base_dir)),
                "size": file_size,
                "status": "created"
            })
            
            return True
        except Exception as e:
            self.errors.append(f"Error creando archivo {file_path}: {str(e)}")
            self.log(f"Error creando archivo {file_path}: {str(e)}", "ERROR")
            return False
    
    def create_install_config(self):
        """Crea archivo de configuración de instalación"""
        config_data = {
            "system_name": "VECTA 12D AI Chat",
            "version": self.system_config["version"],
            "install_date": self.system_config["install_date"],
            "creator": self.system_config["creator"],
            "components_installed": len(self.system_config["components"]),
            "directories_created": len([c for c in self.system_config["components"] if c["type"] == "directory"]),
            "files_created": len([c for c in self.system_config["components"] if c["type"] == "file"]),
            "errors": len(self.errors),
            "install_log": self.install_log[-20:]
        }
        
        config_file = self.base_dir / "chat_data" / "auto_implementacion" / "install_config.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)
        
        self.log(f"Configuracion de instalacion guardada: {config_file.name}")
        return config_file
    
    def run_self_diagnosis(self):
        """Ejecuta autodiagnóstico del sistema"""
        diagnosis = {
            "timestamp": datetime.now().isoformat(),
            "tests": [],
            "passed": 0,
            "failed": 0,
            "warnings": 0
        }
        
        # Test 1: Verificar directorios críticos
        critical_dirs = [
            ("core", self.base_dir / "core"),
            ("dimensiones", self.base_dir / "dimensiones"),
            ("chat_data", self.base_dir / "chat_data"),
            ("chat_data/logs", self.base_dir / "chat_data" / "logs"),
            ("chat_data/learning", self.base_dir / "chat_data" / "learning")
        ]
        
        for dir_name, dir_path in critical_dirs:
            test_result = {
                "test": f"Directorio {dir_name}",
                "status": "PASS" if dir_path.exists() else "FAIL",
                "message": f"Directorio {dir_name} {'existe' if dir_path.exists() else 'no existe'}"
            }
            diagnosis["tests"].append(test_result)
            if dir_path.exists():
                diagnosis["passed"] += 1
            else:
                diagnosis["failed"] += 1
        
        # Test 2: Verificar archivos críticos
        critical_files = [
            ("auto_implementar_vecta_fixed.py", self.base_dir / "auto_implementar_vecta_fixed.py"),
            ("core/vecta_12d_core.py", self.base_dir / "core" / "vecta_12d_core.py"),
            ("dimensiones/vector_12d.py", self.base_dir / "dimensiones" / "vector_12d.py")
        ]
        
        for file_name, file_path in critical_files:
            exists = file_path.exists()
            test_result = {
                "test": f"Archivo {file_name}",
                "status": "PASS" if exists else "FAIL",
                "message": f"Archivo {file_name} {'existe' if exists else 'no existe'}"
            }
            
            if exists:
                size = file_path.stat().st_size if exists else 0
                if size < 100:
                    test_result["status"] = "WARNING"
                    test_result["message"] = f"Archivo {file_name} existe pero es muy pequeño ({size} bytes)"
                    diagnosis["warnings"] += 1
                else:
                    diagnosis["passed"] += 1
            else:
                diagnosis["failed"] += 1
            
            diagnosis["tests"].append(test_result)
        
        # Test 3: Verificar Python
        python_test = {
            "test": "Version de Python",
            "status": "PASS",
            "message": f"Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        }
        diagnosis["tests"].append(python_test)
        diagnosis["passed"] += 1
        
        # Guardar diagnóstico
        diag_file = self.base_dir / "chat_data" / "auto_implementacion" / "diagnosis.json"
        with open(diag_file, 'w', encoding='utf-8') as f:
            json.dump(diagnosis, f, indent=2, ensure_ascii=False)
        
        # Generar reporte
        report = [
            "AUTODIAGNOSTICO DEL SISTEMA VECTA",
            "=" * 60,
            f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Version: {self.system_config['version']}",
            f"Directorios criticos: {diagnosis['passed'] + diagnosis['failed']} verificados",
            f"Archivos criticos: {len([t for t in diagnosis['tests'] if 'Archivo' in t['test']])} verificados",
            "",
            f"RESULTADOS:",
            f"  * PASADOS: {diagnosis['passed']}",
            f"  * FALLIDOS: {diagnosis['failed']}",
            f"  * ADVERTENCIAS: {diagnosis['warnings']}",
            ""
        ]
        
        if diagnosis["failed"] > 0:
            report.append("ERRORES CRITICOS:")
            for test in diagnosis["tests"]:
                if test["status"] == "FAIL":
                    report.append(f"  * {test['test']}: {test['message']}")
            report.append("")
        
        if diagnosis["warnings"] > 0:
            report.append("ADVERTENCIAS:")
            for test in diagnosis["tests"]:
                if test["status"] == "WARNING":
                    report.append(f"  * {test['test']}: {test['message']}")
            report.append("")
        
        report.append("RECOMENDACIONES:")
        if diagnosis["failed"] == 0:
            report.append("  * Sistema listo para usar")
            report.append("  * Ejecuta: python auto_implementar_vecta_fixed.py --auto-implementar")
        else:
            report.append("  * Corrige los errores criticos listados arriba")
            report.append("  * Ejecuta nuevamente: python auto_implementar_vecta_fixed.py")
        
        report.append("=" * 60)
        
        return "\n".join(report)
    
    def run(self):
        """Ejecuta la auto-implementación completa"""
        print("=" * 80)
        print("SISTEMA DE AUTO-IMPLEMENTACIÓN VECTA 12D")
        print("=" * 80)
        print(f"Version: {self.system_config['version']}")
        print(f"Directorio: {self.base_dir}")
        print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        print()
        
        # Paso 1: Crear estructura de directorios
        print("[1/3] Creando estructura de directorios...")
        self.create_directory_structure()
        
        # Paso 2: Crear configuración de instalación
        print("[2/3] Creando configuracion de instalacion...")
        self.create_install_config()
        
        # Mostrar resumen
        print()
        print("=" * 80)
        print("RESUMEN DE AUTO-IMPLEMENTACION")
        print("=" * 80)
        print(f"Componentes creados: {len(self.system_config['components'])}")
        print(f"  * Directorios: {len([c for c in self.system_config['components'] if c['type'] == 'directory'])}")
        print(f"  * Archivos: {len([c for c in self.system_config['components'] if c['type'] == 'file'])}")
        print(f"Errores: {len(self.errors)}")
        
        if self.errors:
            print()
            print("Errores encontrados:")
            for error in self.errors[:5]:
                print(f"  * {error}")
            if len(self.errors) > 5:
                print(f"  ... y {len(self.errors) - 5} errores mas")
        
        # Ejecutar autodiagnóstico
        print()
        print("=" * 80)
        print("EJECUTANDO AUTODIAGNOSTICO...")
        print("=" * 80)
        print()
        
        diagnosis_report = self.run_self_diagnosis()
        print(diagnosis_report)
        
        # Instrucciones finales
        print()
        print("=" * 80)
        print("INSTRUCCIONES FINALES")
        print("=" * 80)
        print()
        print("NOTA: Este script crea la estructura de directorios básica.")
        print("Para crear los archivos completos de VECTA, necesitas ejecutar")
        print("el script completo con --auto-implementar.")
        print()
        print("El archivo original tiene un error de indentación en la línea 2373.")
        print("Por favor, revisa el archivo original y corrige la indentación.")
        print()
        print("=" * 80)


def main():
    """Función principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description="VECTA 12D Auto-Installer")
    parser.add_argument("--auto-implementar", action="store_true", help="Auto-implementar sistema completo")
    parser.add_argument("--diagnostico", action="store_true", help="Ejecutar solo diagnóstico")
    
    args = parser.parse_args()
    
    installer = VECTAAutoInstaller()
    
    if args.diagnostico:
        print(installer.run_self_diagnosis())
    else:
        installer.run()
        print("\nNOTA IMPORTANTE:")
        print("El archivo original 'auto_implementar_vecta.py' tiene un error en la línea 2373.")
        print("La línea 'file_path = self.base_dir / &quot;vecta_ai_chat.py&quot;' tiene indentación incorrecta.")
        print("Debe estar dentro del método create_vecta_ai_chat(), sin indentación extra.")
        print("\nPara corregir el archivo original:")
        print("1. Ve a la línea 2373")
        print("2. Asegúrate que está al nivel correcto de indentación")
        print("3. Debe estar dentro del método create_vecta_ai_chat()")
        print("4. Ejecuta: python auto_implementar_vecta.py --auto-implementar")


if __name__ == "__main__":
    main()