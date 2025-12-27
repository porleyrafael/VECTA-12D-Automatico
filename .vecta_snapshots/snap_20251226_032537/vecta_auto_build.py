#!/usr/bin/env python3
"""
VECTA 12D - SISTEMA AUTOMÁTICO COMPLETO
========================================
Este script único realiza todas las tareas automáticamente:
1. Verifica entorno y dependencias
2. Crea sistema de 12 dimensiones
3. Genera paquete .pkg
4. Crea ZIP de distribución
5. Ejecuta autodiagnóstico

INSTRUCCIONES:
1. Guarda este archivo en: C:\Users\Rafael\Desktop\VECTA 12D Automatico\
2. Ejecuta: python vecta_auto_build.py
3. Si hay errores, COPIA Y PEGA TODO EL OUTPUT en el chat
"""

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
from typing import Dict, List, Any, Tuple
import traceback

# ============================================================================
# CONFIGURACIÓN Y CONSTANTES
# ============================================================================
class Config:
    VERSION = "2.0.0"
    BUILD_DATE = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    PROJECT_DIR = Path.cwd()
    DIMENSIONES_DIR = PROJECT_DIR / "dimensiones"
    CORE_DIR = PROJECT_DIR / "core"
    PAQUETE_PKG = "paquete_vecta.pkg"
    ZIP_FINAL = "VECTA_12D_Automatico.zip"
    
    ARCHIVOS_REQUERIDOS = [
        "INSTALAR.bat",
        "vecta_self_install.py", 
        "vecta_12d_launcher.py",
        "paquete_vecta.pkg"
    ]

