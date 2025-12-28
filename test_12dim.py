# Guarda esto como test_12dim.py y ejecútalo
import importlib
import os

print("🧪 TESTEANDO LAS 12 DIMENSIONES REALES")
print("="*50)

dimensiones = [
    "intencionalidad", "logica", "contexto",
    "temporalidad", "emergencia", "recursividad", 
    "holismo", "singularidad", "metacognicion",
    "transcendencia", "universalidad", "autonomia"
]

for i, dim in enumerate(dimensiones, 1):
    try:
        modulo = importlib.import_module(f"dimensiones.{dim}")
        print(f"{i:2d}. ✅ {dim:20} → CARGADO")
    except Exception as e:
        print(f"{i:2d}. ❌ {dim:20} → ERROR: {str(e)[:50]}")

print(f"\n📊 RESULTADO: Buscando archivos...")
archivos = os.listdir("dimensiones")
print(f"   Archivos en carpeta 'dimensiones/': {len(archivos)}")
for archivo in archivos:
    if archivo.endswith(".py"):
        print(f"   - {archivo}")