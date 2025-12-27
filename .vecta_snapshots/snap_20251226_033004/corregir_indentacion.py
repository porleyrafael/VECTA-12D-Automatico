#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CORRECTOR AUTOMÁTICO DE INDENTACIÓN
====================================
Corrige automáticamente el error de indentación en auto_implementar_vecta.py
"""

import os
import sys

def corregir_auto_implementar():
    """Corrige el error de indentación en auto_implementar_vecta.py"""
    
    archivo = "auto_implementar_vecta.py"
    
    if not os.path.exists(archivo):
        print(f"❌ Error: No se encuentra el archivo {archivo}")
        return False
    
    print(f"📖 Leyendo archivo: {archivo}")
    
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            lineas = f.readlines()
    except UnicodeDecodeError:
        with open(archivo, 'r', encoding='latin-1') as f:
            lineas = f.readlines()
    
    total_lineas = len(lineas)
    print(f"📊 Total de líneas: {total_lineas}")
    
    # Buscar el método create_vecta_ai_chat
    encontrado = False
    inicio_metodo = -1
    fin_metodo = -1
    nivel_indentacion = 0
    
    for i, linea in enumerate(lineas):
        if 'def create_vecta_ai_chat(self):' in linea:
            inicio_metodo = i
            # Calcular nivel de indentación del método
            nivel_indentacion = len(linea) - len(linea.lstrip())
            print(f"✅ Encontrado método en línea {i+1}")
            print(f"   Nivel de indentación: {nivel_indentacion} espacios")
            encontrado = True
        
        # Buscar la línea problemática
        if 'file_path = self.base_dir / "vecta_ai_chat.py"' in linea and encontrado:
            print(f"🔧 Línea problemática encontrada: {i+1}")
            print(f"   Contenido: {linea.rstrip()}")
            
            # Calcular indentación actual
            indent_actual = len(linea) - len(linea.lstrip())
            indent_esperado = nivel_indentacion + 4  # 4 espacios adicionales dentro del método
            
            if indent_actual != indent_esperado:
                print(f"   Problema: Indentación actual={indent_actual}, esperada={indent_esperado}")
                
                # Corregir la indentación
                nueva_linea = ' ' * indent_esperado + linea.lstrip()
                lineas[i] = nueva_linea
                print(f"   ✅ Corregido a: {nueva_linea.rstrip()}")
                
                # Guardar cambios
                with open(archivo, 'w', encoding='utf-8') as f:
                    f.writelines(lineas)
                
                print(f"\n✅ Archivo corregido exitosamente!")
                print(f"   Línea {i+1} ajustada a {indent_esperado} espacios de indentación")
                return True
            else:
                print(f"   ✅ La línea ya tiene la indentación correcta ({indent_actual} espacios)")
                return True
    
    if not encontrado:
        print("❌ No se encontró el método 'create_vecta_ai_chat'")
        return False
    
    # Si llegamos aquí, no encontramos la línea específica pero podemos verificar el archivo
    print("\n⚠️ No se encontró la línea específica, pero verifiquemos la estructura...")
    
    # Buscar problemas de indentación generales cerca del método
    if inicio_metodo != -1:
        print(f"\n📋 Analizando estructura del método (líneas {inicio_metodo+1}-{min(inicio_metodo+50, total_lineas)})...")
        
        cambios = 0
        en_metodo = False
        nivel_actual = 0
        
        for i in range(inicio_metodo, min(inicio_metodo + 100, total_lineas)):
            linea = lineas[i]
            
            if 'def ' in linea and i != inicio_metodo:
                # Nuevo método, terminar análisis
                break
            
            if i == inicio_metodo:
                en_metodo = True
                continue
            
            if en_metodo and linea.strip():
                # Calcular indentación esperada para líneas dentro del método
                if linea.strip().startswith("'''") or linea.strip().startswith('"""'):
                    # Es una cadena multilínea, mantener igual
                    pass
                else:
                    indent_actual = len(linea) - len(linea.lstrip())
                    
                    # Dentro del método, mínimo 4 espacios adicionales
                    if indent_actual > 0 and indent_actual < nivel_indentacion + 4:
                        print(f"   ⚠️ Línea {i+1}: Indentación insuficiente ({indent_actual})")
                        nueva_indent = nivel_indentacion + 4
                        lineas[i] = ' ' * nueva_indent + linea.lstrip()
                        cambios += 1
                        print(f"     Corregido a {nueva_indent} espacios")
        
        if cambios > 0:
            with open(archivo, 'w', encoding='utf-8') as f:
                f.writelines(lineas)
            print(f"\n✅ Realizados {cambios} correcciones de indentación")
            return True
        else:
            print("✅ No se encontraron problemas de indentación obvios")
    
    return False

def verificar_sintaxis():
    """Verifica si el archivo tiene errores de sintaxis después de la corrección"""
    
    print("\n🔍 Verificando sintaxis del archivo...")
    
    try:
        # Intenta compilar el archivo
        with open("auto_implementar_vecta.py", 'r', encoding='utf-8') as f:
            codigo = f.read()
        
        compile(codigo, "auto_implementar_vecta.py", 'exec')
        print("✅ Archivo compila correctamente (sin errores de sintaxis)")
        return True
    except SyntaxError as e:
        print(f"❌ Error de sintaxis encontrado:")
        print(f"   Línea {e.lineno}: {e.msg}")
        print(f"   Texto: {e.text}")
        return False
    except Exception as e:
        print(f"⚠️ Error inesperado: {e}")
        return False

def crear_backup():
    """Crea un backup del archivo original"""
    
    archivo_original = "auto_implementar_vecta.py"
    archivo_backup = "auto_implementar_vecta_backup.py"
    
    if os.path.exists(archivo_original):
        import shutil
        shutil.copy2(archivo_original, archivo_backup)
        print(f"📦 Backup creado: {archivo_backup}")
        return True
    return False

def main():
    """Función principal"""
    
    print("=" * 60)
    print("CORRECTOR AUTOMÁTICO DE INDENTACIÓN")
    print("=" * 60)
    
    # Crear backup primero
    print("\n1️⃣ Creando backup del archivo original...")
    crear_backup()
    
    # Corregir indentación
    print("\n2️⃣ Corrigiendo indentación...")
    if corregir_auto_implementar():
        print("\n✅ Corrección completada")
    else:
        print("\n⚠️ No se pudo corregir automáticamente")
        print("   Puede que necesites editar manualmente el archivo")
    
    # Verificar sintaxis
    print("\n3️⃣ Verificando sintaxis...")
    verificar_sintaxis()
    
    print("\n" + "=" * 60)
    print("INSTRUCCIONES FINALES:")
    print("=" * 60)
    print("1. Ejecuta de nuevo: python auto_implementar_vecta.py")
    print("2. Si sigue habiendo errores, edita manualmente:")
    print("   - Busca 'def create_vecta_ai_chat(self):'")
    print("   - Asegúrate que 'file_path = ...' esté indentado con 8 espacios")
    print("   (4 espacios para el método + 4 espacios para el cuerpo)")
    print("3. El backup está en: auto_implementar_vecta_backup.py")
    print("=" * 60)

if __name__ == "__main__":
    main()