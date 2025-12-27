#!/usr/bin/env python3
"""
SCRIPT DE PRUEBA DEL SISTEMA VECTA 12D FILOSOFICO
"""

import sys
import os
import json
from datetime import datetime
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def probar_dimensiones():
    print("PROBANDO SISTEMA VECTA 12D FILOSOFICO")
    print("=" * 60)
    
    from dimensiones.vector_12d import SistemaVectorial12D
    
    sistema = SistemaVectorial12D()
    
    contextos = [
        {
            "nombre": "Decision Etica Clara",
            "texto": "Debo ayudar a esta persona porque es lo correcto. Mi proposito es claro y mi intencion es pura.",
            "metadata": {
                "tipo": "decision_etica",
                "fuerza_voluntad": 0.8,
                "claridad": 0.9,
                "objetivos": ["ayudar", "hacer lo correcto"]
            }
        },
        {
            "nombre": "Dilema Complejo",
            "texto": "No estoy seguro que hacer. Por un lado quiero ayudar, pero por otro debo considerar las consecuencias.",
            "metadata": {
                "tipo": "dilema",
                "fuerza_voluntad": 0.3,
                "claridad": 0.2,
                "contradicciones": ["ayudar vs consecuencias"]
            }
        },
        {
            "nombre": "Vision Holistica",
            "texto": "Todo esta conectado. Cada accion afecta al sistema completo. Debemos considerar todos los aspectos.",
            "metadata": {
                "tipo": "vision_holistica",
                "enfoque_sistemico": 0.9,
                "complejidad": 0.7,
                "interconexiones": ["todo", "sistema", "aspectos"]
            }
        }
    ]
    
    for contexto in contextos:
        print(f"Contexto: {contexto['nombre']}")
        print(f"  Texto: {contexto['texto'][:80]}...")
        
        vector = sistema.procesar_contexto(contexto)
        analisis = sistema.analisis_profundo(vector)
        
        print(f"  Resultados:")
        print(f"  - Estado: {vector.estado.value}")
        print(f"  - Magnitud: {vector.calcular_magnitud():.3f}")
        print(f"  - Equilibrio: {vector.calcular_equilibrio():.3f}")
        print(f"  - Coherencia: {vector.calcular_coherencia():.3f}")
        
        print(f"  Arquetipo: {analisis['diagnostico_filosofico']['arquetipo_sistemico']}")
        
        print(f"  Dimensiones destacadas:")
        valores = vector.valores
        for i in range(3):
            idx = sorted(range(len(valores)), key=lambda k: abs(valores[k]), reverse=True)[i]
            nombre_dim = sistema.dimensiones[idx].nombre if idx < len(sistema.dimensiones) else f"Dimension {idx+1}"
            print(f"    {i+1}. {nombre_dim}: {valores[idx]:.3f}")
        print()
    
    print("=" * 60)
    print("PRUEBA COMPLETADA")
    
    reporte = {
        "fecha": datetime.now().isoformat(),
        "sistema": sistema.get_estado_sistema(),
        "pruebas": len(contextos),
        "estado": "exitoso"
    }
    
    with open("prueba_filosofica.json", "w", encoding="utf-8") as f:
        json.dump(reporte, f, indent=2, ensure_ascii=False)
    
    print("Reporte guardado en: prueba_filosofica.json")

if __name__ == "__main__":
    probar_dimensiones()
