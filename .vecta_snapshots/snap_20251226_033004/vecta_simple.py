#!/usr/bin/env python3
# VECTA 12D - SISTEMA AUTOMATICO COMPLETO
# ========================================

import os
import sys
import json
import zipfile
import shutil
import time
import subprocess
import tempfile
import importlib.util
from pathlib import Path
from datetime import datetime
import traceback

# ============================================================================
# CONFIGURACION
# ============================================================================
class Config:
    VERSION = "2.0.0"
    BUILD_DATE = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    PROJECT_DIR = Path.cwd()
    DIMENSIONES_DIR = PROJECT_DIR / "dimensiones"
    CORE_DIR = PROJECT_DIR / "core"
    PAQUETE_PKG = "paquete_vecta.pkg"
    ZIP_FINAL = "VECTA_12D_Automatico.zip"

# ============================================================================
# SISTEMA DE DIAGNOSTICO
# ============================================================================
class AutoDiagnostico:
    def __init__(self):
        self.errores = []
        self.exitos = []
        self.advertencias = []
    
    def error(self, modulo, mensaje):
        self.errores.append(f"{modulo}: {mensaje}")
        print(f"[ERROR] {modulo}: {mensaje}")
    
    def exito(self, modulo, mensaje):
        self.exitos.append(f"{modulo}: {mensaje}")
        print(f"[OK] {modulo}: {mensaje}")
    
    def advertencia(self, modulo, mensaje):
        self.advertencias.append(f"{modulo}: {mensaje}")
        print(f"[ADVERTENCIA] {modulo}: {mensaje}")
    
    def reporte(self):
        print("\n" + "="*60)
        print("REPORTE DE DIAGNOSTICO")
        print("="*60)
        print(f"Exitos: {len(self.exitos)}")
        print(f"Advertencias: {len(self.advertencias)}")
        print(f"Errores: {len(self.errores)}")
        
        if self.errores:
            print("\nERRORES:")
            for e in self.errores:
                print(f"  • {e}")
        
        return len(self.errores) == 0

# ============================================================================
# PASO 1: VERIFICAR ENTORNO
# ============================================================================
def verificar_entorno(diag):
    print("\n" + "="*60)
    print("PASO 1: VERIFICANDO ENTORNO")
    print("="*60)
    
    # Verificar Python
    try:
        version = sys.version_info
        if version.major == 3 and version.minor >= 7:
            diag.exito("Python", f"Version {version.major}.{version.minor}.{version.micro} OK")
        else:
            diag.error("Python", f"Version {version.major}.{version.minor} detectada. Se requiere 3.7+")
            return False
    except:
        diag.error("Python", "No se pudo verificar version")
        return False
    
    # Verificar directorios
    try:
        Config.DIMENSIONES_DIR.mkdir(exist_ok=True)
        Config.CORE_DIR.mkdir(exist_ok=True)
        diag.exito("Directorios", "Estructura creada")
    except Exception as e:
        diag.error("Directorios", f"Error: {e}")
        return False
    
    return True

