"""
SISTEMA VECTORIAL 12D - Implementacion completa filosofica
Basado en los conceptos de Rafael Porley
"""

import importlib
import sys
import os
import time
import math
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

class EstadoVector(Enum):
    ESTABLE = "estable"
    OSCILANTE = "oscilante"
    CAOTICO = "caotico"
    RESONANTE = "resonante"
    EMERGENTE = "emergente"

@dataclass
class Vector12D:
    valores: List[float] = field(default_factory=lambda: [0.0] * 12)
    confianzas: List[float] = field(default_factory=lambda: [0.0] * 12)
    pesos: List[float] = field(default_factory=lambda: [0.0833] * 12)
    timestamp: float = field(default_factory=time.time)
    estado: EstadoVector = EstadoVector.ESTABLE
    
    def __post_init__(self):
        if len(self.valores) != 12:
            self.valores = self.valores[:12] + [0.0] * (12 - len(self.valores))
        if len(self.confianzas) != 12:
            self.confianzas = self.confianzas[:12] + [0.0] * (12 - len(self.confianzas))
        
        self._calcular_estado()
    
    def _calcular_estado(self):
        if len(self.valores) > 1:
            varianza = np.var(self.valores)
        else:
            varianza = 0.0
        
        if varianza < 0.05:
            self.estado = EstadoVector.ESTABLE
        elif varianza < 0.2:
            self.estado = EstadoVector.OSCILANTE
        elif varianza < 0.5:
            if self._tiene_resonancia():
                self.estado = EstadoVector.RESONANTE
            else:
                self.estado = EstadoVector.CAOTICO
        else:
            self.estado = EstadoVector.EMERGENTE
    
    def _tiene_resonancia(self) -> bool:
        valores_abs = [abs(v) for v in self.valores]
        if len(valores_abs) < 2:
            return False
            
        for i in range(len(valores_abs)):
            for j in range(i + 1, len(valores_abs)):
                ratio = valores_abs[i] / valores_abs[j] if valores_abs[j] != 0 else 0
                if 0.49 < ratio < 0.51 or 0.66 < ratio < 0.67 or 0.74 < ratio < 0.76:
                    return True
        return False
    
    def calcular_magnitud(self) -> float:
        suma_cuadrados = 0.0
        for i, (valor, confianza) in enumerate(zip(self.valores, self.confianzas)):
            peso_confianza = confianza * self.pesos[i]
            suma_cuadrados += (valor * peso_confianza) ** 2
        
        return math.sqrt(suma_cuadrados) if suma_cuadrados > 0 else 0.0
    
    def normalizar_filosoficamente(self) -> 'Vector12D':
        magnitud = self.calcular_magnitud()
        
        if magnitud > 0:
            factor = 1.0 / magnitud
            valores_normalizados = [v * factor for v in self.valores]
            
            for i in range(len(valores_normalizados)):
                if abs(valores_normalizados[i]) < 0.01 and abs(self.valores[i]) > 0.01:
                    valores_normalizados[i] = 0.01 if self.valores[i] > 0 else -0.01
            
            self.valores = valores_normalizados
        
        return self
    
    def to_dict_filosofico(self) -> Dict[str, Any]:
        magnitud = self.calcular_magnitud()
        
        return {
            "dimensiones": [
                {
                    "indice": i + 1,
                    "valor": self.valores[i],
                    "confianza": self.confianzas[i],
                    "peso_filosofico": self.pesos[i],
                    "significado": self._interpretar_valor(i, self.valores[i])
                }
                for i in range(12)
            ],
            "propiedades_emergentes": {
                "magnitud": magnitud,
                "estado": self.estado.value,
                "coherencia": self.calcular_coherencia(),
                "equilibrio": self.calcular_equilibrio(),
                "potencial_evolutivo": self.calcular_potencial_evolutivo(),
                "timestamp": self.timestamp
            }
        }
    
    def _interpretar_valor(self, dimension: int, valor: float) -> str:
        rangos = [
            (0.8, 1.0, "Manifestacion Plena"),
            (0.6, 0.8, "Expresion Clara"),
            (0.4, 0.6, "Presencia Moderada"),
            (0.2, 0.4, "Incipiente"),
            (0.0, 0.2, "Latente"),
            (-0.2, 0.0, "Resistencia Leve"),
            (-0.4, -0.2, "Oposicion Moderada"),
            (-0.6, -0.4, "Conflicto"),
            (-0.8, -0.6, "Contradiccion Fuerte"),
            (-1.0, -0.8, "Antitesis Completa")
        ]
        
        for min_val, max_val, significado in rangos:
            if min_val <= valor <= max_val:
                return significado
        
        return "Indeterminado"
    
    def calcular_coherencia(self) -> float:
        if len(self.valores) < 2:
            return 1.0
        
        pares_sinergicos = [(0, 1), (1, 2), (3, 4), (5, 6), (7, 8), (9, 10)]
        pares_opuestos = [(0, 11), (2, 9), (4, 7)]
        
        coherencias = []
        
        for i, j in pares_sinergicos:
            if i < len(self.valores) and j < len(self.valores):
                correlacion = self.valores[i] * self.valores[j]
                coherencias.append(max(0.0, correlacion))
        
        for i, j in pares_opuestos:
            if i < len(self.valores) and j < len(self.valores):
                oposicion = -self.valores[i] * self.valores[j]
                coherencias.append(max(0.0, oposicion))
        
        return np.mean(coherencias) if coherencias else 0.5
    
    def calcular_equilibrio(self) -> float:
        valores_pos = [v for v in self.valores if v > 0]
        valores_neg = [v for v in self.valores if v < 0]
        
        if not valores_pos and not valores_neg:
            return 1.0
        
        suma_pos = sum(valores_pos)
        suma_neg = abs(sum(valores_neg))
        
        if suma_pos + suma_neg == 0:
            return 1.0
        
        equilibrio = 1.0 - (abs(suma_pos - suma_neg) / (suma_pos + suma_neg))
        return max(0.0, min(1.0, equilibrio))
    
    def calcular_potencial_evolutivo(self) -> float:
        asimetria = 1.0 - self.calcular_equilibrio()
        
        extremos = sum(1 for v in self.valores if abs(v) > 0.7)
        factor_extremos = extremos / len(self.valores)
        
        potencial = (asimetria * 0.4 + factor_extremos * 0.6)
        return max(0.0, min(1.0, potencial))

