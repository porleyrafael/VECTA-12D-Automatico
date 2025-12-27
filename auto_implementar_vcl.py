#!/usr/bin/env python3
"""
AUTO-IMPLEMENTADOR VECTA VCL COMPLETO
Instala y configura TODO el sistema VECTA Core Language automáticamente
"""

import os
import sys
import json
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

class VECTAAutoInstaller:
    """Instalador automático del sistema VECTA VCL"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.temp_dir = self.base_dir / "temp_vcl_install"
        self.backup_dir = self.base_dir / "backup_vcl"
        self.log_file = self.base_dir / "vcl_installation.log"
        
        # Mapeo de archivos a crear
        self.files_to_create = {
            # Core VCL Engine
            "core/vcl_engine.py": self._get_vcl_engine_code(),
            "core/vcl_integration.py": self._get_vcl_integration_code(),
            "core/vcl_dashboard.py": self._get_vcl_dashboard_code(),
            "core/__init__.py": "# VECTA Core Language Package\n\n__version__ = '1.0.0'\n",
            
            # Testing
            "test_vcl.py": self._get_test_code(),
            "examples/ejemplo_vcl.vecta": self._get_example_vcl_code(),
            
            # Configuración
            "vcl_config.json": self._get_vcl_config(),
            "vcl_quickstart.md": self._get_quickstart_guide(),
            
            # Scripts de utilidad
            "ejecutar_vcl.py": self._get_ejecutar_vcl_code(),
            "monitor_vcl.py": self._get_monitor_vcl_code(),
        }
        
        # Archivos a modificar
        self.files_to_modify = {
            "vecta_launcher.py": self._get_vecta_launcher_patch(),
            "crear_dashboard_vecta.py": self._get_dashboard_patch(),
            "dashboard_vecta.html": self._get_dashboard_html_patch(),
        }
    
    def log(self, message, level="INFO"):
        """Registra mensaje en log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}\n"
        
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(log_entry)
        
        if level == "ERROR":
            print(f"❌ {message}")
        elif level == "WARNING":
            print(f"⚠️  {message}")
        else:
            print(f"✓ {message}")
    
    def create_backup(self, file_path):
        """Crea backup de archivo existente"""
        if not os.path.exists(file_path):
            return
        
        self.backup_dir.mkdir(exist_ok=True)
        
        file_name = Path(file_path).name
        backup_path = self.backup_dir / f"{file_name}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        try:
            shutil.copy2(file_path, backup_path)
            self.log(f"Backup creado: {backup_path}")
            return backup_path
        except Exception as e:
            self.log(f"Error creando backup de {file_path}: {e}", "ERROR")
            return None
    
    def check_prerequisites(self):
        """Verifica requisitos previos"""
        self.log("Verificando requisitos del sistema...")
        
        checks = {
            "Python 3.8+": sys.version_info >= (3, 8),
            "Directorio VECTA": os.path.exists(self.base_dir),
            "Carpeta core": os.path.exists(self.base_dir / "core"),
            "Carpeta dimensiones": os.path.exists(self.base_dir / "dimensiones"),
        }
        
        all_ok = True
        for check, result in checks.items():
            if result:
                self.log(f"  ✓ {check}")
            else:
                self.log(f"  ✗ {check}", "ERROR")
                all_ok = False
        
        return all_ok
    
    def create_directory_structure(self):
        """Crea estructura de directorios necesaria"""
        directories = [
            "core",
            "dimensiones",
            "examples",
            "logs",
            "backup_vcl",
            "temp_vcl_install"
        ]
        
        for directory in directories:
            dir_path = self.base_dir / directory
            dir_path.mkdir(exist_ok=True)
            self.log(f"Creado directorio: {directory}")
    
    def _get_vcl_engine_code(self):
        """Retorna código del motor VCL"""
        return '''#!/usr/bin/env python3
"""
VECTA CORE LANGUAGE (VCL) ENGINE
Implementación exacta de la especificación VCL
Versión: 1.0
Autor: Rafael Porley
"""

import math
import json
from datetime import datetime
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
from enum import Enum

# =========================================================
# SÍMBOLOS BASE VCL (IRREDUCIBLES)
# =========================================================

class VCLSymbolType(Enum):
    """Tipos de símbolos atómicos VCL"""
    INTENTION = "⟐"
    RESOURCE_OR_ENERGY = "⟡"
    SYSTEM_STATE = "⟁"
    TIME_OR_PHASE = "⟢"
    CONSTRAINT = "⟂"
    UNCERTAINTY = "⟣"
    DECISION_COLLAPSE = "⟠"

@dataclass
class VCLSymbol:
    """
    SYMBOL := { FORM, ORIENTATION, WEIGHT, PHASE }
    Cada símbolo es un NODO DE INTENCIÓN
    """
    symbol_type: VCLSymbolType
    form: str
    orientation: Tuple[float, float, float]
    weight: float
    phase: float
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
    
    @property
    def symbol_char(self):
        return self.symbol_type.value
    
    def to_dict(self):
        return {
            "symbol": self.symbol_char,
            "form": self.form,
            "orientation": self.orientation,
            "weight": self.weight,
            "phase": self.phase,
            "metadata": self.metadata
        }
    
    def __repr__(self):
        return f"{self.symbol_char}[{self.form}:ω={self.weight:.2f},φ={self.phase:.2f}]"

class VCLError(Exception):
    """Error específico del motor VCL"""
    pass

class VCLEngine:
    """
    Motor principal del VECTA Core Language
    Implementa: FIELD C = Σ ( SYMBOL ⊗ CONTEXT ⊗ TIME )
    """
    
    def __init__(self):
        self.symbols: List[VCLSymbol] = []
        self.context: Dict[str, Any] = {}
        self.time_reference = datetime.now()
        self.field_history: List[Dict] = []
        self.T_MAX = 10.0
        
        self._initialize_base_symbols()
    
    def _initialize_base_symbols(self):
        """Inicializa símbolos base irreducibles"""
        base_symbols = [
            VCLSymbol(VCLSymbolType.INTENTION, "INTENTION_PURE", (0,0,1), 1.0, 0.0, {"irreducible": True}),
            VCLSymbol(VCLSymbolType.RESOURCE_OR_ENERGY, "RESOURCE_BASE", (1,0,0), 1.0, 0.0, {"irreducible": True}),
            VCLSymbol(VCLSymbolType.SYSTEM_STATE, "STATE_BASELINE", (0,1,0), 1.0, 0.0, {"irreducible": True}),
            VCLSymbol(VCLSymbolType.TIME_OR_PHASE, "TIME_BASELINE", (0,0,0), 1.0, 0.0, {"irreducible": True}),
            VCLSymbol(VCLSymbolType.CONSTRAINT, "CONSTRAINT_BASE", (-1,0,0), 1.0, 0.0, {"irreducible": True}),
            VCLSymbol(VCLSymbolType.UNCERTAINTY, "UNCERTAINTY_BASE", (0,-1,0), 1.0, 0.0, {"irreducible": True}),
            VCLSymbol(VCLSymbolType.DECISION_COLLAPSE, "DECISION_BASE", (0,0,0), 1.0, 0.0, {"irreducible": True}),
        ]
        
        self.symbols.extend(base_symbols)
    
    def add_symbol(self, symbol: VCLSymbol):
        """Añade un símbolo al campo"""
        if symbol.metadata.get("irreducible", False):
            for existing in self.symbols:
                if existing.symbol_type == symbol.symbol_type and existing.metadata.get("irreducible", False):
                    raise VCLError(f"Símbolo irreducible {symbol.symbol_char} ya existe")
        
        self.symbols.append(symbol)
        return symbol
    
    def build_field(self):
        """Construye campo de decisión"""
        field_symbols = self.symbols.copy()
        
        if self.context:
            for symbol in field_symbols:
                context_factor = self._calculate_context_factor(symbol)
                symbol.weight *= context_factor
        
        time_factor = self._calculate_time_factor()
        for symbol in field_symbols:
            symbol.phase = (symbol.phase + time_factor) % (2 * math.pi)
        
        return VCLField(field_symbols, self.context, self.time_reference)
    
    def _calculate_context_factor(self, symbol: VCLSymbol) -> float:
        factor = 1.0
        if "priority_forms" in self.context and symbol.form in self.context["priority_forms"]:
            factor *= 1.5
        if "contradictory_forms" in self.context and symbol.form in self.context["contradictory_forms"]:
            factor *= 0.5
        return factor
    
    def _calculate_time_factor(self) -> float:
        time_diff = (datetime.now() - self.time_reference).total_seconds()
        return (time_diff % 3600) / 3600 * (2 * math.pi)
    
    def run_cycle(self, external_context: Dict = None):
        """Ejecuta un ciclo VCL completo"""
        if external_context:
            self.context.update(external_context)
        
        field = self.build_field()
        
        # Validar campo
        if not any(s.symbol_type == VCLSymbolType.DECISION_COLLAPSE for s in field.symbols):
            raise VCLError("FIELD does NOT generate ⟠ - SYSTEM_ERROR")
        
        collapsed = field.collapse()
        
        return {
            "field": field,
            "collapsed_symbol": collapsed,
            "quantum_state": field.to_quantum_representation(),
            "timestamp": datetime.now().isoformat()
        }

class VCLField:
    """Representa un campo de decisión VCL"""
    
    def __init__(self, symbols: List[VCLSymbol], context: Dict, time_reference: datetime):
        self.symbols = symbols
        self.context = context
        self.time_reference = time_reference
        self.collapsed_symbol: Optional[VCLSymbol] = None
    
    def collapse(self) -> VCLSymbol:
        """Colapsa el campo a una decisión única"""
        collapse_symbols = [s for s in self.symbols 
                          if s.symbol_type == VCLSymbolType.DECISION_COLLAPSE]
        
        if not collapse_symbols:
            raise VCLError("FIELD does NOT generate ⟠")
        
        self.collapsed_symbol = max(collapse_symbols, key=lambda s: s.weight)
        return self.collapsed_symbol
    
    def to_quantum_representation(self) -> str:
        """Convierte a notación cuántica"""
        if not self.symbols:
            return "|Ψ> = 0"
        
        terms = []
        for i, symbol in enumerate(self.symbols, 1):
            amplitude = symbol.weight * math.cos(symbol.phase)
            terms.append(f"{amplitude:.3f}|A{i}>")
        
        return f"|Ψ> = {' + '.join(terms)}"
    
    def audit_log(self) -> Dict:
        return {
            "timestamp": datetime.now().isoformat(),
            "symbol_count": len(self.symbols),
            "has_collapse": self.collapsed_symbol is not None,
            "collapsed_to": self.collapsed_symbol.form if self.collapsed_symbol else None
        }

# =========================================================
# INTERFAZ SIMPLIFICADA
# =========================================================

class VCLInterpreter:
    """Intérprete simplificado para uso rápido"""
    
    def __init__(self):
        self.engine = VCLEngine()
        self.history = []
    
    def interpret(self, vcl_script: str):
        """Interpreta un script VCL básico"""
        lines = vcl_script.strip().split('\\n')
        results = []
        
        for line in lines:
            if line.startswith('[') and ']' in line:
                # Formato: [SYMBOL:FORM]
                parts = line.strip('[]').split(':')
                if len(parts) == 2:
                    symbol_name, form = parts
                    try:
                        symbol_type = VCLSymbolType[symbol_name]
                        symbol = VCLSymbol(
                            symbol_type=symbol_type,
                            form=form,
                            orientation=(0,0,1),
                            weight=0.8,
                            phase=0.0
                        )
                        self.engine.add_symbol(symbol)
                        results.append(f"Añadido: {symbol}")
                    except:
                        results.append(f"Error: Símbolo {symbol_name} no válido")
        
        return {
            "processed_lines": len(lines),
            "symbols_added": len(self.engine.symbols) - 7,  # Excluir base
            "results": results
        }
    
    def quick_decision(self, context: Dict = None):
        """Toma una decisión rápida"""
        cycle_result = self.engine.run_cycle(context)
        
        self.history.append({
            "timestamp": datetime.now().isoformat(),
            "decision": cycle_result["collapsed_symbol"].form,
            "symbols_count": len(cycle_result["field"].symbols)
        })
        
        return cycle_result

# Instancia global para importación fácil
vcl_engine = VCLEngine()
vcl_interpreter = VCLInterpreter()

if __name__ == "__main__":
    print("✅ Motor VCL cargado correctamente")
    print(f"   Símbolos base: {len(vcl_engine.symbols)}")
    print(f"   Versión: 1.0.0")
'''
    
    def _get_vcl_integration_code(self):
        """Retorna código de integración VCL con VECTA 12D"""
        return '''#!/usr/bin/env python3
"""
INTEGRACIÓN VCL CON VECTA 12D
Conecta el lenguaje simbólico con las dimensiones vectoriales
"""

import sys
from pathlib import Path

# Añadir directorio padre al path para importaciones
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from core.vcl_engine import VCLInterpreter, VCLSymbol, VCLSymbolType
except ImportError:
    print("⚠️  Error: No se pudo importar vcl_engine. Ejecuta auto_implementar_vcl.py primero.")
    sys.exit(1)

class VECTA_VCL_Integration:
    """Integra VCL con el sistema VECTA 12D"""
    
    def __init__(self):
        self.vcl = VCLInterpreter()
        self.dimension_map = self._create_dimension_map()
        self.integration_active = False
        
        print("✅ Integración VCL-VECTA 12D inicializada")
    
    def _create_dimension_map(self):
        """Mapea dimensiones VECTA a símbolos VCL"""
        return {
            1: VCLSymbolType.INTENTION,        # Intencionalidad Pura
            2: VCLSymbolType.SYSTEM_STATE,     # Estructura Lógica
            3: VCLSymbolType.SYSTEM_STATE,     # Contexto Sistémico
            4: VCLSymbolType.TIME_OR_PHASE,    # Temporalidad
            5: VCLSymbolType.RESOURCE_OR_ENERGY, # Escala de Impacto
            6: VCLSymbolType.UNCERTAINTY,      # Complejidad Intrínseca
            7: VCLSymbolType.INTENTION,        # Evolución Potencial
            8: VCLSymbolType.CONSTRAINT,       # Simetría/Asimetría
            9: VCLSymbolType.UNCERTAINTY,      # Información/Entropía
            10: VCLSymbolType.INTENTION,       # Consciencia Reflexiva
            11: VCLSymbolType.CONSTRAINT,      # Integridad Ética
            12: VCLSymbolType.DECISION_COLLAPSE # Unificación Holística
        }
    
    def analyze_vecta_state(self, vecta_data: dict):
        """Analiza estado de VECTA y crea símbolos VCL correspondientes"""
        
        # Limpiar símbolos previos (excepto base)
        self.vcl.engine.symbols = [s for s in self.vcl.engine.symbols 
                                  if s.metadata.get("irreducible", False)]
        
        # Crear símbolos basados en dimensiones activas
        for dim_index in range(1, 13):
            dim_key = f"dimension_{dim_index}"
            if dim_key in vecta_data:
                value = vecta_data[dim_key]
                if value > 0.1:  # Solo dimensiones significativas
                    self._create_dimension_symbol(dim_index, value)
        
        # Añadir símbolo de síntesis VECTA
        synthesis_symbol = VCLSymbol(
            symbol_type=VCLSymbolType.DECISION_COLLAPSE,
            form="VECTA_12D_SYNTHESIS",
            orientation=(0, 0, 0),
            weight=0.9,
            phase=0.0,
            metadata={
                "synthesis": True,
                "source": "vecta_12d",
                "dimensions_active": len([v for v in vecta_data.values() if v > 0.1])
            }
        )
        
        self.vcl.engine.add_symbol(synthesis_symbol)
        
        return f"Analizadas {len(vecta_data)} dimensiones, creados {len(self.vcl.engine.symbols)-7} símbolos"
    
    def _create_dimension_symbol(self, dimension: int, value: float):
        """Crea símbolo VCL para una dimensión"""
        symbol_type = self.dimension_map.get(dimension, VCLSymbolType.INTENTION)
        
        # Calcular orientación basada en la dimensión
        import math
        angle = (dimension - 1) * (2 * math.pi / 12)
        orientation = (
            math.cos(angle) * value,
            math.sin(angle) * value,
            dimension / 12
        )
        
        symbol = VCLSymbol(
            symbol_type=symbol_type,
            form=f"DIMENSION_{dimension}",
            orientation=orientation,
            weight=value,
            phase=value * 2 * math.pi,
            metadata={
                "dimension": dimension,
                "original_value": value,
                "vecta_integrated": True
            }
        )
        
        self.vcl.engine.add_symbol(symbol)
    
    def get_vcl_recommendation(self, vecta_data: dict = None):
        """Obtiene recomendación VCL para el estado actual"""
        
        if vecta_data:
            self.analyze_vecta_state(vecta_data)
        
        try:
            result = self.vcl.quick_decision({
                "priority_forms": ["VECTA_12D_SYNTHESIS"],
                "vecta_mode": True
            })
            
            decision = result["collapsed_symbol"]
            
            recommendations = {
                VCLSymbolType.INTENTION: "Enfócate en clarificar objetivos y dirección",
                VCLSymbolType.RESOURCE_OR_ENERGY: "Optimiza la asignación de recursos disponibles",
                VCLSymbolType.SYSTEM_STATE: "Analiza y ajusta los parámetros del sistema",
                VCLSymbolType.TIME_OR_PHASE: "Considera aspectos temporales y sincronización",
                VCLSymbolType.CONSTRAINT: "Identifica y respeta los límites del sistema",
                VCLSymbolType.UNCERTAINTY: "Reconoce y aborda áreas de incertidumbre",
                VCLSymbolType.DECISION_COLLAPSE: "Procede con la implementación seleccionada"
            }
            
            base_rec = recommendations.get(decision.symbol_type, 
                                          "Procede con conciencia sistémica")
            
            # Personalizar según peso
            if decision.weight > 0.8:
                base_rec += " (ALTA PRIORIDAD)"
            elif decision.weight < 0.3:
                base_rec += " (prioridad baja)"
            
            return {
                "recommendation": base_rec,
                "symbol": decision.symbol_char,
                "form": decision.form,
                "weight": decision.weight,
                "quantum_state": result["quantum_state"]
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "recommendation": "Usar enfoque estándar VECTA por ahora",
                "symbol": "⟐",
                "form": "FALLBACK_INTENTION"
            }
    
    def export_integration_report(self):
        """Exporta reporte de integración"""
        return {
            "integration_version": "1.0",
            "dimensions_mapped": len(self.dimension_map),
            "vcl_symbols_count": len(self.vcl.engine.symbols),
            "history_entries": len(self.vcl.history),
            "active": self.integration_active,
            "last_decision": self.vcl.history[-1] if self.vcl.history else None
        }

# Instancia global para fácil acceso
vcl_integration = VECTA_VCL_Integration()

if __name__ == "__main__":
    print("🧪 Probando integración VCL-VECTA 12D...")
    
    # Datos de ejemplo
    vecta_example = {
        "dimension_1": 0.9,   # Intencionalidad alta
        "dimension_2": 0.8,   # Lógica estructurada
        "dimension_3": 0.7,   # Contexto presente
        "dimension_4": 0.6,   # Temporalidad media
    }
    
    print(f"📊 Analizando estado VECTA con {len(vecta_example)} dimensiones...")
    analysis = vcl_integration.analyze_vecta_state(vecta_example)
    print(f"✅ {analysis}")
    
    print("\n🎯 Obteniendo recomendación VCL...")
    recommendation = vcl_integration.get_vcl_recommendation()
    
    print(f"\n📋 RECOMENDACIÓN:")
    print(f"   Símbolo: {recommendation['symbol']}")
    print(f"   Forma: {recommendation['form']}")
    print(f"   Peso: {recommendation['weight']:.2f}")
    print(f"   Recomendación: {recommendation['recommendation']}")
    print(f"   Estado cuántico: {recommendation.get('quantum_state', 'N/A')}")
    
    print("\n✅ Integración funcionando correctamente!")
'''
    
    def _get_vcl_dashboard_code(self):
        """Retorna código del dashboard VCL"""
        return '''#!/usr/bin/env python3
"""
DASHBOARD VCL - Panel de control para VECTA Core Language
"""

from flask import Blueprint, render_template, jsonify, request
import json
from datetime import datetime

# Intentar importar VCL
try:
    from core.vcl_engine import vcl_interpreter, VCLEngine
    from core.vcl_integration import vcl_integration
    VCL_AVAILABLE = True
except ImportError:
    VCL_AVAILABLE = False
    print("⚠️  VCL no disponible. Ejecuta auto_implementar_vcl.py primero.")

# Crear blueprint Flask
vcl_bp = Blueprint('vcl', __name__, 
                  template_folder='../templates',
                  static_folder='../static')

# =========================================================
# RUTAS DEL DASHBOARD VCL
# =========================================================

@vcl_bp.route('/vcl')
def vcl_dashboard():
    """Dashboard principal VCL"""
    if not VCL_AVAILABLE:
        return render_template('vcl_error.html', 
                             error="VCL no está instalado")
    
    # Obtener estado actual
    symbols_count = len(vcl_interpreter.engine.symbols)
    history_count = len(vcl_interpreter.history)
    
    # Símbolos base
    base_symbols = [
        {"char": "⟐", "name": "INTENCIÓN", "desc": "Vector objetivo puro"},
        {"char": "⟡", "name": "RECURSO", "desc": "Capacidad disponible"},
        {"char": "⟁", "name": "ESTADO", "desc": "Estado del sistema"},
        {"char": "⟢", "name": "TIEMPO", "desc": "Horizonte temporal"},
        {"char": "⟂", "name": "RESTRICCIÓN", "desc": "Límite duro"},
        {"char": "⟣", "name": "INCERTIDUMBRE", "desc": "Desconocido explícito"},
        {"char": "⟠", "name": "DECISIÓN", "desc": "Estado final obligatorio"},
    ]
    
    return render_template('vcl_dashboard.html',
                         base_symbols=base_symbols,
                         symbols_count=symbols_count,
                         history_count=history_count,
                         vcl_available=VCL_AVAILABLE)

@vcl_bp.route('/vcl/symbols')
def get_symbols():
    """Obtiene todos los símbolos VCL activos"""
    if not VCL_AVAILABLE:
        return jsonify({"error": "VCL no disponible"}), 500
    
    symbols = []
    for symbol in vcl_interpreter.engine.symbols:
        symbols.append({
            "char": symbol.symbol_char,
            "form": symbol.form,
            "weight": symbol.weight,
            "phase": symbol.phase,
            "type": symbol.symbol_type.name,
            "irreducible": symbol.metadata.get("irreducible", False)
        })
    
    return jsonify({
        "count": len(symbols),
        "symbols": symbols,
        "timestamp": datetime.now().isoformat()
    })

@vcl_bp.route('/vcl/analyze', methods=['POST'])
def analyze_with_vcl():
    """Analiza datos usando VCL"""
    if not VCL_AVAILABLE:
        return jsonify({"error": "VCL no disponible"}), 500
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No se recibieron datos"}), 400
        
        # Usar integración VECTA-VCL si hay datos de dimensiones
        if any(k.startswith('dimension_') for k in data.keys()):
            result = vcl_integration.get_vcl_recommendation(data)
        else:
            # Análisis VCL directo
            result = vcl_interpreter.quick_decision(data)
        
        return jsonify({
            "success": True,
            "result": result,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "success": False,
            "timestamp": datetime.now().isoformat()
        }), 500

@vcl_bp.route('/vcl/history')
def get_history():
    """Obtiene historial de decisiones VCL"""
    if not VCL_AVAILABLE:
        return jsonify({"error": "VCL no disponible"}), 500
    
    return jsonify({
        "history": vcl_interpreter.history[-20:],  # Últimas 20 entradas
        "total": len(vcl_interpreter.history)
    })

@vcl_bp.route('/vcl/reset')
def reset_vcl():
    """Reinicia el motor VCL (solo para desarrollo)"""
    if not VCL_AVAILABLE:
        return jsonify({"error": "VCL no disponible"}), 500
    
    # Reiniciar manteniendo símbolos base
    vcl_interpreter.engine.symbols = [
        s for s in vcl_interpreter.engine.symbols 
        if s.metadata.get("irreducible", False)
    ]
    vcl_interpreter.history = []
    
    return jsonify({
        "success": True,
        "message": "VCL reiniciado",
        "symbols_remaining": len(vcl_interpreter.engine.symbols)
    })

@vcl_bp.route('/vcl/status')
def vcl_status():
    """Estado del sistema VCL"""
    return jsonify({
        "available": VCL_AVAILABLE,
        "version": "1.0.0",
        "symbols_base": 7,
        "symbols_custom": len(vcl_interpreter.engine.symbols) - 7 if VCL_AVAILABLE else 0,
        "history_count": len(vcl_interpreter.history) if VCL_AVAILABLE else 0,
        "integration_active": vcl_integration.integration_active if VCL_AVAILABLE else False,
        "timestamp": datetime.now().isoformat()
    })

# =========================================================
# TEMPLATES HTML PARA VCL
# =========================================================

VCL_DASHBOARD_HTML = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VECTA Core Language Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        body {
            background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
            color: #ffffff;
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
            padding: 20px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            background: linear-gradient(90deg, #00b4db, #0083b0);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .header p {
            color: #a0d2ff;
            font-size: 1.1em;
        }
        
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }
        
        .card {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            padding: 25px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: transform 0.3s, border-color 0.3s;
        }
        
        .card:hover {
            transform: translateY(-5px);
            border-color: #00b4db;
        }
        
        .card h2 {
            color: #00b4db;
            margin-bottom: 15px;
            font-size: 1.4em;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .symbol-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
            margin-top: 15px;
        }
        
        .symbol {
            text-align: center;
            padding: 15px;
            background: rgba(0, 180, 219, 0.1);
            border-radius: 10px;
            border: 1px solid rgba(0, 180, 219, 0.3);
        }
        
        .symbol-char {
            font-size: 2.5em;
            margin-bottom: 5px;
        }
        
        .symbol-name {
            font-size: 0.9em;
            color: #a0d2ff;
        }
        
        .btn {
            display: inline-block;
            padding: 12px 25px;
            background: linear-gradient(90deg, #00b4db, #0083b0);
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1em;
            font-weight: 600;
            transition: all 0.3s;
            text-decoration: none;
            text-align: center;
        }
        
        .btn:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(0, 180, 219, 0.4);
        }
        
        .btn-danger {
            background: linear-gradient(90deg, #ff416c, #ff4b2b);
        }
        
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }
        
        .status-active {
            background: #00ff88;
            box-shadow: 0 0 10px #00ff88;
        }
        
        .status-inactive {
            background: #ff416c;
            box-shadow: 0 0 10px #ff416c;
        }
        
        .metrics {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        
        .metric {
            text-align: center;
            padding: 15px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
        }
        
        .metric-value {
            font-size: 2em;
            font-weight: bold;
            color: #00b4db;
        }
        
        .metric-label {
            font-size: 0.9em;
            color: #a0d2ff;
            margin-top: 5px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 8px;
            color: #a0d2ff;
        }
        
        .form-group input,
        .form-group textarea {
            width: 100%;
            padding: 12px;
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 8px;
            color: white;
            font-size: 1em;
        }
        
        .form-group textarea {
            min-height: 100px;
            resize: vertical;
        }
        
        @media (max-width: 768px) {
            .grid {
                grid-template-columns: 1fr;
            }
            
            .symbol-grid {
                grid-template-columns: repeat(3, 1fr);
            }
            
            .header h1 {
                font-size: 2em;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌌 VECTA Core Language (VCL)</h1>
            <p>Lenguaje simbólico para decisión filosófica automatizada</p>
        </div>
        
        <div class="grid">
            <!-- Panel de símbolos -->
            <div class="card">
                <h2>🔣 Símbolos VCL</h2>
                <div class="symbol-grid">
                    {% for symbol in base_symbols %}
                    <div class="symbol" title="{{ symbol.desc }}">
                        <div class="symbol-char">{{ symbol.char }}</div>
                        <div class="symbol-name">{{ symbol.name }}</div>
                    </div>
                    {% endfor %}
                </div>
                <div class="metrics">
                    <div class="metric">
                        <div class="metric-value">{{ symbols_count }}</div>
                        <div class="metric-label">Símbolos totales</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{{ history_count }}</div>
                        <div class="metric-label">Decisiones tomadas</div>
                    </div>
                </div>
            </div>
            
            <!-- Panel de control -->
            <div class="card">
                <h2><span class="status-indicator {% if vcl_available %}status-active{% else %}status-inactive{% endif %}"></span>
                    Panel de Control</h2>
                
                <div class="form-group">
                    <label for="vcl-input">Ingresa texto VCL:</label>
                    <textarea id="vcl-input" placeholder="Ejemplo: [INTENTION:COMPLETE_PROJECT]&#10;[RESOURCE_OR_ENERGY:AVAILABLE]"></textarea>
                </div>
                
                <div style="display: flex; gap: 10px; margin-top: 20px;">
                    <button class="btn" onclick="analyzeVCL()">🔍 Analizar</button>
                    <button class="btn" onclick="quickDecision()">🎯 Decisión Rápida</button>
                    <button class="btn btn-danger" onclick="resetVCL()">🔄 Reiniciar</button>
                </div>
                
                <div id="result" style="margin-top: 20px; padding: 15px; background: rgba(255,255,255,0.05); border-radius: 10px; display: none;">
                    <!-- Resultados aparecen aquí -->
                </div>
            </div>
            
            <!-- Estado del sistema -->
            <div class="card">
                <h2>📊 Estado del Sistema</h2>
                <div id="system-status">
                    Cargando estado...
                </div>
                <div style="margin-top: 20px;">
                    <button class="btn" onclick="refreshStatus()">🔄 Actualizar Estado</button>
                    <a href="/vcl/status" target="_blank" class="btn" style="margin-left: 10px;">📋 JSON Completo</a>
                </div>
            </div>
            
            <!-- Integración VECTA -->
            <div class="card">
                <h2>🔄 Integración VECTA 12D</h2>
                <p style="margin-bottom: 15px; color: #a0d2ff;">
                    Conecta VCL con tus dimensiones vectoriales existentes.
                </p>
                <div style="display: flex; gap: 10px;">
                    <button class="btn" onclick="testIntegration()">🧪 Probar Integración</button>
                    <a href="/" class="btn">🏠 Volver a VECTA</a>
                </div>
                <div id="integration-result" style="margin-top: 20px;"></div>
            </div>
        </div>
        
        <!-- Historial -->
        <div class="card" style="margin-bottom: 40px;">
            <h2>📜 Historial de Decisiones</h2>
            <div id="history-container">
                Cargando historial...
            </div>
        </div>
    </div>
    
    <script>
        // Función para analizar texto VCL
        function analyzeVCL() {
            const input = document.getElementById('vcl-input').value;
            const resultDiv = document.getElementById('result');
            
            fetch('/vcl/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({vcl_text: input})
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    resultDiv.innerHTML = `
                        <div style="color: #00ff88;">✅ Análisis completado</div>
                        <div style="margin-top: 10px;">Resultado: ${JSON.stringify(data.result, null, 2)}</div>
                    `;
                } else {
                    resultDiv.innerHTML = `
                        <div style="color: #ff416c;">❌ Error: ${data.error}</div>
                    `;
                }
                resultDiv.style.display = 'block';
                refreshStatus();
                loadHistory();
            })
            .catch(error => {
                resultDiv.innerHTML = `<div style="color: #ff416c;">❌ Error de red: ${error}</div>`;
                resultDiv.style.display = 'block';
            });
        }
        
        // Función para decisión rápida
        function quickDecision() {
            const resultDiv = document.getElementById('result');
            
            fetch('/vcl/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({quick: true})
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const result = data.result;
                    resultDiv.innerHTML = `
                        <div style="color: #00ff88;">✅ Decisión tomada</div>
                        <div style="margin-top: 10px; font-size: 2em; text-align: center;">${result.symbol || '⟐'}</div>
                        <div style="text-align: center; margin-top: 10px;">${result.recommendation || 'Procede con conciencia'}</div>
                        <div style="margin-top: 10px; color: #a0d2ff;">Peso: ${result.weight ? result.weight.toFixed(2) : 'N/A'}</div>
                    `;
                } else {
                    resultDiv.innerHTML = `
                        <div style="color: #ff416c;">❌ Error: ${data.error}</div>
                    `;
                }
                resultDiv.style.display = 'block';
                refreshStatus();
                loadHistory();
            });
        }
        
        // Función para reiniciar VCL
        function resetVCL() {
            if (confirm('¿Estás seguro de reiniciar VCL? Se perderán los símbolos personalizados.')) {
                fetch('/vcl/reset')
                    .then(response => response.json())
                    .then(data => {
                        alert(data.message || 'VCL reiniciado');
                        refreshStatus();
                        loadHistory();
                    });
            }
        }
        
        // Función para cargar estado del sistema
        function refreshStatus() {
            fetch('/vcl/status')
                .then(response => response.json())
                .then(data => {
                    const statusDiv = document.getElementById('system-status');
                    statusDiv.innerHTML = `
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
                            <div>
                                <div style="color: #a0d2ff;">Versión</div>
                                <div style="font-size: 1.2em;">${data.version || '1.0.0'}</div>
                            </div>
                            <div>
                                <div style="color: #a0d2ff;">Disponible</div>
                                <div style="font-size: 1.2em; color: ${data.available ? '#00ff88' : '#ff416c'}">
                                    ${data.available ? '✅ Sí' : '❌ No'}
                                </div>
                            </div>
                            <div>
                                <div style="color: #a0d2ff;">Símbolos activos</div>
                                <div style="font-size: 1.2em;">${data.symbols_custom || 0}</div>
                            </div>
                            <div>
                                <div style="color: #a0d2ff;">Historial</div>
                                <div style="font-size: 1.2em;">${data.history_count || 0}</div>
                            </div>
                        </div>
                    `;
                });
        }
        
        // Función para cargar historial
        function loadHistory() {
            fetch('/vcl/history')
                .then(response => response.json())
                .then(data => {
                    const historyDiv = document.getElementById('history-container');
                    if (data.history && data.history.length > 0) {
                        let historyHTML = '<div style="max-height: 300px; overflow-y: auto;">';
                        data.history.slice().reverse().forEach(item => {
                            historyHTML += `
                                <div style="padding: 10px; margin-bottom: 10px; background: rgba(255,255,255,0.05); border-radius: 8px;">
                                    <div style="color: #a0d2ff; font-size: 0.9em;">${item.timestamp || 'Sin fecha'}</div>
                                    <div>${item.decision || 'Sin decisión'}</div>
                                </div>
                            `;
                        });
                        historyHTML += '</div>';
                        historyDiv.innerHTML = historyHTML;
                    } else {
                        historyDiv.innerHTML = '<div style="color: #a0d2ff; text-align: center;">No hay historial aún</div>';
                    }
                });
        }
        
        // Función para probar integración
        function testIntegration() {
            const resultDiv = document.getElementById('integration-result');
            resultDiv.innerHTML = '<div style="color: #a0d2ff;">Probando integración...</div>';
            
            // Datos de ejemplo de VECTA
            const vectaData = {
                dimension_1: 0.9,
                dimension_2: 0.8,
                dimension_3: 0.7,
                dimension_4: 0.6
            };
            
            fetch('/vcl/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(vectaData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const result = data.result;
                    resultDiv.innerHTML = `
                        <div style="color: #00ff88;">✅ Integración funcionando</div>
                        <div style="margin-top: 10px;">
                            <strong>Símbolo:</strong> ${result.symbol || '⟐'}<br>
                            <strong>Recomendación:</strong> ${result.recommendation || 'N/A'}<br>
                            <strong>Estado cuántico:</strong> ${result.quantum_state || 'N/A'}
                        </div>
                    `;
                } else {
                    resultDiv.innerHTML = `<div style="color: #ff416c;">❌ Error: ${data.error}</div>`;
                }
            });
        }
        
        // Cargar datos iniciales
        document.addEventListener('DOMContentLoaded', function() {
            refreshStatus();
            loadHistory();
            
            // Actualizar automáticamente cada 30 segundos
            setInterval(refreshStatus, 30000);
            setInterval(loadHistory, 30000);
        });
    </script>
</body>
</html>
'''
    
    return VCL_DASHBOARD_HTML