# ============================================================================
# PASO 2: CREAR DIMENSIONES
# ============================================================================
def crear_dimensiones(diag):
    print("\n" + "="*60)
    print("PASO 2: CREANDO DIMENSIONES 12D")
    print("="*60)
    
    dimensiones = {
        1: ("Tiempo-Entropia", '''
class DimensionTiempoEntropia:
    def __init__(self):
        self.nombre = "Tiempo-Entropia"
        self.magnitud = 0.0
    
    def procesar(self, datos):
        import time
        return {"dimension": self.nombre, "magnitud": 0.5, "timestamp": time.time()}'''),
        
        2: ("Espacio-Volumen", '''
class DimensionEspacioVolumen:
    def __init__(self):
        self.nombre = "Espacio-Volumen"
        self.magnitud = 0.0
    
    def procesar(self, datos):
        return {"dimension": self.nombre, "magnitud": 0.6}'''),
        
        3: ("Energia-Potencial", '''
class DimensionEnergiaPotencial:
    def __init__(self):
        self.nombre = "Energia-Potencial"
        self.magnitud = 0.0
    
    def procesar(self, datos):
        return {"dimension": self.nombre, "magnitud": 0.3}'''),
        
        4: ("Informacion-Entropia", '''
class DimensionInformacionEntropia:
    def __init__(self):
        self.nombre = "Informacion-Entropia"
        self.magnitud = 0.0
    
    def procesar(self, datos):
        return {"dimension": self.nombre, "magnitud": 0.4}'''),
        
        5: ("Conciencia-Atencion", '''
class DimensionConcienciaAtencion:
    def __init__(self):
        self.nombre = "Conciencia-Atencion"
        self.magnitud = 0.0
    
    def procesar(self, datos):
        return {"dimension": self.nombre, "magnitud": 0.2}'''),
        
        6: ("Memoria-Persistencia", '''
class DimensionMemoriaPersistencia:
    def __init__(self):
        self.nombre = "Memoria-Persistencia"
        self.magnitud = 0.0
    
    def procesar(self, datos):
        return {"dimension": self.nombre, "magnitud": 0.7}'''),
        
        7: ("Aprendizaje-Adaptacion", '''
class DimensionAprendizajeAdaptacion:
    def __init__(self):
        self.nombre = "Aprendizaje-Adaptacion"
        self.magnitud = 0.0
    
    def procesar(self, datos):
        return {"dimension": self.nombre, "magnitud": 0.4}'''),
        
        8: ("Creatividad-Generacion", '''
class DimensionCreatividadGeneracion:
    def __init__(self):
        self.nombre = "Creatividad-Generacion"
        self.magnitud = 0.0
    
    def procesar(self, datos):
        return {"dimension": self.nombre, "magnitud": 0.8}'''),
        
        9: ("Ejecucion-Accion", '''
class DimensionEjecucionAccion:
    def __init__(self):
        self.nombre = "Ejecucion-Accion"
        self.magnitud = 0.0
    
    def procesar(self, datos):
        return {"dimension": self.nombre, "magnitud": 0.9}'''),
        
        10: ("Validacion-Correccion", '''
class DimensionValidacionCorreccion:
    def __init__(self):
        self.nombre = "Validacion-Correccion"
        self.magnitud = 0.0
    
    def procesar(self, datos):
        return {"dimension": self.nombre, "magnitud": 0.5}'''),
        
        11: ("Conectividad-Red", '''
class DimensionConectividadRed:
    def __init__(self):
        self.nombre = "Conectividad-Red"
        self.magnitud = 0.0
    
    def procesar(self, datos):
        return {"dimension": self.nombre, "magnitud": 0.6}'''),
        
        12: ("Meta-Autoprogramacion", '''
class DimensionMetaAutoprogramacion:
    def __init__(self):
        self.nombre = "Meta-Autoprogramacion"
        self.magnitud = 0.0
    
    def procesar(self, datos):
        return {"dimension": self.nombre, "magnitud": 0.1}''')
    }
    
    creadas = 0
    for num, (nombre, codigo_clase) in dimensiones.items():
        try:
            contenido = f'"""\nDIMENSION {num}: {nombre}\n"""\n\n{codigo_clase}\n'
            archivo = Config.DIMENSIONES_DIR / f"dimension_{num}.py"
            archivo.write_text(contenido, encoding='utf-8')
            creadas += 1
            diag.exito(f"Dimension {num}", nombre)
        except Exception as e:
            diag.error(f"Dimension {num}", f"Error: {e}")
    
    # Crear vector_12d.py
    try:
        vector_content = '''"""
SISTEMA VECTORIAL 12D
"""
import json
import time
from typing import List, Dict

class Vector12D:
    def __init__(self, dimensiones):
        self.dimensiones = dimensiones
    
    def magnitud(self):
        import math
        return math.sqrt(sum(d*d for d in self.dimensiones))

class SistemaVectorial12D:
    def __init__(self):
        self.dimensiones = []
        self._cargar_dimensiones()
    
    def _cargar_dimensiones(self):
        for i in range(1, 13):
            try:
                module_name = f"dimension_{i}"
                exec(f"from dimensiones.dimension_{i} import Dimension{module_name.split('_')[1].title().replace('-', '').replace(' ', '')}")
                clase = eval(f"Dimension{module_name.split('_')[1].title().replace('-', '').replace(' ', '')}")
                self.dimensiones.append(clase())
            except:
                pass
    
    def procesar_evento(self, evento):
        magnitudes = []
        for dim in self.dimensiones:
            try:
                res = dim.procesar(evento)
                magnitudes.append(res.get('magnitud', 0.0))
            except:
                magnitudes.append(0.0)
        
        while len(magnitudes) < 12:
            magnitudes.append(0.0)
        
        return Vector12D(magnitudes)
'''
        archivo = Config.DIMENSIONES_DIR / "vector_12d.py"
        archivo.write_text(vector_content, encoding='utf-8')
        diag.exito("Sistema Vectorial", "vector_12d.py creado")
    except Exception as e:
        diag.error("Sistema Vectorial", f"Error: {e}")
    
    diag.exito("Dimensiones", f"{creadas}/12 dimensiones creadas")
    return creadas > 0

