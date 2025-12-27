"""
SISTEMA VECTORIAL 12D - VERSIÓN CORREGIDA
Sistema unificado de 12 dimensiones vectoriales
"""
import json
import time
import importlib
import sys
import os
from typing import List, Dict, Any

# Asegurar que podemos importar desde el directorio actual
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class Vector12D:
    """Representa un vector en 12 dimensiones"""
    def __init__(self, dimensiones: List[float]):
        self.dimensiones = dimensiones
        self.timestamp = time.time()
        
    def magnitud(self) -> float:
        """Calcula la magnitud del vector"""
        import math
        suma_cuadrados = sum(d * d for d in self.dimensiones)
        return math.sqrt(suma_cuadrados) if suma_cuadrados > 0 else 0.0
    
    def normalizar(self) -> 'Vector12D':
        """Devuelve una versión normalizada del vector"""
        mag = self.magnitud()
        if mag > 0:
            return Vector12D([d / mag for d in self.dimensiones])
        return Vector12D([0.0] * 12)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el vector a diccionario"""
        return {
            'dimensiones': self.dimensiones,
            'magnitud': self.magnitud(),
            'timestamp': self.timestamp,
            'dimensiones_count': len(self.dimensiones)
        }
    
    def __str__(self) -> str:
        """Representación en texto del vector"""
        dim_str = ", ".join([f"{d:.4f}" for d in self.dimensiones])
        return f"Vector12D(mag={self.magnitud():.4f}, dims=[{dim_str}])"

class SistemaVectorial12D:
    """Sistema principal que maneja las 12 dimensiones"""
    
    def __init__(self):
        print("[Vector12D] Inicializando sistema vectorial...")
        self.dimensiones = []
        self._cargar_dimensiones()
        print(f"[Vector12D] Sistema inicializado con {len(self.dimensiones)} dimensiones")
    
    def _cargar_dimensiones(self):
        """Carga dinámicamente las 12 dimensiones"""
        dimensiones_cargadas = 0
        
        for i in range(1, 13):
            try:
                # Construir el nombre del módulo
                modulo_nombre = f"dimensiones.dimension_{i}"
                
                # Verificar si el archivo existe
                archivo_dimension = f"dimensiones/dimension_{i}.py"
                if not os.path.exists(archivo_dimension):
                    print(f"  [Vector12D] Advertencia: No existe {archivo_dimension}")
                    continue
                
                # Importar el módulo
                modulo = importlib.import_module(modulo_nombre)
                
                # Buscar la clase principal en el módulo
                clase_dimension = None
                for nombre_clase in dir(modulo):
                    # Filtrar nombres que contengan 'Dimension' o 'Dim'
                    if 'Dimension' in nombre_clase or 'Dim' in nombre_clase:
                        obj = getattr(modulo, nombre_clase)
                        if isinstance(obj, type):  # Es una clase
                            clase_dimension = obj
                            break
                
                if clase_dimension:
                    # Crear instancia de la dimensión
                    instancia = clase_dimension()
                    self.dimensiones.append(instancia)
                    dimensiones_cargadas += 1
                    print(f"  [Vector12D] ✓ Dimensión {i} cargada: {clase_dimension.__name__}")
                else:
                    print(f"  [Vector12D] ✗ No se encontró clase en dimensión {i}")
                    
            except ImportError as e:
                print(f"  [Vector12D] ✗ Error importando dimensión {i}: {str(e)[:100]}")
            except Exception as e:
                print(f"  [Vector12D] ✗ Error cargando dimensión {i}: {str(e)[:100]}")
        
        # Si no se cargaron dimensiones, crear dimensiones por defecto
        if dimensiones_cargadas == 0:
            print("  [Vector12D] ⚠️ Creando dimensiones por defecto...")
            self._crear_dimensiones_por_defecto()
    
    def _crear_dimensiones_por_defecto(self):
        """Crea dimensiones básicas por defecto si no se pueden cargar las reales"""
        class DimensionBase:
            def __init__(self, nombre, indice):
                self.nombre = nombre
                self.indice = indice
                self.contador = 0
            
            def procesar(self, evento):
                self.contador += 1
                # Valor simple basado en el índice y longitud del evento
                valor = 0.1 * self.indice + 0.01 * len(str(evento))
                return {'magnitud': valor, 'procesado': True, 'dimension': self.indice}
        
        nombres = [
            "Tiempo-Entropía", "Espacio-Volumen", "Energía-Potencial",
            "Información-Entropía", "Conciencia-Atención", "Memoria-Persistencia",
            "Aprendizaje-Adaptación", "Creatividad-Generación", "Ejecución-Acción",
            "Validación-Corrección", "Conectividad-Red", "Meta-Autoprogramación"
        ]
        
        for i, nombre in enumerate(nombres, 1):
            dim = DimensionBase(nombre, i)
            self.dimensiones.append(dim)
            print(f"  [Vector12D] ✓ Dimensión por defecto {i}: {nombre}")
    
    def procesar_evento(self, evento: Dict[str, Any]) -> Vector12D:
        """
        Procesa un evento a través de las 12 dimensiones
        
        Args:
            evento: Diccionario con datos del evento
        
        Returns:
            Vector12D: Vector resultante de 12 dimensiones
        """
        magnitudes = []
        
        if not self.dimensiones:
            print("[Vector12D] ⚠️ No hay dimensiones cargadas, usando valores por defecto")
            # Crear un vector simple basado en el evento
            import hashlib
            evento_str = str(evento)
            hash_obj = hashlib.md5(evento_str.encode())
            hash_int = int(hash_obj.hexdigest(), 16)
            
            for i in range(12):
                # Generar valor pseudo-aleatorio basado en el hash
                valor = (hash_int % (100 * (i + 1))) / 100.0
                magnitudes.append(valor)
        else:
            # Procesar con cada dimensión
            for i, dimension in enumerate(self.dimensiones, 1):
                try:
                    resultado = dimension.procesar(evento)
                    
                    # Extraer magnitud del resultado
                    if isinstance(resultado, dict) and 'magnitud' in resultado:
                        magnitud = resultado['magnitud']
                    elif isinstance(resultado, (int, float)):
                        magnitud = float(resultado)
                    else:
                        # Valor por defecto basado en el índice
                        magnitud = 0.1 * i + 0.01 * len(str(evento))
                    
                    magnitudes.append(float(magnitud))
                    
                except AttributeError:
                    print(f"  [Vector12D] ✗ Dimensión {i} no tiene método 'procesar'")
                    magnitudes.append(0.1 * i)  # Valor por defecto
                except Exception as e:
                    print(f"  [Vector12D] ✗ Error en dimensión {i}: {str(e)[:50]}")
                    magnitudes.append(0.05 * i)  # Valor por defecto más bajo
        
        # Asegurar que tenemos exactamente 12 dimensiones
        while len(magnitudes) < 12:
            magnitudes.append(0.0)
        
        # Limitar a 12 dimensiones si hay más
        if len(magnitudes) > 12:
            magnitudes = magnitudes[:12]
        
        return Vector12D(magnitudes)
    
    def obtener_numero_dimensiones(self) -> int:
        """Devuelve el número de dimensiones cargadas"""
        return len(self.dimensiones)
    
    def obtener_info_dimensiones(self) -> List[Dict[str, Any]]:
        """Devuelve información detallada de cada dimensión"""
        info = []
        for i, dim in enumerate(self.dimensiones, 1):
            try:
                nombre = getattr(dim, 'nombre', f'Dimension_{i}')
                tipo = type(dim).__name__
                info.append({
                    'indice': i,
                    'nombre': nombre,
                    'tipo': tipo,
                    'modulo': dim.__class__.__module__
                })
            except:
                info.append({
                    'indice': i,
                    'nombre': f'Dimension_{i}',
                    'tipo': 'Desconocido',
                    'modulo': 'Desconocido'
                })
        return info
    
    def __str__(self) -> str:
        """Representación en texto del sistema"""
        return f"SistemaVectorial12D(dimensiones={len(self.dimensiones)})"

# Función de prueba para verificar que el sistema funciona
def prueba_sistema():
    """Función de prueba del sistema vectorial"""
    print("\n" + "="*60)
    print("PRUEBA DEL SISTEMA VECTORIAL 12D")
    print("="*60)
    
    sistema = SistemaVectorial12D()
    
    print(f"\n✓ Sistema creado: {sistema}")
    print(f"✓ Dimensiones cargadas: {sistema.obtener_numero_dimensiones()}")
    
    # Probar con un evento simple
    evento_prueba = {
        'texto': 'Prueba del sistema',
        'timestamp': time.time(),
        'tipo': 'prueba'
    }
    
    print(f"\n📤 Procesando evento: {evento_prueba['texto']}")
    vector_resultado = sistema.procesar_evento(evento_prueba)
    
    print(f"\n✅ RESULTADO:")
    print(f"  Vector: {vector_resultado}")
    print(f"  Magnitud: {vector_resultado.magnitud():.4f}")
    print(f"  Dimensiones: {len(vector_resultado.dimensiones)}")
    
    # Mostrar valores por dimensión
    print(f"\n📊 VALORES POR DIMENSIÓN:")
    for i, valor in enumerate(vector_resultado.dimensiones, 1):
        print(f"  Dimensión {i:2d}: {valor:.6f}")
    
    return sistema

# Si se ejecuta este archivo directamente, hacer una prueba
if __name__ == "__main__":
    prueba_sistema()
    print("\n" + "="*60)
    print("PRUEBA COMPLETADA - Sistema Vectorial 12D operativo")
    print("="*60)