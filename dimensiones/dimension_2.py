"""
DIMENSION 2 - ESTRUCTURA LOGICA
Coherencia formal y validez racional
"""

import re
import math
import time
from typing import Dict, Any
from dimensiones.dimension_base import DimensionBase, ResultadoDimension, EstadoDimension

class Dimension2(DimensionBase):
    def __init__(self):
        super().__init__(
            numero=2,
            nombre="Estructura Logica",
            descripcion="Coherencia formal y validez racional"
        )
        self.peso_actual = 0.12
        
        self.filosofia = {
            "concepto_central": "Razonamiento solido",
            "principio_operativo": "Validez formal y consistencia interna",
            "relaciones_interdimensionales": [1, 3, 6],
            "polaridad": (-1.0, 1.0)
        }
        
        self.operadores_logicos = ['y', 'o', 'si', 'entonces', 'por lo tanto', 'porque', 'debido a']
        self.falacias_comunes = [
            r'\btodo el mundo sabe\b',
            r'\bsiempre ha sido asi\b',
            r'\bes obvio que\b',
            r'\bno hay otra opcion\b'
        ]
    
    def procesar(self, contexto: Dict[str, Any]) -> ResultadoDimension:
        try:
            texto = contexto.get('texto', '')
            metadata = contexto.get('metadata', {})
            
            coherencia = self._analizar_coherencia(texto)
            estructura = self._analizar_estructura(texto)
            validez = self._analizar_validez(texto, metadata)
            consistencia = self._analizar_consistencia(texto)
            
            valor_crudo = (
                coherencia * 0.35 +
                estructura * 0.25 +
                validez * 0.25 +
                consistencia * 0.15
            )
            
            valor = self._aplicar_filtro_filosofico(valor_crudo, contexto)
            confianza = self._calcular_confianza(valor)
            
            resultado = ResultadoDimension(
                valor=valor,
                confianza=confianza,
                componentes={
                    "coherencia": coherencia,
                    "estructura_logica": estructura,
                    "validez_formal": validez,
                    "consistencia_interna": consistencia
                },
                estado=self.estado,
                timestamp=time.time()
            )
            
            self.registrar_resultado(resultado)
            return resultado
            
        except Exception as e:
            print(f"Error en Dimension 2: {e}")
            return ResultadoDimension(
                valor=0.0,
                confianza=0.1,
                componentes={},
                estado=EstadoDimension.INACTIVA,
                timestamp=time.time()
            )
    
    def _analizar_coherencia(self, texto: str) -> float:
        if not texto:
            return 0.0
            
        oraciones = re.split(r'[.!?]+', texto)
        if len(oraciones) < 2:
            return 0.5
            
        puntos_coherencia = 0
        total_comparaciones = 0
        
        for i in range(len(oraciones) - 1):
            oracion_actual = oraciones[i].strip().lower()
            oracion_siguiente = oraciones[i + 1].strip().lower()
            
            if len(oracion_actual) < 3 or len(oracion_siguiente) < 3:
                continue
                
            total_comparaciones += 1
            
            hay_conector = any(
                conector in oracion_siguiente 
                for conector in ['ademas', 'tambien', 'por otro lado', 'sin embargo', 'no obstante']
            )
            
            mismo_tema = len(set(oracion_actual.split()) & set(oracion_siguiente.split())) > 2
            
            if hay_conector or mismo_tema:
                puntos_coherencia += 1
        
        if total_comparaciones == 0:
            return 0.5
            
        return puntos_coherencia / total_comparaciones
    
    def _analizar_estructura(self, texto: str) -> float:
        if not texto:
            return 0.0
            
        oraciones = re.split(r'[.!?]+', texto)
        estructura_valida = 0
        
        for oracion in oraciones:
            oracion = oracion.strip()
            if len(oracion) < 5:
                continue
                
            tiene_verbo = any(palabra in oracion.lower() for palabra in ['es', 'esta', 'tiene', 'hace', 'puede'])
            tiene_sujeto = len([p for p in oracion.split() if p[0].isupper()]) > 0
            
            if tiene_verbo and tiene_sujeto:
                estructura_valida += 1
        
        total_oraciones = len([o for o in oraciones if len(o.strip()) >= 5])
        if total_oraciones == 0:
            return 0.0
            
        return estructura_valida / total_oraciones
    
    def _analizar_validez(self, texto: str, metadata: Dict[str, Any]) -> float:
        validez = 0.5
        
        if texto:
            texto_lower = texto.lower()
            
            operadores_presentes = sum(1 for op in self.operadores_logicos if op in texto_lower)
            falacias_presentes = sum(1 for falacia in self.falacias_comunes 
                                   if re.search(falacia, texto_lower, re.IGNORECASE))
            
            puntos_validez = operadores_presentes * 0.1
            puntos_falacias = falacias_presentes * (-0.2)
            
            validez = 0.5 + puntos_validez + puntos_falacias
            
            argumentos = metadata.get('argumentos', [])
            if argumentos:
                validez += len(argumentos) * 0.05
        
        return max(0.0, min(1.0, validez))
    
    def _analizar_consistencia(self, texto: str) -> float:
        if not texto:
            return 0.0
            
        palabras_clave = ['siempre', 'nunca', 'todo', 'nada', 'si', 'no']
        menciones = {}
        
        for palabra in palabras_clave:
            conteo = len(re.findall(r'\b' + re.escape(palabra) + r'\b', texto.lower()))
            if conteo > 0:
                menciones[palabra] = conteo
        
        if not menciones:
            return 0.7
            
        conflictos = 0
        
        if 'siempre' in menciones and 'nunca' in menciones:
            conflictos += 1
        if 'todo' in menciones and 'nada' in menciones:
            conflictos += 1
        if 'si' in menciones and 'no' in menciones:
            conflictos += 0.5
        
        consistencia = 1.0 - (conflictos / len(menciones))
        return max(0.0, min(1.0, consistencia))
