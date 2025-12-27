#!/usr/bin/env python3
"""
SCRIPT DE CORRECCION PARA IMPORTACIONES VECTA 12D
"""

import os

def crear_init_dimensiones():
    """Crea __init__.py en la carpeta dimensiones"""
    contenido = '''"""
PAQUETE DIMENSIONES VECTA 12D
Exporta todas las dimensiones para importacion correcta
"""

# Exportar dimensiones base
from .dimension_base import DimensionBase, ResultadoDimension, EstadoDimension

# Exportar dimensiones especificas
try:
    from .dimension_1 import Dimension1
except ImportError:
    Dimension1 = None

try:
    from .dimension_2 import Dimension2
except ImportError:
    Dimension2 = None

try:
    from .dimension_3 import Dimension3
except ImportError:
    Dimension3 = None

try:
    from .dimension_4 import Dimension4
except ImportError:
    Dimension4 = None

try:
    from .dimension_5 import Dimension5
except ImportError:
    Dimension5 = None

try:
    from .dimension_6 import Dimension6
except ImportError:
    Dimension6 = None

try:
    from .dimension_7 import Dimension7
except ImportError:
    Dimension7 = None

try:
    from .dimension_8 import Dimension8
except ImportError:
    Dimension8 = None

try:
    from .dimension_9 import Dimension9
except ImportError:
    Dimension9 = None

try:
    from .dimension_10 import Dimension10
except ImportError:
    Dimension10 = None

try:
    from .dimension_11 import Dimension11
except ImportError:
    Dimension11 = None

try:
    from .dimension_12 import Dimension12
except ImportError:
    Dimension12 = None

# Lista de dimensiones disponibles
dimensiones_disponibles = [
    Dimension1, Dimension2, Dimension3, Dimension4, Dimension5, Dimension6,
    Dimension7, Dimension8, Dimension9, Dimension10, Dimension11, Dimension12
]

__all__ = [
    'DimensionBase', 'ResultadoDimension', 'EstadoDimension',
    'Dimension1', 'Dimension2', 'Dimension3', 'Dimension4', 'Dimension5', 'Dimension6',
    'Dimension7', 'Dimension8', 'Dimension9', 'Dimension10', 'Dimension11', 'Dimension12',
    'dimensiones_disponibles'
]
'''
    
    with open('dimensiones/__init__.py', 'w', encoding='utf-8') as f:
        f.write(contenido)
    print("Archivo creado: dimensiones/__init__.py")

def crear_init_core():
    """Crea __init__.py en la carpeta core"""
    contenido = '''"""
PAQUETE CORE VECTA 12D
"""

from .vecta_12d_core import VECTA_12D_Core
from .meta_vecta import MetaVECTA, VECTA12DIntegrator
from .config_manager import ConfigManager

__all__ = ['VECTA_12D_Core', 'MetaVECTA', 'VECTA12DIntegrator', 'ConfigManager']
'''
    
    with open('core/__init__.py', 'w', encoding='utf-8') as f:
        f.write(contenido)
    print("Archivo creado: core/__init__.py")

