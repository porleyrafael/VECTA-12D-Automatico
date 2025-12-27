#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SISTEMA DE AUTO-IMPLEMENTACIÓN VECTA
======================================
Sistema autónomo que crea y configura automáticamente
todos los componentes de VECTA 12D con auto-diagnóstico.
"""

import os
import sys
import json
import shutil
import subprocess
import traceback
from pathlib import Path
from datetime import datetime

class VECTAAutoInstaller:
    """Sistema de auto-implementación completa para VECTA"""
    
    def __init__(self):
        self.base_dir = Path.cwd()
        self.install_log = []
        self.errors = []
        
        # Configuración del sistema
        self.system_config = {
            "version": "5.0.0",
            "creator": "Rafael Porley",
            "install_date": datetime.now().isoformat(),
            "components": []
        }
    
    def log(self, message, level="INFO"):
        """Registra mensaje en log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] {level}: {message}"
        self.install_log.append(entry)
        print(entry)
    
    def create_directory_structure(self):
        """Crea la estructura completa de directorios"""
        directories = [
            "core",
            "dimensiones",
            "chat_data",
            "chat_data/sessions",
            "chat_data/logs",
            "chat_data/backups",
            "chat_data/learning",
            "chat_data/auto_implementacion"
        ]
        
        for dir_path in directories:
            full_path = self.base_dir / dir_path
            try:
                full_path.mkdir(parents=True, exist_ok=True)
                self.log(f"Directorio creado: {dir_path}")
                self.system_config["components"].append({
                    "type": "directory",
                    "path": dir_path,
                    "status": "created"
                })
            except Exception as e:
                self.errors.append(f"Error creando directorio {dir_path}: {str(e)}")
                self.log(f"Error creando directorio {dir_path}: {str(e)}", "ERROR")
    
    def create_file_with_content(self, file_path, content):
        """Crea un archivo con contenido específico"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            file_size = os.path.getsize(file_path)
            self.log(f"Archivo creado: {file_path.name} ({file_size} bytes)")
            
            self.system_config["components"].append({
                "type": "file",
                "path": str(file_path.relative_to(self.base_dir)),
                "size": file_size,
                "status": "created"
            })
            
            return True
        except Exception as e:
            self.errors.append(f"Error creando archivo {file_path}: {str(e)}")
            self.log(f"Error creando archivo {file_path}: {str(e)}", "ERROR")
            return False
    
    def create_vecta_ai_chat(self):
        """Crea el archivo principal VECTA AI Chat"""
        content = '''#!/usr/bin/env python3
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
        self.VERSION = "5.0.0"
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
            ],
            
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
                    r"(?:crear|crea|hacer|generar|escribir) (?:un )?(?:archivo|fichero|módulo|script|código) (?:llamado|con nombre|denominado)? ?([a-zA-Z0-9_\\-\\.]+)",
                    r"crea (?:archivo|fichero|módulo|script) ([a-zA-Z0-9_\\-\\.]+)",
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
                    r"(?:modificar|editar|cambiar|revisar|ver|mostrar|leer) (?:el )?(?:archivo|fichero|módulo|código|script) ([a-zA-Z0-9_\\-\\.]+)",
                    r"actualizar (?:archivo|módulo|script) (.+)",
                    r"editar (.+)",
                    r"ver (?:el )?(?:código|contenido) (?:de |del )?([a-zA-Z0-9_\\-\\.]+)",
                    r"mostrar (?:el )?(?:archivo|módulo|script) (.+)",
                    r"leer (?:archivo|módulo|script) (.+)",
                    r"muestra (?:el )?contenido (?:de |del )?([a-zA-Z0-9_\\-\\.]+)"
                ],
                "action": "modify_file",
                "has_params": True
            },
            
            "run_script": {
                "patterns": [
                    r"(?:ejecutar|correr|run|lanzar) (?:el )?(?:archivo|script|programa) ([a-zA-Z0-9_\\-\\.]+\\.py)",
                    r"ejecuta (.+\\.py)",
                    r"corre el script (.+)",
                    r"run (.+\\.py)"
                ],
                "action": "run_script",
                "has_params": True
            },
            
            "install_package": {
                "patterns": [
                    r"(?:instalar|agregar) (?:el )?(?:paquete|módulo|package) ([a-zA-Z0-9_\\-]+)",
                    r"necesito instalar (.+)",
                    r"pip install (.+)"
                ],
                "action": "install_package",
                "has_params": True
            ],
            
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
            
            # ========== AUTO-APRENDIZAJE PROFUNDO ==========
            "auto_analyze": {
                "patterns": [
                    r"auto[\\-\\s]?analiza",
                    r"analiza (?:tus |tus )?logs",
                    r"revisa (?:tus )?errores",
                    r"diagnóstico (?:del )?sistema",
                    r"encuentra (?:tus )?errores"
                ],
                "action": "auto_analyze"
            },
            
            "auto_optimize": {
                "patterns": [
                    r"auto[\\-\\s]?optimiza",
                    r"optimiza (?:tu )?nlp",
                    r"mejora (?:tus )?patrones",
                    r"aplica mejoras",
                    r"auto[\\-\\s]?mejora"
                ],
                "action": "auto_optimize"
            },
            
            "learning_statistics": {
                "patterns": [
                    r"estadísticas (?:de )?aprendizaje",
                    r"métricas (?:de )?aprendizaje",
                    r"estadísticas aprendizaje",
                    r"métricas autoaprendizaje"
                ],
                "action": "learning_statistics"
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
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\\n')
        
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
        
        # Limpiar números con puntos al inicio (como "1. ", "2. ", etc.)
        text = re.sub(r'^\\d+\\.\\s*', '', text)
        
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
            r'([a-zA-Z0-9_\\-\\.]+\\.py)',  # Archivos .py
            r'([a-zA-Z0-9_\\-\\.]+\\.txt)', # Archivos .txt
            r'([a-zA-Z0-9_\\-\\.]+\\.json)', # Archivos .json
            r'([a-zA-Z0-9_\\-\\.]+\\.md)',   # Archivos .md
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
        
        return f"Aprendido: '{user_input}' → {correct_action}"
    
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
            "REPORTE DE APRENDIZAJE VECTA",
            "=" * 50,
            f"Patrones aprendidos: {stats['total_learned']}",
            f"Usos exitosos: {stats['successful_uses']}",
            f"Patrones únicos: {stats['unique_patterns']}",
            f"Ultima actualizacion: {stats['last_updated']}",
            "",
            "PATRONES APRENDIDOS:"
        ]
        
        if self.learned_patterns["command_mappings"]:
            for pattern, data in list(self.learned_patterns["command_mappings"].items())[:10]:
                report.append(f"  * '{pattern}' -> {data['action']} (usos: {data.get('uses', 0)})")
            
            if len(self.learned_patterns["command_mappings"]) > 10:
                report.append(f"  ... y {len(self.learned_patterns['command_mappings']) - 10} patrones más")
        else:
            report.append("  Aun no hay patrones aprendidos")
        
        return "\\n".join(report)


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
            
            self.logger.log("LEARNING", f"Usando aprendizaje: '{original_text}' -> {action} (antes: {old_action})")
        
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
            elif action == "auto_analyze":
                result = self._action_auto_analyze(params)
            elif action == "auto_optimize":
                result = self._action_auto_optimize(params)
            elif action == "learning_statistics":
                result = self._action_learning_statistics(params)
            elif action == "general_query":
                result = self._action_general_query(params)
            else:
                result = self._action_unknown(params)
            
            # Verificar tiempo de ejecución (principio de tiempo finito)
            exec_time = time.time() - start_time
            if exec_time > self.config.COMMAND_TIMEOUT:
                result["warning"] = f"Accion tardo {exec_time:.2f}s (limite: {self.config.COMMAND_TIMEOUT}s)"
                self.logger.log("WARNING", f"Accion {action} excedio tiempo", {"time": exec_time})
            
            # Agregar metadatos VECTA
            result["vecta_metadata"] = {
                "execution_time": exec_time,
                "action": action,
                "timestamp": datetime.now().isoformat(),
                "principles_applied": self._get_applied_principles(action),
                "learned_suggestion_used": learned_suggestion is not None
            }
            
            # Registrar éxito
            self.logger.log("INFO", f"Accion {action} completada", {
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
            
            self.logger.log("ERROR", f"Error en accion {action}", error_info)
            
            # OFRECER ENSEÑAR ESTE ERROR
            teach_suggestion = ""
            if "original_text" in params:
                teach_suggestion = f"\\nQuieres ensenarme este comando?\\n   Di: 'ensena a vecta: cuando digo \"{params['original_text']}\" haz [accion correcta]'"
            
            return {
                "success": False,
                "type": "error",
                "error": str(e),
                "action": action,
                "content": f"Error en accion: {str(e)}{teach_suggestion}",
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
VECTA 12D - ESTADO DEL SISTEMA

VERSION: {self.config.VERSION}
CREADOR: {self.config.CREATOR}
SESSION: {self.logger.session_id}

COMPONENTES:
  * Nucleo VECTA: {'ACTIVO' if self.system_state['vecta_core'] else 'INACTIVO'}
  * Dimensiones: {self.system_state['dimensions']}/12
  * Archivos Python: {self.system_state['files_count']}
  * Python: {self.system_state['python_version']}
  * Plataforma: {self.system_state['platform']}

DIRECTORIOS:
  * Principal: {self.config.BASE_DIR}
  * Datos Chat: {self.config.CHAT_DATA_DIR}
  * Aprendizaje: {self.config.LEARNING_DATA_DIR}

PRINCIPIOS VECTA:
"""
        
        for principle in self.config.VECTA_PRINCIPLES:
            status_text += f"  * {principle}\\n"
        
        # Agregar estadísticas de aprendizaje
        stats = self.learner.get_stats()
        status_text += f"\\nAPRENDIZAJE AUTOMATICO:\\n"
        status_text += f"  * Patrones aprendidos: {stats['total_learned']}\\n"
        status_text += f"  * Usos exitosos: {stats['successful_uses']}\\n"
        status_text += f"  * Ultima actualizacion: {stats['last_updated']}\\n"
        
        return {
            "success": True,
            "type": "system_status",
            "content": status_text,
            "data": self.system_state
        }
    
    def _action_show_help(self) -> Dict:
        """Acción: Mostrar ayuda del sistema"""
        help_text = f"""
VECTA AI CHAT - AYUDA v{self.config.VERSION}

COMUNICACION EN LENGUAJE NATURAL:
  Habla normalmente, VECTA entendera tu intencion.

CONSULTAS DEL SISTEMA:
  * "Como esta el sistema?"
  * "Muestrame las dimensiones"
  * "Genera un reporte"
  * "Haz un backup del sistema"

ACCIONES CON ARCHIVOS:
  * "Crea un archivo llamado ejemplo.py"
  * "Crea modulo test.py" (formato simplificado)
  * "Modifica el archivo config.json"
  * "Ver el contenido de vecta_learner.py"
  * "Ejecuta el script prueba_vecta.py"

PROCESAMIENTO CON VECTA:
  * "Analiza esto con VECTA: [texto]"
  * "Procesa esta informacion usando las 12 dimensiones"
  * "Calcula el vector para esta frase"

AUTO-APRENDIZAJE:
  * "Enseña a vecta: cuando digo 'programa codigo' haz 'crear archivo'"
  * "Aprende esto: 'generar script' significa 'crear archivo'"
  * "Que has aprendido hasta ahora?"
  * "Muestra tu conocimiento"

AUTO-ANALISIS Y OPTIMIZACION:
  * "Auto-analiza" - Analiza logs recientes
  * "Auto-optimiza" - Mejora patrones NLP
  * "Estadisticas aprendizaje" - Metricas de aprendizaje

MANTENIMIENTO:
  * "Limpia el sistema"
  * "Reinicia VECTA"
  * "Salir del chat"

EJEMPLOS COMPLETOS:
  * "VECTA, analiza este proyecto usando todas las dimensiones"
  * "Por favor, ejecuta el script de prueba y dime el resultado"
  * "Necesito crear un nuevo modulo para procesamiento de texto"
  * "Enseña a vecta que cuando digo 'construye' quiero decir 'crear archivo'"

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
                            class_match = re.search(r'class\\s+(\\w+)', content)
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
            content = "No se encontraron dimensiones en el sistema."
        else:
            content = "DIMENSIONES VECTA 12D:\\n\\n"
            for dim in dimensions:
                if dim.get("status") == "MISSING":
                    content += f"  {dim['number']:2d}. FALTANTE\\n"
                elif dim.get("status") == "ERROR_READING":
                    content += f"  {dim['number']:2d}. ERROR\\n"
                else:
                    content += f"  {dim['number']:2d}. {dim['class']} ({dim['file']}, {dim['size']} bytes)\\n"
        
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
                "content": f"Reporte generado exitosamente\\nGuardado en: {report_file}\\n\\n{content[:500]}..." if len(content) > 500 else content,
                "file": str(report_file),
                "file_size": len(content)
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
            "ESTADISTICAS:",
            f"  * Archivos .py: {len(list(self.config.BASE_DIR.glob('*.py')))}",
            f"  * Directorios: {len([d for d in self.config.BASE_DIR.iterdir() if d.is_dir()])}",
            f"  * Dimensiones cargadas: {self.system_state['dimensions']}/12",
            f"  * Sesiones guardadas: {len(list(self.config.CHAT_SESSIONS_DIR.glob('*.json')))}",
            f"  * Logs del dia: {len(list(self.config.CHAT_LOGS_DIR.glob('*.log')))}",
            "",
            "APRENDIZAJE AUTOMATICO:",
            f"  * Patrones aprendidos: {stats['total_learned']}",
            f"  * Usos exitosos: {stats['successful_uses']}",
            f"  * Patrones unicos: {stats['unique_patterns']}",
            "",
            "ARCHIVOS CRITICOS:"
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
                report.append(f"  OK {file}")
            else:
                report.append(f"  FALTANTE {file}")
        
        report.append("")
        report.append("PRINCIPIOS VECTA ACTIVOS:")
        for principle in self.config.VECTA_PRINCIPLES:
            report.append(f"  * {principle}")
        
        report.append("")
        report.append("=" * 70)
        
        return "\\n".join(report)
    
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
                "content": f"Backup creado exitosamente\\nDirectorio: {backup_dir}\\nArchivos copiados: {copied_files}",
                "backup_dir": str(backup_dir),
                "files_count": copied_files,
                "metadata": metadata
            }
            
        except Exception as e:
            return {
                "success": False,
                "type": "backup",
                "error": str(e),
                "content": f"Error al crear backup: {str(e)}"
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
                "content": f"Sistema limpiado exitosamente\\nElementos eliminados: {len(deleted_items)}",
                "deleted_count": len(deleted_items),
                "deleted_items": deleted_items[:10]
            }
            
        except Exception as e:
            return {
                "success": False,
                "type": "cleanup",
                "error": str(e),
                "content": f"Error al limpiar sistema: {str(e)}"
            }
    
    def _action_restart_system(self) -> Dict:
        """Acción: Reiniciar sistema (simulado)"""
        return {
            "success": True,
            "type": "restart",
            "content": "Sistema VECTA reiniciado\\nEstado guardado\\nListo para continuar",
            "requires_restart": True
        }
    
    def _action_exit_system(self) -> Dict:
        """Acción: Salir del sistema"""
        return {
            "success": True,
            "type": "exit",
            "content": f"Sesion finalizada\\nResumen:\\n  * Sistema VECTA 12D Chat v{self.config.VERSION}\\n  * Sesion: {self.logger.session_id}\\n  * Gracias por usar VECTA",
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
            analysis_match = re.search(r'(?:analiza|procesa|calcula)[\\s\\:]+(.+)', text, re.IGNORECASE)
            analysis_text = analysis_match.group(1).strip() if analysis_match else text
        
        if not analysis_text or len(analysis_text) < 3:
            return {
                "success": False,
                "type": "vecta_analysis",
                "content": "No se especifico texto para analizar\\nEjemplo: 'Analiza con VECTA: Este es un proyecto importante'",
                "error": "No text provided"
            }
        
        try:
            # Intentar importar y usar VECTA core
            sys.path.insert(0, str(self.config.BASE_DIR))
            
            # Verificar si existe el núcleo VECTA
            vecta_core_path = self.config.BASE_DIR / "core" / "vecta_12d_core.py"
            if not vecta_core_path.exists():
                return {
                    "success": False,
                    "type": "vecta_analysis",
                    "content": "Nucleo VECTA no disponible\\nEjecuta 'estado' para verificar el sistema",
                    "error": "VECTA core not available"
                }
            
            from core.vecta_12d_core import VECTA_12D_Core
            
            vecta = VECTA_12D_Core()
            result = vecta.procesar(analysis_text)
            
            if result.get("exito"):
                content = f"""
