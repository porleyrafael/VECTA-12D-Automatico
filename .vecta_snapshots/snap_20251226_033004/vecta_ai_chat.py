#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VECTA AI CHAT - Sistema Autónomo de Comunicación Inteligente
============================================================
Sistema de chat autoprogramable que interpreta lenguaje natural
y ejecuta acciones automáticas en el sistema VECTA 12D.
"""

import os
import sys
import json
import time
import uuid
import shutil
import subprocess
import traceback
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import re

# ==================== CONFIGURACIÓN DEL SISTEMA ====================

class VECTAConfig:
    """Configuración global del sistema VECTA AI Chat"""
    
    def __init__(self):
        # Directorios del sistema
        self.BASE_DIR = Path(__file__).parent.absolute()
        self.CORE_DIR = self.BASE_DIR / "core"
        self.DIMENSIONS_DIR = self.BASE_DIR / "dimensiones"
        self.CHAT_DATA_DIR = self.BASE_DIR / "chat_data"
        self.CHAT_SESSIONS_DIR = self.CHAT_DATA_DIR / "sessions"
        self.CHAT_LOGS_DIR = self.CHAT_DATA_DIR / "logs"
        self.CHAT_BACKUPS_DIR = self.CHAT_DATA_DIR / "backups"
        self.LEARNING_DATA_DIR = self.CHAT_DATA_DIR / "learning"
        
        # Crear directorios necesarios
        self._create_directories()
        
        # Configuración del sistema
        self.VERSION = "4.1.0"
        self.CREATOR = "Rafael Porley"
        self.AUTO_EXECUTE = True
        self.AUTO_BACKUP = True
        self.MAX_HISTORY = 1000
        self.COMMAND_TIMEOUT = 60
        
        # Principios VECTA
        self.VECTA_PRINCIPLES = [
            "ALWAYS_DECIDE",
            "FINITE_TIME_COLLAPSE", 
            "NO_COMPLEXITY_WITHOUT_GAIN",
            "FULL_AUDITABILITY",
            "SEPARATION_OF_LAYERS"
        ]
        
        # Configuración de lenguaje natural
        self.NLP_PATTERNS = self._load_nlp_patterns()
        
    def _create_directories(self):
        """Crea todos los directorios necesarios"""
        directories = [
            self.CHAT_DATA_DIR,
            self.CHAT_SESSIONS_DIR,
            self.CHAT_LOGS_DIR,
            self.CHAT_BACKUPS_DIR,
            self.LEARNING_DATA_DIR
        ]
        
        for directory in directories:
            directory.mkdir(exist_ok=True)
            
    def _load_nlp_patterns(self) -> Dict[str, Dict]:
        """Carga patrones de lenguaje natural - VERSIÓN MEJORADA"""
        return {
            # ========== COMANDOS DEL SISTEMA ==========
            "system_status": {
                "patterns": [
                    r"(?:estado|status|situación|condición)(?: del sistema)?",
                    r"cómo está (?:el sistema|vecta)",
                    r"qué pasa con vecta",
                    r"información del sistema",
                    r"estado completo"
                ],
                "action": "system_status"
            },
            
            "system_help": {
                "patterns": [
                    r"ayuda|help|comandos|instrucciones",
                    r"qué puedes hacer",
                    r"cómo (?:usar|utilizar) (?:esto|vecta|el sistema)",
                    r"necesito ayuda",
                    r"muestra (?:la )?ayuda"
                ],
                "action": "show_help"
            },
            
            "list_dimensions": {
                "patterns": [
                    r"(?:listar|mostrar|ver) (?:las )?dimensiones",
                    r"cuáles son las dimensiones",
                    r"dimensiones (?:disponibles|existentes)",
                    r"muestra dimensiones"
                ],
                "action": "list_dimensions"
            },
            
            "create_report": {
                "patterns": [
                    r"(?:generar|crear|hacer) (?:un )?reporte",
                    r"necesito un reporte",
                    r"informe del sistema",
                    r"reporte completo"
                ],
                "action": "create_report"
            },
            
            "create_backup": {
                "patterns": [
                    r"(?:crear|hacer) (?:un )?backup",
                    r"(?:crear|hacer) (?:una )?copia de seguridad",
                    r"respaldar (?:el sistema|vecta)",
                    r"backup del sistema"
                ],
                "action": "create_backup"
            },
            
            "clean_system": {
                "patterns": [
                    r"(?:limpiar|borrar) (?:archivos|sistema)",
                    r"eliminar (?:temporales|basura)",
                    r"limpieza (?:del sistema|general)",
                    r"limpia (?:el )?sistema"
                ],
                "action": "clean_system"
            },
            
            "restart_system": {
                "patterns": [
                    r"(?:reiniciar|reinicar) (?:el sistema|vecta)",
                    r"empezar de nuevo",
                    r"resetear (?:sistema|vecta)"
                ],
                "action": "restart_system"
            },
            
            "exit_system": {
                "patterns": [
                    r"(?:salir|terminar|finalizar|exit|quit)",
                    r"cerrar (?:el sistema|vecta|chat)",
                    r"hasta luego|adiós"
                ],
                "action": "exit_system"
            },
            
            # ========== ACCIONES CON ARCHIVOS ==========
            "create_file": {
                "patterns": [
                    r"(?:crear|crea|hacer|generar|escribir) (?:un )?(?:archivo|fichero|módulo|script|código) (?:llamado|con nombre|denominado)? ?([a-zA-Z0-9_\-\.]+)",
                    r"crea (?:archivo|fichero|módulo|script) ([a-zA-Z0-9_\-\.]+)",
                    r"nuevo (?:archivo|módulo|fichero|script) (.+)",
                    r"generar (?:archivo|módulo|script) (.+)",
                    r"escribir (?:archivo|módulo) (.+)",
                    r"programa (?:archivo|módulo) (.+)",
                    r"construye (?:archivo|módulo) (.+)"
                ],
                "action": "create_file",
                "has_params": True
            },
            
            "modify_file": {
                "patterns": [
                    r"(?:modificar|editar|cambiar|revisar|ver|mostrar|leer) (?:el )?(?:archivo|fichero|módulo|código|script) ([a-zA-Z0-9_\-\.]+)",
                    r"actualizar (?:archivo|módulo|script) (.+)",
                    r"editar (.+)",
                    r"ver (?:el )?(?:código|contenido) (?:de |del )?([a-zA-Z0-9_\-\.]+)",
                    r"mostrar (?:el )?(?:archivo|módulo|script) (.+)",
                    r"leer (?:archivo|módulo|script) (.+)",
                    r"muestra (?:el )?contenido (?:de |del )?([a-zA-Z0-9_\-\.]+)"
                ],
                "action": "modify_file",
                "has_params": True
            },
            
            "run_script": {
                "patterns": [
                    r"(?:ejecutar|correr|run|lanzar) (?:el )?(?:archivo|script|programa) ([a-zA-Z0-9_\-\.]+\.py)",
                    r"ejecuta (.+\.py)",
                    r"corre el script (.+)",
                    r"run (.+\.py)"
                ],
                "action": "run_script",
                "has_params": True
            },
            
            "install_package": {
                "patterns": [
                    r"(?:instalar|agregar) (?:el )?(?:paquete|módulo|package) ([a-zA-Z0-9_\-]+)",
                    r"necesito instalar (.+)",
                    r"pip install (.+)"
                ],
                "action": "install_package",
                "has_params": True
            },
            
            # ========== PROCESAMIENTO VECTA ==========
            "analyze_with_vecta": {
                "patterns": [
                    r"(?:analizar|procesar|calcular) (?:con |usando )?vecta",
                    r"vecta (?:analiza|procesa|calcula)",
                    r"usar vecta para",
                    r"analiza (?:con |)vecta:?(.+)"
                ],
                "action": "analyze_with_vecta",
                "has_params": True
            },
            
            # ========== APRENDIZAJE AUTOMÁTICO ==========
            "teach_vecta": {
                "patterns": [
                    r"enseña a vecta:? cuando digo (.+) haz (.+)",
                    r"aprende esto:? (.+) significa (.+)",
                    r"recuerda que (.+) es (.+)",
                    r"enseña:? (.+) → (.+)"
                ],
                "action": "teach_vecta",
                "has_params": True
            },
            
            "show_learning": {
                "patterns": [
                    r"qué has aprendido",
                    r"muestra (?:tu )?aprendizaje",
                    r"conocimiento (?:de |)vecta",
                    r"aprendizaje (?:del )?sistema"
                ],
                "action": "show_learning"
            },
            
            # ========== CONSULTA GENERAL (por defecto) ==========
            "general_query": {
                "patterns": [r".+"],
                "action": "general_query",
                "default": True
            }
        }


class VECTALogger:
    """Sistema de logging y auditoría VECTA"""
    
    def __init__(self, config: VECTAConfig):
        self.config = config
        self.session_id = str(uuid.uuid4())[:8]
        self.log_file = config.CHAT_LOGS_DIR / f"vecta_chat_{datetime.now().strftime('%Y%m%d')}.log"
        self.session_file = config.CHAT_SESSIONS_DIR / f"session_{self.session_id}.json"
        
    def log(self, level: str, message: str, data: Dict = None):
        """Registra un mensaje en el log"""
        timestamp = datetime.now().isoformat()
        log_entry = {
            "timestamp": timestamp,
            "session_id": self.session_id,
            "level": level,
            "message": message,
            "data": data or {}
        }
        
        # Escribir en archivo de log
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
        
        # Mostrar en consola si es importante
        if level in ["ERROR", "WARNING", "ACTION", "LEARNING"]:
            print(f"[{level}] {message}")
            
    def save_session(self, session_data: Dict):
        """Guarda los datos de la sesión actual"""
        session_data["session_id"] = self.session_id
        session_data["last_updated"] = datetime.now().isoformat()
        
        with open(self.session_file, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, indent=2, ensure_ascii=False)
            
    def load_session(self, session_id: str = None) -> Optional[Dict]:
        """Carga una sesión específica o la última"""
        if session_id:
            session_file = self.config.CHAT_SESSIONS_DIR / f"session_{session_id}.json"
        else:
            # Buscar la sesión más reciente
            sessions = list(self.config.CHAT_SESSIONS_DIR.glob("session_*.json"))
            if not sessions:
                return None
            session_file = max(sessions, key=lambda x: x.stat().st_mtime)
            
        if session_file.exists():
            with open(session_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None


class VECTANLP:
    """Procesador de Lenguaje Natural para VECTA - VERSIÓN MEJORADA"""
    
    def __init__(self, config: VECTAConfig):
        self.config = config
        self.intent_cache = {}
        
    def extract_intent(self, text: str) -> Tuple[str, Dict, List]:
        """
        Extrae la intención del texto en lenguaje natural
        Retorna: (acción, parámetros, confianza)
        """
        # Limpiar texto: eliminar comillas al inicio y final
        text = text.strip()
        if (text.startswith('"') and text.endswith('"')) or (text.startswith("'") and text.endswith("'")):
            text = text[1:-1].strip()
        
        text_lower = text.lower()
        
        # Buscar coincidencia con patrones
        best_match = None
        best_params = {}
        best_confidence = 0
        
        for intent_name, intent_data in self.config.NLP_PATTERNS.items():
            for pattern in intent_data["patterns"]:
                # Intentar coincidencia exacta primero
                if re.fullmatch(pattern, text_lower):
                    params = self._extract_parameters(intent_data, text)
                    return intent_data["action"], params, 1.0
                
                # Buscar patrón en el texto
                match = re.search(pattern, text_lower)
                if match:
                    confidence = len(match.group()) / len(text_lower) if text_lower else 0
                    if confidence > best_confidence:
                        best_confidence = confidence
                        best_match = intent_data
                        best_params = self._extract_parameters(intent_data, text, match)
        
        # Si hay coincidencia buena (> 0.3), usarla
        if best_match and best_confidence > 0.3:
            return best_match["action"], best_params, best_confidence
        
        # Por defecto, consulta general
        for intent_name, intent_data in self.config.NLP_PATTERNS.items():
            if intent_data.get("default"):
                return intent_data["action"], {"original_text": text}, 0.1
        
        return "unknown", {"original_text": text}, 0.0
    
    def _extract_parameters(self, intent_data: Dict, text: str, match=None) -> Dict:
        """Extrae parámetros del texto"""
        params = {"original_text": text}
        
        if intent_data.get("has_params") and match:
            # Extraer grupos de captura
            if match.groups():
                for i, group in enumerate(match.groups(), 1):
                    if group:
                        params[f"param_{i}"] = group
        
        # Extraer nombres de archivos comunes
        file_patterns = [
            r'([a-zA-Z0-9_\-\.]+\.py)',  # Archivos .py
            r'([a-zA-Z0-9_\-\.]+\.txt)', # Archivos .txt
            r'([a-zA-Z0-9_\-\.]+\.json)', # Archivos .json
            r'([a-zA-Z0-9_\-\.]+\.md)',   # Archivos .md
        ]
        
        for pattern in file_patterns:
            file_match = re.search(pattern, text)
            if file_match:
                params["file_name"] = file_match.group(1)
                break
        
        # Extraer texto después de ":" para análisis
        if ":" in text:
            parts = text.split(":", 1)
            if len(parts) > 1:
                params["text_after_colon"] = parts[1].strip()
        
        return params


# ==================== SISTEMA DE APRENDIZAJE ====================

class VECTALearner:
    """Sistema de auto-aprendizaje para VECTA"""
    
    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = "chat_data/learning/learned_patterns.json"
        
        self.config_path = Path(config_path)
        self.learned_patterns = self._load_learned_patterns()
        
    def _load_learned_patterns(self) -> Dict:
        """Carga patrones aprendidos"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            "patterns": [],
            "command_mappings": {},
            "statistics": {
                "total_learned": 0,
                "successful_uses": 0,
                "last_updated": datetime.now().isoformat()
            }
        }
    
    def learn(self, user_input: str, correct_action: str, params: Dict = None) -> str:
        """Aprende un nuevo patrón"""
        pattern_key = self._simplify_text(user_input)
        
        self.learned_patterns["command_mappings"][pattern_key] = {
            "action": correct_action,
            "params": params or {},
            "learned_at": datetime.now().isoformat(),
            "uses": 0
        }
        
        self.learned_patterns["patterns"].append({
            "input": user_input,
            "action": correct_action,
            "params": params or {},
            "timestamp": datetime.now().isoformat()
        })
        
        self.learned_patterns["statistics"]["total_learned"] += 1
        self.learned_patterns["statistics"]["last_updated"] = datetime.now().isoformat()
        
        self._save_learned_patterns()
        
        return f"✅ Aprendido: '{user_input}' → {correct_action}"
    
    def get_suggestion(self, user_input: str) -> Optional[Dict]:
        """Obtiene sugerencia basada en aprendizaje previo"""
        simplified = self._simplify_text(user_input)
        
        # Buscar mapeo directo
        for pattern, mapping in self.learned_patterns["command_mappings"].items():
            if self._text_matches_pattern(simplified, pattern):
                # Incrementar contador de usos
                mapping["uses"] = mapping.get("uses", 0) + 1
                self.learned_patterns["statistics"]["successful_uses"] += 1
                self._save_learned_patterns()
                
                return {
                    "action": mapping["action"],
                    "params": mapping["params"],
                    "confidence": 0.9,
                    "source": "learned_pattern"
                }
        
        # Buscar similitudes
        for pattern_data in self.learned_patterns["patterns"]:
            similarity = self._calculate_similarity(user_input, pattern_data["input"])
            if similarity > 0.7:
                return {
                    "action": pattern_data["action"],
                    "params": pattern_data["params"],
                    "confidence": similarity,
                    "source": "similar_pattern"
                }
        
        return None
    
    def _text_matches_pattern(self, text: str, pattern: str) -> bool:
        """Verifica si el texto coincide con un patrón"""
        # Conversión simple: si el patrón está contenido en el texto o viceversa
        return pattern in text or text in pattern
    
    def _simplify_text(self, text: str) -> str:
        """Simplifica texto para comparación"""
        return text.lower().replace('"', '').replace("'", "").replace("¿", "").replace("?", "").replace("¡", "").replace("!", "").strip()
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calcula similitud entre dos textos"""
        words1 = set(self._simplify_text(text1).split())
        words2 = set(self._simplify_text(text2).split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union if union > 0 else 0.0
    
    def _save_learned_patterns(self):
        """Guarda patrones aprendidos"""
        self.config_path.parent.mkdir(exist_ok=True)
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.learned_patterns, f, indent=2, ensure_ascii=False)
    
    def get_stats(self) -> Dict:
        """Obtiene estadísticas de aprendizaje"""
        return {
            "total_learned": self.learned_patterns["statistics"]["total_learned"],
            "successful_uses": self.learned_patterns["statistics"]["successful_uses"],
            "unique_patterns": len(self.learned_patterns["command_mappings"]),
            "last_updated": self.learned_patterns["statistics"]["last_updated"]
        }
    
    def show_learning_report(self) -> str:
        """Muestra reporte de aprendizaje"""
        stats = self.get_stats()
        
        report = [
            "📊 REPORTE DE APRENDIZAJE VECTA",
            "=" * 50,
            f"Patrones aprendidos: {stats['total_learned']}",
            f"Usos exitosos: {stats['successful_uses']}",
            f"Patrones únicos: {stats['unique_patterns']}",
            f"Última actualización: {stats['last_updated']}",
            "",
            "🔍 PATRONES APRENDIDOS:"
        ]
        
        if self.learned_patterns["command_mappings"]:
            for pattern, data in list(self.learned_patterns["command_mappings"].items())[:10]:  # Mostrar primeros 10
                report.append(f"  • '{pattern}' → {data['action']} (usos: {data.get('uses', 0)})")
            
            if len(self.learned_patterns["command_mappings"]) > 10:
                report.append(f"  ... y {len(self.learned_patterns['command_mappings']) - 10} patrones más")
        else:
            report.append("  Aún no hay patrones aprendidos")
        
        return "\n".join(report)


# ==================== EJECUTOR DE ACCIONES ====================

class VECTAActionExecutor:
    """Ejecutor de acciones autónomo para VECTA"""
    
    def __init__(self, config: VECTAConfig, logger: VECTALogger):
        self.config = config
        self.logger = logger
        self.system_state = self._load_system_state()
        self.learner = VECTALearner()
        
    def execute(self, action: str, params: Dict) -> Dict:
        """
        Ejecuta una acción y retorna resultado
        Sigue principios VECTA: decisión, tiempo finito, auditabilidad
        """
        start_time = time.time()
        
        # CONSULTAR AL SISTEMA DE APRENDIZAJE
        original_text = params.get("original_text", "")
        learned_suggestion = self.learner.get_suggestion(original_text)
        
        if learned_suggestion and learned_suggestion["confidence"] > 0.8:
            # SOBREESCRIBIR con aprendizaje
            old_action = action
            action = learned_suggestion["action"]
            params.update(learned_suggestion["params"])
            
            self.logger.log("LEARNING", f"Usando aprendizaje: '{original_text}' → {action} (antes: {old_action})")
        
        # Registrar inicio de acción
        self.logger.log("ACTION", f"Iniciando acción: {action}", params)
        
        try:
            # Ejecutar acción según tipo
            if action == "system_status":
                result = self._action_system_status()
            elif action == "show_help":
                result = self._action_show_help()
            elif action == "list_dimensions":
                result = self._action_list_dimensions()
            elif action == "create_report":
                result = self._action_create_report()
            elif action == "create_backup":
                result = self._action_create_backup()
            elif action == "clean_system":
                result = self._action_clean_system()
            elif action == "restart_system":
                result = self._action_restart_system()
            elif action == "exit_system":
                result = self._action_exit_system()
            elif action == "analyze_with_vecta":
                result = self._action_analyze_with_vecta(params)
            elif action == "run_script":
                result = self._action_run_script(params)
            elif action == "create_file":
                result = self._action_create_file(params)
            elif action == "modify_file":
                result = self._action_modify_file(params)
            elif action == "install_package":
                result = self._action_install_package(params)
            elif action == "teach_vecta":
                result = self._action_teach_vecta(params)
            elif action == "show_learning":
                result = self._action_show_learning()
            elif action == "general_query":
                result = self._action_general_query(params)
            else:
                result = self._action_unknown(params)
            
            # Verificar tiempo de ejecución (principio de tiempo finito)
            exec_time = time.time() - start_time
            if exec_time > self.config.COMMAND_TIMEOUT:
                result["warning"] = f"Acción tardó {exec_time:.2f}s (límite: {self.config.COMMAND_TIMEOUT}s)"
                self.logger.log("WARNING", f"Acción {action} excedió tiempo", {"time": exec_time})
            
            # Agregar metadatos VECTA
            result["vecta_metadata"] = {
                "execution_time": exec_time,
                "action": action,
                "timestamp": datetime.now().isoformat(),
                "principles_applied": self._get_applied_principles(action),
                "learned_suggestion_used": learned_suggestion is not None
            }
            
            # Registrar éxito
            self.logger.log("INFO", f"Acción {action} completada", {
                "time": exec_time,
                "success": result.get("success", True)
            })
            
            return result
            
        except Exception as e:
            # Registrar error (principio de auditabilidad)
            exec_time = time.time() - start_time
            error_info = {
                "action": action,
                "error": str(e),
                "traceback": traceback.format_exc(),
                "execution_time": exec_time
            }
            
            self.logger.log("ERROR", f"Error en acción {action}", error_info)
            
            # OFRECER ENSEÑAR ESTE ERROR
            teach_suggestion = ""
            if "original_text" in params:
                teach_suggestion = f"\n💡 ¿Quieres enseñarme este comando?\n   Di: 'enseña a vecta: cuando digo \"{params['original_text']}\" haz [acción correcta]'"
            
            return {
                "success": False,
                "type": "error",
                "error": str(e),
                "action": action,
                "content": f"❌ Error en acción: {str(e)}{teach_suggestion}",
                "vecta_metadata": {
                    "execution_time": exec_time,
                    "error_handled": True,
                    "principles_violated": ["NO_COMPLEXITY_WITHOUT_GAIN"] if exec_time > 10 else []
                }
            }
    
    def _load_system_state(self) -> Dict:
        """Carga el estado actual del sistema"""
        return {
            "vecta_core": self._check_vecta_core(),
            "dimensions": self._count_dimensions(),
            "python_version": sys.version.split()[0],
            "platform": sys.platform,
            "files_count": len(list(self.config.BASE_DIR.glob("*.py"))),
            "last_updated": datetime.now().isoformat()
        }
    
    def _check_vecta_core(self) -> bool:
        """Verifica si el núcleo VECTA está disponible"""
        core_files = [
            "core/vecta_12d_core.py",
            "core/meta_vecta.py",
            "dimensiones/vector_12d.py"
        ]
        
        for file in core_files:
            if not (self.config.BASE_DIR / file).exists():
                return False
        return True
    
    def _count_dimensions(self) -> int:
        """Cuenta las dimensiones disponibles"""
        if not self.config.DIMENSIONS_DIR.exists():
            return 0
        
        dimension_files = list(self.config.DIMENSIONS_DIR.glob("dimension_*.py"))
        return len(dimension_files)
    
    def _get_applied_principles(self, action: str) -> List[str]:
        """Determina qué principios VECTA se aplicaron"""
        principles = ["FULL_AUDITABILITY"]  # Siempre se aplica
        
        if action not in ["unknown", "general_query"]:
            principles.append("ALWAYS_DECIDE")
        
        # Verificar tiempo finito
        principles.append("FINITE_TIME_COLLAPSE")
        
        return principles
    
    # ==================== ACCIONES DEL SISTEMA ====================
    
    def _action_system_status(self) -> Dict:
        """Acción: Mostrar estado del sistema"""
        self.system_state = self._load_system_state()  # Actualizar
        
        status_text = f"""
