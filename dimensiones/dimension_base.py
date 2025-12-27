"""
CLASE BASE PARA DIMENSIONES VECTORIALES VECTA 12D
Implementacion filosofica segun Rafael Porley
"""

import time
import math
import numpy as np
import sys
import os
from typing import Dict, Any, List, Tuple
from dataclasses import dataclass
from enum import Enum

class EstadoDimension(Enum):
    ACTIVA = "activa"
    INACTIVA = "inactiva"
    SATURADA = "saturada"
    RESONANDO = "resonando"

@dataclass
class ResultadoDimension:
    valor: float
    confianza: float
    componentes: Dict[str, float]
    estado: EstadoDimension
    timestamp: float
    
class DimensionBase:
    """Clase base abstracta para todas las dimensiones VECTA"""
    
    def __init__(self, numero: int, nombre: str, descripcion: str):
        self.numero = numero
        self.nombre = nombre
        self.descripcion = descripcion
        self.peso_base = 0.0833
        self.peso_actual = self.peso_base
        self.estado = EstadoDimension.ACTIVA
        self.historial = []
        self.umbral_saturacion = 0.85
        self.tiempo_resonancia = 0.0
        self.creacion = time.time()
        
        self.filosofia = {
            "concepto_central": "",
            "principio_operativo": "",
            "relaciones_interdimensionales": [],
            "polaridad": (0.0, 0.0)
        }
        
    def procesar(self, contexto: Dict[str, Any]) -> ResultadoDimension:
        raise NotImplementedError("Cada dimension debe implementar este metodo")
    
    def _aplicar_filtro_filosofico(self, valor_crudo: float, contexto: Dict[str, Any]) -> float:
        valor = max(-1.0, min(1.0, valor_crudo))
        
        if self.estado == EstadoDimension.RESONANDO:
            ciclo = math.sin(self.tiempo_resonancia * math.pi * 2) * 0.3
            valor += ciclo
            self.tiempo_resonancia += 0.1
        
        if abs(valor) > self.umbral_saturacion:
            factor_saturacion = 1.0 - (abs(valor) - self.umbral_saturacion) / (1.0 - self.umbral_saturacion)
            valor *= factor_saturacion
            self.estado = EstadoDimension.SATURADA
        
        return valor
    
    def _calcular_confianza(self, valor: float, consistencia: float = 0.5) -> float:
        if abs(valor) < 0.3:
            conf_base = 0.5 + abs(valor) * 0.5
        else:
            conf_base = 0.8
            
        if len(self.historial) > 0:
            valores_previos = [h.valor for h in self.historial[-5:]]
            varianza = np.var(valores_previos) if len(valores_previos) > 1 else 0.0
            ajuste_consistencia = 1.0 - min(1.0, varianza * 2)
            conf_base *= (0.3 + ajuste_consistencia * 0.7)
        
        return min(0.99, max(0.01, conf_base))
    
    def registrar_resultado(self, resultado: ResultadoDimension):
        self.historial.append(resultado)
        if len(self.historial) > 1000:
            self.historial = self.historial[-1000:]
    
    def actualizar_peso(self, nuevo_peso: float, razon: str = ""):
        self.peso_actual = max(0.01, min(1.0, nuevo_peso))
        
    def activar_resonancia(self, frecuencia: float = 1.0):
        self.estado = EstadoDimension.RESONANDO
        self.tiempo_resonancia = frecuencia
        
    def get_estado_filosofico(self) -> Dict[str, Any]:
        return {
            "dimension": self.numero,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "estado": self.estado.value,
            "peso_actual": self.peso_actual,
            "historial_len": len(self.historial),
            "filosofia": self.filosofia,
            "creacion": self.creacion,
            "activa": self.estado != EstadoDimension.INACTIVA
        }