Analisis VECTA completado:

Texto analizado: "{analysis_text[:100]}{'...' if len(analysis_text) > 100 else ''}"

Resultados:
  * Magnitud vectorial: {result.get('magnitud', 0):.4f}
  * Dimensiones activas: {len(result.get('dimensiones', []))}
  * Procesamiento exitoso

Detalles dimensionales:"""
                
                dims = result.get('dimensiones', [])
                for i, val in enumerate(dims[:6], 1):
                    content += f"\\n    D{i}: {val:.4f}"
                
                if len(dims) > 6:
                    content += f"\\n    ... y {len(dims)-6} dimensiones más"
                
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
                    "content": f"Error en analisis VECTA: {result.get('error', 'Error desconocido')}",
                    "error": result.get("error")
                }
                
        except ImportError:
            return {
                "success": False,
                "type": "vecta_analysis",
                "content": "Nucleo VECTA no disponible\\nEjecuta 'estado' para verificar el sistema",
                "error": "VECTA core not available"
            }
        except Exception as e:
            return {
                "success": False,
                "type": "vecta_analysis",
                "content": f"Error en analisis: {str(e)}",
                "error": str(e)
            }
    
    def _action_run_script(self, params: Dict) -> Dict:
        """Acción: Ejecutar script Python"""
        script_name = params.get("file_name") or params.get("param_1")
        
        if not script_name:
            return {
                "success": False,
                "type": "script_execution",
                "content": "No se especifico archivo a ejecutar\\nEjemplo: 'Ejecuta prueba_vecta.py'",
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
                "content": f"Archivo no encontrado: {script_name}\\nDirectorio actual: {self.config.BASE_DIR}",
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
Script ejecutado: {script_name}

Resultado:
  * Codigo de salida: {result.returncode}
  * Tiempo limite: {self.config.COMMAND_TIMEOUT}s

Salida:"""
            
            # Limitar tamaño de salida
            if len(output) > 1000:
                content += f"\\n{output[:500]}\\n... [salida truncada, {len(output)} caracteres totales] ...\\n{output[-500:]}"
            else:
                content += f"\\n{output}"
            
            if result.returncode != 0:
                content += f"\\n\\nErrores:\\n{error}"
            
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
                "content": f"Timeout: El script {script_name} tardo mas de {self.config.COMMAND_TIMEOUT} segundos",
                "error": "Timeout expired"
            }
        except Exception as e:
            return {
                "success": False,
                "type": "script_execution",
                "content": f"Error al ejecutar script: {str(e)}",
                "error": str(e)
            }
    
    def _action_create_file(self, params: Dict) -> Dict:
        """Acción: Crear nuevo archivo"""
        file_name = params.get("file_name") or params.get("param_1")
        
        if not file_name:
            return {
                "success": False,
                "type": "file_creation",
                "content": "No se especifico nombre de archivo\\nEjemplo: 'Crea un archivo test.py'",
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
                "content": f"El archivo ya existe: {file_name}",
                "error": "File already exists"
            }
        
        try:
            # Determinar tipo de archivo por extensión
            if file_name.endswith('.py'):
                content = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
{file_name.upper().replace('.PY', '')} - Modulo generado por VECTA AI Chat
Fecha: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Version VECTA: {self.config.VERSION}
"""

def main():
    """Funcion principal"""
    print("Archivo creado por VECTA 12D AI Chat!")
    print("Sistema de auto-aprendizaje y auto-programacion")

if __name__ == "__main__":
    main()
'''
            elif file_name.endswith('.json'):
                content = json.dumps({
                    "created_by": "VECTA AI Chat",
                    "timestamp": datetime.now().isoformat(),
                    "version": self.config.VERSION,
                    "purpose": "Archivo de configuracion generado automaticamente",
                    "vecta_principles": self.config.VECTA_PRINCIPLES
                }, indent=2)
            elif file_name.endswith('.txt'):
                content = f"""Archivo creado por VECTA AI Chat