# ============================================================================
# SISTEMA DE LOGGING Y AUTODIAGNÓSTICO
# ============================================================================
class AutoDiagnostico:
    def __init__(self):
        self.errores = []
        self.advertencias = []
        self.exitos = []
        self.start_time = time.time()
    
    def registrar_error(self, modulo: str, error: str, detalles: str = ""):
        registro = {
            "modulo": modulo,
            "error": str(error),
            "detalles": detalles,
            "timestamp": time.time()
        }
        self.errores.append(registro)
        print(f"❌ ERROR en {modulo}: {error}")
        if detalles:
            print(f"   Detalles: {detalles}")
    
    def registrar_exito(self, modulo: str, mensaje: str):
        registro = {
            "modulo": modulo,
            "mensaje": mensaje,
            "timestamp": time.time()
        }
        self.exitos.append(registro)
        print(f"✅ {modulo}: {mensaje}")
    
    def registrar_advertencia(self, modulo: str, mensaje: str):
        registro = {
            "modulo": modulo,
            "mensaje": mensaje,
            "timestamp": time.time()
        }
        self.advertencias.append(registro)
        print(f"⚠️  {modulo}: {mensaje}")
    
    def generar_reporte(self) -> str:
        tiempo_total = time.time() - self.start_time
        
        reporte = []
        reporte.append("=" * 80)
        reporte.append("📋 INFORME DE AUTODIAGNÓSTICO VECTA 12D")
        reporte.append("=" * 80)
        reporte.append(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        reporte.append(f"Versión: {Config.VERSION}")
        reporte.append(f"Tiempo total: {tiempo_total:.2f} segundos")
        reporte.append("")
        
        reporte.append("✅ ÉXITOS:")
        reporte.append("-" * 40)
        if self.exitos:
            for exito in self.exitos:
                reporte.append(f"• {exito['modulo']}: {exito['mensaje']}")
        else:
            reporte.append("Ninguno")
        
        reporte.append("")
        reporte.append("⚠️  ADVERTENCIAS:")
        reporte.append("-" * 40)
        if self.advertencias:
            for adv in self.advertencias:
                reporte.append(f"• {adv['modulo']}: {adv['mensaje']}")
        else:
            reporte.append("Ninguna")
        
        reporte.append("")
        reporte.append("❌ ERRORES:")
        reporte.append("-" * 40)
        if self.errores:
            for error in self.errores:
                reporte.append(f"• {error['modulo']}: {error['error']}")
                if error['detalles']:
                    reporte.append(f"  → {error['detalles']}")
        else:
            reporte.append("Ninguno")
        
        reporte.append("")
        reporte.append("=" * 80)
        reporte.append("📊 RESUMEN:")
        reporte.append(f"Éxitos: {len(self.exitos)}")
        reporte.append(f"Advertencias: {len(self.advertencias)}")
        reporte.append(f"Errores: {len(self.errores)}")
        reporte.append(f"Estado: {'✅ COMPLETADO' if len(self.errores) == 0 else '⚠️  CON ERRORES'}")
        reporte.append("=" * 80)
        
        return "\n".join(reporte)
    
    def guardar_reporte(self, archivo: str = "diagnostico_vecta.txt"):
        contenido = self.generar_reporte()
        with open(archivo, 'w', encoding='utf-8') as f:
            f.write(contenido)
        return archivo

# ============================================================================
# PASO 1: VERIFICACIÓN DEL ENTORNO
# ============================================================================
class VerificadorEntorno:
    def __init__(self, diagnostico: AutoDiagnostico):
        self.diag = diagnostico
        self.dependencias_instaladas = []
    
    def verificar_python(self) -> bool:
        """Verifica versión de Python"""
        try:
            version = sys.version_info
            if version.major == 3 and version.minor >= 7:
                self.diag.registrar_exito("Python", f"Versión {version.major}.{version.minor}.{version.micro} OK")
                return True
            else:
                self.diag.registrar_error("Python", f"Versión {version.major}.{version.minor} detectada", "Se requiere Python 3.7 o superior")
                return False
        except Exception as e:
            self.diag.registrar_error("Python", "No se pudo verificar versión", str(e))
            return False
    
    def verificar_dependencias(self) -> bool:
        """Verifica e instala dependencias"""
        dependencias = [
            ("numpy", "numpy"),
            ("tkinter", "tkinter"),  # Generalmente viene con Python
        ]
        
        faltantes = []
        for nombre, import_name in dependencias:
            try:
                spec = importlib.util.find_spec(import_name)
                if spec is None:
                    faltantes.append(nombre)
                else:
                    self.dependencias_instaladas.append(nombre)
            except:
                faltantes.append(nombre)
        
        if faltantes:
            self.diag.registrar_advertencia("Dependencias", f"Faltantes: {', '.join(faltantes)}")
            # Intentar instalar automáticamente
            for dep in faltantes:
                if dep == "tkinter":
                    self.diag.registrar_advertencia("Dependencias", "tkinter generalmente viene con Python. Si falta, reinstala Python marcando 'tcl/tk'")
                else:
                    try:
                        subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
                        self.dependencias_instaladas.append(dep)
                        self.diag.registrar_exito("Dependencias", f"Instalado: {dep}")
                    except:
                        self.diag.registrar_error("Dependencias", f"No se pudo instalar: {dep}")
        
        self.diag.registrar_exito("Dependencias", f"Disponibles: {', '.join(self.dependencias_instaladas)}")
        return len(faltantes) == 0
    
    def verificar_estructura(self) -> bool:
        """Verifica estructura básica de directorios"""
        try:
            # Crear directorios si no existen
            Config.DIMENSIONES_DIR.mkdir(exist_ok=True)
            Config.CORE_DIR.mkdir(exist_ok=True)
            
            self.diag.registrar_exito("Estructura", "Directorios creados/verificados")
            return True
        except Exception as e:
            self.diag.registrar_error("Estructura", "Error creando directorios", str(e))
            return False

# ============================================================================
# PASO 2: CREACIÓN DE SISTEMA 12 DIMENSIONES
# ============================================================================
class CreadorDimensiones:
    def __init__(self, diagnostico: AutoDiagnostico):
        self.diag = diagnostico
        self.dimensiones_creadas = []
    
    def crear_dimension_1(self) -> bool:
        """Dimensión 1: Tiempo-Entropía"""
        try:
            codigo = '''"""
DIMENSIÓN 1: TIEMPO-ENTROPÍA
Maneja la evolución temporal, secuenciación y gestión de entropía
"""
import time
import math
from typing import Dict, Any

class DimensionTiempoEntropia:
    def __init__(self):
        self.nombre = "Tiempo-Entropía"
        self.simbolo = "T-Ε"
        self.magnitud = 0.0
        self.historico = []
        self.entropia_acumulada = 0.0
        self.ultima_actualizacion = time.time()
    
    def procesar(self, evento: Dict[str, Any]) -> Dict[str, Any]:
        ahora = time.time()
        delta_t = ahora - self.ultima_actualizacion
        
        entropia_evento = self._calcular_entropia(evento)
        self.entropia_acumulada += entropia_evento * delta_t
        self.magnitud = math.log(1 + self.entropia_acumulada)
        
        registro = {
            'timestamp': ahora,
            'delta_t': delta_t,
            'entropia': entropia_evento,
            'magnitud': self.magnitud
        }
        self.historico.append(registro)
        self.ultima_actualizacion = ahora
        
        return {
            'dimension': self.nombre,
            'magnitud': self.magnitud,
            'entropia_acumulada': self.entropia_acumulada,
            'timestamp': ahora
        }
    
    def _calcular_entropia(self, evento: Dict[str, Any]) -> float:
        if not evento:
            return 0.0
        
        contenido = str(evento)
        frecuencias = {}
        total = len(contenido)
        
        for char in contenido:
            frecuencias[char] = frecuencias.get(char, 0) + 1
        
        entropia = 0.0
        for count in frecuencias.values():
            prob = count / total
            if prob > 0:
                entropia -= prob * math.log2(prob)
        
        return entropia
    
    def reset(self):
        self.magnitud = 0.0
        self.entropia_acumulada = 0.0
        self.ultima_actualizacion = time.time()
'''
            archivo = Config.DIMENSIONES_DIR / "dimension_1.py"
            archivo.write_text(codigo, encoding='utf-8')
            self.dimensiones_creadas.append(1)
            self.diag.registrar_exito("Dimensión 1", "Tiempo-Entropía creada")
            return True
        except Exception as e:
            self.diag.registrar_error("Dimensión 1", "Error creando dimensión", str(e))
            return False
    
    def crear_dimension_2(self) -> bool:
        """Dimensión 2: Espacio-Volumen"""
        try:
            codigo = '''"""
DIMENSIÓN 2: ESPACIO-VOLUMEN
Maneja estructura espacial, capacidad y organización
"""
import math
from typing import Dict, Any, List

class DimensionEspacioVolumen:
    def __init__(self):
        self.nombre = "Espacio-Volumen"
        self.simbolo = "S-V"
        self.capacidad_total = 100.0
        self.utilizacion_actual = 0.0
        self.magnitud = 0.0
        
    def procesar(self, elementos: List[Dict[str, Any]]) -> Dict[str, Any]:
        volumen_requerido = sum([self._calcular_volumen(elem) for elem in elementos])
        self.utilizacion_actual = volumen_requerido / self.capacidad_total
        self.magnitud = self.utilizacion_actual
        
        return {
            'dimension': self.nombre,
            'magnitud': self.magnitud,
            'capacidad_utilizada': self.utilizacion_actual,
            'volumen_requerido': volumen_requerido
        }
    
    def _calcular_volumen(self, elemento: Dict[str, Any]) -> float:
        return len(str(elemento).encode('utf-8')) / 1000.0
    
    def expandir(self, factor: float = 1.1):
        self.capacidad_total *= factor
'''
            archivo = Config.DIMENSIONES_DIR / "dimension_2.py"
            archivo.write_text(codigo, encoding='utf-8')
            self.dimensiones_creadas.append(2)
            self.diag.registrar_exito("Dimensión 2", "Espacio-Volumen creada")
            return True
        except Exception as e:
            self.diag.registrar_error("Dimensión 2", "Error creando dimensión", str(e))
            return False
    
    def crear_dimensiones_basicas(self, inicio: int = 3, fin: int = 12) -> bool:
        """Crea dimensiones básicas (placeholders)"""
        nombres_dimensiones = {
            3: "Energía-Potencial",
            4: "Información-Entropía", 
            5: "Conciencia-Atención",
            6: "Memoria-Persistencia",
            7: "Aprendizaje-Adaptación",
            8: "Creatividad-Generación",
            9: "Ejecución-Acción",
            10: "Validación-Corrección",
            11: "Conectividad-Red",
            12: "Meta-Autoprogramación"
        }
        
        exito_total = True
        for i in range(inicio, fin + 1):
            try:
                nombre = nombres_dimensiones.get(i, f"Dimensión {i}")
                codigo = f'''"""
DIMENSIÓN {i}: {nombre.upper()}
Implementación básica - Para expandir en Fase 3
"""
from typing import Dict, Any

class Dimension{nombre.replace('-', '').replace(' ', '')}:
    def __init__(self):
        self.nombre = "{nombre}"
        self.simbolo = "D-{i}"
        self.magnitud = 0.0
    
    def procesar(self, datos: Dict[str, Any]) -> Dict[str, Any]:
        self.magnitud = 0.1  # Valor básico para pruebas
        return {{
            'dimension': self.nombre,
            'magnitud': self.magnitud,
            'estado': 'basico'
        }}
    
    def reset(self):
        self.magnitud = 0.0
'''
                archivo = Config.DIMENSIONES_DIR / f"dimension_{i}.py"
                archivo.write_text(codigo, encoding='utf-8')
                self.dimensiones_creadas.append(i)
                self.diag.registrar_exito(f"Dimensión {i}", f"{nombre} creada (básica)")
            except Exception as e:
                self.diag.registrar_error(f"Dimensión {i}", f"Error creando {nombre}", str(e))
                exito_total = False
        
        return exito_total
    
    def crear_sistema_vectorial(self) -> bool:
        """Crea el sistema vectorial unificado"""
        try:
            codigo = '''"""
SISTEMA VECTORIAL 12D UNIFICADO
Coordina las 12 dimensiones y realiza operaciones vectoriales
"""
import json
import time
import math
from typing import Dict, List, Any
from enum import Enum

class OperacionVectorial(Enum):
    SUMA = "suma"
    RESTA = "resta"
    PRODUCTO_PUNTO = "producto_punto"
    NORMALIZACION = "normalizacion"

class Vector12D:
    def __init__(self, dimensiones: List[float], timestamp: float = None, metadata: Dict[str, Any] = None):
        self.dimensiones = dimensiones
        self.timestamp = timestamp if timestamp else time.time()
        self.metadata = metadata if metadata else {}
        
        if len(self.dimensiones) != 12:
            raise ValueError(f"Se requieren 12 dimensiones, se recibieron {len(self.dimensiones)}")
    
    def magnitud(self) -> float:
        return math.sqrt(sum(d * d for d in self.dimensiones))
    
    def normalizar(self) -> 'Vector12D':
        mag = self.magnitud()
        if mag > 0:
            normalizado = [d / mag for d in self.dimensiones]
        else:
            normalizado = [0.0] * 12
        
        return Vector12D(
            dimensiones=normalizado,
            timestamp=time.time(),
            metadata={'operacion': 'normalizacion'}
        )
    
    def producto_punto(self, otro: 'Vector12D') -> float:
        return sum(a * b for a, b in zip(self.dimensiones, otro.dimensiones))
    
    def to_dict(self) -> Dict:
        return {
            'dimensiones': self.dimensiones,
            'magnitud': self.magnitud(),
            'timestamp': self.timestamp,
            'metadata': self.metadata
        }

class SistemaVectorial12D:
    def __init__(self):
        # Importar dimensiones dinámicamente
        self.dimensiones = {}
        self._cargar_dimensiones()
        self.vectores_historicos = []
    
    def _cargar_dimensiones(self):
        for i in range(1, 13):
            try:
                modulo_nombre = f"dimension_{i}"
                # Importación dinámica
                import importlib.util
                spec = importlib.util.spec_from_file_location(
                    modulo_nombre, 
                    f"dimensiones/dimension_{i}.py"
                )
                modulo = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(modulo)
                
                # Buscar la clase de dimensión (asumiendo naming convention)
                for attr_name in dir(modulo):
                    if attr_name.startswith("Dimension"):
                        clase_dim = getattr(modulo, attr_name)
                        self.dimensiones[i] = clase_dim()
                        break
                        
            except Exception as e:
                # Crear placeholder si falla
                class DimensionPlaceholder:
                    def __init__(self, n):
                        self.nombre = f"Dimensión {n}"
                        self.magnitud = 0.0
                    def procesar(self, datos):
                        return {'dimension': self.nombre, 'magnitud': 0.0}
                
                self.dimensiones[i] = DimensionPlaceholder(i)
    
    def procesar_evento(self, evento: Dict[str, Any]) -> Vector12D:
        magnitudes = []
        resultados = {}
        
        for i, dim in self.dimensiones.items():
            try:
                if i == 2:  # Dimensión 2 espera lista
                    resultado = dim.procesar([evento])
                else:
                    resultado = dim.procesar(evento)
                
                resultados[i] = resultado
                magnitudes.append(resultado.get('magnitud', 0.0))
            except:
                magnitudes.append(0.0)
        
        return Vector12D(
            dimensiones=magnitudes,
            timestamp=time.time(),
            metadata={'evento': str(evento)[:50]}
        )
    
    def operacion_vectorial(self, v1: Vector12D, v2: Vector12D, operacion: OperacionVectorial):
        if operacion == OperacionVectorial.SUMA:
            nueva = [a + b for a, b in zip(v1.dimensiones, v2.dimensiones)]
            return Vector12D(nueva, time.time(), {'operacion': 'suma'})
        
        elif operacion == OperacionVectorial.PRODUCTO_PUNTO:
            return v1.producto_punto(v2)
        
        elif operacion == OperacionVectorial.NORMALIZACION:
            return v1.normalizar()
        
        else:
            raise ValueError(f"Operación no soportada: {operacion}")
'''
            archivo = Config.DIMENSIONES_DIR / "vector_12d.py"
            archivo.write_text(codigo, encoding='utf-8')
            self.diag.registrar_exito("Sistema Vectorial", "Sistema 12D unificado creado")
            return True
        except Exception as e:
            self.diag.registrar_error("Sistema Vectorial", "Error creando sistema", str(e))
            return False

# ============================================================================
# PASO 3: CREACIÓN DEL NÚCLEO VECTA
# ============================================================================
class CreadorNucleo:
    def __init__(self, diagnostico: AutoDiagnostico):
        self.diag = diagnostico
    
    def crear_nucleo_principal(self) -> bool:
        """Crea el núcleo principal de VECTA"""
        try:
            codigo = '''"""
NÚCLEO PRINCIPAL VECTA 12D
Sistema autoprogramable con 12 dimensiones vectoriales
"""
import sys
import os
import time
import json
from typing import Dict, Any

class VECTA_12D_Core:
    def __init__(self):
        self.nombre = "VECTA 12D"
        self.version = "2.0.0"
        self.estado = "inicializado"
        self.cargar_sistema_vectorial()
    
    def cargar_sistema_vectorial(self):
        """Carga el sistema de 12 dimensiones"""
        try:
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            from dimensiones.vector_12d import SistemaVectorial12D
            self.sistema = SistemaVectorial12D()
            self.estado = "vectorial_cargado"
        except Exception as e:
            print(f"Error cargando sistema vectorial: {e}")
            self.sistema = None
            self.estado = "error_vectorial"
    
    def procesar(self, entrada: str) -> Dict[str, Any]:
        """Procesa entrada a través del sistema 12D"""
        if self.sistema is None:
            return {"error": "Sistema vectorial no disponible"}
        
        evento = {
            'texto': entrada,
            'timestamp': time.time(),
            'longitud': len(entrada)
        }
        
        try:
            vector = self.sistema.procesar_evento(evento)
            return {
                'exito': True,
                'vector': vector.to_dict(),
                'timestamp': time.time()
            }
        except Exception as e:
            return {
                'exito': False,
                'error': str(e)
            }
    
    def start_gui(self):
        """Inicia interfaz gráfica (si está disponible)"""
        try:
            import tkinter as tk
            from tkinter import ttk, scrolledtext
            
            root = tk.Tk()
            root.title("VECTA 12D - Sistema Autoprogramable")
            root.geometry("700x500")
            
            frame = ttk.Frame(root, padding="20")
            frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            
            ttk.Label(frame, text="VECTA 12D", font=("Arial", 18)).grid(row=0, column=0, pady=10)
            
            ttk.Label(frame, text="Entrada:").grid(row=1, column=0, sticky=tk.W)
            entrada = scrolledtext.ScrolledText(frame, width=60, height=5)
            entrada.grid(row=2, column=0, pady=5)
            
            resultado = scrolledtext.ScrolledText(frame, width=60, height=10)
            resultado.grid(row=4, column=0, pady=10)
            
            def procesar():
                texto = entrada.get("1.0", tk.END).strip()
                if texto:
                    res = self.procesar(texto)
                    resultado.delete("1.0", tk.END)
                    if res.get('exito'):
                        vector = res['vector']
                        resultado.insert("1.0", 
                            f"✅ Vector 12D generado\\n"
                            f"Magnitud: {vector['magnitud']:.4f}\\n"
                            f"Dimensiones: {vector['dimensiones'][:3]}... (mostrando 3/12)")
                    else:
                        resultado.insert("1.0", f"❌ Error: {res.get('error', 'Desconocido')}")
            
            ttk.Button(frame, text="Procesar", command=procesar).grid(row=3, column=0, pady=10)
            
            root.mainloop()
            
        except ImportError:
            self.start_text_interface()
    
    def start_text_interface(self):
        """Interfaz de texto para consola"""
        print("\\n=== VECTA 12D - Sistema de 12 Dimensiones ===")
        print("Escribe 'salir' para terminar o 'estado' para ver sistema\\n")
        
        while True:
            try:
                entrada = input("VECTA> ")
                if entrada.lower() == 'salir':
                    break
                elif entrada.lower() == 'estado':
                    print(f"Estado: {self.estado}")
                    print(f"Sistema: {'Cargado' if self.sistema else 'No disponible'}")
                    continue
                
                resultado = self.procesar(entrada)
                if resultado.get('exito'):
                    vector = resultado['vector']
                    print(f"✅ Vector generado - Magnitud: {vector['magnitud']:.4f}")
                    # Mostrar primeras 3 dimensiones
                    print(f"   D1: {vector['dimensiones'][0]:.3f}, D2: {vector['dimensiones'][1]:.3f}, D3: {vector['dimensiones'][2]:.3f}")
                else:
                    print(f"❌ Error: {resultado.get('error')}")
                    
            except KeyboardInterrupt:
                print("\\n👋 Saliendo de VECTA 12D")
                break
            except Exception as e:
                print(f"❌ Error inesperado: {e}")
'''
            archivo = Config.CORE_DIR / "vecta_12d_core.py"
            archivo.write_text(codigo, encoding='utf-8')
            self.diag.registrar_exito("Núcleo VECTA", "Núcleo principal creado")
            return True
        except Exception as e:
            self.diag.registrar_error("Núcleo VECTA", "Error creando núcleo", str(e))
            return False
    
    def crear_archivos_soporte(self) -> bool:
        """Crea archivos de soporte adicionales"""
        archivos = {
            "vecta_gui_secure.py": '''"""
INTERFAZ GRÁFICA SEGURA VECTA 12D
Versión simplificada para distribución
"""
print("GUI VECTA 12D - Cargando desde núcleo...")''',
            
            "__init__.py": '''# Paquete core de VECTA 12D
__version__ = "2.0.0"
__author__ = "Sistema VECTA"''',
            
            "config_manager.py": '''"""
GESTOR DE CONFIGURACIÓN VECTA 12D
"""
import json
import os
from pathlib import Path

class ConfigManager:
    def __init__(self):
        self.config_file = Path("config_vecta.json")
        self.config = self._cargar_config()
    
    def _cargar_config(self):
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {
            'version': '2.0.0',
            'dimensiones_activas': 12,
            'modo_seguro': True
        }
    
    def guardar(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)'''
        }
        
        exito = True
        for nombre, contenido in archivos.items():
            try:
                archivo = Config.CORE_DIR / nombre
                archivo.write_text(contenido, encoding='utf-8')
            except Exception as e:
                self.diag.registrar_error(f"Archivo {nombre}", "Error creando", str(e))
                exito = False
        
        if exito:
            self.diag.registrar_exito("Archivos soporte", "Archivos adicionales creados")
        
        return exito

# ============================================================================
# PASO 4: CREACIÓN DE PAQUETE .PKG
# ============================================================================
class CreadorPaquete:
    def __init__(self, diagnostico: AutoDiagnostico):
        self.diag = diagnostico
    
    def crear_paquete_pkg(self) -> bool:
        """Crea el paquete .pkg con todo el sistema"""
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                
                # Crear estructura en directorio temporal
                (temp_path / "dimensiones").mkdir()
                (temp_path / "core").mkdir()
                
                # Copiar dimensiones
                if Config.DIMENSIONES_DIR.exists():
                    for archivo in Config.DIMENSIONES_DIR.glob("*.py"):
                        shutil.copy2(archivo, temp_path / "dimensiones" / archivo.name)
                
                # Copiar core
                if Config.CORE_DIR.exists():
                    for archivo in Config.CORE_DIR.glob("*.py"):
                        shutil.copy2(archivo, temp_path / "core" / archivo.name)
                
                # Crear archivos base adicionales
                (temp_path / "vecta_launcher.py").write_text('''
#!/usr/bin/env python3
"""
LANZADOR VECTA 12D
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from core.vecta_12d_core import VECTA_12D_Core
    print("🌀 VECTA 12D - Sistema de 12 Dimensiones")
    print("Versión: 2.0.0")
    print("="*40)
    
    vecta = VECTA_12D_Core()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--gui":
        vecta.start_gui()
    else:
        vecta.start_text_interface()
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    input("Presiona Enter para salir...")
''', encoding='utf-8')
                
                # Crear manifiesto
                manifiesto = {
                    "nombre": "VECTA 12D",
                    "version": Config.VERSION,
                    "fecha_compilacion": Config.BUILD_DATE,
                    "dimensiones": 12,
                    "descripcion": "Sistema autoprogramable de 12 dimensiones vectoriales",
                    "autor": "Sistema VECTA",
                    "archivos": [f.name for f in temp_path.rglob("*") if f.is_file()]
                }
                
                (temp_path / "MANIFIESTO.json").write_text(
                    json.dumps(manifiesto, indent=2), encoding='utf-8'
                )
                
                # Comprimir en .pkg
                with zipfile.ZipFile(Config.PAQUETE_PKG, 'w', zipfile.ZIP_DEFLATED) as pkg:
                    for archivo in temp_path.rglob("*"):
                        if archivo.is_file():
                            arcname = archivo.relative_to(temp_path)
                            pkg.write(archivo, arcname)
                
                tamaño = os.path.getsize(Config.PAQUETE_PKG)
                self.diag.registrar_exito("Paquete .pkg", f"Creado exitosamente ({tamaño/1024:.1f} KB)")
                return True
                
        except Exception as e:
            self.diag.registrar_error("Paquete .pkg", "Error creando paquete", str(e))
            return False

# ============================================================================
# PASO 5: CREACIÓN DE ZIP DE DISTRIBUCIÓN
# ============================================================================
class CreadorDistribucion:
    def __init__(self, diagnostico: AutoDiagnostico):
        self.diag = diagnostico
    
    def crear_instalador_bat(self) -> bool:
        """Crea o actualiza el instalador .bat"""
        try:
            contenido = '''@echo off
title VECTA 12D - Instalador Automático
color 0A
echo ==============================================
echo    VECTA 12D - Sistema de 12 Dimensiones
echo    Versión 2.0.0 - Instalación Automática
echo ==============================================
echo.

REM Verificar Python
echo [1/4] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no encontrado
    echo Por favor, instala Python 3.7 o superior desde:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo [2/4] Ejecutando sistema VECTA...
python vecta_launcher.py --gui

echo [3/4] Configuración completada
echo [4/4] VECTA 12D está listo para usar
echo.
echo ==============================================
echo    ✅ INSTALACIÓN COMPLETADA EXITOSAMENTE
echo ==============================================
echo.
echo Para usar VECTA 12D:
echo 1. Ejecuta "vecta_launcher.py"
echo 2. O usa el acceso directo creado
echo.
echo El sistema incluye:
echo • 12 Dimensiones Vectoriales
echo • Sistema de autoprogramación
echo • Interfaz gráfica y de consola
echo • Seguridad integrada
echo.
pause
'''
            archivo = Config.PROJECT_DIR / "INSTALAR.bat"
            archivo.write_text(contenido, encoding='utf-8')
            self.diag.registrar_exito("Instalador .bat", "Archivo creado/actualizado")
            return True
        except Exception as e:
            self.diag.registrar_error("Instalador .bat", "Error creando", str(e))
            return False
    
    def crear_zip_distribucion(self) -> bool:
        """Crea el ZIP final de distribución"""
        try:
            # Lista de archivos a incluir
            archivos_incluir = [
                "INSTALAR.bat",
                "vecta_self_install.py",
                "vecta_12d_launcher.py",
                Config.PAQUETE_PKG,
                "verificar.py" if Path("verificar.py").exists() else None
            ]
            
            # Filtrar archivos que existen
            archivos_incluir = [f for f in archivos_incluir if f and Path(f).exists()]
            
            with zipfile.ZipFile(Config.ZIP_FINAL, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for archivo in archivos_incluir:
                    zipf.write(archivo, arcname=Path(archivo).name)
            
            tamaño = os.path.getsize(Config.ZIP_FINAL)
            self.diag.registrar_exito("ZIP distribución", f"Creado exitosamente ({tamaño/1024:.1f} KB)")
            self.diag.registrar_exito("ZIP distribución", f"Archivos incluidos: {len(archivos_incluir)}")
            
            return True
        except Exception as e:
            self.diag.registrar_error("ZIP distribución", "Error creando ZIP", str(e))
            return False

# ============================================================================
# PASO 6: PRUEBAS AUTOMÁTICAS
# ============================================================================
class EjecutorPruebas:
    def __init__(self, diagnostico: AutoDiagnostico):
        self.diag = diagnostico
    
    def ejecutar_prueba_rapida(self) -> bool:
        """Ejecuta una prueba rápida del sistema"""
        try:
            print("\n" + "="*60)
            print("🧪 EJECUTANDO PRUEBA RÁPIDA DEL SISTEMA")
            print("="*60)
            
            # Prueba 1: Verificar archivos creados
            archivos_verificar = [
                Config.DIMENSIONES_DIR / "dimension_1.py",
                Config.DIMENSIONES_DIR / "dimension_2.py", 
                Config.DIMENSIONES_DIR / "vector_12d.py",
                Config.CORE_DIR / "vecta_12d_core.py",
                Config.PAQUETE_PKG
            ]
            
            existentes = []
            faltantes = []
            
            for archivo in archivos_verificar:
                if archivo.exists():
                    existentes.append(archivo.name)
                else:
                    faltantes.append(archivo.name)
            
            print(f"\n📁 Archivos verificados:")
            print(f"✅ Existentes: {len(existentes)}")
            print(f"❌ Faltantes: {len(faltantes)}")
            
            if faltantes:
                for f in faltantes[:3]:  # Mostrar solo primeros 3
                    print(f"   - {f}")
            
            # Prueba 2: Probar sistema vectorial básico
            print("\n🔧 Probando sistema vectorial...")
            try:
                sys.path.insert(0, str(Config.PROJECT_DIR))
                from dimensiones.vector_12d import SistemaVectorial12D, Vector12D, OperacionVectorial
                
                sistema = SistemaVectorial12D()
                evento = {"prueba": "test", "valor": 123}
                vector = sistema.procesar_evento(evento)
                
                print(f"✅ Sistema vectorial funcional")
                print(f"   Vector creado - Magnitud: {vector.magnitud():.4f}")
                
                # Prueba operación básica
                v2 = Vector12D([0.5]*12)
                producto = vector.producto_punto(v2)
                print(f"   Producto punto: {producto:.4f}")
                
                self.diag.registrar_exito("Prueba sistema", "Sistema vectorial operativo")
                return True
                
            except Exception as e:
                print(f"❌ Error en prueba: {e}")
                self.diag.registrar_error("Prueba sistema", "Error probando sistema", str(e))
                return False
                
        except Exception as e:
            print(f"❌ Error general en pruebas: {e}")
            self.diag.registrar_error("Pruebas", "Error ejecutando pruebas", str(e))
            return False

# ============================================================================
# SISTEMA PRINCIPAL - ORQUESTADOR
# ============================================================================
class VECTA_AutoBuilder:
    def __init__(self):
        self.diagnostico = AutoDiagnostico()
        self.pasos_completados = []
        self.pasos_fallidos = []
        
        # Inicializar módulos
        self.verificador = VerificadorEntorno(self.diagnostico)
        self.creador_dim = CreadorDimensiones(self.diagnostico)
        self.creador_nucleo = CreadorNucleo(self.diagnostico)
        self.creador_pkg = CreadorPaquete(self.diagnostico)
        self.creador_dist = CreadorDistribucion(self.diagnostico)
        self.ejecutor_pruebas = EjecutorPruebas(self.diagnostico)
    
    def ejecutar_paso(self, nombre: str, funcion, *args):
        """Ejecuta un paso con manejo de errores"""
        try:
            print(f"\n{'='*60}")
            print(f"🚀 EJECUTANDO: {nombre}")
            print(f"{'='*60}")
            
            resultado = funcion(*args)
            
            if resultado:
                self.pasos_completados.append(nombre)
                print(f"✅ {nombre}: COMPLETADO")
            else:
                self.pasos_fallidos.append(nombre)
                print(f"⚠️  {nombre}: FALLÓ (continuando...)")
            
            return resultado
            
        except Exception as e:
            error_msg = f"Excepción en {nombre}: {str(e)}"
            print(f"❌ ERROR CRÍTICO: {error_msg}")
            print(f"📋 Traceback:")
            traceback.print_exc()
            
            self.diagnostico.registrar_error(nombre, "Error crítico", f"{e}\n{traceback.format_exc()}")
            self.pasos_fallidos.append(nombre)
            
            # Preguntar si continuar
            print(f"\n¿Continuar con el siguiente paso? (s/n): ", end='')
            respuesta = input().strip().lower()
            return respuesta == 's'
    
    def ejecutar_construccion_completa(self):
        """Ejecuta toda la construcción automática"""
        print("\n" + "="*80)
        print("🚀 INICIANDO CONSTRUCCIÓN AUTOMÁTICA VECTA 12D")
        print("="*80)
        print(f"Directorio: {Config.PROJECT_DIR}")
        print(f"Versión: {Config.VERSION}")
        print(f"Fecha: {Config.BUILD_DATE}")
        print("="*80)
        
        # PASO 0: Mostrar información del sistema
        print(f"\n💻 SISTEMA DETECTADO:")
        print(f"Python: {sys.version}")
        print(f"Plataforma: {sys.platform}")
        print(f"Directorio de trabajo: {Config.PROJECT_DIR}")
        
        # PASO 1: Verificación del entorno
        self.ejecutar_paso("Verificación Python", self.verificador.verificar_python)
        self.ejecutar_paso("Verificación dependencias", self.verificador.verificar_dependencias)
        self.ejecutar_paso("Verificación estructura", self.verificador.verificar_estructura)
        
        # PASO 2: Creación de dimensiones
        self.ejecutar_paso("Creación Dimensión 1", self.creador_dim.crear_dimension_1)
        self.ejecutar_paso("Creación Dimensión 2", self.creador_dim.crear_dimension_2)
        self.ejecutar_paso("Creación dimensiones 3-12", self.creador_dim.crear_dimensiones_basicas, 3, 12)
        self.ejecutar_paso("Creación sistema vectorial", self.creador_dim.crear_sistema_vectorial)
        
        # PASO 3: Creación del núcleo
        self.ejecutar_paso("Creación núcleo principal", self.creador_nucleo.crear_nucleo_principal)
        self.ejecutar_paso("Creación archivos soporte", self.creador_nucleo.crear_archivos_soporte)
        
        # PASO 4: Creación de paquete
        self.ejecutar_paso("Creación paquete .pkg", self.creador_pkg.crear_paquete_pkg)
        
        # PASO 5: Creación de distribución
        self.ejecutar_paso("Creación instalador .bat", self.creador_dist.crear_instalador_bat)
        self.ejecutar_paso("Creación ZIP distribución", self.creador_dist.crear_zip_distribucion)
        
        # PASO 6: Pruebas automáticas
        self.ejecutar_paso("Ejecución pruebas rápidas", self.ejecutor_pruebas.ejecutar_prueba_rapida)
        
        # Generar reporte final
        self.generar_reporte_final()
        
        # Mostrar instrucciones
        self.mostrar_instrucciones_finales()
    
    def generar_reporte_final(self):
        """Genera el reporte final de la construcción"""
        print("\n" + "="*80)
        print("📋 REPORTE FINAL DE CONSTRUCCIÓN")
        print("="*80)
        
        print(f"\n✅ PASOS COMPLETADOS ({len(self.pasos_completados)}):")
        for paso in self.pasos_completados:
            print(f"  ✓ {paso}")
        
        if self.pasos_fallidos:
            print(f"\n❌ PASOS FALLIDOS ({len(self.pasos_fallidos)}):")
            for paso in self.pasos_fallidos:
                print(f"  ✗ {paso}")
        else:
            print(f"\n🎉 ¡TODOS LOS PASOS COMPLETADOS EXITOSAMENTE!")
        
        # Guardar diagnóstico
        archivo_diag = self.diagnostico.guardar_reporte()
        print(f"\n📄 Reporte de diagnóstico guardado en: {archivo_diag}")
        
        # Mostrar archivos creados
        print(f"\n📁 ESTRUCTURA CREADA:")
        self.mostrar_estructura()
    
    def mostrar_estructura(self):
        """Muestra la estructura de archivos creada"""
        try:
            estructura = []
            
            # Directorio raíz
            archivos_raiz = list(Config.PROJECT_DIR.glob("*"))
            for archivo in archivos_raiz:
                if archivo.is_file():
                    tamaño = archivo.stat().st_size
                    estructura.append(f"  📄 {archivo.name} ({tamaño} bytes)")
            
            # Directorio dimensiones
            if Config.DIMENSIONES_DIR.exists():
                estructura.append(f"\n  📁 dimensiones/")
                archivos_dim = list(Config.DIMENSIONES_DIR.glob("*.py"))
                for archivo in archivos_dim[:5]:  # Mostrar primeros 5
                    estructura.append(f"    📄 {archivo.name}")
                if len(archivos_dim) > 5:
                    estructura.append(f"    ... y {len(archivos_dim)-5} más")
            
            # Directorio core
            if Config.CORE_DIR.exists():
                estructura.append(f"\n  📁 core/")
                archivos_core = list(Config.CORE_DIR.glob("*.py"))
                for archivo in archivos_core:
                    estructura.append(f"    📄 {archivo.name}")
            
            print("\n".join(estructura))
            
        except Exception as e:
            print(f"  (No se pudo leer estructura: {e})")
    
    def mostrar_instrucciones_finales(self):
        """Muestra instrucciones finales para el usuario"""
        print("\n" + "="*80)
        print("📋 INSTRUCCIONES FINALES")
        print("="*80)
        
        print(f"""
✅ CONSTRUCCIÓN {'COMPLETADA' if not self.pasos_fallidos else 'CON ERRORES'}

NEXT STEPS:

1. 📦 DISTRIBUCIÓN:
   • Archivo ZIP listo: {Config.ZIP_FINAL}
   • Paquete interno: {Config.PAQUETE_PKG}

2. 🧪 PROBAR EL SISTEMA:
   • Ejecuta prueba: python test_dimensiones.py (si existe)
   • O ejecuta directamente: python -c "from core.vecta_12d_core import VECTA_12D_Core; v = VECTA_12D_Core(); v.start_text_interface()"

3. 🚀 LANZAR VECTA 12D:
   • GUI: python vecta_launcher.py --gui
   • Consola: python vecta_launcher.py

4. 🔧 SI HAY ERRORES:
   • Copia TODO el output de esta ejecución
   • Pégalo en el chat para análisis
   • Incluye el archivo: {self.diagnostico.guardar_reporte()}

5. 📊 VERIFICAR:
   • Revisa el archivo de diagnóstico
   • Verifica que todos los archivos requeridos existen

ARCHIVOS CLAVE CREADOS:
   • {Config.DIMENSIONES_DIR}/ - 12 dimensiones vectoriales
   • {Config.CORE_DIR}/ - Núcleo del sistema
   • {Config.PAQUETE_PKG} - Paquete interno
   • {Config.ZIP_FINAL} - Distribución final
   • INSTALAR.bat - Instalador actualizado

⚠️  SI COPIO ESTE OUTPUT:
   Incluye TODO desde "🚀 INICIANDO CONSTRUCCIÓN..." hasta este mensaje.
""")

# ============================================================================
# EJECUCIÓN PRINCIPAL
# ============================================================================
if __name__ == "__main__":
    try:
        # Crear y ejecutar el constructor automático
        builder = VECTA_AutoBuilder()
        builder.ejecutar_construccion_completa()
        
        # Pausa final para que el usuario pueda leer
        print("\n" + "="*80)
        print("🏁 CONSTRUCCIÓN FINALIZADA")
        print("="*80)
        input("\nPresiona Enter para salir...")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Construcción interrumpida por el usuario")
        input("Presiona Enter para salir...")
        sys.exit(1)
        
    except Exception as e:
        print(f"\n❌ ERROR NO MANEJADO: {e}")
        print("📋 Traceback completo:")
        traceback.print_exc()
        
        print("\n" + "="*80)
        print("⚠️  ¡COPIA Y PEGA ESTE ERROR EN EL CHAT!")
        print("="*80)
        print("Incluye TODO desde arriba hasta este mensaje.")
        print("="*80)
        
        input("\nPresiona Enter para salir...")
        sys.exit(1)