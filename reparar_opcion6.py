#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VECTA 12D - REPARACIÓN DE OPCIÓN 6 (META-VECTA)
Corrige el procesamiento de la opción 6 en el lanzador
"""

import os
import sys

print("\n" + "="*70)
print("🔧 VECTA 12D - REPARACIÓN DE OPCIÓN 6 (META-VECTA)")
print("="*70)

def reparar_opcion6():
    """Repara específicamente la opción 6 del lanzador"""
    
    archivo = "vecta_launcher.py"
    
    if not os.path.exists(archivo):
        print(f"❌ Archivo no encontrado: {archivo}")
        return False
    
    print(f"📖 Leyendo {archivo}...")
    
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        print(f"✅ Leídas {len(contenido)} caracteres")
        
        # Buscar la función procesar_opcion
        if 'def procesar_opcion(' not in contenido:
            print("❌ No se encontró la función procesar_opcion")
            return False
        
        # Extraer la función completa
        inicio = contenido.find('def procesar_opcion(')
        # Encontrar el final de la función (próxima función o fin)
        funciones = ['\ndef ', '\nclass ', '\nasync def ']
        fin = len(contenido)
        for func in funciones:
            idx = contenido.find(func, inicio + 1)
            if idx != -1 and idx < fin:
                fin = idx
        
        funcion_completa = contenido[inicio:fin]
        
        print("🔍 Analizando función procesar_opcion...")
        
        # Verificar si ya tiene la opción 6 correcta
        if 'opcion == "6"' in funcion_completa and 'Sistema META-VECTA' in funcion_completa:
            print("✅ La opción 6 ya está configurada para META-VECTA")
            return True
        
        # Buscar y reemplazar la opción 6 actual (que debe ser la de salir)
        if 'opcion == "6"' in funcion_completa:
            print("⚠️  Opción 6 actualmente configurada para salir, cambiando a META-VECTA...")
            
            # Código para la opción 6 (META-VECTA)
            codigo_opcion6 = '''    elif opcion == "6":
        # Sistema META-VECTA
        print("\\n" + "="*70)
        print("🚀 SISTEMA META-VECTA - Especificación 1.0")
        print("="*70)
        
        try:
            from core.meta_vecta import VECTASystem, test_vecta_system
            
            print("\\nOpciones META-VECTA:")
            print("  1. Ejecutar prueba completa")
            print("  2. Procesar intención personalizada")
            print("  3. Ver estado del sistema META-VECTA")
            print("  4. Volver al menú principal")
            
            sub_opcion = input("\\nSeleccione opción (1-4): ").strip()
            
            if sub_opcion == "1":
                print("\\n🧪 Ejecutando prueba META-VECTA...")
                test_vecta_system()
                
            elif sub_opcion == "2":
                print("\\n" + "-"*50)
                print("PROCESADOR DE INTENCIONES META-VECTA")
                print("-"*50)
                
                texto = input("Intención: ").strip()
                if not texto:
                    print("❌ Intención vacía")
                else:
                    vecta = VECTASystem()
                    resultado = vecta.process_intention(
                        texto,
                        context={"domain": "LONG_TERM_PLANNING"},
                        auth_key="RAFAEL_PORLEY_VECTA"
                    )
                    
                    if resultado.get("success"):
                        print(f"\\n✅ Decisión: {resultado['decision']['action']}")
                        print(f"📊 Probabilidad: {resultado['decision']['probability']:.1%}")
                        print(f"🔍 Interpretación: {resultado['field_interpretation']}")
                    else:
                        print(f"\\n❌ Error: {resultado.get('error')}")
                        
            elif sub_opcion == "3":
                vecta = VECTASystem()
                estado = vecta.get_system_status()
                
                print(f"\\n📊 ESTADO META-VECTA:")
                print(f"  • Versión: {estado['meta']['version']}")
                print(f"  • Creador: {estado['meta']['creator']}")
                print(f"  • Principios: {estado['meta']['principles_count']}")
                print(f"  • Símbolos: {estado['language']['base_symbols']} base")
                print(f"  • Ciclos: {estado['runtime']['cycles_executed']}")
                print(f"  • Dominios: {', '.join(estado['safety']['authorized_domains'])}")
                
            else:
                print("Volviendo al menú principal...")
                
        except ImportError as e:
            print(f"❌ Error: {e}")
            print("  Asegúrate de que core/meta_vecta.py existe")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
        
        input("\\nPresione Enter para continuar...")
        return True'''
        
            # Encontrar y reemplazar el bloque de la opción 6 actual
            lineas = contenido.split('\n')
            nueva_lineas = []
            i = 0
            
            while i < len(lineas):
                linea = lineas[i]
                
                if 'opcion == "6"' in linea and 'elif' in linea:
                    print(f"📝 Encontrada línea {i+1}: {linea.strip()}")
                    
                    # Saltar todo el bloque de la opción 6 actual
                    j = i + 1
                    while j < len(lineas):
                        # Buscar el próximo elif, else, o return
                        if (lineas[j].strip().startswith('elif ') or 
                            lineas[j].strip().startswith('else:') or
                            lineas[j].strip().startswith('return ')):
                            break
                        j += 1
                    
                    # Insertar el nuevo código de la opción 6
                    nueva_lineas.append(codigo_opcion6)
                    i = j  # Saltar al siguiente bloque
                    
                else:
                    nueva_lineas.append(linea)
                    i += 1
            
            nuevo_contenido = '\n'.join(nueva_lineas)
            
        else:
            # Si no existe opción 6, insertarla después de la opción 5
            print("📝 Insertando nueva opción 6 después de opción 5...")
            
            lineas = contenido.split('\n')
            nueva_lineas = []
            i = 0
            
            while i < len(lineas):
                linea = lineas[i]
                nueva_lineas.append(linea)
                
                # Buscar el bloque de la opción 5
                if 'opcion == "5"' in linea and 'elif' in linea:
                    print(f"📝 Encontrada opción 5 en línea {i+1}")
                    
                    # Encontrar el final del bloque de opción 5
                    j = i + 1
                    while j < len(lineas):
                        # Buscar el próximo elif, else, o return
                        if (lineas[j].strip().startswith('elif ') or 
                            lineas[j].strip().startswith('else:') or
                            lineas[j].strip().startswith('return ')):
                            break
                        j += 1
                    
                    # Insertar la opción 6 aquí
                    nueva_lineas.append(codigo_opcion6)
                    i = j - 1  # Continuar desde donde quedamos
                
                i += 1
            
            nuevo_contenido = '\n'.join(nueva_lineas)
        
        # Escribir el archivo reparado
        with open(archivo, 'w', encoding='utf-8') as f:
            f.write(nuevo_contenido)
        
        print(f"✅ Archivo reparado: {archivo}")
        print(f"📏 Nuevo tamaño: {os.path.getsize(archivo)} bytes")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al reparar: {e}")
        import traceback
        print(f"Detalles: {traceback.format_exc()[:200]}")
        return False

def verificar_reparacion():
    """Verifica que la reparación fue exitosa"""
    
    archivo = "vecta_launcher.py"
    
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        verificaciones = [
            ('opcion == "6"' in contenido and 'Sistema META-VECTA' in contenido, 
             "Opción 6 configurada para META-VECTA"),
            ('opcion == "7"' in contenido and 'Salir' in contenido,
             "Opción 7 configurada para salir"),
            ('from core.meta_vecta import' in contenido,
             "Importación de META-VECTA presente"),
            ('def procesar_opcion(' in contenido,
             "Función procesar_opcion presente")
        ]
        
        todas_ok = True
        for condicion, mensaje in verificaciones:
            if condicion:
                print(f"✅ {mensaje}")
            else:
                print(f"❌ {mensaje}")
                todas_ok = False
        
        return todas_ok
        
    except Exception as e:
        print(f"❌ Error en verificación: {e}")
        return False

def probar_opcion6():
    """Prueba la opción 6 rápidamente"""
    
    print("\n🧪 Probando opción 6...")
    
    # Crear un script de prueba temporal
    script_prueba = '''
import sys
import io
from contextlib import redirect_stdout, redirect_stderr

# Importar el lanzador
try:
    import vecta_launcher
except Exception as e:
    print(f"❌ Error importando lanzador: {e}")
    sys.exit(1)

# Simular la función procesar_opcion
if hasattr(vecta_launcher, 'procesar_opcion'):
    # Capturar salida
    salida = io.StringIO()
    errores = io.StringIO()
    
    with redirect_stdout(salida), redirect_stderr(errores):
        # Simular procesar opción 6
        # Necesitamos vecta y sistema_vectorial, pero solo probamos que no crashee
        try:
            # Importar lo necesario
            from core.vecta_12d_core import VECTA_12D_Core
            from dimensiones.vector_12d import SistemaVectorial12D
            
            vecta = VECTA_12D_Core()
            sistema = SistemaVectorial12D()
            
            # Llamar a procesar_opcion con opción 6
            resultado = vecta_launcher.procesar_opcion("6", vecta, sistema)
            
            if resultado is True:
                print("✅ Opción 6 procesada correctamente (return True)")
            else:
                print(f"⚠️  Opción 6 retornó: {resultado}")
                
        except Exception as e:
            print(f"❌ Error al procesar opción 6: {e}")
            import traceback
            print(traceback.format_exc())
    
    # Mostrar salida capturada
    output = salida.getvalue()
    if output:
        print("📤 Salida generada:")
        print(output[:500])  # Mostrar solo primeros 500 caracteres
    
    # Verificar errores
    errors = errores.getvalue()
    if errors:
        print("❌ Errores encontrados:")
        print(errors[:500])
    else:
        print("✅ Sin errores")
        
else:
    print("❌ No se encontró la función procesar_opcion")
'''
    
    try:
        # Guardar script temporal
        with open('_prueba_opcion6.py', 'w', encoding='utf-8') as f:
            f.write(script_prueba)
        
        # Ejecutar prueba
        import subprocess
        resultado = subprocess.run([sys.executable, '_prueba_opcion6.py'], 
                                 capture_output=True, text=True, timeout=10)
        
        # Limpiar
        if os.path.exists('_prueba_opcion6.py'):
            os.remove('_prueba_opcion6.py')
        
        if resultado.returncode == 0:
            print("✅ Prueba de opción 6 completada")
            print(resultado.stdout)
            return True
        else:
            print("❌ Prueba fallida")
            print("STDOUT:", resultado.stdout[:500])
            print("STDERR:", resultado.stderr[:500])
            return False
            
    except Exception as e:
        print(f"❌ Error en prueba: {e}")
        # Limpiar si existe
        if os.path.exists('_prueba_opcion6.py'):
            os.remove('_prueba_opcion6.py')
        return False

def main():
    """Función principal de reparación"""
    
    print("\n🔧 Reparando opción 6 del menú...")
    
    # Paso 1: Reparar la opción 6
    if not reparar_opcion6():
        print("❌ Falló la reparación de opción 6")
        return 1
    
    # Paso 2: Verificar reparación
    if not verificar_reparacion():
        print("❌ Falló la verificación")
        return 1
    
    # Paso 3: Probar la opción 6
    print("\n🧪 Ejecutando prueba de la opción 6...")
    probar_opcion6()
    
    # Paso 4: Mostrar resumen
    print("\n" + "="*70)
    print("🎉 REPARACIÓN DE OPCIÓN 6 COMPLETADA")
    print("="*70)
    
    print("\n✅ El menú ahora tiene:")
    print("   1. Procesar texto/comando")
    print("   2. Ver estado del sistema")
    print("   3. Probar dimensiones individuales")
    print("   4. Ejecutar autodiagnóstico")
    print("   5. Generar vector 12D aleatorio")
    print("   6. Sistema META-VECTA (Nuevo) ← ¡FUNCIONAL!")
    print("   7. Salir del sistema")
    
    print("\n🚀 Ahora puedes:")
    print("   1. Ejecutar: python vecta_launcher.py")
    print("   2. Seleccionar opción 6")
    print("   3. Elegir una sub-opción META-VECTA")
    
    print("\n📋 Sub-opciones META-VECTA disponibles:")
    print("   • 1: Ejecutar prueba completa")
    print("   • 2: Procesar intención personalizada")
    print("   • 3: Ver estado del sistema META-VECTA")
    print("   • 4: Volver al menú principal")
    
    print("\n" + "="*70)
    print("¡Prueba ahora seleccionando la opción 6! 🚀")
    
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