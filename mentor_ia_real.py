#!/usr/bin/env python3
"""
MENTOR IA REAL para VECTA 12D
Analiza código REAL y sugiere mejoras REALES
"""

import ast
import os
import json
import subprocess
import difflib
from pathlib import Path
from datetime import datetime

class MentorIAReal:
    """IA que analiza código VECTA y sugiere mejoras reales"""
    
    def __init__(self, proyecto_path):
        self.proyecto = Path(proyecto_path)
        self.reportes_path = self.proyecto / "reportes_ia"
        self.reportes_path.mkdir(exist_ok=True)
        
        # Dimensiones por implementar (basado en tu filosofía VECTA)
        self.dimensiones_pendientes = [
            "4_temporalidad", "5_emergencia", "6_recursividad",
            "7_holismo", "8_singularidad", "9_metacognicion",
            "10_transcendencia", "11_universalidad", "12_autonomia"
        ]
        
        print(f"🤖 MENTOR IA REAL inicializado")
        print(f"📁 Proyecto: {self.proyecto}")
        print(f"🔍 Dimensiones pendientes: {len(self.dimensiones_pendientes)}")
    
    def analizar_estado_actual(self):
        """Analiza el código REAL de VECTA y devuelve mejoras concretas"""
        print("\n" + "="*60)
        print("🔍 ANALIZANDO CÓDIGO REAL DE VECTA...")
        print("="*60)
        
        mejoras = []
        
        # 1. Verificar qué dimensiones existen
        dim_path = self.proyecto / "dimensiones"
        dimensiones_existentes = []
        
        if dim_path.exists():
            for archivo in dim_path.glob("*.py"):
                dimensiones_existentes.append(archivo.stem)
        
        print(f"✅ Dimensiones encontradas: {len(dimensiones_existentes)}")
        print(f"   {', '.join(dimensiones_existentes[:3])}...")
        
        # 2. Sugerir dimensiones faltantes
        for dim in self.dimensiones_pendientes:
            if dim not in dimensiones_existentes:
                mejoras.append({
                    "tipo": "nueva_dimension",
                    "prioridad": "ALTA",
                    "dimension": dim,
                    "descripcion": f"Crear dimensión {dim}",
                    "codigo_sugerido": self._generar_esqueleto_dimension(dim),
                    "archivo_destino": f"dimensiones/{dim}.py"
                })
        
        # 3. Analizar complejidad del código
        core_path = self.proyecto / "core"
        if core_path.exists():
            for archivo in core_path.glob("*.py"):
                complejidad = self._analizar_complejidad(archivo)
                if complejidad["lineas"] > 200:
                    mejoras.append({
                        "tipo": "refactorizacion",
                        "prioridad": "MEDIA",
                        "archivo": str(archivo),
                        "descripcion": f"Archivo muy grande ({complejidad['lineas']} líneas)",
                        "sugerencia": "Considerar dividir en módulos más pequeños"
                    })
        
        # 4. Verificar dashboard
        dashboard_path = self.proyecto / "dashboard_vecta.html"
        if dashboard_path.exists():
            with open(dashboard_path, 'r', encoding='utf-8') as f:
                contenido = f.read()
                if "12 dimensiones" not in contenido:
                    mejoras.append({
                        "tipo": "ui_mejora",
                        "prioridad": "MEDIA",
                        "archivo": "dashboard_vecta.html",
                        "descripcion": "Dashboard no muestra 12 dimensiones",
                        "sugerencia": "Actualizar interfaz para mostrar todas las dimensiones"
                    })
        
        return mejoras
    
    def _generar_esqueleto_dimension(self, nombre_dim):
        """Genera código REAL para una nueva dimensión"""
        # Basado en las dimensiones existentes que ya tienes
        plantilla = f'''
"""
DIMENSIÓN: {nombre_dim.upper()}
{'='*50}
Fecha creación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Generada por: Mentor IA Real de VECTA 12D
"""

import numpy as np
from typing import List, Dict, Any

class Dimension{nombre_dim.capitalize()}:
    """Implementación de la dimensión {nombre_dim}"""
    
    def __init__(self):
        self.nombre = "{nombre_dim}"
        self.version = "1.0"
        self.descripcion = "Dimensión generada automáticamente por IA Mentor"
        self.parametros = {{}}
        
        print(f"✅ Dimensión {{self.nombre}} inicializada")
    
    def analizar(self, datos: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analiza datos según esta dimensión
        
        Args:
            datos: Diccionario con información a analizar
            
        Returns:
            Dict con resultados del análisis
        """
        resultados = {{
            "dimension": self.nombre,
            "timestamp": "{datetime.now().isoformat()}",
            "metrica_1": 0.0,
            "metrica_2": 0.0,
            "observaciones": "Dimensión en desarrollo - necesita implementación específica"
        }}
        
        # TODO: Implementar lógica específica de esta dimensión
        # Basarse en las dimensiones 1-3 existentes como referencia
        
        return resultados
    
    def validar(self, vector: List[float]) -> bool:
        """Valida si un vector cumple con esta dimensión"""
        if not vector:
            return False
        
        # Validación básica
        return all(isinstance(v, (int, float)) for v in vector)
    
    def exportar_config(self) -> Dict[str, Any]:
        """Exporta configuración de la dimensión"""
        return {{
            "nombre": self.nombre,
            "version": self.version,
            "estado": "generado_automaticamente",
            "fecha_creacion": "{datetime.now().isoformat()}",
            "completada": False,
            "pendiente_implementacion": True
        }}

# ============================================================================
# FUNCIÓN DE FÁBRICA (para integrar con VECTA)
# ============================================================================

def crear_dimension():
    """Función estándar para crear instancia de esta dimensión"""
    return Dimension{nombre_dim.capitalize()}()

# ============================================================================
# PRUEBA RÁPIDA
# ============================================================================

if __name__ == "__main__":
    print(f"🧪 Probando dimensión {{nombre_dim}}...")
    dim = crear_dimension()
    print(f"Nombre: {{dim.nombre}}")
    print(f"Descripción: {{dim.descripcion}}")
    
    # Prueba básica
    datos_prueba = {{"test": True}}
    resultado = dim.analizar(datos_prueba)
    print(f"Resultado: {{resultado}}")
'''
        return plantilla
    
    def _analizar_complejidad(self, archivo_path):
        """Analiza complejidad básica de un archivo Python"""
        try:
            with open(archivo_path, 'r', encoding='utf-8') as f:
                lineas = f.readlines()
            
            # Contar líneas, funciones, clases
            funciones = 0
            clases = 0
            
            for linea in lineas:
                linea_limpia = linea.strip()
                if linea_limpia.startswith("def "):
                    funciones += 1
                elif linea_limpia.startswith("class "):
                    clases += 1
            
            return {
                "archivo": str(archivo_path.name),
                "lineas": len(lineas),
                "funciones": funciones,
                "clases": clases,
                "complejidad": "ALTA" if len(lineas) > 200 else "MEDIA" if len(lineas) > 100 else "BAJA"
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def generar_reporte_mejoras(self, mejoras):
        """Genera reporte con mejoras sugeridas"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        reporte_path = self.reportes_path / f"mejoras_sugeridas_{timestamp}.json"
        
        reporte = {
            "fecha_generacion": datetime.now().isoformat(),
            "total_mejoras": len(mejoras),
            "mejoras_prioridad_alta": len([m for m in mejoras if m["prioridad"] == "ALTA"]),
            "mejoras_prioridad_media": len([m for m in mejoras if m["prioridad"] == "MEDIA"]),
            "mejoras_detalladas": mejoras
        }
        
        with open(reporte_path, 'w', encoding='utf-8') as f:
            json.dump(reporte, f, indent=2, ensure_ascii=False)
        
        # También generar versión legible
        txt_path = self.reportes_path / f"mejoras_sugeridas_{timestamp}.txt"
        self._generar_reporte_texto(mejoras, txt_path)
        
        return reporte_path
    
    def _generar_reporte_texto(self, mejoras, output_path):
        """Genera reporte en texto legible"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("           REPORTE DE MEJORAS SUGERIDAS POR IA MENTOR\n")
            f.write("="*70 + "\n\n")
            f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total mejoras sugeridas: {len(mejoras)}\n\n")
            
            for i, mejora in enumerate(mejoras, 1):
                f.write(f"[{i}] {'='*50}\n")
                f.write(f"TIPO: {mejora['tipo'].upper()}\n")
                f.write(f"PRIORIDAD: {mejora['prioridad']}\n")
                f.write(f"DESCRIPCIÓN: {mejora['descripcion']}\n")
                
                if 'archivo' in mejora:
                    f.write(f"ARCHIVO: {mejora['archivo']}\n")
                
                if 'archivo_destino' in mejora:
                    f.write(f"ARCHIVO DESTINO: {mejora['archivo_destino']}\n")
                
                if 'sugerencia' in mejora:
                    f.write(f"SUGERENCIA: {mejora['sugerencia']}\n")
                
                f.write("\n")
    
    def aplicar_mejora(self, mejora, confirmar=True):
        """Aplica una mejora sugerida al código REAL"""
        
        print(f"\n{'='*60}")
        print(f"⚡ APLICANDO MEJORA: {mejora['descripcion']}")
        print(f"{'='*60}")
        
        if mejora["tipo"] == "nueva_dimension":
            return self._crear_nueva_dimension(mejora, confirmar)
        
        elif mejora["tipo"] == "refactorizacion":
            print(f"⚠️  Refactorización necesita implementación manual")
            print(f"   Archivo: {mejora.get('archivo', 'N/A')}")
            print(f"   Sugerencia: {mejora.get('sugerencia', 'N/A')}")
            return False
        
        elif mejora["tipo"] == "ui_mejora":
            print(f"⚠️  Mejora de UI necesita implementación manual")
            return False
        
        else:
            print(f"❌ Tipo de mejora no soportado: {mejora['tipo']}")
            return False
    
    def _crear_nueva_dimension(self, mejora, confirmar):
        """Crea una nueva dimensión REAL"""
        archivo_destino = self.proyecto / mejora["archivo_destino"]
        
        # Verificar si ya existe
        if archivo_destino.exists():
            print(f"⚠️  El archivo ya existe: {archivo_destino}")
            return False
        
        # Mostrar preview del código
        print("\n📄 PREVIEW DEL CÓDIGO A GENERAR:")
        print("-"*40)
        codigo = mejora["codigo_sugerido"]
        lineas = codigo.split('\n')[:20]  # Mostrar primeras 20 líneas
        for linea in lineas:
            print(linea)
        
        if len(codigo.split('\n')) > 20:
            print("... [código continúa] ...")
        
        print("-"*40)
        
        # Confirmación
        if confirmar:
            respuesta = input("\n¿Crear esta dimensión? (s/n): ").strip().lower()
            if respuesta != 's':
                print("❌ Cancelado por usuario")
                return False
        
        # Crear directorio si no existe
        archivo_destino.parent.mkdir(exist_ok=True)
        
        # Guardar archivo
        try:
            with open(archivo_destino, 'w', encoding='utf-8') as f:
                f.write(codigo)
            
            print(f"✅ DIMENSIÓN CREADA: {archivo_destino}")
            print(f"   Líneas generadas: {len(codigo.split(chr(10)))}")
            
            # Registrar en historial
            self._registrar_implementacion(mejora)
            
            return True
            
        except Exception as e:
            print(f"❌ Error creando dimensión: {e}")
            return False
    
    def _registrar_implementacion(self, mejora):
        """Registra la implementación en historial"""
        historial_path = self.reportes_path / "historial_implementaciones.json"
        
        if historial_path.exists():
            with open(historial_path, 'r', encoding='utf-8') as f:
                historial = json.load(f)
        else:
            historial = []
        
        entrada = {
            "timestamp": datetime.now().isoformat(),
            "tipo": mejora["tipo"],
            "descripcion": mejora["descripcion"],
            "dimension": mejora.get("dimension", "N/A"),
            "archivo": mejora.get("archivo_destino", mejora.get("archivo", "N/A")),
            "estado": "completado"
        }
        
        historial.append(entrada)
        
        with open(historial_path, 'w', encoding='utf-8') as f:
            json.dump(historial, f, indent=2, ensure_ascii=False)
        
        print(f"📝 Implementación registrada en historial")

# ============================================================================
# INTERFAZ INTERACTIVA PARA NOVATOS
# ============================================================================

def menu_interactivo():
    """Menú interactivo para usar el Mentor IA"""
    
    print("\n" + "="*70)
    print("            MENTOR IA REAL - VECTA 12D")
    print("="*70)
    
    # Ruta automática (ajusta si es necesario)
    proyecto_path = Path.cwd()
    mentor = MentorIAReal(proyecto_path)
    
    while True:
        print("\n" + "-"*50)
        print("¿QUÉ QUIERES HACER?")
        print("1. 🔍 Analizar código VECTA (buscar mejoras)")
        print("2. 📊 Ver mejoras sugeridas anteriores")
        print("3. ⚡ Aplicar mejora automáticamente")
        print("4. 🚀 Crear nueva dimensión (guiado)")
        print("5. 📈 Ver progreso general")
        print("6. ❌ Salir")
        print("-"*50)
        
        opcion = input("\nElige (1-6): ").strip()
        
        if opcion == "1":
            print("\n🔍 Analizando código VECTA...")
            mejoras = mentor.analizar_estado_actual()
            
            if mejoras:
                reporte_path = mentor.generar_reporte_mejoras(mejoras)
                print(f"\n✅ Análisis completado!")
                print(f"📁 Reporte guardado en: {reporte_path}")
                
                # Mostrar resumen
                alta = len([m for m in mejoras if m["prioridad"] == "ALTA"])
                media = len([m for m in mejoras if m["prioridad"] == "MEDIA"])
                
                print(f"\n📊 RESUMEN:")
                print(f"   • Mejoras PRIORIDAD ALTA: {alta}")
                print(f"   • Mejoras PRIORIDAD MEDIA: {media}")
                print(f"   • Total sugerencias: {len(mejoras)}")
                
                # Mostrar algunas sugerencias
                print(f"\n🎯 SUGERENCIAS DESTACADAS:")
                for i, mejora in enumerate(mejoras[:3], 1):
                    if mejora["tipo"] == "nueva_dimension":
                        print(f"   {i}. [NUEVA DIMENSIÓN] {mejora['dimension']}")
            else:
                print("🎉 ¡VECTA ya está optimizado! No se encontraron mejoras urgentes.")
        
        elif opcion == "2":
            # Mostrar reportes anteriores
            reportes = list(mentor.reportes_path.glob("mejoras_sugeridas_*.txt"))
            if reportes:
                print("\n📜 REPORTES ANTERIORES:")
                for i, reporte in enumerate(sorted(reportes, reverse=True)[:5], 1):
                    fecha = reporte.stem.replace("mejoras_sugeridas_", "")
                    fecha_formato = f"{fecha[0:4]}-{fecha[4:6]}-{fecha[6:8]} {fecha[9:11]}:{fecha[11:13]}"
                    print(f"   {i}. {fecha_formato} - {reporte.name}")
                
                ver = input("\n¿Ver el último reporte? (s/n): ").strip().lower()
                if ver == 's':
                    ultimo = sorted(reportes, reverse=True)[0]
                    with open(ultimo, 'r', encoding='utf-8') as f:
                        print("\n" + f.read())
            else:
                print("❌ No hay reportes anteriores. Ejecuta primero 'Analizar código'")
        
        elif opcion == "3":
            print("\n⚠️  Primero debes analizar el código (opción 1)")
            print("   Luego podrás aplicar mejoras específicas.")
        
        elif opcion == "4":
            print("\n🚀 CREACIÓN GUIADA DE NUEVA DIMENSIÓN")
            print("-"*40)
            
            # Mostrar dimensiones pendientes
            print("\nDimensiones pendientes de implementar:")
            for i, dim in enumerate(mentor.dimensiones_pendientes, 1):
                print(f"   {i}. {dim}")
            
            try:
                seleccion = input("\n¿Qué dimensión quieres crear? (número o nombre): ").strip()
                
                if seleccion.isdigit():
                    idx = int(seleccion) - 1
                    if 0 <= idx < len(mentor.dimensiones_pendientes):
                        dim_seleccionada = mentor.dimensiones_pendientes[idx]
                    else:
                        print("❌ Número inválido")
                        continue
                else:
                    dim_seleccionada = seleccion
                
                # Crear mejora para esta dimensión
                mejora = {
                    "tipo": "nueva_dimension",
                    "prioridad": "ALTA",
                    "dimension": dim_seleccionada,
                    "descripcion": f"Crear dimensión {dim_seleccionada}",
                    "codigo_sugerido": mentor._generar_esqueleto_dimension(dim_seleccionada),
                    "archivo_destino": f"dimensiones/{dim_seleccionada}.py"
                }
                
                # Aplicar
                if mentor.aplicar_mejora(mejora, confirmar=True):
                    print(f"\n🎉 ¡DIMENSIÓN {dim_seleccionada.upper()} CREADA!")
                    print("   Ahora puedes personalizarla según tus necesidades filosóficas.")
                    
            except Exception as e:
                print(f"❌ Error: {e}")
        
        elif opcion == "5":
            print("\n📈 PROGRESO GENERAL DE VECTA 12D")
            print("-"*40)
            
            # Contar dimensiones existentes
            dim_path = proyecto_path / "dimensiones"
            if dim_path.exists():
                dimensiones_existentes = len(list(dim_path.glob("*.py")))
            else:
                dimensiones_existentes = 0
            
            print(f"\n📊 ESTADO ACTUAL:")
            print(f"   • Dimensiones implementadas: {dimensiones_existentes}/12")
            print(f"   • Porcentaje completado: {(dimensiones_existentes/12)*100:.1f}%")
            print(f"   • Pendientes: {12 - dimensiones_existentes}")
            
            if dimensiones_existentes < 12:
                print(f"\n🎯 SIGUIENTES PASOS SUGERIDOS:")
                print(f"   1. Ejecuta 'Analizar código' (opción 1)")
                print(f"   2. Crea las dimensiones faltantes (opción 4)")
                print(f"   3. Personaliza cada dimensión con tu filosofía")
            else:
                print("\n🎉 ¡VECTA 12D COMPLETADO!")
                print("   Todas las dimensiones están implementadas.")
        
        elif opcion == "6":
            print("\n👋 ¡Hasta luego! Recuerda:")
            print("   • VECTA crece con cada mejora que aplicas")
            print("   • El Mentor IA está aquí para sugerir, tú decides")
            print("   • ¡La autoprogramación REAL ha comenzado!")
            break
        
        else:
            print("❌ Opción no válida. Usa 1-6.")

# ============================================================================
# EJECUCIÓN PRINCIPAL
# ============================================================================

if __name__ == "__main__":
    try:
        menu_interactivo()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrumpido por usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        print("   Por favor, reporta este error para mejorar el Mentor IA")