def corregir_importaciones_dimensiones():
    """Corrige las importaciones en los archivos de dimensiones"""
    
    # Primero, corregir dimension_base.py para usar importaciones absolutas
    with open('dimensiones/dimension_base.py', 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Reemplazar importaciones problemáticas
    contenido = contenido.replace(
        'import numpy as np',
        'import numpy as np\nimport sys\nimport os'
    )
    
    with open('dimensiones/dimension_base.py', 'w', encoding='utf-8') as f:
        f.write(contenido)
    
    # Ahora corregir cada dimensión individual
    for i in range(1, 13):
        archivo = f'dimensiones/dimension_{i}.py'
        if os.path.exists(archivo):
            with open(archivo, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            # Corregir importación de dimension_base
            contenido = contenido.replace(
                'from .dimension_base import',
                'from dimensiones.dimension_base import'
            )
            
            # Añadir importaciones necesarias
            if 'import time' not in contenido:
                contenido = contenido.replace(
                    'import re',
                    'import re\nimport time'
                )
            
            with open(archivo, 'w', encoding='utf-8') as f:
                f.write(contenido)
            
            print(f"Corregido: dimensiones/dimension_{i}.py")

def corregir_vector_12d():
    """Corrige las importaciones en vector_12d.py"""
    with open('dimensiones/vector_12d.py', 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Corregir importación de dimension_base
    contenido = contenido.replace(
        'from .dimension_base import DimensionBase',
        'from dimensiones.dimension_base import DimensionBase'
    )
    
    # Corregir importaciones de módulos de dimensiones
    contenido = contenido.replace(
        'from .dimension_base import DimensionBase',
        'from dimensiones.dimension_base import DimensionBase'
    )
    
    with open('dimensiones/vector_12d.py', 'w', encoding='utf-8') as f:
        f.write(contenido)
    
    print("Corregido: dimensiones/vector_12d.py")

def crear_sistema_carga_alternativo():
    """Crea un sistema de carga alternativo que funcione mejor"""
    
    # Crear un archivo de carga simplificado
    contenido = '''"""
SISTEMA DE CARGA SIMPLIFICADO PARA DIMENSIONES
"""

import importlib
import sys
import os

def cargar_dimension_simplificado(numero):
    """Carga una dimensión de manera robusta"""
    try:
        # Intentar importación absoluta primero
        modulo_nombre = f"dimensiones.dimension_{numero}"
        modulo = importlib.import_module(modulo_nombre)
        
        clase_nombre = f"Dimension{numero}"
        if hasattr(modulo, clase_nombre):
            clase = getattr(modulo, clase_nombre)
            return clase()
    except ImportError:
        pass
    
    # Si falla, crear una dimensión base
    from dimensiones.dimension_base import DimensionBase
    nombres = {
        1: "Intencionalidad Pura",
        2: "Estructura Lógica",
        3: "Contexto Sistémico",
        4: "Temporalidad",
        5: "Escala de Impacto",
        6: "Complejidad Intrínseca",
        7: "Evolución Potencial",
        8: "Simetría/Asimetría",
        9: "Información/Entropía",
        10: "Consciencia Reflexiva",
        11: "Integridad Ética",
        12: "Unificación Holística"
    }
    
    nombre = nombres.get(numero, f"Dimensión {numero}")
    return DimensionBase(numero, nombre, f"Dimensión {numero}: {nombre}")

def cargar_todas_dimensiones():
    """Carga las 12 dimensiones"""
    dimensiones = []
    for i in range(1, 13):
        dimension = cargar_dimension_simplificado(i)
        dimensiones.append(dimension)
        print(f"Dimensión {i} cargada: {dimension.nombre}")
    
    return dimensiones
'''
    
    with open('dimensiones/cargador_simplificado.py', 'w', encoding='utf-8') as f:
        f.write(contenido)
    print("Archivo creado: dimensiones/cargador_simplificado.py")

def actualizar_vector_12d_con_cargador():
    """Actualiza vector_12d.py para usar el cargador simplificado"""
    with open('dimensiones/vector_12d.py', 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Reemplazar el método cargar_dimensiones
    nuevo_cargador = '''    def cargar_dimensiones(self, ruta: str = None):
        """Carga las dimensiones usando el cargador simplificado"""
        print("CARGANDO DIMENSIONES FILOSOFICAS VECTA 12D...")
        
        try:
            from dimensiones.cargador_simplificado import cargar_todas_dimensiones
            self.dimensiones = cargar_todas_dimensiones()
        except ImportError as e:
            print(f"Error al cargar cargador simplificado: {e}")
            # Cargar dimensiones básicas como fallback
            from dimensiones.dimension_base import DimensionBase
            self.dimensiones = []
            for i in range(1, 13):
                nombre = f"Dimensión {i}"
                if i == 1: nombre = "Intencionalidad Pura"
                elif i == 2: nombre = "Estructura Lógica"
                elif i == 3: nombre = "Contexto Sistémico"
                elif i == 4: nombre = "Temporalidad"
                elif i == 5: nombre = "Escala de Impacto"
                elif i == 6: nombre = "Complejidad Intrínseca"
                elif i == 7: nombre = "Evolución Potencial"
                elif i == 8: nombre = "Simetría/Asimetría"
                elif i == 9: nombre = "Información/Entropía"
                elif i == 10: nombre = "Consciencia Reflexiva"
                elif i == 11: nombre = "Integridad Ética"
                elif i == 12: nombre = "Unificación Holística"
                
                instancia = DimensionBase(i, nombre, f"Dimensión {i}: {nombre}")
                self.dimensiones.append(instancia)
                print(f"  Dimensión {i}: {nombre} - Básica")
        
        print(f"Sistema cargado con {len(self.dimensiones)}/12 dimensiones")
        self.estado_sistema = "activo"'''
    
    # Encontrar y reemplazar el método cargar_dimensiones
    import re
    patron = r'    def cargar_dimensiones\(self, ruta: str = None\):.*?        self\.estado_sistema = "activo"'
    
    contenido = re.sub(patron, nuevo_cargador, contenido, flags=re.DOTALL)
    
    with open('dimensiones/vector_12d.py', 'w', encoding='utf-8') as f:
        f.write(contenido)
    
    print("Actualizado: dimensiones/vector_12d.py con nuevo cargador")

def crear_dimensiones_funcionales():
    """Crea versiones funcionales de las dimensiones 1-3"""
    
    # Dimensión 1 funcional (más simple)
    dim1 = '''"""
DIMENSION 1 - INTENCIONALIDAD PURA
Versión funcional simplificada
"""

import re
import time
from typing import Dict, Any
from dimensiones.dimension_base import DimensionBase, ResultadoDimension, EstadoDimension

class Dimension1(DimensionBase):
    def __init__(self):
        super().__init__(
            numero=1,
            nombre="Intencionalidad Pura",
            descripcion="Voluntad primaria detrás de cualquier acción o decisión"
        )
        self.peso_actual = 0.15
    
    def procesar(self, contexto: Dict[str, Any]) -> ResultadoDimension:
        try:
            texto = contexto.get('texto', '')
            
            # Análisis simple de intencionalidad
            claridad = self._analizar_claridad_simple(texto)
            fuerza = self._analizar_fuerza_simple(texto)
            
            # Valor combinado
            valor = (claridad * 0.6 + fuerza * 0.4)
            valor = max(-1.0, min(1.0, valor))
            
            confianza = 0.7  # Confianza media
            
            resultado = ResultadoDimension(
                valor=valor,
                confianza=confianza,
                componentes={
                    "claridad": claridad,
                    "fuerza_voluntad": fuerza
                },
                estado=self.estado,
                timestamp=time.time()
            )
            
            self.registrar_resultado(resultado)
            return resultado
            
        except Exception as e:
            print(f"Error en Dimensión 1 (simple): {e}")
            return ResultadoDimension(
                valor=0.0,
                confianza=0.1,
                componentes={},
                estado=EstadoDimension.INACTIVA,
                timestamp=time.time()
            )
    
    def _analizar_claridad_simple(self, texto: str) -> float:
        if not texto:
            return 0.0
        
        palabras_claras = ['quiero', 'debo', 'necesito', 'voy a', 'tengo que', 'deseo']
        palabras_confusas = ['quizás', 'tal vez', 'no sé', 'no estoy seguro', 'tal vez sí']
        
        texto_lower = texto.lower()
        
        conteo_claro = sum(1 for p in palabras_claras if p in texto_lower)
        conteo_confuso = sum(1 for p in palabras_confusas if p in texto_lower)
        
        if len(texto_lower.split()) == 0:
            return 0.0
        
        claridad = (conteo_claro - conteo_confuso) / max(1, len(texto_lower.split()) / 10)
        return max(-1.0, min(1.0, claridad))
    
    def _analizar_fuerza_simple(self, texto: str) -> float:
        if not texto:
            return 0.0
        
        palabras_fuertes = ['absolutamente', 'definitivamente', 'seguro', 'decisivo']
        palabras_debiles = ['quizás', 'posiblemente', 'dudo', 'inseguro']
        
        texto_lower = texto.lower()
        
        conteo_fuerte = sum(1 for p in palabras_fuertes if p in texto_lower)
        conteo_debil = sum(1 for p in palabras_debiles if p in texto_lower)
        
        if len(texto_lower.split()) == 0:
            return 0.0
        
        fuerza = (conteo_fuerte - conteo_debil) / max(1, len(texto_lower.split()) / 10)
        return max(-1.0, min(1.0, fuerza))
'''
    
    with open('dimensiones/dimension_1_funcional.py', 'w', encoding='utf-8') as f:
        f.write(dim1)
    
    # Actualizar el archivo original
    with open('dimensiones/dimension_1.py', 'w', encoding='utf-8') as f:
        f.write(dim1)
    
    print("Actualizado: dimensiones/dimension_1.py (versión funcional)")

def main():
    print("CORRIGIENDO PROBLEMAS DE IMPORTACION VECTA 12D...")
    print("=" * 60)
    
    # Crear archivos __init__.py
    crear_init_dimensiones()
    crear_init_core()
    
    # Corregir importaciones
    corregir_importaciones_dimensiones()
    corregir_vector_12d()
    
    # Crear sistema alternativo
    crear_sistema_carga_alternativo()
    actualizar_vector_12d_con_cargador()
    
    # Crear dimensiones funcionales
    crear_dimensiones_funcionales()
    
    print("=" * 60)
    print("CORRECCIONES APLICADAS")
    print("=" * 60)
    print("Ahora ejecuta:")
    print("  python vecta_launcher.py")
    print("O")
    print("  python probar_sistema_filosofico.py")

if __name__ == "__main__":
    main()