╔══════════════════════════════════════════════════════════════╗
║                    VECTA 12D - ESTADO DEL SISTEMA           ║
╚══════════════════════════════════════════════════════════════╝

VERSIÓN: {self.config.VERSION}
CREADOR: {self.config.CREATOR}
SESSION: {self.logger.session_id}

COMPONENTES:
  • Núcleo VECTA: {'✅ ACTIVO' if self.system_state['vecta_core'] else '❌ INACTIVO'}
  • Dimensiones: {self.system_state['dimensions']}/12
  • Archivos Python: {self.system_state['files_count']}
  • Python: {self.system_state['python_version']}
  • Plataforma: {self.system_state['platform']}

DIRECTORIOS:
  • Principal: {self.config.BASE_DIR}
  • Datos Chat: {self.config.CHAT_DATA_DIR}
  • Aprendizaje: {self.config.LEARNING_DATA_DIR}

PRINCIPIOS VECTA:
"""
        
        for principle in self.config.VECTA_PRINCIPLES:
            status_text += f"  • {principle}\n"
        
        # Agregar estadísticas de aprendizaje
        stats = self.learner.get_stats()
        status_text += f"\n🧠 APRENDIZAJE AUTOMÁTICO:\n"
        status_text += f"  • Patrones aprendidos: {stats['total_learned']}\n"
        status_text += f"  • Usos exitosos: {stats['successful_uses']}\n"
        status_text += f"  • Última actualización: {stats['last_updated']}\n"
        
        return {
            "success": True,
            "type": "system_status",
            "content": status_text,
            "data": self.system_state
        }
    
    def _action_show_help(self) -> Dict:
        """Acción: Mostrar ayuda del sistema"""
        help_text = f"""