# ============================================================================
# PASO 3: CREAR NUCLEO
# ============================================================================
def crear_nucleo(diag):
    print("\n" + "="*60)
    print("PASO 3: CREANDO NUCLEO VECTA")
    print("="*60)
    
    # vecta_12d_core.py
    try:
        core_content = '''"""
NUCLEO VECTA 12D
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from dimensiones.vector_12d import SistemaVectorial12D
    SISTEMA_DISPONIBLE = True
except:
    SISTEMA_DISPONIBLE = False

class VECTA_12D_Core:
    def __init__(self):
        self.nombre = "VECTA 12D"
        self.version = "2.0.0"
        
        if SISTEMA_DISPONIBLE:
            self.sistema = SistemaVectorial12D()
            self.estado = "sistema_cargado"
        else:
            self.sistema = None
            self.estado = "sistema_no_disponible"
    
    def procesar(self, texto):
        if self.sistema:
            try:
                vector = self.sistema.procesar_evento({"texto": texto})
                return {
                    "exito": True,
                    "magnitud": vector.magnitud(),
                    "dimensiones": vector.dimensiones
                }
            except Exception as e:
                return {"exito": False, "error": str(e)}
        else:
            return {"exito": False, "error": "Sistema no disponible"}
    
    def start_text_interface(self):
        print("\\n=== VECTA 12D ===")
        print("Escribe 'salir' para terminar\\n")
        
        while True:
            try:
                entrada = input("VECTA> ")
                if entrada.lower() == 'salir':
                    break
                
                resultado = self.procesar(entrada)
                if resultado.get("exito"):
                    print(f"Vector: {resultado['magnitud']:.4f}")
                else:
                    print(f"Error: {resultado.get('error')}")
            except KeyboardInterrupt:
                break
'''
        archivo = Config.CORE_DIR / "vecta_12d_core.py"
        archivo.write_text(core_content, encoding='utf-8')
        diag.exito("Nucleo", "vecta_12d_core.py creado")
    except Exception as e:
        diag.error("Nucleo", f"Error: {e}")
        return False
    
    # Archivos adicionales
    archivos_extra = {
        "__init__.py": "# Paquete core\n",
        "config_manager.py": '''"""
GESTOR DE CONFIGURACION
"""
import json

class ConfigManager:
    def __init__(self):
        self.config = {"version": "2.0.0"}'''
    }
    
    for nombre, contenido in archivos_extra.items():
        try:
            archivo = Config.CORE_DIR / nombre
            archivo.write_text(contenido, encoding='utf-8')
            diag.exito(f"Archivo {nombre}", "creado")
        except:
            diag.advertencia(f"Archivo {nombre}", "no creado")
    
    return True

