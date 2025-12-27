#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VECTA 12D - AUTO-REPARACIÓN DE MENÚ
Script automático para corregir el error de sintaxis en el menú
"""

import os
import sys
import time

print("\n" + "="*70)
print("🔧 VECTA 12D - AUTO-REPARACIÓN DE MENÚ")
print("="*70)

def reparar_menu_lanzador():
    """Repara el error de sintaxis en vecta_launcher.py"""
    
    archivo = "vecta_launcher.py"
    
    if not os.path.exists(archivo):
        print(f"❌ Archivo no encontrado: {archivo}")
        return False
    
    print(f"📖 Leyendo {archivo}...")
    
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            lineas = f.readlines()
        
        print(f"✅ Leídas {len(lineas)} líneas")
        
        # Buscar el menú problemático
        menu_encontrado = False
        lineas_reparadas = []
        
        for i, linea in enumerate(lineas):
            if "6. Sistema META-VECTA (Nuevo)" in linea and not linea.strip().startswith("print"):
                print(f"⚠️  Línea {i+1} con error: {linea.strip()}")
                # Corregir la línea - agregar print
                linea_corregida = '    print("6. Sistema META-VECTA (Nuevo)")\n'
                lineas_reparadas.append(linea_corregida)
                menu_encontrado = True
                print(f"✅ Línea corregida: {linea_corregida.strip()}")
            elif "7. Salir del sistema" in linea and not linea.strip().startswith("print"):
                print(f"⚠️  Línea {i+1} con error: {linea.strip()}")
                # Corregir la línea - agregar print
                linea_corregida = '    print("7. Salir del sistema")\n'
                lineas_reparadas.append(linea_corregida)
                print(f"✅ Línea corregida: {linea_corregida.strip()}")
            else:
                lineas_reparadas.append(linea)
        
        if not menu_encontrado:
            # Intentar otro método: buscar la función mostrar_menu_principal
            print("🔍 Buscando función mostrar_menu_principal...")
            
            # Unir las líneas para buscar mejor
            contenido = ''.join(lineas)
            
            # Definir el menú corregido
            menu_corregido = '''def mostrar_menu_principal():
    """Muestra el menú principal de opciones."""
    print("\\n" + "═" * 70)
    print("MENÚ PRINCIPAL - VECTA 12D")
    print("═" * 70)
    print("1. Procesar texto/comando")
    print("2. Ver estado del sistema")
    print("3. Probar dimensiones individuales")
    print("4. Ejecutar autodiagnóstico")
    print("5. Generar vector 12D aleatorio")
    print("6. Sistema META-VECTA (Nuevo)")
    print("7. Salir del sistema")
    print("═" * 70)
'''
            
            # Reemplazar la función completa
            if 'def mostrar_menu_principal():' in contenido:
                # Encontrar inicio y fin de la función
                inicio = contenido.find('def mostrar_menu_principal():')
                # Buscar el próximo def o return
                fin = contenido.find('\ndef ', inicio + 1)
                if fin == -1:
                    fin = len(contenido)
                
                # Crear nuevo contenido
                nuevo_contenido = contenido[:inicio] + menu_corregido + contenido[fin:]
                lineas_reparadas = nuevo_contenido.splitlines(keepends=True)
                print("✅ Función mostrar_menu_principal reemplazada completamente")
            else:
                print("❌ No se encontró la función del menú")
                return False
        
        # Escribir el archivo reparado
        with open(archivo, 'w', encoding='utf-8') as f:
            f.writelines(lineas_reparadas)
        
        print(f"✅ Archivo reparado: {archivo}")
        print(f"📏 Nuevo tamaño: {os.path.getsize(archivo)} bytes")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al reparar: {e}")
        return False

def verificar_reparacion():
    """Verifica que la reparación fue exitosa"""
    
    archivo = "vecta_launcher.py"
    
    try:
        # Verificar sintaxis Python
        print("\n🔍 Verificando sintaxis Python...")
        import ast
        with open(archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()
        ast.parse(contenido)  # Esto lanza SyntaxError si hay error
        print("✅ Sintaxis Python válida")
        
        # Verificar que el menú esté correcto
        if 'print("6. Sistema META-VECTA (Nuevo)")' in contenido:
            print("✅ Menú META-VECTA presente")
        else:
            print("⚠️  Menú META-VECTA no encontrado")
        
        # Verificar que no haya líneas problemáticas
        lineas_problematicas = []
        for i, linea in enumerate(contenido.split('\n'), 1):
            if "6. Sistema META-VECTA (Nuevo)" in linea and not linea.strip().startswith("print"):
                lineas_problematicas.append(i)
            if "7. Salir del sistema" in linea and not linea.strip().startswith("print"):
                lineas_problematicas.append(i)
        
        if lineas_problematicas:
            print(f"⚠️  Líneas potencialmente problemáticas: {lineas_problematicas}")
            return False
        else:
            print("✅ Sin líneas problemáticas detectadas")
            return True
            
    except SyntaxError as e:
        print(f"❌ Error de sintaxis: {e}")
        return False
    except Exception as e:
        print(f"❌ Error en verificación: {e}")
        return False

def probar_lanzador():
    """Prueba el lanzador rápidamente"""
    
    print("\n🧪 Probando ejecución del lanzador...")
    
    # Crear un script de prueba temporal
    script_prueba = '''
import sys
import io
from contextlib import redirect_stdout, redirect_stderr

# Capturar salida
salida_capturada = io.StringIO()
errores_capturada = io.StringIO()

try:
    with redirect_stdout(salida_capturada), redirect_stderr(errores_capturada):
        # Ejecutar el lanzador brevemente
        import vecta_launcher
        # Solo importar, no ejecutar main automáticamente
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)

# Verificar que no hay errores
errores = errores_capturada.getvalue()
if errores:
    print(f"⚠️  Errores encontrados: {errores[:200]}")
else:
    print("✅ Sin errores en importación")
    
# Verificar que se puede crear el menú
if "mostrar_menu_principal" in dir(vecta_launcher):
    print("✅ Función mostrar_menu_principal disponible")
else:
    print("❌ Función del menú no disponible")
'''
    
    try:
        # Guardar script temporal
        with open('_prueba_menu.py', 'w', encoding='utf-8') as f:
            f.write(script_prueba)
        
        # Ejecutar prueba
        import subprocess
        resultado = subprocess.run([sys.executable, '_prueba_menu.py'], 
                                 capture_output=True, text=True, timeout=5)
        
        # Limpiar
        if os.path.exists('_prueba_menu.py'):
            os.remove('_prueba_menu.py')
        
        if resultado.returncode == 0:
            print("✅ Prueba de ejecución exitosa")
            print(resultado.stdout)
            return True
        else:
            print("❌ Prueba fallida")
            print("STDOUT:", resultado.stdout)
            print("STDERR:", resultado.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error en prueba: {e}")
        # Limpiar si existe
        if os.path.exists('_prueba_menu.py'):
            os.remove('_prueba_menu.py')
        return False

def main():
    """Función principal de reparación"""
    
    # Paso 1: Reparar el menú
    if not reparar_menu_lanzador():
        print("❌ Falló la reparación del menú")
        return 1
    
    # Paso 2: Verificar reparación
    if not verificar_reparacion():
        print("❌ Falló la verificación")
        return 1
    
    # Paso 3: Probar el lanzador
    if not probar_lanzador():
        print("⚠️  Advertencia en prueba del lanzador")
    
    # Paso 4: Mostrar resumen
    print("\n" + "="*70)
    print("🎉 AUTO-REPARACIÓN COMPLETADA")
    print("="*70)
    
    print("\n✅ El menú ha sido reparado correctamente")
    print("✅ Sintaxis Python verificada")
    print("✅ Estructura del menú corregida")
    
    print("\n🚀 Ahora puedes ejecutar:")
    print("   python vecta_launcher.py")
    
    print("\n📋 Nuevo menú disponible:")
    print("   1. Procesar texto/comando")
    print("   2. Ver estado del sistema")
    print("   3. Probar dimensiones individuales")
    print("   4. Ejecutar autodiagnóstico")
    print("   5. Generar vector 12D aleatorio")
    print("   6. Sistema META-VECTA (Nuevo)")
    print("   7. Salir del sistema")
    
    print("\n" + "="*70)
    
    return 0

if __name__ == "__main__":
    try:
        exit_code = main()
        input("\nPresiona Enter para salir...")
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n❌ Reparación interrumpida")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)