╔══════════════════════════════════════════════════════════════╗
║                    VECTA AI CHAT - AYUDA v{self.config.VERSION}           ║
╚══════════════════════════════════════════════════════════════╝

COMUNICACIÓN EN LENGUAJE NATURAL:
  Habla normalmente, VECTA entenderá tu intención.

📊 CONSULTAS DEL SISTEMA:
  • "¿Cómo está el sistema?"
  • "Muéstrame las dimensiones"
  • "Genera un reporte"
  • "Haz un backup del sistema"

🛠️ ACCIONES CON ARCHIVOS:
  • "Crea un archivo llamado ejemplo.py"
  • "Crea módulo test.py" (formato simplificado)
  • "Modifica el archivo config.json"
  • "Ver el contenido de vecta_learner.py"
  • "Ejecuta el script prueba_vecta.py"

🧠 PROCESAMIENTO CON VECTA:
  • "Analiza esto con VECTA: [texto]"
  • "Procesa esta información usando las 12 dimensiones"
  • "Calcula el vector para esta frase"

🎓 AUTO-APRENDIZAJE:
  • "Enseña a vecta: cuando digo 'programa código' haz 'crear archivo'"
  • "Aprende esto: 'generar script' significa 'crear archivo'"
  • "¿Qué has aprendido hasta ahora?"
  • "Muestra tu conocimiento"