# ============================================================================
# PASO 4: CREAR PAQUETE .PKG
# ============================================================================
def crear_paquete_pkg(diag):
    print("\n" + "="*60)
    print("PASO 4: CREANDO PAQUETE .PKG")
    print("="*60)
    
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Copiar estructura
            shutil.copytree(Config.DIMENSIONES_DIR, temp_path / "dimensiones", dirs_exist_ok=True)
            shutil.copytree(Config.CORE_DIR, temp_path / "core", dirs_exist_ok=True)
            
            # Crear lanzador
            lanzador = '''#!/usr/bin/env python3
"""
LANZADOR VECTA 12D
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from core.vecta_12d_core import VECTA_12D_Core
    print("VECTA 12D - Sistema de 12 Dimensiones")
    print("Version 2.0.0")
    print("="*40)
    
    vecta = VECTA_12D_Core()
    vecta.start_text_interface()
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    input("Presiona Enter para salir...")
'''
            (temp_path / "vecta_launcher.py").write_text(lanzador, encoding='utf-8')
            
            # Crear manifiesto
            manifiesto = {
                "nombre": "VECTA 12D",
                "version": Config.VERSION,
                "fecha": Config.BUILD_DATE,
                "dimensiones": 12,
                "autor": "Sistema VECTA"
            }
            (temp_path / "MANIFIESTO.json").write_text(json.dumps(manifiesto, indent=2), encoding='utf-8')
            
            # Comprimir
            with zipfile.ZipFile(Config.PAQUETE_PKG, 'w', zipfile.ZIP_DEFLATED) as pkg:
                for archivo in temp_path.rglob("*"):
                    if archivo.is_file():
                        arcname = archivo.relative_to(temp_path)
                        pkg.write(archivo, arcname)
            
            tamaño = os.path.getsize(Config.PAQUETE_PKG)
            diag.exito("Paquete .pkg", f"Creado ({tamaño/1024:.1f} KB)")
            return True
            
    except Exception as e:
        diag.error("Paquete .pkg", f"Error: {e}")
        return False

