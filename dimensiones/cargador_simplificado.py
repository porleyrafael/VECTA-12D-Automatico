"""
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