🔧 MANTENIMIENTO:
  • "Limpia el sistema"
  • "Reinicia VECTA"
  • "Salir del chat"

💡 EJEMPLOS COMPLETOS:
  • "VECTA, analiza este proyecto usando todas las dimensiones"
  • "Por favor, ejecuta el script de prueba y dime el resultado"
  • "Necesito crear un nuevo módulo para procesamiento de texto"
  • "Enseña a vecta que cuando digo 'construye' quiero decir 'crear archivo'"

Sistema VECTA 12D - Creado por {self.config.CREATOR}
"""
        
        return {
            "success": True,
            "type": "help",
            "content": help_text
        }
    
    def _action_list_dimensions(self) -> Dict:
        """Acción: Listar dimensiones disponibles"""
        dimensions = []
        
        if self.config.DIMENSIONS_DIR.exists():
            for i in range(1, 13):
                dim_file = self.config.DIMENSIONS_DIR / f"dimension_{i}.py"
                if dim_file.exists():
                    try:
                        with open(dim_file, 'r', encoding='utf-8') as f:
                            content = f.read(200)
                            class_match = re.search(r'class\s+(\w+)', content)
                            class_name = class_match.group(1) if class_match else f"Dimension_{i}"
                            dimensions.append({
                                "number": i,
                                "file": dim_file.name,
                                "class": class_name,
                                "size": dim_file.stat().st_size
                            })
                    except:
                        dimensions.append({
                            "number": i,
                            "file": dim_file.name,
                            "status": "ERROR_READING"
                        })
                else:
                    dimensions.append({
                        "number": i,
                        "status": "MISSING"
                    })
        
        # Formatear respuesta
        if not dimensions:
            content = "❌ No se encontraron dimensiones en el sistema."
        else:
            content = "📊 DIMENSIONES VECTA 12D:\n\n"
            for dim in dimensions:
                if dim.get("status") == "MISSING":
                    content += f"  {dim['number']:2d}. ❌ FALTANTE\n"
                elif dim.get("status") == "ERROR_READING":
                    content += f"  {dim['number']:2d}. ⚠️  ERROR\n"
                else:
                    content += f"  {dim['number']:2d}. ✅ {dim['class']} ({dim['file']}, {dim['size']} bytes)\n"
        
        return {
            "success": True,
            "type": "dimensions_list",
            "content": content,
            "dimensions": dimensions,
            "total": len([d for d in dimensions if d.get("status") != "MISSING"])
        }
    
    def _action_create_report(self) -> Dict:
        """Acción: Crear reporte del sistema"""
        try:
            # Buscar script de reporte existente
            report_script = self.config.BASE_DIR / "generar_reporte_completo.py"
            if report_script.exists():
                result = subprocess.run(
                    [sys.executable, str(report_script)],
                    capture_output=True,
                    text=True,
                    cwd=str(self.config.BASE_DIR),
                    timeout=30
                )
                
                content = result.stdout if result.returncode == 0 else result.stderr
                success = result.returncode == 0
            else:
                # Crear reporte básico
                content = self._generate_basic_report()
                success = True
            
            # Guardar reporte en archivo
            report_file = self.config.CHAT_LOGS_DIR / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return {
                "success": success,
                "type": "report",
                "content": f"✅ Reporte generado exitosamente\n📄 Guardado en: {report_file}\n\n{content[:500]}..." if len(content) > 500 else content,
                "file": str(report_file),
                "file_size": len(content)
            }
            
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "type": "report",
                "error": "Timeout al generar reporte",
                "content": "El reporte tardó más de 30 segundos en generarse"
            }
        except Exception as e:
            return {
                "success": False,
                "type": "report",
                "error": str(e),
                "content": f"Error al generar reporte: {str(e)}"
            }
    
    def _generate_basic_report(self) -> str:
        """Genera un reporte básico del sistema"""
        stats = self.learner.get_stats()
        
        report = [
            "=" * 70,
            f"REPORTE VECTA 12D - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "=" * 70,
            f"Sistema: VECTA AI Chat v{self.config.VERSION}",
            f"Directorio: {self.config.BASE_DIR}",
            "",
            "ESTADÍSTICAS:",
            f"  • Archivos .py: {len(list(self.config.BASE_DIR.glob('*.py')))}",
            f"  • Directorios: {len([d for d in self.config.BASE_DIR.iterdir() if d.is_dir()])}",
            f"  • Dimensiones cargadas: {self.system_state['dimensions']}/12",
            f"  • Sesiones guardadas: {len(list(self.config.CHAT_SESSIONS_DIR.glob('*.json')))}",
            f"  • Logs del día: {len(list(self.config.CHAT_LOGS_DIR.glob('*.log')))}",
            "",
            "APRENDIZAJE AUTOMÁTICO:",
            f"  • Patrones aprendidos: {stats['total_learned']}",
            f"  • Usos exitosos: {stats['successful_uses']}",
            f"  • Patrones únicos: {stats['unique_patterns']}",
            "",
            "ARCHIVOS CRÍTICOS:"
        ]
        
        critical_files = [
            "vecta_ai_chat.py",
            "core/vecta_12d_core.py",
            "core/meta_vecta.py",
            "dimensiones/vector_12d.py"
        ]
        
        for file in critical_files:
            file_path = self.config.BASE_DIR / file
            if file_path.exists():
                report.append(f"  ✅ {file}")
            else:
                report.append(f"  ❌ {file} (FALTANTE)")
        
        report.append("")
        report.append("PRINCIPIOS VECTA ACTIVOS:")
        for principle in self.config.VECTA_PRINCIPLES:
            report.append(f"  • {principle}")
        
        report.append("")
        report.append("=" * 70)
        
        return "\n".join(report)
    
    def _action_create_backup(self) -> Dict:
        """Acción: Crear backup del sistema"""
        try:
            backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            backup_dir = self.config.CHAT_BACKUPS_DIR / backup_name
            
            # Crear directorio de backup
            backup_dir.mkdir(exist_ok=True)
            
            # Copiar archivos importantes
            files_to_backup = [
                "*.py",
                "*.json",
                "*.txt",
                "*.md",
                "*.bat"
            ]
            
            copied_files = 0
            for pattern in files_to_backup:
                for file in self.config.BASE_DIR.glob(pattern):
                    try:
                        if file.is_file():
                            shutil.copy2(file, backup_dir / file.name)
                            copied_files += 1
                    except:
                        pass
            
            # Copiar directorios importantes
            dirs_to_backup = ["core", "dimensiones", "chat_data"]
            for dir_name in dirs_to_backup:
                dir_path = self.config.BASE_DIR / dir_name
                if dir_path.exists():
                    dest_dir = backup_dir / dir_name
                    shutil.copytree(dir_path, dest_dir, dirs_exist_ok=True)
                    copied_files += len(list(dir_path.rglob("*")))
            
            # Crear metadata del backup
            metadata = {
                "backup_name": backup_name,
                "timestamp": datetime.now().isoformat(),
                "files_copied": copied_files,
                "system_state": self.system_state,
                "vecta_version": self.config.VERSION,
                "learning_stats": self.learner.get_stats()
            }
            
            metadata_file = backup_dir / "backup_metadata.json"
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2)
            
            return {
                "success": True,
                "type": "backup",
                "content": f"✅ Backup creado exitosamente\n📂 Directorio: {backup_dir}\n📊 Archivos copiados: {copied_files}",
                "backup_dir": str(backup_dir),
                "files_count": copied_files,
                "metadata": metadata
            }
            
        except Exception as e:
            return {
                "success": False,
                "type": "backup",
                "error": str(e),
                "content": f"❌ Error al crear backup: {str(e)}"
            }
    
    def _action_clean_system(self) -> Dict:
        """Acción: Limpiar sistema de archivos temporales"""
        try:
            deleted_items = []
            
            # Eliminar archivos .pyc
            for pyc_file in self.config.BASE_DIR.rglob("*.pyc"):
                try:
                    pyc_file.unlink()
                    deleted_items.append(str(pyc_file))
                except:
                    pass
            
            # Eliminar directorios __pycache__
            for cache_dir in self.config.BASE_DIR.rglob("__pycache__"):
                try:
                    shutil.rmtree(cache_dir)
                    deleted_items.append(str(cache_dir))
                except:
                    pass
            
            return {
                "success": True,
                "type": "cleanup",
                "content": f"✅ Sistema limpiado exitosamente\n🗑️  Elementos eliminados: {len(deleted_items)}",
                "deleted_count": len(deleted_items),
                "deleted_items": deleted_items[:10]
            }
            
        except Exception as e:
            return {
                "success": False,
                "type": "cleanup",
                "error": str(e),
                "content": f"❌ Error al limpiar sistema: {str(e)}"
            }
    
    def _action_restart_system(self) -> Dict:
        """Acción: Reiniciar sistema (simulado)"""
        return {
            "success": True,
            "type": "restart",
            "content": "🔄 Sistema VECTA reiniciado\n💾 Estado guardado\n✨ Listo para continuar",
            "requires_restart": True
        }
    
    def _action_exit_system(self) -> Dict:
        """Acción: Salir del sistema"""
        return {
            "success": True,
            "type": "exit",
            "content": f"👋 Sesión finalizada\n📊 Resumen:\n  • Sistema VECTA 12D Chat v{self.config.VERSION}\n  • Sesión: {self.logger.session_id}\n  • Gracias por usar VECTA",
            "requires_exit": True
        }
    
    def _action_analyze_with_vecta(self, params: Dict) -> Dict:
        """Acción: Analizar texto con VECTA"""
        text = params.get("original_text", "")
        text_after_colon = params.get("text_after_colon", "")
        
        # Extraer texto para análisis
        if text_after_colon:
            analysis_text = text_after_colon
        else:
            # Intentar extraer texto después de "analiza" o "procesa"
            analysis_match = re.search(r'(?:analiza|procesa|calcula)[\s\:]+(.+)', text, re.IGNORECASE)
            analysis_text = analysis_match.group(1).strip() if analysis_match else text
        
        if not analysis_text or len(analysis_text) < 3:
            return {
                "success": False,
                "type": "vecta_analysis",
                "content": "❌ No se especificó texto para analizar\n💡 Ejemplo: 'Analiza con VECTA: Este es un proyecto importante'",
                "error": "No text provided"
            }
        
        try:
            # Intentar importar y usar VECTA core
            sys.path.insert(0, str(self.config.BASE_DIR))
            
            from core.vecta_12d_core import VECTA_12D_Core
            
            vecta = VECTA_12D_Core()
            result = vecta.procesar(analysis_text)
            
            if result.get("exito"):
                content = f"""
