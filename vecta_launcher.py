#!/usr/bin/env python3
"""
VECTA 12D LAUNCHER - Sistema Autoprogramable Filosofico
============================================
Lanzador principal del sistema de 12 dimensiones vectoriales.
"""

import sys
import os
import traceback
from datetime import datetime
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

def mostrar_banner():
    print("=" * 70)
    print("VECTA 12D - SISTEMA AUTOPROGRAMABLE")
    print("12 Dimensiones Vectoriales Filosoficas")
    print("=" * 70)
    print(f"Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Directorio: {BASE_DIR}")
    print("=" * 70)

def inicializar_sistema():
    print("[1/3] INICIALIZANDO SISTEMA VECTA 12D FILOSOFICO...")
    
    directorios_necesarios = ['core', 'dimensiones', 'chat_data']
    for dir_name in directorios_necesarios:
        if not os.path.exists(dir_name):
            print(f"ERROR: Directorio '{dir_name}' no encontrado")
            crear = input(f"Crear directorio '{dir_name}'? (s/n): ")
            if crear.lower() == 's':
                os.makedirs(dir_name, exist_ok=True)
                print(f"Directorio '{dir_name}' creado")
            else:
                return None
        print(f"Directorio '{dir_name}' encontrado")
    
    archivos_criticos = [
        'core/vecta_12d_core.py',
        'core/meta_vecta.py',
        'dimensiones/vector_12d.py',
        'dimensiones/dimension_base.py'
    ]
    
    for archivo in archivos_criticos:
        ruta_archivo = os.path.join(BASE_DIR, archivo)
        if not os.path.exists(ruta_archivo):
            print(f"ERROR: Archivo critico '{archivo}' no encontrado")
            return None
        print(f"Archivo critico '{archivo}' encontrado")
    
    try:
        from dimensiones.vector_12d import SistemaVectorial12D
        sistema_vectorial = SistemaVectorial12D()
        estado = sistema_vectorial.get_estado_sistema()
        print(f"Sistema Vectorial 12D inicializado")
        print(f"  - Dimensiones activas: {estado['dimensiones_activas']}/12")
        print(f"  - Estado: {estado['estado']}")
        print(f"  - Version: {estado['version']}")
    except Exception as e:
        print(f"ERROR al inicializar Sistema Vectorial 12D: {e}")
        traceback.print_exc()
        return None
    
    try:
        from core.meta_vecta import MetaVECTA, VECTA12DIntegrator
        meta_vecta = MetaVECTA()
        print(f"META-VECTA inicializado (v{meta_vecta.version})")
        print(f"  - Principios activos: {len(meta_vecta.principles)}")
        print(f"  - Creador: {meta_vecta.creator}")
        
        integrador = VECTA12DIntegrator(meta_vecta, sistema_vectorial)
        print("Integrador VECTA 12D Filosofico creado")
        
        print("[2/3] DIAGNOSTICO INICIAL DEL SISTEMA...")
        contexto_prueba = {
            "texto": "Sistema VECTA 12D inicializado correctamente",
            "metadata": {
                "tipo": "inicializacion",
                "timestamp": time.time(),
                "version": "filosofico_1.0"
            }
        }
        
        vector_inicial = sistema_vectorial.procesar_contexto(contexto_prueba)
        analisis = sistema_vectorial.analisis_profundo(vector_inicial)
        
        print(f"  - Estado vectorial: {vector_inicial.estado.value}")
        print(f"  - Magnitud filosofica: {vector_inicial.calcular_magnitud():.3f}")
        print(f"  - Equilibrio: {vector_inicial.calcular_equilibrio():.3f}")
        print(f"  - Arquetipo: {analisis['diagnostico_filosofico']['arquetipo_sistemico']}")
        
    except Exception as e:
        print(f"ERROR al inicializar META-VECTA: {e}")
        traceback.print_exc()
        return None
    
    print("[3/3] SISTEMA VECTA 12D INICIALIZADO CORRECTAMENTE")
    print("=" * 70)
    
    return {
        'vectorial': sistema_vectorial,
        'meta': meta_vecta,
        'integrator': integrador,
        'analisis_inicial': analisis
    }

def modo_interactivo(sistema):
    print("MODO INTERACTIVO VECTA 12D")
    print("Comandos: texto, analizar, estado, salir")
    print("-" * 50)
    
    while True:
        try:
            comando = input("VECTA> ").strip()
            
            if not comando:
                continue
                
            if comando.lower() == 'salir':
                print("Saliendo del sistema...")
                break
                
            elif comando.lower() == 'estado':
                estado = sistema['vectorial'].get_estado_sistema()
                print(f"Estado del sistema: {estado['estado']}")
                print(f"Dimensiones activas: {estado['dimensiones_activas']}/12")
                print(f"Tiempo operacion: {estado['tiempo_operacion']:.1f}s")
                
            elif comando.lower() == 'analizar':
                texto = input("Ingrese texto para analizar: ").strip()
                if texto:
                    contexto = {
                        "texto": texto,
                        "metadata": {
                            "tipo": "analisis_interactivo",
                            "timestamp": time.time()
                        }
                    }
                    vector = sistema['vectorial'].procesar_contexto(contexto)
                    analisis = sistema['vectorial'].analisis_profundo(vector)
                    
                    print("RESULTADOS DEL ANALISIS:")
                    print(f"Estado: {vector.estado.value}")
                    print(f"Magnitud: {vector.calcular_magnitud():.3f}")
                    print(f"Coherencia: {vector.calcular_coherencia():.3f}")
                    print(f"Dimension dominante: {analisis['diagnostico_filosofico']['nombre_dimension_dominante']}")
                    print(f"Arquetipo: {analisis['diagnostico_filosofico']['arquetipo_sistemico']}")
                    
                    recomendaciones = analisis['recomendaciones_evolutivas']
                    if recomendaciones:
                        print("Recomendaciones:")
                        for rec in recomendaciones:
                            print(f"  [{rec['prioridad'].upper()}] {rec['accion']}")
                else:
                    print("Error: texto vacio")
                    
            elif comando.lower().startswith('texto '):
                texto = comando[6:].strip()
                if texto:
                    contexto = {
                        "texto": texto,
                        "metadata": {
                            "tipo": "comando_directo",
                            "timestamp": time.time()
                        }
                    }
                    vector = sistema['vectorial'].procesar_contexto(contexto)
                    print(f"Procesado. Valor dimensional dominante: {vector.valores[0]:.3f}")
                else:
                    print("Error: texto vacio")
                    
            else:
                print("Comando no reconocido. Comandos: texto, analizar, estado, salir")
                
        except KeyboardInterrupt:
            print("\nInterrumpido por usuario")
            break
        except Exception as e:
            print(f"Error: {e}")

def main():
    mostrar_banner()
    
    sistema = inicializar_sistema()
    if not sistema:
        print("ERROR: No se pudo inicializar el sistema")
        sys.exit(1)
    
    modo_interactivo(sistema)
    
    print("Sistema VECTA 12D finalizado correctamente")

if __name__ == "__main__":
    main()
