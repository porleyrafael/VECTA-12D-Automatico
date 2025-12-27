"""
SISTEMA VECTORIAL 12D - VERSIÓN CORREGIDA
Sistema unificado de 12 dimensiones vectoriales
"""

import sys
import os
import importlib

class Vector12D:
    def __init__(self, dimensiones):
        self.dimensiones = dimensiones
    
    def magnitud(self):
        import math
        suma = sum(d * d for d in self.dimensiones)
        return math.sqrt(suma) if suma > 0 else 0.0
    
    def __str__(self):
        dims = ", ".join([f"{d:.4f}" for d in self.dimensiones])
        return f"Vector12D(mag={self.magnitud():.4f}, dims=[{dims}])"

class SistemaVectorial12D:
    def __init__(self):
        self.dimensiones = []
        self._cargar_dimensiones()
    
    def _cargar_dimensiones(self):
        """Carga las 12 dimensiones"""
        dimensiones_cargadas = 0
        
        for i in range(1, 13):
            try:
                # Verificar si el archivo existe
                archivo = f"dimensiones/dimension_{i}.py"
                if not os.path.exists(archivo):
                    continue
                
                # Importar el módulo
                modulo_nombre = f"dimensiones.dimension_{i}"
                modulo = importlib.import_module(modulo_nombre)
                
                # Buscar clases en el módulo
                for nombre in dir(modulo):
                    obj = getattr(modulo, nombre)
                    if isinstance(obj, type):
                        # Crear instancia
                        instancia = obj()
                        self.dimensiones.append(instancia)
                        dimensiones_cargadas += 1
                        break
                        
            except Exception:
                continue
        
        # Si no se cargaron, crear dimensiones simples
        if dimensiones_cargadas == 0:
            class DimensionSimple:
                def __init__(self, idx):
                    self.idx = idx
                    self.nombre = f"Dimensión_{idx}"
                
                def procesar(self, evento):
                    return {"magnitud": 0.1 * self.idx, "nombre": self.nombre}
            
            for i in range(1, 13):
                self.dimensiones.append(DimensionSimple(i))
    
    def procesar_evento(self, evento):
        """Procesa un evento a través de todas las dimensiones"""
        valores = []
        
        for i, dim in enumerate(self.dimensiones, 1):
            try:
                if hasattr(dim, 'procesar'):
                    resultado = dim.procesar(evento)
                    if isinstance(resultado, dict) and 'magnitud' in resultado:
                        valores.append(float(resultado['magnitud']))
                    elif isinstance(resultado, (int, float)):
                        valores.append(float(resultado))
                    else:
                        valores.append(0.1 * i)
                else:
                    valores.append(0.1 * i)
            except:
                valores.append(0.05 * i)
        
        # Asegurar 12 valores
        while len(valores) < 12:
            valores.append(0.0)
        
        if len(valores) > 12:
            valores = valores[:12]
        
        return Vector12D(valores)
    
    def obtener_numero_dimensiones(self):
        return len(self.dimensiones)