✅ Análisis VECTA completado:

📝 Texto analizado: "{analysis_text[:100]}{'...' if len(analysis_text) > 100 else ''}"

📊 Resultados:
  • Magnitud vectorial: {result.get('magnitud', 0):.4f}
  • Dimensiones activas: {len(result.get('dimensiones', []))}
  • Procesamiento exitoso

🔍 Detalles dimensionales:"""
                
                dims = result.get('dimensiones', [])
                for i, val in enumerate(dims[:6], 1):
                    content += f"\n    D{i}: {val:.4f}"
                
                if len(dims) > 6:
                    content += f"\n    ... y {len(dims)-6} dimensiones más"
                
                return {
                    "success": True,
                    "type": "vecta_analysis",
                    "content": content,
                    "data": result,
                    "text_analyzed": analysis_text
                }
            else:
                return {
                    "success": False,
                    "type": "vecta_analysis",
                    "content": f"❌ Error en análisis VECTA: {result.get('error', 'Error desconocido')}",
                    "error": result.get("error")
                }
                
        except ImportError:
            return {
                "success": False,
                "type": "vecta_analysis",
                "content": "❌ Núcleo VECTA no disponible\n🔧 Ejecuta 'estado' para verificar el sistema",
                "error": "VECTA core not available"
            }
        except Exception as e:
            return {
                "success": False,
                "type": "vecta_analysis",
                "content": f"❌ Error en análisis: {str(e)}",
                "error": str(e)
            }
    
    def _action_run_script(self, params: Dict) -> Dict:
        """Acción: Ejecutar script Python"""
        script_name = params.get("file_name") or params.get("param_1")
        
        if not script_name:
            return {
                "success": False,
                "type": "script_execution",
                "content": "❌ No se especificó archivo a ejecutar\n💡 Ejemplo: 'Ejecuta prueba_vecta.py'",
                "error": "No script specified"
            }
        
        # Asegurar extensión .py si no la tiene
        if not script_name.endswith('.py'):
            script_name += '.py'
        
        script_path = self.config.BASE_DIR / script_name
        
        if not script_path.exists():
            return {
                "success": False,
                "type": "script_execution",
                "content": f"❌ Archivo no encontrado: {script_name}\n📂 Directorio actual: {self.config.BASE_DIR}",
                "error": "File not found"
            }
        
        try:
            result = subprocess.run(
                [sys.executable, str(script_path)],
                capture_output=True,
                text=True,
                cwd=str(self.config.BASE_DIR),
                timeout=self.config.COMMAND_TIMEOUT
            )
            
            output = result.stdout if result.stdout else "(sin salida)"
            error = result.stderr if result.stderr else "(sin errores)"
            
            content = f"""
✅ Script ejecutado: {script_name}

📊 Resultado:
  • Código de salida: {result.returncode}
  • Tiempo límite: {self.config.COMMAND_TIMEOUT}s

📄 Salida:"""
            
            # Limitar tamaño de salida
            if len(output) > 1000:
                content += f"\n{output[:500]}\n... [salida truncada, {len(output)} caracteres totales] ...\n{output[-500:]}"
            else:
                content += f"\n{output}"
            
            if result.returncode != 0:
                content += f"\n\n❌ Errores:\n{error}"
            
            return {
                "success": result.returncode == 0,
                "type": "script_execution",
                "content": content,
                "return_code": result.returncode,
                "output": output,
                "error": error,
                "script": script_name
            }
            
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "type": "script_execution",
                "content": f"❌ Timeout: El script {script_name} tardó más de {self.config.COMMAND_TIMEOUT} segundos",
                "error": "Timeout expired"
            }
        except Exception as e:
            return {
                "success": False,
                "type": "script_execution",
                "content": f"❌ Error al ejecutar script: {str(e)}",
                "error": str(e)
            }
    
    def _action_create_file(self, params: Dict) -> Dict:
        """Acción: Crear nuevo archivo"""
        file_name = params.get("file_name") or params.get("param_1")
        
        if not file_name:
            return {
                "success": False,
                "type": "file_creation",
                "content": "❌ No se especificó nombre de archivo\n💡 Ejemplo: 'Crea un archivo test.py'",
                "error": "No filename specified"
            }
        
        # Asegurar extensión .py si no la tiene y es un módulo
        if not '.' in file_name and not file_name.endswith('.py'):
            file_name += '.py'
        
        file_path = self.config.BASE_DIR / file_name
        
        # Verificar si ya existe
        if file_path.exists():
            return {
                "success": False,
                "type": "file_creation", 
                "content": f"❌ El archivo ya existe: {file_name}",
                "error": "File already exists"
            }
        
        try:
            # Determinar tipo de archivo por extensión
            if file_name.endswith('.py'):
                content = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
{file_name.upper().replace('.PY', '')} - Módulo generado por VECTA AI Chat
Fecha: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Versión VECTA: {self.config.VERSION}
"""

def main():
    """Función principal"""
    print("¡Archivo creado por VECTA 12D AI Chat!")
    print("Sistema de auto-aprendizaje y auto-programación")

if __name__ == "__main__":
    main()