@vcl_bp.route('/vcl/dashboard')
def serve_dashboard():
    """Sirve el dashboard VCL"""
    return render_template_string(VCL_DASHBOARD_HTML,
                                 base_symbols=[
                                     {"char": "⟐", "name": "INTENCIÓN", "desc": "Vector objetivo puro"},
                                     {"char": "⟡", "name": "RECURSO", "desc": "Capacidad disponible"},
                                     {"char": "⟁", "name": "ESTADO", "desc": "Estado del sistema"},
                                     {"char": "⟢", "name": "TIEMPO", "desc": "Horizonte temporal"},
                                     {"char": "⟂", "name": "RESTRICCIÓN", "desc": "Límite duro"},
                                     {"char": "⟣", "name": "INCERTIDUMBRE", "desc": "Desconocido explícito"},
                                     {"char": "⟠", "name": "DECISIÓN", "desc": "Estado final obligatorio"},
                                 ],
                                 symbols_count=12,
                                 history_count=5,
                                 vcl_available=VCL_AVAILABLE)

def register_vcl_blueprint(app):
    """Registra el blueprint VCL en una aplicación Flask"""
    app.register_blueprint(vcl_bp, url_prefix='/vcl')
    print("✅ Blueprint VCL registrado en la aplicación Flask")

