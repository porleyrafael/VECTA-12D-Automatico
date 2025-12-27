"""
DIMENSION 1 - INTENCIONALIDAD PURA
Versión funcional simplificada
"""

import re
import time
from typing import Dict, Any
from dimensiones.dimension_base import DimensionBase, ResultadoDimension, EstadoDimension

class Dimension1(DimensionBase):
    def __init__(self):
        super().__init__(
            numero=1,
            nombre="Intencionalidad Pura",
            descripcion="Voluntad primaria detrás de cualquier acción o decisión"
        )
        self.peso_actual = 0.15
    
    def procesar(self, contexto: Dict[str, Any]) -> ResultadoDimension:
        try:
            texto = contexto.get('texto', '')
            
            # Análisis simple de intencionalidad
            claridad = self._analizar_claridad_simple(texto)
            fuerza = self._analizar_fuerza_simple(texto)
            
            # Valor combinado
            valor = (claridad * 0.6 + fuerza * 0.4)
            valor = max(-1.0, min(1.0, valor))
            
            confianza = 0.7  # Confianza media
            
            resultado = ResultadoDimension(
                valor=valor,
                confianza=confianza,
                componentes={
                    "claridad": claridad,
                    "fuerza_voluntad": fuerza
                },
                estado=self.estado,
                timestamp=time.time()
            )
            
            self.registrar_resultado(resultado)
            return resultado
            
        except Exception as e:
            print(f"Error en Dimensión 1 (simple): {e}")
            return ResultadoDimension(
                valor=0.0,
                confianza=0.1,
                componentes={},
                estado=EstadoDimension.INACTIVA,
                timestamp=time.time()
            )
    
    def _analizar_claridad_simple(self, texto: str) -> float:
        if not texto:
            return 0.0
        
        palabras_claras = ['quiero', 'debo', 'necesito', 'voy a', 'tengo que', 'deseo']
        palabras_confusas = ['quizás', 'tal vez', 'no sé', 'no estoy seguro', 'tal vez sí']
        
        texto_lower = texto.lower()
        
        conteo_claro = sum(1 for p in palabras_claras if p in texto_lower)
        conteo_confuso = sum(1 for p in palabras_confusas if p in texto_lower)
        
        if len(texto_lower.split()) == 0:
            return 0.0
        
        claridad = (conteo_claro - conteo_confuso) / max(1, len(texto_lower.split()) / 10)
        return max(-1.0, min(1.0, claridad))
    
    def _analizar_fuerza_simple(self, texto: str) -> float:
        if not texto:
            return 0.0
        
        palabras_fuertes = ['absolutamente', 'definitivamente', 'seguro', 'decisivo']
        palabras_debiles = ['quizás', 'posiblemente', 'dudo', 'inseguro']
        
        texto_lower = texto.lower()
        
        conteo_fuerte = sum(1 for p in palabras_fuertes if p in texto_lower)
        conteo_debil = sum(1 for p in palabras_debiles if p in texto_lower)
        
        if len(texto_lower.split()) == 0:
            return 0.0
        
        fuerza = (conteo_fuerte - conteo_debil) / max(1, len(texto_lower.split()) / 10)
        return max(-1.0, min(1.0, fuerza))