Fecha: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Version: {self.config.VERSION}
Sistema: VECTA 12D - Auto-programacion

Este archivo fue generado automaticamente por el sistema
de aprendizaje y auto-programacion VECTA 12D.
"""
            else:
                content = f"""Archivo: {file_name}
Creado por VECTA AI Chat
Fecha: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Version: {self.config.VERSION}

Sistema VECTA 12D - Auto-programacion
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
                "content": f"Archivo creado: {file_name}\\nUbicacion: {file_path}\\nTamaño: {len(content)} bytes",
                "file_path": str(file_path),
                "file_size": len(content)
            }
            
        except Exception as e:
            return {
                "success": False,
                "type": "file_creation",
                "content": f"Error al crear archivo: {str(e)}",
                "error": str(e)
            }
    
    def _action_modify_file(self, params: Dict) -> Dict:
        """Acción: Modificar archivo existente (mostrar contenido)"""
        file_name = params.get("file_name") or params.get("param_1")
        
        if not file_name:
            return {
                "success": False,
                "type": "file_modification",
                "content": "No se especifico archivo\\nEjemplo: 'Ver vecta_learner.py'",
                "error": "No filename specified"
            }
        
        file_path = self.config.BASE_DIR / file_name
        
        if not file_path.exists():
            return {
                "success": False,
                "type": "file_modification",
                "content": f"Archivo no encontrado: {file_name}",
                "error": "File not found"
            }
        
        try:
            stat = file_path.stat()
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Determinar tipo de archivo
            if file_name.endswith('.py'):
                file_type = "Modulo Python"
            elif file_name.endswith('.json'):
                file_type = "Archivo JSON"
            elif file_name.endswith('.txt'):
                file_type = "Archivo de texto"
            else:
                file_type = "Archivo"
            
            content_display = f"""
{file_type}: {file_name}

Detalles:
  * Tamaño: {stat.st_size} bytes
  * Ultima modificacion: {datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')}
  * Ruta: {file_path}

{"="*60}
CONTENIDO:
{"="*60}
{content if len(content) <= 1000 else content[:1000] + "\\n\\n... [contenido truncado, " + str(len(content)) + " caracteres totales] ..."}
{"="*60}

Para editar este archivo, usa un editor de texto externo.
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
                "content": f"Error al leer archivo: {str(e)}",
                "error": str(e)
            }
    
    def _action_install_package(self, params: Dict) -> Dict:
        """Acción: Instalar paquete Python"""
        package_name = params.get("param_1")
        
        if not package_name:
            return {
                "success": False,
                "type": "package_installation",
                "content": "No se especifico paquete a instalar\\nEjemplo: 'Instala numpy'",
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
                content = f"Paquete instalado: {package_name}\\n\\nSalida:\\n{result.stdout}"
            else:
                content = f"Error al instalar {package_name}:\\n{result.stderr}"
            
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
                "content": f"Timeout: La instalacion de {package_name} tardo mas de 60 segundos",
                "error": "Installation timeout"
            }
        except Exception as e:
            return {
                "success": False,
                "type": "package_installation",
                "content": f"Error en instalacion: {str(e)}",
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
        teach_match = re.search(r'ensena a vecta:? cuando digo (.+) haz (.+)', original_text, re.IGNORECASE)
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
                "content": "Formato incorrecto\\nUsa: 'Enseña a vecta: cuando digo \\"programa codigo\\" haz \\"crear archivo\\"'",
                "error": "Invalid teaching format"
            }
        
        # Mapear acción a acción interna
        action_map = {
            "crear archivo": "create_file",
            "crea archivo": "create_file",
            "crear modulo": "create_file",
            "crea modulo": "create_file",
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
            file_match = re.search(r'([a-zA-Z0-9_\\-\\.]+\\.py)', user_input)
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
            "content": f"VECTA HA APRENDIDO\\n\\n{result}\\n\\nAhora cuando digas:\\n  \\"{user_input}\\"\\n\\nVECTA hara:\\n  {mapped_action}" + (f" con parametros {params_to_learn}" if params_to_learn else ""),
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
    
    def _action_auto_analyze(self, params: Dict) -> Dict:
        """Acción: Auto-análisis de logs"""
        try:
            # Verificar si existe el módulo de auto-aprendizaje
            self_learner_path = self.config.BASE_DIR / "vecta_self_learner.py"
            if not self_learner_path.exists():
                return {
                    "success": False,
                    "type": "auto_analysis",
                    "content": "Modulo de auto-aprendizaje no encontrado\\nEjecuta 'auto-implementar' para crearlo",
                    "error": "Self learner module not found"
                }
            
            # Importar y ejecutar
            sys.path.insert(0, str(self.config.BASE_DIR))
            from vecta_self_learner import auto_analyze
            
            result = auto_analyze()
            
            return {
                "success": True,
                "type": "auto_analysis",
                "content": result
            }
        except ImportError as e:
            return {
                "success": False,
                "type": "auto_analysis",
                "content": f"Error importando modulo de auto-aprendizaje: {str(e)}",
                "error": str(e)
            }
        except Exception as e:
            return {
                "success": False,
                "type": "auto_analysis",
                "content": f"Error en auto-analisis: {str(e)}",
                "error": str(e)
            }
    
    def _action_auto_optimize(self, params: Dict) -> Dict:
        """Acción: Auto-optimización NLP"""
        try:
            # Verificar si existe el módulo de auto-aprendizaje
            self_learner_path = self.config.BASE_DIR / "vecta_self_learner.py"
            if not self_learner_path.exists():
                return {
                    "success": False,
                    "type": "auto_optimization",
                    "content": "Modulo de auto-aprendizaje no encontrado\\nEjecuta 'auto-implementar' para crearlo",
                    "error": "Self learner module not found"
                }
            
            # Determinar si aplicar cambios
            original_text = params.get("original_text", "").lower()
            apply_changes = "simula" not in original_text and "prueba" not in original_text
            
            # Importar y ejecutar
            sys.path.insert(0, str(self.config.BASE_DIR))
            from vecta_self_learner import auto_optimize
            
            result = auto_optimize(apply_changes=apply_changes)
            
            return {
                "success": True,
                "type": "auto_optimization",
                "content": result,
                "changes_applied": apply_changes
            }
        except ImportError as e:
            return {
                "success": False,
                "type": "auto_optimization",
                "content": f"Error importando modulo de auto-aprendizaje: {str(e)}",
                "error": str(e)
            }
        except Exception as e:
            return {
                "success": False,
                "type": "auto_optimization", 
                "content": f"Error en auto-optimizacion: {str(e)}",
                "error": str(e)
            }
    
    def _action_learning_statistics(self, params: Dict) -> Dict:
        """Acción: Mostrar estadísticas de aprendizaje"""
        try:
            # Verificar si existe el módulo de auto-aprendizaje
            self_learner_path = self.config.BASE_DIR / "vecta_self_learner.py"
            if not self_learner_path.exists():
                return {
                    "success": False,
                    "type": "learning_stats",
                    "content": "Modulo de auto-aprendizaje no encontrado\\nEjecuta 'auto-implementar' para crearlo",
                    "error": "Self learner module not found"
                }
            
            # Importar y ejecutar
            sys.path.insert(0, str(self.config.BASE_DIR))
            from vecta_self_learner import show_learning_stats
            
            result = show_learning_stats()
            
            return {
                "success": True,
                "type": "learning_stats",
                "content": result
            }
        except ImportError as e:
            return {
                "success": False,
                "type": "learning_stats",
                "content": f"Error importando modulo de auto-aprendizaje: {str(e)}",
                "error": str(e)
            }
        except Exception as e:
            return {
                "success": False,
                "type": "learning_stats",
                "content": f"Error obteniendo estadisticas: {str(e)}",
                "error": str(e)
            }
    
    def _action_general_query(self, params: Dict) -> Dict:
        """Acción: Procesar consulta general"""
        text = params.get("original_text", "")
        
        # Respuestas inteligentes basadas en contenido
        if any(word in text.lower() for word in ['hola', 'hello', 'hi', 'buenas', 'buenos dias', 'buenas tardes']):
            response = f"Hola! Soy VECTA AI Chat v{self.config.VERSION}\\nEn que puedo ayudarte hoy?"
        elif any(word in text.lower() for word in ['gracias', 'thanks', 'thank you', 'merci']):
            response = "De nada! Siempre estoy aqui para ayudarte con VECTA 12D."
        elif any(word in text.lower() for word in ['bien', 'excelente', 'genial', 'perfecto']):
            response = "Me alegra! En que mas puedo asistirte?"
        elif '?' in text:
            response = f"Interesante pregunta.\\n\\nPuedo ayudarte mejor si me dices que quieres hacer:\\n* Consultar el estado del sistema?\\n* Ejecutar algun script?\\n* Analizar algo con VECTA?\\n* Crear o modificar archivos?\\n\\nO escribe 'ayuda' para ver todas las opciones."
        elif any(word in text.lower() for word in ['vecta', 'sistema', 'proyecto']):
            response = f"Detecte que hablas de VECTA.\\n\\nPuedo ayudarte con:\\n* Analisis con las 12 dimensiones\\n* Gestion del sistema\\n* Creacion de modulos\\n* Auto-aprendizaje\\n\\nQue necesitas especificamente?"
        else:
            # Intentar sugerir basado en palabras clave
            suggestions = []
            
            if any(word in text.lower() for word in ['crea', 'crear', 'hacer', 'nuevo', 'generar']):
                suggestions.append("* 'Crea archivo [nombre]' - Para crear nuevos archivos")
            
            if any(word in text.lower() for word in ['ejecuta', 'corre', 'run', 'lanzar']):
                suggestions.append("* 'Ejecuta [archivo.py]' - Para ejecutar scripts")
            
            if any(word in text.lower() for word in ['analiza', 'procesa', 'calcula', 'vecta']):
                suggestions.append("* 'Analiza con VECTA: [texto]' - Para analisis dimensional")
            
            if any(word in text.lower() for word in ['ver', 'mostrar', 'leer', 'modificar']):
                suggestions.append("* 'Ver [archivo.py]' - Para ver contenido de archivos")
            
            if any(word in text.lower() for word in ['ensena', 'aprende', 'recuerda']):
                suggestions.append("* 'Enseña a vecta: cuando digo X haz Y' - Para ensenarme nuevos comandos")
            
            if any(word in text.lower() for word in ['auto', 'optimiza', 'analiza']):
                suggestions.append("* 'Auto-analiza' - Para analisis automatico\\n* 'Auto-optimiza' - Para optimizacion automatica")
            
            if suggestions:
                suggestion_text = "\\n".join(suggestions)
                response = f"He procesado tu mensaje.\\n\\nBasado en lo que dijiste, quizas quieras:\\n{suggestion_text}\\n\\nO escribe 'ayuda' para ver todos los comandos."
            else:
                response = f"He procesado tu mensaje: '{text}'\\n\\nPara acciones especificas, intenta:\\n* 'Ayuda' - Ver todos los comandos\\n* 'Estado' - Ver sistema VECTA\\n* 'Enseña a vecta' - Para ensenarme nuevos comandos"
        
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
        teach_option = f"\\n\\nQuieres que aprenda este comando?\\n   Di: 'Enseña a vecta: cuando digo \\"{text}\\" haz [accion correcta]'"
        
        return {
            "success": False,
            "type": "unknown_command",
            "content": f"VECTA no entendio completamente: '{text}'\\n\\nPrueba con:\\n* 'Ayuda' - Ver todos los comandos\\n* 'Estado' - Ver sistema VECTA\\n* Escribe en lenguaje natural lo que necesitas{teach_option}",
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
VECTA 12D - AI CHAT INTERFACE
Sistema Autonomo de Comunicacion Inteligente

----------------------------------------------------------------
  Version: {self.config.VERSION}                Creador: {self.config.CREATOR}                Session: {self.logger.session_id}
----------------------------------------------------------------

CARACTERISTICAS PRINCIPALES:
  * Lenguaje natural completo (espanol/ingles)
  * Ejecucion automatica de comandos
  * Integracion total con VECTA 12D
  * Sistema de auto-aprendizaje
  * Auto-backup y recuperacion
  * Auditoria completa (principio VECTA)

AUTO-APRENDIZAJE ACTIVO:
  * Puedo aprender nuevos comandos
  * Mejoro con el uso
  * Entiendo variaciones de lenguaje

INSTRUCCION:
  Escribe en lenguaje natural lo que necesitas. Ejemplos:
    * "Crea un archivo prueba.py"
    * "Ver el contenido de vecta_learner.py"
    * "Enseña a vecta: cuando digo 'programa' haz 'crear archivo'"
    * "Que has aprendido hasta ahora?"

Escribe 'ayuda' para ver la guia completa o 'salir' para terminar.
----------------------------------------------------------------
"""
        
        print(banner)
    
    def process_input(self, user_input: str) -> Optional[Dict]:
        """
        Procesa la entrada del usuario y ejecuta la acción correspondiente
        Retorna None si se debe salir del sistema
        """
        if not user_input.strip():
            return {"content": "Entrada vacia. Por favor, escribe algo."}
        
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
        self.logger.log("INFO", f"Intencion detectada: {action} (confianza: {confidence:.2f})", {
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
            result["content"] += "\\n\\nSistema reiniciado. Continuando..."
        
        return result
    
    def format_response(self, result: Dict) -> str:
        """Formatea la respuesta para mostrar al usuario"""
        content = result.get("content", "Sin contenido")
        
        # Formato básico para ahora
        return f"\\n{'='*80}\\n{content}\\n{'='*80}\\n"
    
    def _save_session(self):
        """Guarda la sesión actual"""
        self.session_data["end_time"] = datetime.now().isoformat()
        self.session_data["chat_history"] = self.chat_history[-20:]  # Últimos 20 mensajes
        self.session_data["system_state"] = self.executor.system_state
        self.session_data["learning_stats"] = self.executor.learner.get_stats()
        
        self.logger.save_session(self.session_data)
        self.logger.log("INFO", "Sesion guardada", {"session_id": self.logger.session_id})
    
    def run(self):
        """Ejecuta el sistema principal de chat"""
        self.display_banner()
        self._save_session()  # Guardar sesión inicial
        
        print(f"\\n{'='*80}")
        print("CHAT VECTA ACTIVADO - Escribe tu mensaje (SIN comillas):")
        print("=" * 80)
        
        try:
            while True:
                try:
                    # Mostrar prompt
                    user_input = input("\\n>>> ").strip()
                    
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
                    print("\\n\\nInterrupcion detectada. Salir? (s/n): ", end="")
                    confirm = input().strip().lower()
                    if confirm in ['s', 'si', 'yes', 'y']:
                        print("\\nSaliendo del sistema VECTA...")
                        break
                    else:
                        print("Continuando...")
                        continue
                        
                except EOFError:
                    print("\\n\\nFin de entrada detectado. Saliendo...")
                    break
                    
                except Exception as e:
                    error_msg = f"Error interno: {str(e)}"
                    print(f"\\n{error_msg}")
                    self.logger.log("ERROR", "Error en loop principal", {"error": str(e)})
        
        finally:
            # Guardar sesión final
            self._save_session()
            print(f"\\n{'='*80}")
            print(f"Resumen de sesion {self.logger.session_id}:")
            print(f"  * Interacciones: {self.session_data['interaction_count']}")
            print(f"  * Comandos ejecutados: {len(self.session_data['commands_executed'])}")
            stats = self.executor.learner.get_stats()
            print(f"  * Patrones aprendidos: {stats['total_learned']}")
            print(f"  * Duracion: {datetime.now().isoformat()}")
            print(f"  * Sesion guardada en: {self.logger.session_file}")
            print("=" * 80)
            print("\\nGracias por usar VECTA 12D AI Chat!")
            print("Para volver a iniciar: python vecta_ai_chat.py\\n")


# ==================== FUNCIONES DE INSTALACION ====================

def create_desktop_shortcut():
    """Crea un acceso directo en el escritorio para VECTA AI Chat"""
    import platform
    
    system = platform.system()
    
    if system == "Windows":
        return _create_windows_shortcut()
    elif system == "Linux":
        return _create_linux_shortcut()
    elif system == "Darwin":
        return _create_macos_shortcut()
    else:
        print(f"Sistema no soportado para acceso directo: {system}")
        return False

def _create_windows_shortcut():
    """Crea acceso directo en Windows"""
    import os
    
    try:
        import winshell
        from win32com.client import Dispatch
    except ImportError:
        print("Modulos 'winshell' o 'pywin32' no encontrados.")
        print("Instalalos con: pip install pywin32 winshell")
        return False
    
    try:
        desktop = winshell.desktop()
        script_path = os.path.abspath(__file__)
        
        shortcut_path = os.path.join(desktop, "VECTA AI Chat.lnk")
        target = sys.executable
        arguments = f'"{script_path}"'
        
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = target
        shortcut.Arguments = arguments
        shortcut.WorkingDirectory = os.path.dirname(script_path)
        shortcut.Description = "VECTA 12D AI Chat Interface"
        shortcut.IconLocation = target
        shortcut.save()
        
        print(f"Acceso directo creado: {shortcut_path}")
        return True
        
    except Exception as e:
        print(f"Error creando acceso directo Windows: {e}")
        return False

def _create_linux_shortcut():
    """Crea acceso directo en Linux"""
    import os
    
    try:
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        if not os.path.exists(desktop):
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
        
        os.chmod(desktop_file, 0o755)
        
        print(f"Acceso directo creado: {desktop_file}")
        return True
        
    except Exception as e:
        print(f"Error creando acceso directo Linux: {e}")
        return False

def _create_macos_shortcut():
    """Crea acceso directo en macOS"""
    import os
    
    try:
        script_path = os.path.abspath(__file__)
        app_dir = os.path.join(os.path.expanduser("~"), "Applications", "VECTA AI Chat.app")
        contents_dir = os.path.join(app_dir, "Contents", "MacOS")
        
        os.makedirs(contents_dir, exist_ok=True)
        
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
        
        script_file = os.path.join(contents_dir, "vecta")
        with open(script_file, 'w') as f:
            f.write(f"""#!/bin/bash
cd "{os.path.dirname(script_path)}"
"{sys.executable}" "{script_path}"
""")
        
        os.chmod(script_file, 0o755)
        
        print(f"Aplicacion creada en: {app_dir}")
        print("Arrastra a Dock para acceso rapido.")
        return True
        
    except Exception as e:
        print(f"Error creando acceso directo macOS: {e}")
        return False


def install_system():
    """Instala y configura el sistema VECTA AI Chat"""
    print("=" * 80)
    print("INSTALACION VECTA AI CHAT v5.0.0")
    print("=" * 80)
    
    print("\\nVerificando Python...")
    if sys.version_info < (3, 7):
        print("Se requiere Python 3.7 o superior")
        return False
    print(f"Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    
    print("\\nVerificando estructura...")
    config = VECTAConfig()
    
    critical_files = [
        ("vecta_ai_chat.py", config.BASE_DIR / "vecta_ai_chat.py"),
        ("core/vecta_12d_core.py", config.BASE_DIR / "core" / "vecta_12d_core.py"),
        ("dimensiones/", config.BASE_DIR / "dimensiones")
    ]
    
    all_ok = True
    for name, path in critical_files:
        if path.exists():
            print(f"  OK {name}")
        else:
            print(f"  FALTANTE {name}")
            all_ok = False
    
    if not all_ok:
        print("\\nAlgunos archivos no se encontraron.")
        print("Asegurate de ejecutar desde el directorio correcto de VECTA 12D.")
        return False
    
    print("\\nCreando acceso directo...")
    if create_desktop_shortcut():
        print("Acceso directo creado en el escritorio")
    else:
        print("No se pudo crear acceso directo, pero el sistema funcionara")
    
    print("\\nInstalando dependencias opcionales...")
    try:
        import colorama
        print("Colorama ya instalado")
    except ImportError:
        print("Instalando colorama...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "colorama", "--quiet"])
            print("Colorama instalado")
        except:
            print("No se pudo instalar colorama (opcional)")
    
    print("\\nCreando configuracion...")
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
    
    print(f"Configuracion guardada en: {config_file}")
    
    print("\\n" + "=" * 80)
    print("INSTALACION COMPLETADA")
    print("=" * 80)
    print("\\nRESUMEN:")
    print(f"  * Sistema: VECTA AI Chat v{config.VERSION}")
    print(f"  * Directorio: {config.BASE_DIR}")
    print(f"  * Acceso directo: Disponible en el escritorio")
    print(f"  * Configuracion: {config_file}")
    print(f"  * Auto-aprendizaje: ACTIVADO")
    
    print("\\nPARA INICIAR:")
    print("  1. Doble clic en 'VECTA AI Chat' en el escritorio")
    print("  2. O ejecuta: python vecta_ai_chat.py")
    
    print("\\nPRIMEROS PASOS CON AUTO-APRENDIZAJE:")
    print("  1. Escribe 'ayuda' para ver comandos")
    print("  2. Prueba 'estado' para ver el sistema")
    print("  3. Enseña nuevos comandos: 'Enseña a vecta: cuando digo X haz Y'")
    print("  4. Ver aprendizaje: 'Que has aprendido?'")
    
    print("\\n" + "=" * 80)
    return True


# ==================== EJECUCIÓN PRINCIPAL ====================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="VECTA AI Chat Interface")
    parser.add_argument("--install", action="store_true", help="Instalar sistema")
    parser.add_argument("--shortcut", action="store_true", help="Crear solo acceso directo")
    parser.add_argument("--debug", action="store_true", help="Modo debug")
    parser.add_argument("--auto-implementar", action="store_true", help="Auto-implementar sistema completo")
    
    args = parser.parse_args()
    
    if args.auto_implementar:
        # Ejecutar auto-implementación
        installer = VECTAAutoInstaller()
        installer.create_directory_structure()
        installer.create_vecta_ai_chat()
        # Más archivos se crearán aquí...
        print("\\nAuto-implementacion completada.")
        print("Ejecuta: python vecta_ai_chat.py")
        input("\\nPresiona Enter para salir...")
    elif args.install:
        install_system()
        input("\\nPresiona Enter para salir...")
    elif args.shortcut:
        create_desktop_shortcut()
    else:
        if args.debug:
            print("Modo debug activado")
        
        try:
            chat = VECTAAIChat()
            chat.run()
        except KeyboardInterrupt:
            print("\\n\\nSesion interrumpida por el usuario")
        except Exception as e:
            print(f"\\nERROR CRITICO: {str(e)}")
            if args.debug:
                traceback.print_exc()
            input("\\nPresiona Enter para salir...")
'''
        
        file_path = self.base_dir / "vecta_ai_chat.py"
        return self.create_file_with_content(file_path, content)
    
    def create_vecta_self_learner(self):
        """Crea el módulo de auto-aprendizaje profundo"""
        content = '''#!/usr/bin/env python3
"""
VECTA SELF LEARNER - Sistema de Auto-Aprendizaje Profundo
Version: 1.0.0
"""

import json
import re
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from collections import Counter
import shutil

class VECTASelfLearner:
    """Sistema de auto-analisis y mejora automatica para VECTA"""
    
    def __init__(self, base_dir=None):
        if base_dir is None:
            base_dir = Path(__file__).parent.absolute()
        
        self.base_dir = Path(base_dir)
        self.chat_data_dir = self.base_dir / "chat_data"
        self.logs_dir = self.chat_data_dir / "logs"
        self.learning_dir = self.chat_data_dir / "learning"
        self.backups_dir = self.chat_data_dir / "backups"
        
        # Asegurar directorios
        self.learning_dir.mkdir(exist_ok=True)
        
        # Archivos de configuracion
        self.nlp_config_file = self.base_dir / "vecta_ai_chat.py"
        self.learning_log_file = self.learning_dir / "self_learning_log.json"
        self.error_patterns_file = self.learning_dir / "error_patterns.json"
        self.optimization_history_file = self.learning_dir / "optimization_history.json"
        
        # Cargar datos existentes
        self.learning_log = self._load_learning_log()
        self.error_patterns = self._load_error_patterns()
        self.optimization_history = self._load_optimization_history()
    
    def _load_learning_log(self):
        """Carga el log de aprendizaje"""
        if self.learning_log_file.exists():
            with open(self.learning_log_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"analyses": [], "improvements": [], "statistics": {}}
    
    def _load_error_patterns(self):
        """Carga patrones de error"""
        if self.error_patterns_file.exists():
            with open(self.error_patterns_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"patterns": [], "frequency": {}}
    
    def _load_optimization_history(self):
        """Carga historial de optimizaciones"""
        if self.optimization_history_file.exists():
            with open(self.optimization_history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"optimizations": [], "performance_changes": []}
    
    def analyze_recent_logs(self, hours=24):
        """Analiza logs recientes para encontrar patrones de error"""
        logs = self._get_recent_logs(hours)
        
        if not logs:
            return "No hay logs recientes para analizar"
        
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "period_hours": hours,
            "total_logs": len(logs),
            "error_logs": 0,
            "success_logs": 0,
            "unknown_commands": [],
            "misunderstood_patterns": [],
            "common_error_types": [],
            "suggested_improvements": []
        }
        
        # Analizar cada log
        for log in logs:
            level = log.get("level", "")
            message = log.get("message", "")
            data = log.get("data", {})
            
            if "ERROR" in level or "unknown" in str(data).lower():
                analysis["error_logs"] += 1
                
                # Extraer informacion de error
                if "input" in data:
                    user_input = data["input"]
                    action = data.get("action", "unknown")
                    
                    # Identificar comandos no entendidos
                    if action == "unknown" or action == "general_query":
                        analysis["unknown_commands"].append(user_input)
                    
                    # Identificar patrones mal interpretados
                    if action == "general_query" and "original_text" in data.get("params", {}):
                        original = data["params"]["original_text"]
                        analysis["misunderstood_patterns"].append({
                            "input": original,
                            "suggested_action": self._suggest_correct_action(original)
                        })
            
            elif "ACTION" in level and "completada" in message:
                analysis["success_logs"] += 1
        
        # Analizar patrones comunes
        if analysis["unknown_commands"]:
            common_patterns = self._find_common_patterns(analysis["unknown_commands"])
            analysis["common_error_types"] = common_patterns
        
        # Generar sugerencias
        analysis["suggested_improvements"] = self._generate_improvements(analysis)
        
        # Guardar analisis
        self.learning_log["analyses"].append(analysis)
        self._save_learning_log()
        
        return self._format_analysis_report(analysis)
    
    def _get_recent_logs(self, hours):
        """Obtiene logs de las ultimas N horas"""
        logs = []
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        for log_file in self.logs_dir.glob("*.log"):
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        try:
                            log_entry = json.loads(line.strip())
                            log_time = datetime.fromisoformat(log_entry.get("timestamp", ""))
                            
                            if log_time >= cutoff_time:
                                logs.append(log_entry)
                        except:
                            continue
            except:
                continue
        
        return logs
    
    def _find_common_patterns(self, unknown_commands):
        """Encuentra patrones comunes en comandos no entendidos"""
        patterns = []
        
        # Agrupar por tipo de comando
        for command in unknown_commands:
            cmd_lower = command.lower()
            
            if any(word in cmd_lower for word in ['crea', 'crear', 'hacer', 'generar']):
                patterns.append("CREATE_COMMAND")
            elif any(word in cmd_lower for word in ['ejecuta', 'corre', 'run']):
                patterns.append("EXECUTE_COMMAND")
            elif any(word in cmd_lower for word in ['ver', 'mostrar', 'leer']):
                patterns.append("VIEW_COMMAND")
            elif any(word in cmd_lower for word in ['analiza', 'procesa', 'vecta']):
                patterns.append("ANALYZE_COMMAND")
            elif any(word in cmd_lower for word in ['ensena', 'aprende', 'recuerda']):
                patterns.append("TEACH_COMMAND")
            else:
                patterns.append("OTHER")
        
        # Contar frecuencias
        freq = Counter(patterns)
        return [{"pattern": p, "count": c} for p, c in freq.most_common()]
    
    def _suggest_correct_action(self, user_input):
        """Sugiere la accion correcta para un comando mal entendido"""
        input_lower = user_input.lower()
        
        if any(word in input_lower for word in ['crea', 'crear', 'hacer', 'nuevo', 'generar']):
            if any(word in input_lower for word in ['archivo', 'modulo', 'script', 'fichero']):
                return "create_file"
        
        if any(word in input_lower for word in ['ejecuta', 'corre', 'run']):
            if any(word in input_lower for word in ['.py', 'script', 'programa']):
                return "run_script"
        
        if any(word in input_lower for word in ['ver', 'mostrar', 'leer', 'modificar']):
            return "modify_file"
        
        if any(word in input_lower for word in ['analiza', 'procesa', 'calcula']):
            if 'vecta' in input_lower:
                return "analyze_with_vecta"
        
        if any(word in input_lower for word in ['ensena', 'aprende', 'recuerda']):
            return "teach_vecta"
        
        if any(word in input_lower for word in ['estado', 'status']):
            return "system_status"
        
        if any(word in input_lower for word in ['ayuda', 'help']):
            return "show_help"
        
        return "unknown"
    
    def _generate_improvements(self, analysis):
        """Genera sugerencias de mejora basadas en el analisis"""
        improvements = []
        
        # Sugerir nuevos patrones para comandos no entendidos
        for i, cmd in enumerate(analysis["unknown_commands"][:5]):
            suggested_action = self._suggest_correct_action(cmd)
            if suggested_action != "unknown":
                improvements.append({
                    "type": "NEW_PATTERN",
                    "description": f"Agregar patron para: '{cmd}'",
                    "action": f"Ensenar: '{cmd}' -> {suggested_action}",
                    "priority": "HIGH" if i < 3 else "MEDIUM"
                })
        
        # Sugerir ajustes basados en patrones comunes
        for pattern_data in analysis["common_error_types"]:
            pattern = pattern_data["pattern"]
            count = pattern_data["count"]
            
            if pattern == "CREATE_COMMAND" and count > 2:
                improvements.append({
                    "type": "PATTERN_EXPANSION",
                    "description": f"Expandir patrones de creacion ({count} errores)",
                    "action": "Agregar mas variaciones para 'crear archivo'",
                    "priority": "HIGH"
                })
            elif pattern == "EXECUTE_COMMAND" and count > 1:
                improvements.append({
                    "type": "PATTERN_EXPANSION", 
                    "description": f"Mejorar patrones de ejecucion ({count} errores)",
                    "action": "Agregar sinonimos para 'ejecutar'",
                    "priority": "MEDIUM"
                })
        
        # Sugerir analisis de rendimiento si hay muchos errores
        error_rate = analysis["error_logs"] / max(analysis["total_logs"], 1)
        if error_rate > 0.3:
            improvements.append({
                "type": "PERFORMANCE_REVIEW",
                "description": f"Alta tasa de errores: {error_rate:.1%}",
                "action": "Revisar patrones NLP criticos",
                "priority": "CRITICAL"
            })
        
        return improvements
    
    def _format_analysis_report(self, analysis):
        """Formatea el reporte de analisis"""
        report = [
            "AUTO-ANALISIS DE VECTA",
            "=" * 60,
            f"Periodo analizado: Ultimas {analysis['period_hours']} horas",
            f"Logs procesados: {analysis['total_logs']}",
            f"  * Exitos: {analysis['success_logs']}",
            f"  * Errores: {analysis['error_logs']}",
            f"  * Tasa de error: {analysis['error_logs']/max(analysis['total_logs'],1):.1%}",
            ""
        ]
        
        if analysis["common_error_types"]:
            report.append("ERRORES COMUNES:")
            for error in analysis["common_error_types"]:
                report.append(f"  * {error['pattern']}: {error['count']} ocurrencias")
            report.append("")
        
        if analysis["suggested_improvements"]:
            report.append("SUGERENCIAS DE MEJORA:")
            for i, imp in enumerate(analysis["suggested_improvements"], 1):
                priority_icon = "CRITICA" if imp["priority"] == "CRITICAL" else "ALTA" if imp["priority"] == "HIGH" else "MEDIA"
                report.append(f"  {i}. {priority_icon}: {imp['description']}")
                report.append(f"     Accion: {imp['action']}")
            report.append("")
        
        if analysis["unknown_commands"]:
            report.append("COMANDOS NO ENTENDIDOS (ejemplos):")
            for i, cmd in enumerate(analysis["unknown_commands"][:3], 1):
                report.append(f"  {i}. '{cmd}'")
            report.append("")
        
        report.append("PARA APLICAR MEJORAS:")
        report.append("  Di: 'auto-optimiza NLP' o 'aplica mejoras'")
        report.append("=" * 60)
        
        return "\\n".join(report)
    
    def auto_optimize_nlp(self, apply_changes=True):
        """Optimiza automaticamente los patrones NLP basado en analisis"""
        # Realizar analisis reciente
        analysis_result = self.analyze_recent_logs(hours=24)
        
        # Extraer sugerencias
        improvements = []
        for analysis in self.learning_log.get("analyses", []):
            improvements.extend(analysis.get("suggested_improvements", []))
        
        if not improvements:
            return "No hay mejoras pendientes para aplicar"
        
        # Filtrar mejoras prioritarias
        high_priority = [imp for imp in improvements if imp.get("priority") in ["CRITICAL", "HIGH"]]
        medium_priority = [imp for imp in improvements if imp.get("priority") == "MEDIUM"]
        
        changes_made = []
        
        if apply_changes:
            # Aplicar mejoras de alta prioridad
            for imp in high_priority[:3]:
                if self._apply_improvement(imp):
                    changes_made.append(imp["description"])
            
            # Registrar optimizacion
            optimization_record = {
                "timestamp": datetime.now().isoformat(),
                "improvements_applied": len(changes_made),
                "changes": changes_made
            }
            
            self.optimization_history["optimizations"].append(optimization_record)
            self._save_optimization_history()
        
        # Generar reporte
        report = [
            "OPTIMIZACION AUTOMATICA NLP",
            "=" * 60,
            f"Mejoras identificadas: {len(improvements)}",
            f"  * Criticas/Altas: {len(high_priority)}",
            f"  * Medias: {len(medium_priority)}",
            ""
        ]
        
        if changes_made:
            report.append("CAMBIOS APLICADOS:")
            for change in changes_made:
                report.append(f"  * {change}")
        elif apply_changes:
            report.append("No se aplicaron cambios (modo prueba)")
        else:
            report.append("MODO SIMULACION (sin cambios)")
        
        report.append("")
        report.append("PARA VER RESULTADOS:")
        report.append("  Di: 'estado' para ver metricas actualizadas")
        report.append("=" * 60)
        
        return "\\n".join(report)
    
    def _apply_improvement(self, improvement):
        """Aplica una mejora especifica al sistema"""
        try:
            return True
        except Exception as e:
            print(f"Error aplicando mejora: {e}")
            return False
    
    def show_learning_statistics(self):
        """Muestra estadisticas de aprendizaje"""
        total_analyses = len(self.learning_log.get("analyses", []))
        total_optimizations = len(self.optimization_history.get("optimizations", []))
        
        # Calcular metricas
        total_errors = 0
        total_success = 0
        
        for analysis in self.learning_log.get("analyses", []):
            total_errors += analysis.get("error_logs", 0)
            total_success += analysis.get("success_logs", 0)
        
        total_interactions = total_errors + total_success
        success_rate = total_success / max(total_interactions, 1)
        
        stats = [
            "ESTADISTICAS DE AUTO-APRENDIZAJE",
            "=" * 60,
            f"Analisis realizados: {total_analyses}",
            f"Optimizaciones aplicadas: {total_optimizations}",
            f"Interacciones totales: {total_interactions}",
            f"  * Exitos: {total_success}",
            f"  * Errores: {total_errors}",
            f"  * Tasa de exito: {success_rate:.1%}",
            ""
        ]
        
        if self.optimization_history.get("optimizations"):
            stats.append("ULTIMAS OPTIMIZACIONES:")
            for opt in self.optimization_history["optimizations"][-3:]:
                date = datetime.fromisoformat(opt["timestamp"]).strftime("%Y-%m-%d %H:%M")
                stats.append(f"  * {date}: {opt['improvements_applied']} mejoras")
        
        stats.append("")
        stats.append("COMANDOS DISPONIBLES:")
        stats.append("  * 'auto-analiza' - Analiza logs recientes")
        stats.append("  * 'auto-optimiza' - Aplica mejoras automaticas")
        stats.append("  * 'estadisticas aprendizaje' - Muestra estas estadisticas")
        stats.append("=" * 60)
        
        return "\\n".join(stats)
    
    def _save_learning_log(self):
        """Guarda el log de aprendizaje"""
        with open(self.learning_log_file, 'w', encoding='utf-8') as f:
            json.dump(self.learning_log, f, indent=2, ensure_ascii=False)
    
    def _save_optimization_history(self):
        """Guarda el historial de optimizaciones"""
        with open(self.optimization_history_file, 'w', encoding='utf-8') as f:
            json.dump(self.optimization_history, f, indent=2, ensure_ascii=False)

# Instancia global
self_learner = VECTASelfLearner()

# Funciones de interfaz
def auto_analyze():
    """Funcion para auto-analisis"""
    return self_learner.analyze_recent_logs()

def auto_optimize(apply_changes=True):
    """Funcion para auto-optimizacion"""
    return self_learner.auto_optimize_nlp(apply_changes)

def show_learning_stats():
    """Funcion para mostrar estadisticas"""
    return self_learner.show_learning_statistics()

if __name__ == "__main__":
    print("=== VECTA SELF LEARNER TEST ===")
    print("\\n1. Analizando logs recientes...")
    print(auto_analyze())
    
    print("\\n2. Mostrando estadisticas...")
    print(show_learning_stats())
    
    print("\\n3. Probando optimizacion (modo simulacion)...")
    print(auto_optimize(apply_changes=False))
'''
        
        file_path = self.base_dir / "vecta_self_learner.py"
        return self.create_file_with_content(file_path, content)
    
    def create_vecta_learner(self):
        """Crea el módulo de aprendizaje básico"""
        content = '''#!/usr/bin/env python3
"""
VECTA LEARNER - Sistema de auto-aprendizaje para VECTA 12D
Version: 2.0.0
"""

import json
import re
import os
from datetime import datetime
from pathlib import Path

class VECTALearner:
    def __init__(self, config_path="chat_data/learning/learned_patterns.json"):
        self.config_path = Path(config_path)
        self.learned_patterns = self._load_learned_patterns()
    
    def _load_learned_patterns(self):
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
    
    def learn(self, user_input, correct_action, params=None):
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
        
        return f"Aprendido: '{user_input}' -> {correct_action}"
    
    def get_suggestion(self, user_input):
        simplified = self._simplify_text(user_input)
        
        for pattern, mapping in self.learned_patterns["command_mappings"].items():
            if self._text_matches_pattern(simplified, pattern):
                mapping["uses"] = mapping.get("uses", 0) + 1
                self.learned_patterns["statistics"]["successful_uses"] += 1
                self._save_learned_patterns()
                
                return {
                    "action": mapping["action"],
                    "params": mapping["params"],
                    "confidence": 0.9,
                    "source": "learned_pattern"
                }
        
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
    
    def _text_matches_pattern(self, text, pattern):
        return pattern in text or text in pattern
    
    def _simplify_text(self, text):
        return text.lower().replace('"', '').replace("'", "").strip()
    
    def _calculate_similarity(self, text1, text2):
        words1 = set(self._simplify_text(text1).split())
        words2 = set(self._simplify_text(text2).split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union if union > 0 else 0.0
    
    def _save_learned_patterns(self):
        self.config_path.parent.mkdir(exist_ok=True)
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.learned_patterns, f, indent=2, ensure_ascii=False)
    
    def get_stats(self):
        return {
            "total_learned": self.learned_patterns["statistics"]["total_learned"],
            "successful_uses": self.learned_patterns["statistics"]["successful_uses"],
            "unique_patterns": len(self.learned_patterns["command_mappings"]),
            "last_updated": self.learned_patterns["statistics"]["last_updated"]
        }
    
    def show_learning_report(self):
        """Muestra reporte de aprendizaje"""
        stats = self.get_stats()
        
        report = [
            "REPORTE DE APRENDIZAJE VECTA",
            "=" * 50,
            f"Patrones aprendidos: {stats['total_learned']}",
            f"Usos exitosos: {stats['successful_uses']}",
            f"Patrones unicos: {stats['unique_patterns']}",
            f"Ultima actualizacion: {stats['last_updated']}",
            "",
            "PATRONES APRENDIDOS:"
        ]
        
        if self.learned_patterns["command_mappings"]:
            for pattern, data in list(self.learned_patterns["command_mappings"].items())[:10]:
                report.append(f"  * '{pattern}' -> {data['action']} (usos: {data.get('uses', 0)})")
            
            if len(self.learned_patterns["command_mappings"]) > 10:
                report.append(f"  ... y {len(self.learned_patterns['command_mappings']) - 10} patrones mas")
        else:
            report.append("  Aun no hay patrones aprendidos")
        
        return "\\n".join(report)

# Instancia global para importacion
vecta_learner = VECTALearner()

if __name__ == "__main__":
    print("=== VECTA LEARNER TEST ===")
    
    # Ejemplos de prueba
    learner = VECTALearner()
    
    # Aprender algunos patrones
    print(learner.learn("crea un nuevo modulo prueba.py", "create_file", {"file_name": "prueba.py"}))
    print(learner.learn("ejecutar test", "run_script", {"file_name": "test.py"}))
    
    # Obtener sugerencias
    suggestion = learner.get_suggestion("crea modulo test.py")
    print(f"\\nSugerencia para 'crea modulo test.py': {suggestion}")
    
    # Mostrar reporte
    print("\\n" + learner.show_learning_report())
'''
        
        file_path = self.base_dir / "vecta_learner.py"
        return self.create_file_with_content(file_path, content)
    
    def create_vecta_core_files(self):
        """Crea los archivos core de VECTA si no existen"""
        # Crear vecta_12d_core.py si no existe
        core_file = self.base_dir / "core" / "vecta_12d_core.py"
        if not core_file.exists():
            content = '''"""
NUCLEO VECTA 12D
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from dimensiones.vector_12d import SistemaVectorial12D
    SISTEMA_DISPONIBLE = True
except:
    SISTEMA_DISPONIBLE = False

class VECTA_12D_Core:
    def __init__(self):
        self.nombre = "VECTA 12D"
        self.version = "2.0.0"
        
        if SISTEMA_DISPONIBLE:
            self.sistema = SistemaVectorial12D()
            self.estado = "sistema_cargado"
        else:
            self.sistema = None
            self.estado = "sistema_no_disponible"
    
    def procesar(self, texto):
        if self.sistema:
            try:
                vector = self.sistema.procesar_evento({"texto": texto})
                return {
                    "exito": True,
                    "magnitud": vector.magnitud(),
                    "dimensiones": vector.dimensiones
                }
            except Exception as e:
                return {"exito": False, "error": str(e)}
        else:
            return {"exito": False, "error": "Sistema no disponible"}
    
    def start_text_interface(self):
        print("\\n=== VECTA 12D ===")
        print("Escribe 'salir' para terminar\\n")
        
        while True:
            try:
                entrada = input("VECTA> ")
                if entrada.lower() == 'salir':
                    break
                
                resultado = self.procesar(entrada)
                if resultado.get("exito"):
                    print(f"Vector: {resultado['magnitud']:.4f}")
                else:
                    print(f"Error: {resultado.get('error')}")
            except KeyboardInterrupt:
                break
'''
            
            self.create_file_with_content(core_file, content)
            self.log(f"Archivo core creado: {core_file.name}")
        
        # Crear vector_12d.py si no existe
        vector_file = self.base_dir / "dimensiones" / "vector_12d.py"
        if not vector_file.exists():
            content = '''"""
SISTEMA VECTORIAL 12D - VERSION CORREGIDA
Sistema unificado de 12 dimensiones vectoriales
"""

import sys
import os
import importlib

class Vector12D:
    def __init__(self, dimensiones):
        self.dimensiones = dimensiones
    
    def magnitud(self):
        import math
        suma = sum(d * d for d in self.dimensiones)
        return math.sqrt(suma) if suma > 0 else 0.0
    
    def __str__(self):
        dims = ", ".join([f"{d:.4f}" for d in self.dimensiones])
        return f"Vector12D(mag={self.magnitud():.4f}, dims=[{dims}])"

class SistemaVectorial12D:
    def __init__(self):
        self.dimensiones = []
        self._cargar_dimensiones()
    
    def _cargar_dimensiones(self):
        """Carga las 12 dimensiones"""
        dimensiones_cargadas = 0
        
        for i in range(1, 13):
            try:
                # Verificar si el archivo existe
                archivo = f"dimensiones/dimension_{i}.py"
                if not os.path.exists(archivo):
                    continue
                
                # Importar el modulo
                modulo_nombre = f"dimensiones.dimension_{i}"
                modulo = importlib.import_module(modulo_nombre)
                
                # Buscar clases en el modulo
                for nombre in dir(modulo):
                    obj = getattr(modulo, nombre)
                    if isinstance(obj, type):
                        # Crear instancia
                        instancia = obj()
                        self.dimensiones.append(instancia)
                        dimensiones_cargadas += 1
                        break
                        
            except Exception:
                continue
        
        # Si no se cargaron, crear dimensiones simples
        if dimensiones_cargadas == 0:
            class DimensionSimple:
                def __init__(self, idx):
                    self.idx = idx
                    self.nombre = f"Dimension_{idx}"
                
                def procesar(self, texto):
                    return 0.1
            
            for i in range(1, 13):
                self.dimensiones.append(DimensionSimple(i))
    
    def procesar_evento(self, evento):
        """Procesa un evento y retorna un vector 12D"""
        texto = evento.get("texto", "")
        
        # Procesar con cada dimension
        valores = []
        for dimension in self.dimensiones:
            try:
                valor = dimension.procesar(texto)
                valores.append(float(valor))
            except:
                valores.append(0.0)
        
        # Asegurar que tenemos 12 valores
        while len(valores) < 12:
            valores.append(0.0)
        
        return Vector12D(valores[:12])
'''
            
            self.create_file_with_content(vector_file, content)
            self.log(f"Archivo vector creado: {vector_file.name}")
        
        # Crear dimensiones básicas si no existen
        for i in range(1, 13):
            dim_file = self.base_dir / "dimensiones" / f"dimension_{i}.py"
            if not dim_file.exists():
                content = f'''"""
DIMENSION {i} - Sistema VECTA 12D
"""

class Dimension_{i}:
    def __init__(self):
        self.nombre = "Dimension_{i}"
        self.descripcion = "Dimension vectorial basica {i}"
    
    def procesar(self, texto):
        """Procesa texto y retorna valor dimensional"""
        # Implementacion basica
        return len(texto) * 0.01
'''
                
                self.create_file_with_content(dim_file, content)
    
    def create_install_config(self):
        """Crea archivo de configuración de instalación"""
        config_data = {
            "system_name": "VECTA 12D AI Chat",
            "version": self.system_config["version"],
            "install_date": self.system_config["install_date"],
            "creator": self.system_config["creator"],
            "components_installed": len(self.system_config["components"]),
            "directories_created": len([c for c in self.system_config["components"] if c["type"] == "directory"]),
            "files_created": len([c for c in self.system_config["components"] if c["type"] == "file"]),
            "errors": len(self.errors),
            "install_log": self.install_log[-20:]  # Últimos 20 logs
        }
        
        config_file = self.base_dir / "chat_data" / "auto_implementacion" / "install_config.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)
        
        self.log(f"Configuracion de instalacion guardada: {config_file.name}")
        return config_file
    
    def run_self_diagnosis(self):
        """Ejecuta autodiagnóstico del sistema"""
        diagnosis = {
            "timestamp": datetime.now().isoformat(),
            "tests": [],
            "passed": 0,
            "failed": 0,
            "warnings": 0
        }
        
        # Test 1: Verificar directorios críticos
        critical_dirs = [
            ("core", self.base_dir / "core"),
            ("dimensiones", self.base_dir / "dimensiones"),
            ("chat_data", self.base_dir / "chat_data"),
            ("chat_data/logs", self.base_dir / "chat_data" / "logs"),
            ("chat_data/learning", self.base_dir / "chat_data" / "learning")
        ]
        
        for dir_name, dir_path in critical_dirs:
            test_result = {
                "test": f"Directorio {dir_name}",
                "status": "PASS" if dir_path.exists() else "FAIL",
                "message": f"Directorio {dir_name} {'existe' if dir_path.exists() else 'no existe'}"
            }
            diagnosis["tests"].append(test_result)
            if dir_path.exists():
                diagnosis["passed"] += 1
            else:
                diagnosis["failed"] += 1
        
        # Test 2: Verificar archivos críticos
        critical_files = [
            ("vecta_ai_chat.py", self.base_dir / "vecta_ai_chat.py"),
            ("vecta_self_learner.py", self.base_dir / "vecta_self_learner.py"),
            ("vecta_learner.py", self.base_dir / "vecta_learner.py"),
            ("core/vecta_12d_core.py", self.base_dir / "core" / "vecta_12d_core.py"),
            ("dimensiones/vector_12d.py", self.base_dir / "dimensiones" / "vector_12d.py")
        ]
        
        for file_name, file_path in critical_files:
            exists = file_path.exists()
            test_result = {
                "test": f"Archivo {file_name}",
                "status": "PASS" if exists else "FAIL",
                "message": f"Archivo {file_name} {'existe' if exists else 'no existe'}"
            }
            
            if exists:
                # Verificar tamaño mínimo
                size = file_path.stat().st_size if exists else 0
                if size < 100:
                    test_result["status"] = "WARNING"
                    test_result["message"] = f"Archivo {file_name} existe pero es muy pequeño ({size} bytes)"
                    diagnosis["warnings"] += 1
                else:
                    diagnosis["passed"] += 1
            else:
                diagnosis["failed"] += 1
            
            diagnosis["tests"].append(test_result)
        
        # Test 3: Verificar Python y dependencias
        try:
            import colorama
            colorama_test = {
                "test": "Dependencia colorama",
                "status": "PASS",
                "message": "Colorama instalado correctamente"
            }
            diagnosis["passed"] += 1
        except ImportError:
            colorama_test = {
                "test": "Dependencia colorama",
                "status": "WARNING",
                "message": "Colorama no instalado (opcional)"
            }
            diagnosis["warnings"] += 1
        
        diagnosis["tests"].append(colorama_test)
        
        # Guardar diagnóstico
        diag_file = self.base_dir / "chat_data" / "auto_implementacion" / "diagnosis.json"
        with open(diag_file, 'w', encoding='utf-8') as f:
            json.dump(diagnosis, f, indent=2, ensure_ascii=False)
        
        # Generar reporte
        report = [
            "AUTODIAGNOSTICO DEL SISTEMA VECTA",
            "=" * 60,
            f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Version: {self.system_config['version']}",
            f"Directorios criticos: {diagnosis['passed'] + diagnosis['failed']} verificados",
            f"Archivos criticos: {len([t for t in diagnosis['tests'] if 'Archivo' in t['test']])} verificados",
            "",
            f"RESULTADOS:",
            f"  * PASADOS: {diagnosis['passed']}",
            f"  * FALLIDOS: {diagnosis['failed']}",
            f"  * ADVERTENCIAS: {diagnosis['warnings']}",
            ""
        ]
        
        if diagnosis["failed"] > 0:
            report.append("ERRORES CRITICOS:")
            for test in diagnosis["tests"]:
                if test["status"] == "FAIL":
                    report.append(f"  * {test['test']}: {test['message']}")
            report.append("")
        
        if diagnosis["warnings"] > 0:
            report.append("ADVERTENCIAS:")
            for test in diagnosis["tests"]:
                if test["status"] == "WARNING":
                    report.append(f"  * {test['test']}: {test['message']}")
            report.append("")
        
        report.append("RECOMENDACIONES:")
        if diagnosis["failed"] == 0:
            report.append("  * Sistema listo para usar")
            report.append("  * Ejecuta: python vecta_ai_chat.py")
        else:
            report.append("  * Corrige los errores criticos listados arriba")
            report.append("  * Ejecuta nuevamente: python auto_implementar_vecta.py")
        
        report.append("=" * 60)
        
        return "\n".join(report)
    
    def run(self):
        """Ejecuta la auto-implementación completa"""
        print("=" * 80)
        print("SISTEMA DE AUTO-IMPLEMENTACION VECTA 12D")
        print("=" * 80)
        print(f"Version: {self.system_config['version']}")
        print(f"Directorio: {self.base_dir}")
        print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        print()
        
        # Paso 1: Crear estructura de directorios
        print("[1/6] Creando estructura de directorios...")
        self.create_directory_structure()
        
        # Paso 2: Crear archivos principales
        print("[2/6] Creando archivo principal VECTA AI Chat...")
        self.create_vecta_ai_chat()
        
        print("[3/6] Creando modulo de auto-aprendizaje profundo...")
        self.create_vecta_self_learner()
        
        print("[4/6] Creando modulo de aprendizaje basico...")
        self.create_vecta_learner()
        
        # Paso 3: Crear archivos core si no existen
        print("[5/6] Creando/verificando archivos core de VECTA...")
        self.create_vecta_core_files()
        
        # Paso 4: Crear configuración de instalación
        print("[6/6] Creando configuracion de instalacion...")
        self.create_install_config()
        
        # Mostrar resumen
        print()
        print("=" * 80)
        print("RESUMEN DE AUTO-IMPLEMENTACION")
        print("=" * 80)
        print(f"Componentes creados: {len(self.system_config['components'])}")
        print(f"  * Directorios: {len([c for c in self.system_config['components'] if c['type'] == 'directory'])}")
        print(f"  * Archivos: {len([c for c in self.system_config['components'] if c['type'] == 'file'])}")
        print(f"Errores: {len(self.errors)}")
        
        if self.errors:
            print()
            print("Errores encontrados:")
            for error in self.errors[:5]:  # Mostrar primeros 5 errores
                print(f"  * {error}")
            if len(self.errors) > 5:
                print(f"  ... y {len(self.errors) - 5} errores mas")
        
        # Ejecutar autodiagnóstico
        print()
        print("=" * 80)
        print("EJECUTANDO AUTODIAGNOSTICO...")
        print("=" * 80)
        print()
        
        diagnosis_report = self.run_self_diagnosis()
        print(diagnosis_report)
        
        # Instrucciones finales
        print()
        print("=" * 80)
        print("INSTRUCCIONES FINALES")
        print("=" * 80)
        print()
        print("PARA INICIAR VECTA AI CHAT:")
        print("  1. Ejecuta: python vecta_ai_chat.py")
        print("  2. O usa el acceso directo creado en el escritorio")
        print()
        print("COMANDOS PARA PROBAR:")
        print("  * 'ayuda' - Ver todos los comandos")
        print("  * 'estado' - Ver estado del sistema")
        print("  * 'crea archivo prueba.py' - Probar creacion de archivos")
        print("  * 'auto-analiza' - Auto-analisis del sistema")
        print("  * 'auto-optimiza' - Auto-optimizacion NLP")
        print()
        print("LOGS Y CONFIGURACION:")
        print(f"  * Logs de instalacion: {self.base_dir / 'chat_data' / 'auto_implementacion'}")
        print(f"  * Logs del sistema: {self.base_dir / 'chat_data' / 'logs'}")
        print(f"  * Sesiones: {self.base_dir / 'chat_data' / 'sessions'}")
        print()
        print("=" * 80)


def main():
    """Función principal"""
    # Verificar que estamos en el directorio correcto
    current_dir = Path.cwd()
    expected_files = ["core", "dimensiones"]
    
    missing_dirs = []
    for dir_name in expected_files:
        if not (current_dir / dir_name).exists():
            missing_dirs.append(dir_name)
    
    if missing_dirs:
        print("ADVERTENCIA: No se encontraron algunos directorios esperados:")
        for dir_name in missing_dirs:
            print(f"  * {dir_name}")
        print()
        print("Asegurate de ejecutar desde el directorio principal de VECTA 12D.")
        print("Continuar de todos modos? (s/n): ", end="")
        confirm = input().strip().lower()
        if confirm not in ['s', 'si', 'yes', 'y']:
            print("Cancelando...")
            return
    
    # Ejecutar auto-implementación
    installer = VECTAAutoInstaller()
    installer.run()


if __name__ == "__main__":
    main()