if __name__ == "__main__":
    print("🚀 Dashboard VCL cargado correctamente")
    print("💡 Usa: from core.vcl_dashboard import register_vcl_blueprint")
    print("     para integrar con tu aplicación Flask existente")
'''
    
    def _get_vcl_config(self):
        """Retorna configuración VCL en JSON"""
        return '''{
  "vcl_configuration": {
    "version": "1.0.0",
    "creator": "Rafael Porley",
    "installation_date": "''' + datetime.now().isoformat() + '''",
    
    "core_components": [
      "vcl_engine.py",
      "vcl_integration.py", 
      "vcl_dashboard.py"
    ],
    
    "symbols": {
      "irreducible": [
        {"symbol": "⟐", "name": "INTENTION", "description": "Pure objective vector"},
        {"symbol": "⟡", "name": "RESOURCE_OR_ENERGY", "description": "Any available capacity"},
        {"symbol": "⟁", "name": "SYSTEM_STATE", "description": "Snapshot of conditions"},
        {"symbol": "⟢", "name": "TIME_OR_PHASE", "description": "Temporal horizon"},
        {"symbol": "⟂", "name": "CONSTRAINT", "description": "Hard boundary"},
        {"symbol": "⟣", "name": "UNCERTAINTY", "description": "Explicit unknown"},
        {"symbol": "⟠", "name": "DECISION_COLLAPSE", "description": "Mandatory final state"}
      ]
    },
    
    "integration": {
      "vecta_12d_mapping": {
        "dimension_1": "INTENTION",
        "dimension_2": "SYSTEM_STATE",
        "dimension_3": "SYSTEM_STATE",
        "dimension_4": "TIME_OR_PHASE",
        "dimension_5": "RESOURCE_OR_ENERGY",
        "dimension_6": "UNCERTAINTY",
        "dimension_7": "INTENTION",
        "dimension_8": "CONSTRAINT",
        "dimension_9": "UNCERTAINTY",
        "dimension_10": "INTENTION",
        "dimension_11": "CONSTRAINT",
        "dimension_12": "DECISION_COLLAPSE"
      }
    },
    
    "dashboard": {
      "url": "/vcl",
      "endpoints": [
        "/vcl/symbols",
        "/vcl/analyze",
        "/vcl/history",
        "/vcl/status",
        "/vcl/reset"
      ]
    },
    
    "auto_start": true,
    "log_level": "INFO"
  }
}
'''
    
    def _get_quickstart_guide(self):
        """Retorna guía de inicio rápido"""
        return '''# 🚀 GUÍA DE INICIO RÁPIDO VCL (VECTA Core Language)

## 📋 ¿Qué se instaló?

✅ **Motor VCL** (`core/vcl_engine.py`) - Procesamiento simbólico
✅ **Integración VECTA** (`core/vcl_integration.py`) - Conexión con 12D
✅ **Dashboard** (`core/vcl_dashboard.py`) - Interfaz web
✅ **Configuración** (`vcl_config.json`) - Ajustes del sistema
✅ **Scripts de utilidad** - Para uso rápido

## 🎯 USO INMEDIATO

### 1. USAR EN PYTHON:
```python
from core.vcl_engine import vcl_interpreter

# Decisión rápida
result = vcl_interpreter.quick_decision({
    "priority_forms": ["COMPLETE_PROJECT"],
    "constraints": ["TIME_LIMITED"]
})

print(f"Decisión: {result['collapsed_symbol'].form}")
print(f"Símbolo: {result['collapsed_symbol'].symbol_char}")