class SistemaVectorial12D:
    
    def __init__(self, ruta_dimensiones: str = None):
        self.dimensiones = []
        self.historico_vectores = []
        self.estado_sistema = "inicializando"
        self.inicializacion_time = time.time()
        
        self.pesos_filosoficos = [
            0.15, 0.12, 0.10, 0.08, 0.08, 0.08,
            0.07, 0.07, 0.06, 0.06, 0.06, 0.07
        ]
        
        self.cargar_dimensiones(ruta_dimensiones)
    
    def cargar_dimensiones(self, ruta: str = None):
        """Carga las dimensiones usando el cargador simplificado"""
        print("CARGANDO DIMENSIONES FILOSOFICAS VECTA 12D...")
        
        try:
            from dimensiones.cargador_simplificado import cargar_todas_dimensiones
            self.dimensiones = cargar_todas_dimensiones()
        except ImportError as e:
            print(f"Error al cargar cargador simplificado: {e}")
            # Cargar dimensiones básicas como fallback
            from dimensiones.dimension_base import DimensionBase
            self.dimensiones = []
            for i in range(1, 13):
                nombre = f"Dimensión {i}"
                if i == 1: nombre = "Intencionalidad Pura"
                elif i == 2: nombre = "Estructura Lógica"
                elif i == 3: nombre = "Contexto Sistémico"
                elif i == 4: nombre = "Temporalidad"
                elif i == 5: nombre = "Escala de Impacto"
                elif i == 6: nombre = "Complejidad Intrínseca"
                elif i == 7: nombre = "Evolución Potencial"
                elif i == 8: nombre = "Simetría/Asimetría"
                elif i == 9: nombre = "Información/Entropía"
                elif i == 10: nombre = "Consciencia Reflexiva"
                elif i == 11: nombre = "Integridad Ética"
                elif i == 12: nombre = "Unificación Holística"
                
                instancia = DimensionBase(i, nombre, f"Dimensión {i}: {nombre}")
                self.dimensiones.append(instancia)
                print(f"  Dimensión {i}: {nombre} - Básica")
        
        print(f"Sistema cargado con {len(self.dimensiones)}/12 dimensiones")
        self.estado_sistema = "activo"
    
    def procesar_contexto(self, contexto: Dict[str, Any]) -> Vector12D:
        inicio_proceso = time.time()
        
        if not contexto or ('texto' not in contexto and 'metadata' not in contexto):
            contexto = {"texto": "", "metadata": {}, "error": "contexto_vacio"}
        
        valores = []
        confianzas = []
        
        for i, dimension in enumerate(self.dimensiones):
            try:
                resultado = dimension.procesar(contexto)
                valores.append(resultado.valor)
                confianzas.append(resultado.confianza)
                
            except Exception as e:
                print(f"Error procesando dimension {i+1}: {e}")
                valores.append(0.0)
                confianzas.append(0.1)
        
        vector = Vector12D(
            valores=valores,
            confianzas=confianzas,
            pesos=self.pesos_filosoficos[:len(valores)]
        )
        
        vector.normalizar_filosoficamente()
        
        self.historico_vectores.append({
            "vector": vector.to_dict_filosofico(),
            "contexto": {k: v for k, v in contexto.items() if k != 'metadata'},
            "timestamp": inicio_proceso,
            "tiempo_procesamiento": time.time() - inicio_proceso
        })
        
        if len(self.historico_vectores) > 100:
            self.historico_vectores = self.historico_vectores[-100:]
        
        return vector
    
    def analisis_profundo(self, vector: Vector12D) -> Dict[str, Any]:
        return {
            "diagnostico_filosofico": self._diagnosticar_filosoficamente(vector),
            "patrones_interdimensionales": self._identificar_patrones(vector),
            "recomendaciones_evolutivas": self._generar_recomendaciones(vector),
            "proyeccion_temporal": self._proyectar_evolucion(vector)
        }
    
    def _diagnosticar_filosoficamente(self, vector: Vector12D) -> Dict[str, Any]:
        valores_abs = [abs(v) for v in vector.valores]
        if valores_abs:
            indice_dominante = valores_abs.index(max(valores_abs))
        else:
            indice_dominante = 0
        
        equilibrio = vector.calcular_equilibrio()
        arquetipo = self._determinar_arquetipo(vector)
        
        return {
            "dimension_dominante": indice_dominante + 1,
            "nombre_dimension_dominante": self.dimensiones[indice_dominante].nombre if indice_dominante < len(self.dimensiones) else "Desconocida",
            "equilibrio_filosofico": equilibrio,
            "arquetipo_sistemico": arquetipo,
            "nivel_coherencia": vector.calcular_coherencia(),
            "estado_vectorial": vector.estado.value
        }
    
    def _determinar_arquetipo(self, vector: Vector12D) -> str:
        perfiles = {
            "Sabio": vector.valores[0] > 0.6 and vector.valores[9] > 0.5,
            "Logico": vector.valores[1] > 0.7 and vector.valores[5] > 0.4,
            "Evolutivo": vector.valores[6] > 0.6 and vector.valores[3] > 0.5,
            "Etico": vector.valores[10] > 0.7,
            "Holistico": vector.valores[11] > 0.6 and vector.calcular_coherencia() > 0.7,
            "Pragmatico": vector.valores[4] > 0.6 and vector.valores[8] > 0.5,
            "Reflexivo": vector.valores[9] > 0.7,
            "Sistemico": vector.valores[2] > 0.6 and vector.valores[5] > 0.5,
            "Indeterminado": True
        }
        
        for arquetipo, condicion in perfiles.items():
            if condicion and arquetipo != "Indeterminado":
                return arquetipo
        
        return "Indeterminado"
    
    def _identificar_patrones(self, vector: Vector12D) -> List[Dict[str, Any]]:
        patrones = []
        
        valores_pos = sum(1 for v in vector.valores if v > 0.3)
        valores_neg = sum(1 for v in vector.valores if v < -0.3)
        
        if valores_pos > 6 and valores_neg < 2:
            patrones.append({
                "nombre": "Polaridad Positiva",
                "descripcion": "Predominio de manifestaciones positivas",
                "intensidad": valores_pos / 12.0
            })
        elif valores_neg > 6 and valores_pos < 2:
            patrones.append({
                "nombre": "Polaridad Negativa",
                "descripcion": "Predominio de resistencias u oposiciones",
                "intensidad": valores_neg / 12.0
            })
        
        equilibrio = vector.calcular_equilibrio()
        if equilibrio > 0.8:
            patrones.append({
                "nombre": "Equilibrio Armonico",
                "descripcion": "Balance filosofico notable entre dimensiones",
                "intensidad": equilibrio
            })
        
        if vector.estado == EstadoVector.RESONANTE:
            patrones.append({
                "nombre": "Resonancia Interdimensional",
                "descripcion": "Dimensiones en sincronia armonica",
                "intensidad": 0.9
            })
        
        return patrones
    
    def _generar_recomendaciones(self, vector: Vector12D) -> List[Dict[str, Any]]:
        recomendaciones = []
        diagnostico = self._diagnosticar_filosoficamente(vector)
        
        equilibrio = diagnostico["equilibrio_filosofico"]
        if equilibrio < 0.5:
            recomendaciones.append({
                "tipo": "equilibrio",
                "prioridad": "alta",
                "accion": "Explorar dimensiones opuestas a las dominantes",
                "razon": f"Equilibrio filosofico bajo ({equilibrio:.2f})"
            })
        
        coherencia = diagnostico["nivel_coherencia"]
        if coherencia < 0.6:
            recomendaciones.append({
                "tipo": "coherencia",
                "prioridad": "media",
                "accion": "Revisar consistencia entre intenciones y acciones",
                "razon": f"Coherencia sistemica baja ({coherencia:.2f})"
            })
        
        arquetipo = diagnostico["arquetipo_sistemico"]
        if arquetipo == "Indeterminado":
            recomendaciones.append({
                "tipo": "identidad",
                "prioridad": "media",
                "accion": "Desarrollar perfil filosofico mas definido",
                "razon": "Arquetipo sistemico no definido"
            })
        
        return recomendaciones
    
    def _proyectar_evolucion(self, vector: Vector12D) -> Dict[str, Any]:
        potencial = vector.calcular_potencial_evolutivo()
        estado = vector.estado
        
        if estado == EstadoVector.ESTABLE:
            trayectoria = "Mantenimiento del estado actual"
            probabilidad_cambio = 0.2
        elif estado == EstadoVector.OSCILANTE:
            trayectoria = "Ajuste y reequilibrio progresivo"
            probabilidad_cambio = 0.5
        elif estado == EstadoVector.RESONANTE:
            trayectoria = "Amplificacion de patrones emergentes"
            probabilidad_cambio = 0.7
        elif estado == EstadoVector.EMERGENTE:
            trayectoria = "Transformacion significativa inminente"
            probabilidad_cambio = 0.9
        else:
            trayectoria = "Reorganizacion disruptiva"
            probabilidad_cambio = 0.8
        
        return {
            "potencial_evolutivo": potencial,
            "trayectoria_probable": trayectoria,
            "probabilidad_cambio_significativo": probabilidad_cambio,
            "horizonte_temporal": {
                "corto_plazo": "1-3 ciclos procesales",
                "medio_plazo": "10-20 ciclos procesales",
                "largo_plazo": "50+ ciclos procesales"
            }
        }
    
    def get_estado_sistema(self) -> Dict[str, Any]:
        return {
            "estado": self.estado_sistema,
            "dimensiones_activas": len([d for d in self.dimensiones if hasattr(d, 'estado') and d.estado.value != "inactiva"]),
            "total_dimensiones": len(self.dimensiones),
            "historico_vectores": len(self.historico_vectores),
            "tiempo_operacion": time.time() - self.inicializacion_time,
            "pesos_filosoficos": self.pesos_filosoficos,
            "version": "VECTA 12D Filosofico 1.0"
        }
