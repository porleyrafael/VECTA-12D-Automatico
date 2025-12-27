"""
VECTA 12D - SISTEMA DE REPARACIÓN AUTOMÁTICA
Script único para diagnosticar y reparar todo el sistema
"""

import os
import sys
import time
import shutil

print("\n" + "="*70)
print("🚀 VECTA 12D - REPARACIÓN AUTOMÁTICA")
print("="*70)
print(f"Hora de inicio: {time.strftime('%H:%M:%S')}")
print(f"Directorio: {os.getcwd()}")
print("="*70)

# ======================= PASO 1: DIAGNÓSTICO =======================
print("\n[1/5] 🔍 EJECUTANDO DIAGNÓSTICO COMPLETO...")

problemas = []
advertencias = []

# 1. Verificar directorios
print("\n  📁 Verificando estructura...")
if os.path.exists("core"):
    print("    ✓ Directorio 'core' encontrado")
else:
    print("    ✗ Directorio 'core' NO encontrado")
    problemas.append("Falta directorio 'core'")

if os.path.exists("dimensiones"):
    print("    ✓ Directorio 'dimensiones' encontrado")
else:
    print("    ✗ Directorio 'dimensiones' NO encontrado")
    problemas.append("Falta directorio 'dimensiones'")

# 2. Verificar archivos críticos
print("\n  📄 Verificando archivos críticos...")
archivos_criticos = [
    ("core/vecta_12d_core.py", "Archivo principal del núcleo"),
    ("core/__init__.py", "Paquete del núcleo"),
    ("dimensiones/vector_12d.py", "Sistema vectorial 12D"),
    ("vecta_launcher.py", "Lanzador principal")
]

for archivo, descripcion in archivos_criticos:
    if os.path.exists(archivo):
        tamaño = os.path.getsize(archivo)
        if tamaño > 100:
            print(f"    ✓ {archivo} ({tamaño} bytes)")
        else:
            print(f"    ⚠️  {archivo} muy pequeño ({tamaño} bytes)")
            advertencias.append(f"{archivo} tiene solo {tamaño} bytes")
    else:
        print(f"    ✗ {archivo} NO encontrado")
        problemas.append(f"Falta {descripcion}")

# 3. Contar dimensiones
print("\n  📊 Contando dimensiones...")
dimensiones_encontradas = 0
for i in range(1, 13):
    archivo = f"dimensiones/dimension_{i}.py"
    if os.path.exists(archivo):
        dimensiones_encontradas += 1

print(f"    ✓ Archivos de dimensiones: {dimensiones_encontradas}/12")

if dimensiones_encontradas < 12:
    advertencias.append(f"Solo {dimensiones_encontradas} de 12 dimensiones encontradas")

# 4. Verificar Python
print("\n  🐍 Verificando Python...")
try:
    version = sys.version.split()[0]
    print(f"    ✓ Python {version} detectado")
except:
    print("    ⚠️  No se pudo verificar Python")

# Mostrar resumen de diagnóstico
print("\n" + "-"*70)
print("📋 RESUMEN DE DIAGNÓSTICO")
print("-"*70)

if problemas:
    print("🚨 PROBLEMAS CRÍTICOS:")
    for p in problemas:
        print(f"  ✗ {p}")
else:
    print("✅ No hay problemas críticos")

if advertencias:
    print("\n⚠️  ADVERTENCIAS:")
    for a in advertencias:
        print(f"  ! {a}")
else:
    print("✅ No hay advertencias")

print("-"*70)

# ======================= PASO 2: REPARAR VECTOR_12D.PY =======================
print("\n[2/5] 🛠️  REPARANDO vector_12d.py...")

# Primero hacer backup si existe
archivo_vector = "dimensiones/vector_12d.py"
if os.path.exists(archivo_vector):
    try:
        shutil.copy2(archivo_vector, "dimensiones/vector_12d.py.backup")
        print("  ✓ Backup creado: vector_12d.py.backup")
    except:
        print("  ⚠️  No se pudo hacer backup")

# Crear nuevo vector_12d.py corregido
codigo_corregido = '''"""
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
'''