'''
            elif file_name.endswith('.json'):
                content = json.dumps({
                    "created_by": "VECTA AI Chat",
                    "timestamp": datetime.now().isoformat(),
                    "version": self.config.VERSION,
                    "purpose": "Archivo de configuración generado automáticamente",
                    "vecta_principles": self.config.VECTA_PRINCIPLES
                }, indent=2)
            elif file_name.endswith('.txt'):
                content = f"""Archivo creado por VECTA AI Chat
Fecha: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Versión: {self.config.VERSION}
Sistema: VECTA 12D - Auto-programación

Este archivo fue generado automáticamente por el sistema
de aprendizaje y auto-programación VECTA 12D.
"""
            else:
                content = f"""Archivo: {file_name}
Creado por VECTA AI Chat
Fecha: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Versión: {self.config.VERSION}

Sistema VECTA 12D - Auto-programación
"""
            
            # Crear archivo
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # APRENDER ESTE PATRÓN SI VIENE DE UN COMANDO NUEVO
            original_text = params.get("original_text", "")
            if original_text and "crea" in original_text.lower() and "archivo" in original_text.lower():
                # Verificar si es un patrón que deberíamos aprender
                if not any(word in original_text.lower() for word in ["llamado", "con nombre", "denominado"]):
                    # Es un patrón simplificado, aprenderlo
                    self.learner.learn(original_text, "create_file", {"file_name": file_name})
            
            return {
                "success": True,
                "type": "file_creation",
                "content": f"✅ Archivo creado: {file_name}\n📂 Ubicación: {file_path}\n📏 Tamaño: {len(content)} bytes",
                "file_path": str(file_path),
                "file_size": len(content)
            }
            
        except Exception as e:
            return {
                "success": False,
                "type": "file_creation",
                "content": f"❌ Error al crear archivo: {str(e)}",
                "error": str(e)
            }
    
    def _action_modify_file(self, params: Dict) -> Dict:
        """Acción: Modificar archivo existente (mostrar contenido)"""
        file_name = params.get("file_name") or params.get("param_1")
        
        if not file_name:
            return {
                "success": False,
                "type": "file_modification",
                "content": "❌ No se especificó archivo\n💡 Ejemplo: 'Ver vecta_learner.py'",
                "error": "No filename specified"
            }
        
        file_path = self.config.BASE_DIR / file_name
        
        if not file_path.exists():
            return {
                "success": False,
                "type": "file_modification",
                "content": f"❌ Archivo no encontrado: {file_name}",
                "error": "File not found"
            }
        
        try:
            stat = file_path.stat()
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Determinar tipo de archivo
            if file_name.endswith('.py'):
                file_type = "🐍 Módulo Python"
            elif file_name.endswith('.json'):
                file_type = "📊 Archivo JSON"
            elif file_name.endswith('.txt'):
                file_type = "📄 Archivo de texto"
            else:
                file_type = "📁 Archivo"
            
            content_display = f"""
{file_type}: {file_name}

📊 Detalles:
  • Tamaño: {stat.st_size} bytes
  • Última modificación: {datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')}
  • Ruta: {file_path}

{"="*60}
CONTENIDO:
{"="*60}
{content if len(content) <= 1000 else content[:1000] + "\n\n... [contenido truncado, " + str(len(content)) + " caracteres totales] ..."}
{"="*60}

💡 Para editar este archivo, usa un editor de texto externo.
"""
            
            return {
                "success": True,
                "type": "file_modification",
                "content": content_display,
                "file_path": str(file_path),
                "file_size": stat.st_size,
                "content_preview": content[:1000] if len(content) > 1000 else content
            }
            
        except Exception as e:
            return {
                "success": False,
                "type": "file_modification",
                "content": f"❌ Error al leer archivo: {str(e)}",
                "error": str(e)
            }
    
    def _action_install_package(self, params: Dict) -> Dict:
        """Acción: Instalar paquete Python"""
        package_name = params.get("param_1")
        
        if not package_name:
            return {
                "success": False,
                "type": "package_installation",
                "content": "❌ No se especificó paquete a instalar\n💡 Ejemplo: 'Instala numpy'",
                "error": "No package specified"
            }
        
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", package_name],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                content = f"✅ Paquete instalado: {package_name}\n\n📄 Salida:\n{result.stdout}"
            else:
                content = f"❌ Error al instalar {package_name}:\n{result.stderr}"
            
            return {
                "success": result.returncode == 0,
                "type": "package_installation",
                "content": content,
                "package": package_name,
                "output": result.stdout,
                "error": result.stderr if result.returncode != 0 else None
            }
            
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "type": "package_installation",
                "content": f"❌ Timeout: La instalación de {package_name} tardó más de 60 segundos",
                "error": "Installation timeout"
            }
        except Exception as e:
            return {
                "success": False,
                "type": "package_installation",
                "content": f"❌ Error en instalación: {str(e)}",
                "error": str(e)
            }
    
    def _action_teach_vecta(self, params: Dict) -> Dict:
        """Acción: Enseñar a VECTA un nuevo comando"""
        original_text = params.get("original_text", "")
        
        # Extraer partes del patrón de enseñanza
        # Formato: "enseña a vecta: cuando digo X haz Y"
        # O: "cuando digo X haz Y"
        
        user_input = None
        action_to_learn = None
        
        # Patrón 1: "enseña a vecta: cuando digo X haz Y"
        teach_match = re.search(r'enseña a vecta:? cuando digo (.+) haz (.+)', original_text, re.IGNORECASE)
        if teach_match:
            user_input = teach_match.group(1).strip().strip('"\'')
            action_to_learn = teach_match.group(2).strip().strip('"\'')
        
        # Patrón 2: "aprende esto: X significa Y"
        learn_match = re.search(r'aprende esto:? (.+) significa (.+)', original_text, re.IGNORECASE)
        if learn_match and not user_input:
            user_input = learn_match.group(1).strip().strip('"\'')
            action_to_learn = learn_match.group(2).strip().strip('"\'')
        
        # Patrón 3: "recuerda que X es Y"
        remember_match = re.search(r'recuerda que (.+) es (.+)', original_text, re.IGNORECASE)
        if remember_match and not user_input:
            user_input = remember_match.group(1).strip().strip('"\'')
            action_to_learn = remember_match.group(2).strip().strip('"\'')
        
        if not user_input or not action_to_learn:
            return {
                "success": False,
                "type": "learning",
                "content": "❌ Formato incorrecto\n💡 Usa: 'Enseña a vecta: cuando digo \"programa código\" haz \"crear archivo\"'",
                "error": "Invalid teaching format"
            }
        
        # Mapear acción a acción interna
        action_map = {
            "crear archivo": "create_file",
            "crea archivo": "create_file",
            "crear módulo": "create_file",
            "crea módulo": "create_file",
            "crear script": "create_file",
            "crea script": "create_file",
            
            "ejecutar": "run_script",
            "ejecuta": "run_script",
            "correr": "run_script",
            "run": "run_script",
            
            "analizar con vecta": "analyze_with_vecta",
            "analiza con vecta": "analyze_with_vecta",
            "procesar con vecta": "analyze_with_vecta",
            
            "estado": "system_status",
            "status": "system_status",
            "estado del sistema": "system_status",
            
            "ayuda": "show_help",
            "help": "show_help",
            
            "dimensiones": "list_dimensions",
            "lista dimensiones": "list_dimensions",
            
            "backup": "create_backup",
            "copia de seguridad": "create_backup",
            
            "limpiar": "clean_system",
            "limpiar sistema": "clean_system",
            
            "reiniciar": "restart_system",
            "reiniciar sistema": "restart_system",
            
            "salir": "exit_system",
            "exit": "exit_system"
        }
        
        # Buscar acción mapeada o usar directamente
        mapped_action = action_map.get(action_to_learn.lower())
        if not mapped_action:
            mapped_action = action_to_learn
        
        # Extraer parámetros si es creación de archivo
        file_param = None
        if mapped_action == "create_file":
            # Intentar extraer nombre de archivo del user_input
            file_match = re.search(r'([a-zA-Z0-9_\-\.]+\.py)', user_input)
            if file_match:
                file_param = file_match.group(1)
            else:
                # Si no tiene extensión, agregar .py
                words = user_input.split()
                if words:
                    last_word = words[-1]
                    if '.' not in last_word:
                        file_param = last_word + '.py'
        
        params_to_learn = {}
        if file_param:
            params_to_learn["file_name"] = file_param
        
        # Enseñar al sistema
        result = self.learner.learn(user_input, mapped_action, params_to_learn)
        
        return {
            "success": True,
            "type": "learning",
            "content": f"🧠 VECTA HA APRENDIDO\n\n{result}\n\nAhora cuando digas:\n  \"{user_input}\"\n\nVECTA hará:\n  {mapped_action}" + (f" con parámetros {params_to_learn}" if params_to_learn else ""),
            "learned_input": user_input,
            "learned_action": mapped_action,
            "params": params_to_learn
        }
    
    def _action_show_learning(self) -> Dict:
        """Acción: Mostrar lo que ha aprendido VECTA"""
        report = self.learner.show_learning_report()
        
        return {
            "success": True,
            "type": "learning_report",
            "content": report,
            "stats": self.learner.get_stats()
        }
    
    def _action_general_query(self, params: Dict) -> Dict:
        """Acción: Procesar consulta general"""
        text = params.get("original_text", "")
        
        # Respuestas inteligentes basadas en contenido
        if any(word in text.lower() for word in ['hola', 'hello', 'hi', 'buenas', 'buenos días', 'buenas tardes']):
            response = f"👋 ¡Hola! Soy VECTA AI Chat v{self.config.VERSION}\n¿En qué puedo ayudarte hoy?"
        elif any(word in text.lower() for word in ['gracias', 'thanks', 'thank you', 'merci']):
            response = "🙏 ¡De nada! Siempre estoy aquí para ayudarte con VECTA 12D."
        elif any(word in text.lower() for word in ['bien', 'excelente', 'genial', 'perfecto']):
            response = "😊 ¡Me alegra! ¿En qué más puedo asistirte?"
        elif '?' in text:
            response = f"🤔 Interesante pregunta.\n\nPuedo ayudarte mejor si me dices qué quieres hacer:\n• ¿Consultar el estado del sistema?\n• ¿Ejecutar algún script?\n• ¿Analizar algo con VECTA?\n• ¿Crear o modificar archivos?\n\nO escribe 'ayuda' para ver todas las opciones."
        elif any(word in text.lower() for word in ['vecta', 'sistema', 'proyecto']):
            response = f"💭 Detecté que hablas de VECTA.\n\nPuedo ayudarte con:\n• Análisis con las 12 dimensiones\n• Gestión del sistema\n• Creación de módulos\n• Auto-aprendizaje\n\n¿Qué necesitas específicamente?"
        else:
            # Intentar sugerir basado en palabras clave
            suggestions = []
            
            if any(word in text.lower() for word in ['crea', 'crear', 'hacer', 'nuevo', 'generar']):
                suggestions.append("• 'Crea archivo [nombre]' - Para crear nuevos archivos")
            
            if any(word in text.lower() for word in ['ejecuta', 'corre', 'run', 'lanzar']):
                suggestions.append("• 'Ejecuta [archivo.py]' - Para ejecutar scripts")
            
            if any(word in text.lower() for word in ['analiza', 'procesa', 'calcula', 'vecta']):
                suggestions.append("• 'Analiza con VECTA: [texto]' - Para análisis dimensional")
            
            if any(word in text.lower() for word in ['ver', 'mostrar', 'leer', 'modificar']):
                suggestions.append("• 'Ver [archivo.py]' - Para ver contenido de archivos")
            
            if any(word in text.lower() for word in ['enseña', 'aprende', 'recuerda']):
                suggestions.append("• 'Enseña a vecta: cuando digo X haz Y' - Para enseñarme nuevos comandos")
            
            if suggestions:
                suggestion_text = "\n".join(suggestions)
                response = f"💭 He procesado tu mensaje.\n\nBasado en lo que dijiste, quizás quieras:\n{suggestion_text}\n\nO escribe 'ayuda' para ver todos los comandos."
            else:
                response = f"💭 He procesado tu mensaje: '{text}'\n\nPara acciones específicas, intenta:\n• 'Ayuda' - Ver todos los comandos\n• 'Estado' - Ver sistema VECTA\n• 'Enseña a vecta' - Para enseñarme nuevos comandos"
        
        return {
            "success": True,
            "type": "general_response",
            "content": response,
            "original_text": text
        }
    
    def _action_unknown(self, params: Dict) -> Dict:
        """Acción: Comando desconocido"""
        text = params.get("original_text", "N/A")
        
        # OFRECER ENSEÑAR ESTE COMANDO
        teach_option = f"\n\n🎓 ¿Quieres que aprenda este comando?\n   Di: 'Enseña a vecta: cuando digo \"{text}\" haz [acción correcta]'"
        
        return {
            "success": False,
            "type": "unknown_command",
            "content": f"❓ VECTA no entendió completamente: '{text}'\n\n💡 Prueba con:\n• 'Ayuda' - Ver todos los comandos\n• 'Estado' - Ver sistema VECTA\n• Escribe en lenguaje natural lo que necesitas{teach_option}",
            "original_text": text,
            "can_learn": True
        }


class VECTAAIChat:
    """Sistema principal de chat VECTA AI"""
    
    def __init__(self):
        self.config = VECTAConfig()
        self.logger = VECTALogger(self.config)
        self.nlp = VECTANLP(self.config)
        self.executor = VECTAActionExecutor(self.config, self.logger)
        
        # Historial de chat
        self.chat_history = []
        self.max_history = self.config.MAX_HISTORY
        
        # Estado de la sesión
        self.session_data = {
            "session_id": self.logger.session_id,
            "start_time": datetime.now().isoformat(),
            "interaction_count": 0,
            "commands_executed": []
        }
        
    def display_banner(self):
        """Muestra el banner del sistema"""
        banner = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║    ██╗   ██╗███████╗ ██████╗████████╗ █████╗     █████╗ ██╗                 ║
║    ██║   ██║██╔════╝██╔════╝╚══██╔══╝██╔══██╗   ██╔══██╗██║                 ║
║    ██║   ██║█████╗  ██║        ██║   ███████║   ███████║██║                 ║
║    ╚██╗ ██╔╝██╔══╝  ██║        ██║   ██╔══██║   ██╔══██║██║                 ║
║     ╚████╔╝ ███████╗╚██████╗   ██║   ██║  ██║██╗██║  ██║███████╗            ║
║      ╚═══╝  ╚══════╝ ╚═════╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚══════╝            ║
║                                                                              ║
║                     VECTA 12D - AI CHAT INTERFACE                           ║
║                 Sistema Autónomo de Comunicación Inteligente                 ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

────────────────────────────────────────────────────────────────────────────────
  Versión: {self.config.VERSION}                Creador: {self.config.CREATOR}                Session: {self.logger.session_id}
────────────────────────────────────────────────────────────────────────────────

🎯 CARACTERÍSTICAS PRINCIPALES:
  • Lenguaje natural completo (español/inglés)
  • Ejecución automática de comandos
  • Integración total con VECTA 12D
  • Sistema de auto-aprendizaje
  • Auto-backup y recuperación
  • Auditoría completa (principio VECTA)

🧠 AUTO-APRENDIZAJE ACTIVO:
  • Puedo aprender nuevos comandos
  • Mejoro con el uso
  • Entiendo variaciones de lenguaje

💡 INSTRUCCIÓN:
  Escribe en lenguaje natural lo que necesitas. Ejemplos:
    • "Crea un archivo prueba.py"
    • "Ver el contenido de vecta_learner.py"
    • "Enseña a vecta: cuando digo 'programa' haz 'crear archivo'"
    • "¿Qué has aprendido hasta ahora?"

📝 Escribe 'ayuda' para ver la guía completa o 'salir' para terminar.
────────────────────────────────────────────────────────────────────────────────
"""
        
        print(banner)
    
    def process_input(self, user_input: str) -> Optional[Dict]:
        """
        Procesa la entrada del usuario y ejecuta la acción correspondiente
        Retorna None si se debe salir del sistema
        """
        if not user_input.strip():
            return {"content": "🔇 Entrada vacía. Por favor, escribe algo."}
        
        # Incrementar contador de interacciones
        self.session_data["interaction_count"] += 1
        
        # Registrar entrada del usuario
        self.chat_history.append({
            "type": "user",
            "content": user_input,
            "timestamp": datetime.now().isoformat()
        })
        
        # Extraer intención usando NLP
        action, params, confidence = self.nlp.extract_intent(user_input)
        
        # Log de intención detectada
        self.logger.log("INFO", f"Intención detectada: {action} (confianza: {confidence:.2f})", {
            "input": user_input,
            "params": params,
            "confidence": confidence
        })
        
        # Ejecutar acción
        result = self.executor.execute(action, params)
        
        # Registrar resultado
        self.session_data["commands_executed"].append({
            "action": action,
            "input": user_input,
            "timestamp": datetime.now().isoformat(),
            "success": result.get("success", False)
        })
        
        # Guardar en historial
        self.chat_history.append({
            "type": "vecta",
            "content": result.get("content", "Sin respuesta"),
            "action": action,
            "timestamp": datetime.now().isoformat(),
            "success": result.get("success", False)
        })
        
        # Mantener historial limitado
        if len(self.chat_history) > self.max_history * 2:
            self.chat_history = self.chat_history[-self.max_history*2:]
        
        # Verificar si hay que reiniciar o salir
        if result.get("requires_exit"):
            self._save_session()
            return None
        elif result.get("requires_restart"):
            self._save_session()
            # Simular reinicio
            result["content"] += "\n\n🔄 Sistema reiniciado. Continuando..."
        
        return result
    
    def format_response(self, result: Dict) -> str:
        """Formatea la respuesta para mostrar al usuario"""
        content = result.get("content", "Sin contenido")
        
        # Formato básico para ahora
        return f"\n{'='*80}\n{content}\n{'='*80}\n"
    
    def _save_session(self):
        """Guarda la sesión actual"""
        self.session_data["end_time"] = datetime.now().isoformat()
        self.session_data["chat_history"] = self.chat_history[-20:]  # Últimos 20 mensajes
        self.session_data["system_state"] = self.executor.system_state
        self.session_data["learning_stats"] = self.executor.learner.get_stats()
        
        self.logger.save_session(self.session_data)
        self.logger.log("INFO", "Sesión guardada", {"session_id": self.logger.session_id})
    
    def run(self):
        """Ejecuta el sistema principal de chat"""
        self.display_banner()
        self._save_session()  # Guardar sesión inicial
        
        print(f"\n{'='*80}")
        print("💬 CHAT VECTA ACTIVADO - Escribe tu mensaje (SIN comillas):")
        print("=" * 80)
        
        try:
            while True:
                try:
                    # Mostrar prompt
                    user_input = input("\n>>> ").strip()
                    
                    # Procesar entrada
                    result = self.process_input(user_input)
                    
                    # Si result es None, salir
                    if result is None:
                        break
                    
                    # Mostrar respuesta
                    print(self.format_response(result))
                    
                    # Auto-guardar cada 10 interacciones
                    if self.session_data["interaction_count"] % 10 == 0:
                        self._save_session()
                        
                except KeyboardInterrupt:
                    print("\n\n⚠️  Interrupción detectada. ¿Salir? (s/n): ", end="")
                    confirm = input().strip().lower()
                    if confirm in ['s', 'si', 'yes', 'y']:
                        print("\n👋 Saliendo del sistema VECTA...")
                        break
                    else:
                        print("↩️  Continuando...")
                        continue
                        
                except EOFError:
                    print("\n\n📴 Fin de entrada detectado. Saliendo...")
                    break
                    
                except Exception as e:
                    error_msg = f"❌ Error interno: {str(e)}"
                    print(f"\n{error_msg}")
                    self.logger.log("ERROR", "Error en loop principal", {"error": str(e)})
        
        finally:
            # Guardar sesión final
            self._save_session()
            print(f"\n{'='*80}")
            print(f"📊 Resumen de sesión {self.logger.session_id}:")
            print(f"  • Interacciones: {self.session_data['interaction_count']}")
            print(f"  • Comandos ejecutados: {len(self.session_data['commands_executed'])}")
            stats = self.executor.learner.get_stats()
            print(f"  • Patrones aprendidos: {stats['total_learned']}")
            print(f"  • Duración: {datetime.now().isoformat()}")
            print(f"  • Sesión guardada en: {self.logger.session_file}")
            print("=" * 80)
            print("\n¡Gracias por usar VECTA 12D AI Chat!")
            print("Para volver a iniciar: python vecta_ai_chat.py\n")


# ==================== CREACIÓN DE ACCESO DIRECTO ====================

def create_desktop_shortcut():
    """Crea un acceso directo en el escritorio para VECTA AI Chat"""
    import platform
    
    system = platform.system()
    
    if system == "Windows":
        return _create_windows_shortcut()
    elif system == "Linux":
        return _create_linux_shortcut()
    elif system == "Darwin":  # macOS
        return _create_macos_shortcut()
    else:
        print(f"⚠️  Sistema no soportado para acceso directo: {system}")
        return False

def _create_windows_shortcut():
    """Crea acceso directo en Windows"""
    import os
    
    try:
        # Verificar si los módulos necesarios están instalados
        try:
            import winshell
            from win32com.client import Dispatch
        except ImportError:
            print("❌ Módulos 'winshell' o 'pywin32' no encontrados.")
            print("   Instálalos con: pip install pywin32 winshell")
            return False
        
        desktop = winshell.desktop()
        script_path = os.path.abspath(__file__)
        
        # Crear acceso directo
        shortcut_path = os.path.join(desktop, "VECTA AI Chat.lnk")
        target = sys.executable  # Python ejecutable
        arguments = f'"{script_path}"'
        
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = target
        shortcut.Arguments = arguments
        shortcut.WorkingDirectory = os.path.dirname(script_path)
        shortcut.Description = "VECTA 12D AI Chat Interface"
        shortcut.IconLocation = target  # Usar icono de Python
        shortcut.save()
        
        print(f"✅ Acceso directo creado: {shortcut_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error creando acceso directo Windows: {e}")
        return False

def _create_linux_shortcut():
    """Crea acceso directo en Linux"""
    import os
    
    try:
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        if not os.path.exists(desktop):
            # Algunas distribuciones usan 'Escritorio'
            desktop = os.path.join(os.path.expanduser("~"), "Escritorio")
        
        script_path = os.path.abspath(__file__)
        desktop_file = os.path.join(desktop, "vecta_ai_chat.desktop")
        
        desktop_content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name=VECTA AI Chat
Comment=VECTA 12D AI Chat Interface
Exec={sys.executable} "{script_path}"
Path={os.path.dirname(script_path)}
Icon=utilities-terminal
Terminal=true
Categories=Development;
"""
        
        with open(desktop_file, 'w') as f:
            f.write(desktop_content)
        
        # Hacer ejecutable
        os.chmod(desktop_file, 0o755)
        
        print(f"✅ Acceso directo creado: {desktop_file}")
        return True
        
    except Exception as e:
        print(f"❌ Error creando acceso directo Linux: {e}")
        return False

def _create_macos_shortcut():
    """Crea acceso directo en macOS"""
    import os
    
    try:
        # En macOS, creamos un script en Applications
        script_path = os.path.abspath(__file__)
        app_dir = os.path.join(os.path.expanduser("~"), "Applications", "VECTA AI Chat.app")
        contents_dir = os.path.join(app_dir, "Contents", "MacOS")
        
        os.makedirs(contents_dir, exist_ok=True)
        
        # Crear archivo Info.plist
        info_plist = os.path.join(app_dir, "Contents", "Info.plist")
        with open(info_plist, 'w') as f:
            f.write(f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>vecta</string>
    <key>CFBundleName</key>
    <string>VECTA AI Chat</string>
    <key>CFBundleIdentifier</key>
    <string>com.vecta.aichat</string>
</dict>
</plist>
""")
        
        # Crear script ejecutable
        script_file = os.path.join(contents_dir, "vecta")
        with open(script_file, 'w') as f:
            f.write(f"""#!/bin/bash
cd "{os.path.dirname(script_path)}"
"{sys.executable}" "{script_path}"
""")
        
        os.chmod(script_file, 0o755)
        
        print(f"✅ Aplicación creada en: {app_dir}")
        print("   Arrastra a Dock para acceso rápido.")
        return True
        
    except Exception as e:
        print(f"❌ Error creando acceso directo macOS: {e}")
        return False


def install_system():
    """Instala y configura el sistema VECTA AI Chat"""
    print("=" * 80)
    print("🛠️  INSTALACIÓN VECTA AI CHAT v4.1.0")
    print("=" * 80)
    
    # Verificar Python
    print("\n🔍 Verificando Python...")
    if sys.version_info < (3, 7):
        print("❌ Se requiere Python 3.7 o superior")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    
    # Verificar directorios
    print("\n📂 Verificando estructura...")
    config = VECTAConfig()
    
    critical_files = [
        ("vecta_ai_chat.py", config.BASE_DIR / "vecta_ai_chat.py"),
        ("core/vecta_12d_core.py", config.BASE_DIR / "core" / "vecta_12d_core.py"),
        ("dimensiones/", config.BASE_DIR / "dimensiones")
    ]
    
    all_ok = True
    for name, path in critical_files:
        if path.exists():
            print(f"  ✅ {name}")
        else:
            print(f"  ❌ {name} (NO ENCONTRADO)")
            all_ok = False
    
    if not all_ok:
        print("\n⚠️  Algunos archivos no se encontraron.")
        print("   Asegúrate de ejecutar desde el directorio correcto de VECTA 12D.")
        return False
    
    # Crear acceso directo
    print("\n🔗 Creando acceso directo...")
    if create_desktop_shortcut():
        print("✅ Acceso directo creado en el escritorio")
    else:
        print("⚠️  No se pudo crear acceso directo, pero el sistema funcionará")
    
    # Instalar dependencias opcionales
    print("\n📦 Instalando dependencias opcionales...")
    try:
        import colorama
        print("✅ Colorama ya instalado")
    except ImportError:
        print("🔧 Instalando colorama...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "colorama", "--quiet"])
            print("✅ Colorama instalado")
        except:
            print("⚠️  No se pudo instalar colorama (opcional)")
    
    # Crear archivo de configuración
    print("\n⚙️  Creando configuración...")
    config_data = {
        "version": config.VERSION,
        "install_date": datetime.now().isoformat(),
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "platform": sys.platform,
        "auto_execute": config.AUTO_EXECUTE,
        "principles": config.VECTA_PRINCIPLES
    }
    
    config_file = config.CHAT_DATA_DIR / "installation_config.json"
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config_data, f, indent=2)
    
    print(f"✅ Configuración guardada en: {config_file}")
    
    # Mensaje final
    print("\n" + "=" * 80)
    print("🎉 INSTALACIÓN COMPLETADA")
    print("=" * 80)
    print("\n📋 RESUMEN:")
    print(f"  • Sistema: VECTA AI Chat v{config.VERSION}")
    print(f"  • Directorio: {config.BASE_DIR}")
    print(f"  • Acceso directo: Disponible en el escritorio")
    print(f"  • Configuración: {config_file}")
    print(f"  • Auto-aprendizaje: ACTIVADO")
    
    print("\n🚀 PARA INICIAR:")
    print("  1. Doble clic en 'VECTA AI Chat' en el escritorio")
    print("  2. O ejecuta: python vecta_ai_chat.py")
    
    print("\n💡 PRIMEROS PASOS CON AUTO-APRENDIZAJE:")
    print("  1. Escribe 'ayuda' para ver comandos")
    print("  2. Prueba 'estado' para ver el sistema")
    print("  3. Enseña nuevos comandos: 'Enseña a vecta: cuando digo X haz Y'")
    print("  4. Ver aprendizaje: '¿Qué has aprendido?'")
    
    print("\n" + "=" * 80)
    return True


# ==================== EJECUCIÓN PRINCIPAL ====================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="VECTA AI Chat Interface")
    parser.add_argument("--install", action="store_true", help="Instalar sistema")
    parser.add_argument("--shortcut", action="store_true", help="Crear solo acceso directo")
    parser.add_argument("--debug", action="store_true", help="Modo debug")
    
    args = parser.parse_args()
    
    if args.install:
        install_system()
        input("\nPresiona Enter para salir...")
    elif args.shortcut:
        create_desktop_shortcut()
    else:
        # Ejecutar chat normal
        if args.debug:
            print("🐛 Modo debug activado")
        
        try:
            chat = VECTAAIChat()
            chat.run()
        except KeyboardInterrupt:
            print("\n\n👋 Sesión interrumpida por el usuario")
        except Exception as e:
            print(f"\n💥 ERROR CRÍTICO: {str(e)}")
            if args.debug:
                traceback.print_exc()
            input("\nPresiona Enter para salir...")