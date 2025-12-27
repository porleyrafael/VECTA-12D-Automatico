"""
DIMENSION 3 - CONTEXTO SISTEMICO
Relacion con el entorno y sistemas circundantes
"""

import re
import math
import time
from typing import Dict, Any
from dimensiones.dimension_base import DimensionBase, ResultadoDimension, EstadoDimension

class Dimension3(DimensionBase):
    def __init__(self):
        super().__init__(
            numero=3,
            nombre="Contexto Sistemico",
            descripcion="Relacion con el entorno y sistemas circundantes"
        )
        self.peso_actual = 0.10
        
        self.filosofia = {
            "concepto_central": "Interconexion sistemica",
            "principio_operativo": "Integracion y adaptabilidad ambiental",
            "relaciones_interdimensionales": [2, 4, 5],
            "polaridad": (-1.0, 1.0)
        }
        
        self.palabras_sistemicas = [
            'sistema', 'contexto', 'entorno', 'ambiente', 'ecosistema',
            'relacion', 'interaccion', 'conexion', 'red', 'complejo',
            'global', 'local', 'macro', 'micro', 'holistico'
        ]
    
    def procesar(self, contexto: Dict[str, Any]) -> ResultadoDimension:
        try:
            texto = contexto.get('texto', '')
            metadata = contexto.get('metadata', {})
            
            integracion = self._analizar_integracion(texto)
            adaptabilidad = self._analizar_adaptabilidad(texto, metadata)
            interconexion = self._analizar_interconexion(texto)
            perspectiva = self._analizar_perspectiva(texto)
            
            valor_crudo = (
                integracion * 0.30 +
                adaptabilidad * 0.25 +
                interconexion * 0.25 +
                perspectiva * 0.20
            )
            
            valor = self._aplicar_filtro_filosofico(valor_crudo, contexto)
            confianza = self._calcular_confianza(valor)
            
            resultado = ResultadoDimension(
                valor=valor,
                confianza=confianza,
                componentes={
                    "integracion_contextual": integracion,
                    "adaptabilidad_sistemica": adaptabilidad,
                    "nivel_interconexion": interconexion,
                    "perspectiva_multinivel": perspectiva
                },
                estado=self.estado,
                timestamp=time.time()
            )
            
            self.registrar_resultado(resultado)
            return resultado
            
        except Exception as e:
            print(f"Error en Dimension 3: {e}")
            return ResultadoDimension(
                valor=0.0,
                confianza=0.1,
                componentes={},
                estado=EstadoDimension.INACTIVA,
                timestamp=time.time()
            )
    
    def _analizar_integracion(self, texto: str) -> float:
        if not texto:
            return 0.0
            
        menciones_sistemicas = sum(
            1 for palabra in self.palabras_sistemicas 
            if palabra in texto.lower()
        )
        
        palabras_totales = len(texto.split())
        if palabras_totales == 0:
            return 0.0
            
        densidad_sistemica = menciones_sistemicas / (palabras_totales / 100)
        
        return min(1.0, densidad_sistemica * 0.5)
    
    def _analizar_adaptabilidad(self, texto: str, metadata: Dict[str, Any]) -> float:
        adaptabilidad = metadata.get('adaptabilidad', 0.5)
        
        if texto:
            texto_lower = texto.lower()
            
            palabras_flexibles = ['puede', 'podria', 'posible', 'alternativa',
                                'depende', 'contexto', 'situacion', 'condicion']
            palabras_rigidas = ['siempre', 'nunca', 'imposible', 'obligatorio',
                              'necesariamente', 'absoluto', 'definitivo']
            
            flexibles = sum(1 for p in palabras_flexibles if p in texto_lower)
            rigidas = sum(1 for p in palabras_rigidas if p in texto_lower)
            
            diferencia = flexibles - rigidas
            adaptabilidad_texto = 0.5 + (diferencia * 0.1)
            
            adaptabilidad = (adaptabilidad + max(0.0, min(1.0, adaptabilidad_texto))) / 2.0
        
        return adaptabilidad
    
    def _analizar_interconexion(self, texto: str) -> float:
        if not texto:
            return 0.0
            
        conectores_relacionales = [
            'y', 'con', 'entre', 'para', 'desde', 'hacia', 'hasta',
            'mediante', 'a traves', 'gracias a', 'debido a', 'porque'
        ]
        
        conteo_conectores = sum(
            1 for conector in conectores_relacionales 
            if conector in texto.lower()
        )
        
        oraciones = re.split(r'[.!?]+', texto)
        oraciones_validas = [o for o in oraciones if len(o.strip()) > 5]
        
        if len(oraciones_validas) < 2:
            return 0.5
            
        densidad_conexion = conteo_conectores / len(oraciones_validas)
        
        return min(1.0, densidad_conexion)
    
    def _analizar_perspectiva(self, texto: str) -> float:
        if not texto:
            return 0.0
            
        perspectivas = {
            "individual": ['yo', 'mi', 'me', 'mio', 'propio'],
            "colectivo": ['nosotros', 'nuestro', 'comun', 'grupo', 'equipo'],
            "global": ['todos', 'humanidad', 'mundo', 'global', 'universal'],
            "especifico": ['especifico', 'particular', 'concreto', 'determinado']
        }
        
        conteos = {}
        for perspectiva, palabras in perspectivas.items():
            conteos[perspectiva] = sum(1 for p in palabras if p in texto.lower())
        
        total_perspectivas = sum(1 for c in conteos.values() if c > 0)
        
        if total_perspectivas == 0:
            return 0.3
        elif total_perspectivas == 1:
            return 0.5
        elif total_perspectivas == 2:
            return 0.7
        else:
            return 0.9