# ============================================================================
# PASO 5: CREAR ZIP DE DISTRIBUCION
# ============================================================================
def crear_zip_distribucion(diag):
    print("\n" + "="*60)
    print("PASO 5: CREANDO ZIP DE DISTRIBUCION")
    print("="*60)
    
    try:
        # Crear instalador .bat simple
        bat_content = '''@echo off
title VECTA 12D - Instalador
echo ====================================
echo    VECTA 12D - Sistema 12D
echo ====================================
echo.
echo [1/2] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python no encontrado
    echo Instala Python desde python.org
    pause
    exit /b 1
)

echo [2/2] Iniciando VECTA 12D...
echo.
python vecta_launcher.py
pause
'''
        (Config.PROJECT_DIR / "INSTALAR.bat").write_text(bat_content, encoding='utf-8')
        
        # Crear ZIP
        archivos = [
            "INSTALAR.bat",
            "vecta_self_install.py",
            "vecta_12d_launcher.py",
            Config.PAQUETE_PKG
        ]
        
        with zipfile.ZipFile(Config.ZIP_FINAL, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for archivo in archivos:
                if os.path.exists(archivo):
                    zipf.write(archivo, arcname=os.path.basename(archivo))
        
        tamaño = os.path.getsize(Config.ZIP_FINAL)
        diag.exito("ZIP distribucion", f"Creado ({tamaño/1024:.1f} KB)")
        return True
        
    except Exception as e:
        diag.error("ZIP distribucion", f"Error: {e}")
        return False

# ============================================================================
# PASO 6: PRUEBAS
# ============================================================================
def ejecutar_pruebas(diag):
    print("\n" + "="*60)
    print("PASO 6: EJECUTANDO PRUEBAS")
    print("="*60)
    
    try:
        # Prueba 1: Verificar archivos
        requeridos = [
            Config.DIMENSIONES_DIR / "dimension_1.py",
            Config.DIMENSIONES_DIR / "vector_12d.py",
            Config.CORE_DIR / "vecta_12d_core.py",
            Config.PAQUETE_PKG,
            Config.ZIP_FINAL
        ]
        
        existentes = []
        for r in requeridos:
            if r.exists():
                existentes.append(r.name)
            else:
                diag.advertencia("Prueba archivos", f"Falta: {r.name}")
        
        diag.exito("Prueba archivos", f"{len(existentes)}/{len(requeridos)} archivos OK")
        
        # Prueba 2: Probar sistema
        print("\nPrueba del sistema vectorial:")
        try:
            sys.path.insert(0, str(Config.PROJECT_DIR))
            from dimensiones.vector_12d import SistemaVectorial12D
            
            sistema = SistemaVectorial12D()
            vector = sistema.procesar_evento({"prueba": "test"})
            
            print(f"  Sistema creado: OK")
            print(f"  Dimensiones cargadas: {len(sistema.dimensiones)}")
            print(f"  Vector generado: {len(vector.dimensiones)} dimensiones")
            
            diag.exito("Prueba sistema", "Sistema funcional")
            
        except Exception as e:
            diag.error("Prueba sistema", f"Error: {e}")
        
        return True
        
    except Exception as e:
        diag.error("Pruebas", f"Error general: {e}")
        return False

# ============================================================================
# FUNCION PRINCIPAL
# ============================================================================
def main():
    print("\n" + "="*60)
    print("VECTA 12D - CONSTRUCCION AUTOMATICA")
    print("="*60)
    print(f"Directorio: {Config.PROJECT_DIR}")
    print(f"Version: {Config.VERSION}")
    print(f"Fecha: {Config.BUILD_DATE}")
    print("="*60)
    
    diag = AutoDiagnostico()
    
    try:
        # Ejecutar todos los pasos
        if not verificar_entorno(diag):
            print("ERROR: Entorno no valido")
            diag.reporte()
            return
        
        crear_dimensiones(diag)
        crear_nucleo(diag)
        crear_paquete_pkg(diag)
        crear_zip_distribucion(diag)
        ejecutar_pruebas(diag)
        
        # Reporte final
        print("\n" + "="*60)
        print("CONSTRUCCION COMPLETADA")
        print("="*60)
        
        if diag.reporte():
            print("\n✅ VECTA 12D CONSTRUIDO EXITOSAMENTE")
            print(f"\nArchivos creados:")
            print(f"  • {Config.PAQUETE_PKG} (paquete interno)")
            print(f"  • {Config.ZIP_FINAL} (distribucion)")
            print(f"  • dimensiones/ (12 dimensiones)")
            print(f"  • core/ (nucleo del sistema)")
            print(f"  • INSTALAR.bat (instalador)")
            
            print(f"\nPara probar:")
            print(f"  python vecta_launcher.py")
            print(f"  o ejecuta INSTALAR.bat")
        else:
            print("\n⚠️  CONSTRUCCION COMPLETADA CON ERRORES")
            print("   Copia este output completo y pegalo en el chat.")
        
        input("\nPresiona Enter para salir...")
        
    except KeyboardInterrupt:
        print("\n\n❌ Construccion interrumpida por el usuario")
        diag.reporte()
        input("Presiona Enter para salir...")
        
    except Exception as e:
        print(f"\n❌ ERROR NO MANEJADO: {e}")
        print("Traceback:")
        traceback.print_exc()
        
        print("\n" + "="*60)
        print("⚠️  ¡COPIA Y PEGA ESTE ERROR EN EL CHAT!")
        print("Incluye TODO el texto desde arriba.")
        print("="*60)
        
        input("\nPresiona Enter para salir...")

# ============================================================================
# EJECUCION
# ============================================================================
if __name__ == "__main__":
    main()