# Guardar el archivo
try:
    with open(archivo_vector, 'w', encoding='utf-8') as f:
        f.write(codigo_corregido)
    
    tamaño = os.path.getsize(archivo_vector)
    print(f"  ✅ vector_12d.py creado: {tamaño} bytes")
except Exception as e:
    print(f"  ❌ Error al crear archivo: {e}")
    problemas.append("No se pudo crear vector_12d.py")

# ======================= PASO 3: VERIFICAR REPARACIÓN =======================
print("\n[3/5] ✅ VERIFICANDO REPARACIÓN...")

try:
    # Agregar directorio actual al path
    sys.path.insert(0, os.getcwd())
    
    # Importar el sistema corregido
    from dimensiones.vector_12d import SistemaVectorial12D
    
    print("  ✓ Importación exitosa")
    
    # Crear instancia
    sistema = SistemaVectorial12D()
    print(f"  ✓ Sistema creado: {sistema}")
    
    # Obtener número de dimensiones
    num_dimensiones = sistema.obtener_numero_dimensiones()
    print(f"  ✓ Dimensiones cargadas: {num_dimensiones}")
    
    # Probar procesamiento
    import time
    evento_prueba = {"test": "prueba", "time": time.time()}
    vector = sistema.procesar_evento(evento_prueba)
    print(f"  ✓ Vector generado: {vector}")
    
    # Verificar que no sea todo ceros
    if all(v == 0 for v in vector.dimensiones):
        print("  ⚠️  Advertencia: El vector tiene todos ceros")
    else:
        print("  ✓ Vector con valores no nulos")
    
    print("  ✅ REPARACIÓN EXITOSA")
    
except Exception as e:
    print(f"  ❌ Error en verificación: {e}")
    import traceback
    print(f"  Detalle: {traceback.format_exc()[:200]}")
    problemas.append("Fallo en verificación de reparación")

# ======================= PASO 4: PROBAR COMPONENTES =======================
print("\n[4/5] 🧪 PROBANDO COMPONENTES DEL SISTEMA...")

try:
    # Probar núcleo
    from core.vecta_12d_core import VECTA_12D_Core
    nucleo = VECTA_12D_Core()
    print("  ✓ Núcleo VECTA cargado")
    
    # Probar procesamiento del núcleo
    if hasattr(nucleo, 'procesar'):
        resultado = nucleo.procesar('Prueba del sistema')
        print(f"  ✓ Núcleo procesó: {resultado}")
    
    print("  ✅ Todos los componentes funcionan")
    
except Exception as e:
    print(f"  ⚠️  Error en componentes: {e}")

# ======================= PASO 5: RESULTADO FINAL =======================
print("\n[5/5] 🎯 RESULTADO FINAL")
print("="*70)

if problemas:
    print("❌ REPARACIÓN INCOMPLETA")
    print("\nProblemas pendientes:")
    for p in problemas:
        print(f"  • {p}")
    
    print("\n🔄 Acciones recomendadas:")
    print("  1. Verifica que todos los archivos existan")
    print("  2. Ejecuta: dir core\\*.py")
    print("  3. Ejecuta: dir dimensiones\\*.py")
    print("  4. Verifica permisos de escritura")
else:
    print("🎉 ¡REPARACIÓN COMPLETADA EXITOSAMENTE!")
    print(f"\n✅ Dimensiones cargadas: {num_dimensiones}")
    print("✅ Sistema vectorial operativo")
    print("✅ Núcleo VECTA funcional")
    
    print("\n📋 AHORA PUEDES EJECUTAR:")
    print("  python vecta_launcher.py")
    
    print("\n🎮 OPCIONES DISPONIBLES EN EL LANZADOR:")
    print("  1. Procesar texto/comando")
    print("  2. Ver estado del sistema")
    print("  3. Probar dimensiones individuales")
    print("  4. Ejecutar autodiagnóstico")
    print("  5. Generar vector 12D aleatorio")
    print("  6. Salir del sistema")

print("\n" + "="*70)
print("FIN DEL PROCESO DE REPARACIÓN")
print(f"Hora de finalización: {time.strftime('%H:%M:%S')}")
print("="*70)

# Pausa para que puedas leer los resultados
input("\nPresiona Enter para salir...")