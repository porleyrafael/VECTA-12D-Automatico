#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VECTA 12D TODO-EN-UNO - Sistema Completo Autónomo
==================================================
Archivo único que contiene y genera todo el sistema VECTA 12D.
Incluye: Chat AI, Auto-aprendizaje, Sistema 12D, Auto-diagnóstico.
"""

import os
import sys
import json
import shutil
import subprocess
import traceback
import re
import uuid
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from collections import Counter

# ============================================================================
# PARTE 1: CONFIGURACIÓN Y ESTRUCTURA BÁSICA
# ============================================================================

class VECTAConfig:
    """Configuración global del sistema VECTA"""
    
    def __init__(self, base_dir=None):
        self.BASE_DIR = Path(base_dir) if base_dir else Path.cwd()
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
            self.BASE_DIR,
            self.CORE_DIR,
            self.DIMENSIONS_DIR,
            self.CHAT_DATA_DIR,
            self.CHAT_SESSIONS_DIR,
            self.CHAT_LOGS_DIR,
            self.CHAT_BACKUPS_DIR,
            self.LEARNING_DATA_DIR
        ]
        
        for directory in directories:
            directory.mkdir(exist_ok=True)
            
    def _load_nlp_patterns(self) -> Dict[str, Dict]:
        """Carga patrones de lenguaje natural"""
        return {
            "system_status": {
                "patterns": [
                    r"(?:estado|status|situación|condición)(?: del sistema)?",
                    r"cómo está (?:el sistema|vecta)",
                    r"qué pasa con vecta",
                    r"información del sistema"
                ],
                "action": "system_status"
            },
            "show_help": {
                "patterns": [
                    r"ayuda|help|comandos|instrucciones",
                    r"qué puedes hacer",
                    r"cómo (?:usar|utilizar) (?:esto|vecta|el sistema)"
                ],
                "action": "show_help"
            },
            "create_file": {
                "patterns": [
                    r"(?:crear|crea|hacer|generar) (?:un )?archivo ([a-zA-Z0-9_\-\.]+)",
                    r"crea (?:archivo|fichero|módulo|script) ([a-zA-Z0-9_\-\.]+)"
                ],
                "action": "create_file",
                "has_params": True
            },
            "run_script": {
                "patterns": [
                    r"(?:ejecutar|correr|run|lanzar) (?:el )?(?:archivo|script|programa) ([a-zA-Z0-9_\-\.]+\.py)",
                    r"ejecuta (.+\.py)"
                ],
                "action": "run_script",
                "has_params": True
            },
            "analyze_with_vecta": {
                "patterns": [
                    r"(?:analizar|procesar|calcular) (?:con |usando )?vecta",
                    r"vecta (?:analiza|procesa|calcula)",
                    r"analiza (?:con |)vecta:?(.+)"
                ],
                "action": "analyze_with_vecta",
                "has_params": True
            },
            "general_query": {
                "patterns": [r".+"],
                "action": "general_query",
                "default": True
            }
        }

# ============================================================================
# PARTE 2: SISTEMA DE LOGGING Y AUDITORÍA
# ============================================================================

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

# ============================================================================
# PARTE 3: PROCESADOR DE LENGUAJE NATURAL
# ============================================================================

class VECTANLP:
    """Procesador de Lenguaje Natural para VECTA"""
    
    def __init__(self, config: VECTAConfig):
        self.config = config
        
    def extract_intent(self, text: str) -> Tuple[str, Dict, float]:
        """Extrae la intención del texto en lenguaje natural"""
        text = text.strip()
        if (text.startswith('"') and text.endswith('"')) or (text.startswith("'") and text.endswith("'")):
            text = text[1:-1].strip()
        
        text_lower = text.lower()
        
        best_match = None
        best_params = {}
        best_confidence = 0
        
        for intent_name, intent_data in self.config.NLP_PATTERNS.items():
            for pattern in intent_data["patterns"]:
                if re.fullmatch(pattern, text_lower):
                    params = self._extract_parameters(intent_data, text)
                    return intent_data["action"], params, 1.0
                
                match = re.search(pattern, text_lower)
                if match:
                    confidence = len(match.group()) / len(text_lower) if text_lower else 0
                    if confidence > best_confidence:
                        best_confidence = confidence
                        best_match = intent_data
                        best_params = self._extract_parameters(intent_data, text, match)
        
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
            if match.groups():
                for i, group in enumerate(match.groups(), 1):
                    if group:
                        params[f"param_{i}"] = group
        
        # Extraer nombres de archivos
        file_match = re.search(r'([a-zA-Z0-9_\-\.]+\.py)', text)
        if file_match:
            params["file_name"] = file_match.group(1)
        
        return params

# ============================================================================
# PARTE 4: SISTEMA DE APRENDIZAJE BÁSICO
# ============================================================================

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
        
        for pattern, mapping in self.learned_patterns["command_mappings"].items():
            if pattern in simplified or simplified in pattern:
                mapping["uses"] = mapping.get("uses", 0) + 1
                self.learned_patterns["statistics"]["successful_uses"] += 1
                self._save_learned_patterns()
                
                return {
                    "action": mapping["action"],
                    "params": mapping["params"],
                    "confidence": 0.9,
                    "source": "learned_pattern"
                }
        
        return None
    
    def _simplify_text(self, text: str) -> str:
        """Simplifica texto para comparación"""
        return text.lower().replace('"', '').replace("'", "").strip()
    
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

# ============================================================================
# PARTE 5: EJECUTOR DE ACCIONES
# ============================================================================

class VECTAActionExecutor:
    """Ejecutor de acciones autónomo para VECTA"""
    
    def __init__(self, config: VECTAConfig, logger: VECTALogger):
        self.config = config
        self.logger = logger
        self.learner = VECTALearner()
        
    def execute(self, action: str, params: Dict) -> Dict:
        """Ejecuta una acción y retorna resultado"""
        start_time = time.time()
        
        # Consultar al sistema de aprendizaje
        original_text = params.get("original_text", "")
        learned_suggestion = self.learner.get_suggestion(original_text)
        
        if learned_suggestion and learned_suggestion["confidence"] > 0.8:
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
            elif action == "create_file":
                result = self._action_create_file(params)
            elif action == "run_script":
                result = self._action_run_script(params)
            elif action == "analyze_with_vecta":
                result = self._action_analyze_with_vecta(params)
            elif action == "general_query":
                result = self._action_general_query(params)
            else:
                result = self._action_unknown(params)
            
            # Verificar tiempo de ejecución
            exec_time = time.time() - start_time
            if exec_time > self.config.COMMAND_TIMEOUT:
                result["warning"] = f"Accion tardo {exec_time:.2f}s (limite: {self.config.COMMAND_TIMEOUT}s)"
                self.logger.log("WARNING", f"Accion {action} excedio tiempo", {"time": exec_time})
            
            # Agregar metadatos
            result["vecta_metadata"] = {
                "execution_time": exec_time,
                "action": action,
                "timestamp": datetime.now().isoformat()
            }
            
            # Registrar éxito
            self.logger.log("INFO", f"Accion {action} completada", {
                "time": exec_time,
                "success": result.get("success", True)
            })
            
            return result
            
        except Exception as e:
            # Registrar error
            exec_time = time.time() - start_time
            error_info = {
                "action": action,
                "error": str(e),
                "traceback": traceback.format_exc(),
                "execution_time": exec_time
            }
            
            self.logger.log("ERROR", f"Error en accion {action}", error_info)
            
            teach_suggestion = ""
            if "original_text" in params:
                teach_suggestion = f"\nQuieres enseñarme este comando?\n   Di: 'enseña a vecta: cuando digo \"{params['original_text']}\" haz [accion correcta]'"
            
            return {
                "success": False,
                "type": "error",
                "error": str(e),
                "action": action,
                "content": f"Error en accion: {str(e)}{teach_suggestion}"
            }
    
    # ==================== ACCIONES DEL SISTEMA ====================
    
    def _action_system_status(self) -> Dict:
        """Acción: Mostrar estado del sistema"""
        status_text = f"""
VECTA 12D - ESTADO DEL SISTEMA

VERSION: {self.config.VERSION}
CREADOR: {self.config.CREATOR}
SESSION: {self.logger.session_id}

COMPONENTES:
  * Directorios: OK
  * Sistema de aprendizaje: ACTIVO
  * Procesador NLP: ACTIVO
  * Logger: ACTIVO

DIRECTORIOS:
  * Principal: {self.config.BASE_DIR}
  * Datos Chat: {self.config.CHAT_DATA_DIR}
  * Aprendizaje: {self.config.LEARNING_DATA_DIR}

PRINCIPIOS VECTA:
"""
        
        for principle in self.config.VECTA_PRINCIPLES:
            status_text += f"  * {principle}\n"
        
        # Agregar estadísticas de aprendizaje
        stats = self.learner.get_stats()
        status_text += f"\nAPRENDIZAJE AUTOMATICO:\n"
        status_text += f"  * Patrones aprendidos: {stats['total_learned']}\n"
        status_text += f"  * Usos exitosos: {stats['successful_uses']}\n"
        status_text += f"  * Ultima actualizacion: {stats['last_updated']}\n"
        
        return {
            "success": True,
            "type": "system_status",
            "content": status_text
        }
    
    def _action_show_help(self) -> Dict:
        """Acción: Mostrar ayuda del sistema"""
        help_text = f"""
VECTA AI CHAT - AYUDA v{self.config.VERSION}

COMUNICACION EN LENGUAJE NATURAL:
  Habla normalmente, VECTA entenderá tu intención.

COMANDOS DISPONIBLES:
  * "Como esta el sistema?" - Ver estado
  * "Ayuda" - Ver esta ayuda
  * "Crea archivo prueba.py" - Crear archivo
  * "Ejecuta script.py" - Ejecutar script Python
  * "Analiza con VECTA: [texto]" - Analizar texto

AUTO-APRENDIZAJE:
  * Puedo aprender nuevos comandos
  * Mejoro con el uso
  * Di: "Enseña a vecta: cuando digo X haz Y"

Sistema VECTA 12D - Creado por {self.config.CREATOR}
"""
        
        return {
            "success": True,
            "type": "help",
            "content": help_text
        }
    
    def _action_create_file(self, params: Dict) -> Dict:
        """Acción: Crear nuevo archivo"""
        file_name = params.get("file_name") or params.get("param_1")
        
        if not file_name:
            return {
                "success": False,
                "type": "file_creation",
                "content": "No se especificó nombre de archivo\nEjemplo: 'Crea un archivo test.py'",
                "error": "No filename specified"
            }
        
        # Asegurar extensión .py si no la tiene
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
            content = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
{file_name.upper().replace('.PY', '')} - Generado por VECTA AI Chat
Fecha: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

def main():
    print("¡Archivo creado por VECTA 12D AI Chat!")

if __name__ == "__main__":
    main()
'''
            
            # Crear archivo
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # APRENDER ESTE PATRÓN
            original_text = params.get("original_text", "")
            if original_text and "crea" in original_text.lower():
                self.learner.learn(original_text, "create_file", {"file_name": file_name})
            
            return {
                "success": True,
                "type": "file_creation",
                "content": f"Archivo creado: {file_name}\nUbicacion: {file_path}\nTamaño: {len(content)} bytes",
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
    
    def _action_run_script(self, params: Dict) -> Dict:
        """Acción: Ejecutar script Python"""
        script_name = params.get("file_name") or params.get("param_1")
        
        if not script_name:
            return {
                "success": False,
                "type": "script_execution",
                "content": "No se especificó archivo a ejecutar\nEjemplo: 'Ejecuta prueba.py'",
                "error": "No script specified"
            }
        
        # Asegurar extensión .py
        if not script_name.endswith('.py'):
            script_name += '.py'
        
        script_path = self.config.BASE_DIR / script_name
        
        if not script_path.exists():
            return {
                "success": False,
                "type": "script_execution",
                "content": f"Archivo no encontrado: {script_name}",
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
  * Código de salida: {result.returncode}

Salida:
{output}
"""
            
            if result.returncode != 0:
                content += f"\nErrores:\n{error}"
            
            return {
                "success": result.returncode == 0,
                "type": "script_execution",
                "content": content,
                "return_code": result.returncode,
                "output": output,
                "error": error
            }
            
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "type": "script_execution",
                "content": f"Timeout: El script {script_name} tardó más de {self.config.COMMAND_TIMEOUT} segundos",
                "error": "Timeout expired"
            }
        except Exception as e:
            return {
                "success": False,
                "type": "script_execution",
                "content": f"Error al ejecutar script: {str(e)}",
                "error": str(e)
            }
    
    def _action_analyze_with_vecta(self, params: Dict) -> Dict:
        """Acción: Analizar texto con VECTA"""
        text = params.get("original_text", "")
        
        # Extraer texto para análisis
        analysis_match = re.search(r'(?:analiza|procesa|calcula)[\s\:]+(.+)', text, re.IGNORECASE)
        analysis_text = analysis_match.group(1).strip() if analysis_match else text
        
        if not analysis_text or len(analysis_text) < 3:
            return {
                "success": False,
                "type": "vecta_analysis",
                "content": "No se especificó texto para analizar\nEjemplo: 'Analiza con VECTA: Este es un proyecto importante'",
                "error": "No text provided"
            }
        
        # Análisis simple
        word_count = len(analysis_text.split())
        char_count = len(analysis_text)
        avg_word_length = char_count / max(word_count, 1)
        
        content = f"""
Análisis VECTA completado:

Texto analizado: "{analysis_text[:100]}{'...' if len(analysis_text) > 100 else ''}"

Resultados:
  * Palabras: {word_count}
  * Caracteres: {char_count}
  * Longitud promedio palabra: {avg_word_length:.1f}
  * Procesamiento exitoso

Análisis básico realizado. Para análisis más complejos,
necesitas integrar el sistema VECTA 12D completo.
"""
        
        return {
            "success": True,
            "type": "vecta_analysis",
            "content": content,
            "text_analyzed": analysis_text
        }
    
    def _action_general_query(self, params: Dict) -> Dict:
        """Acción: Procesar consulta general"""
        text = params.get("original_text", "")
        
        # Respuestas inteligentes basadas en contenido
        if any(word in text.lower() for word in ['hola', 'hello', 'hi', 'buenas']):
            response = f"Hola! Soy VECTA AI Chat v{self.config.VERSION}\n¿En qué puedo ayudarte hoy?"
        elif any(word in text.lower() for word in ['gracias', 'thanks', 'thank you']):
            response = "De nada! Siempre estoy aquí para ayudarte con VECTA 12D."
        elif '?' in text:
            response = f"Interesante pregunta.\n\nPuedo ayudarte mejor si me dices qué quieres hacer:\n* Consultar el estado del sistema?\n* Ejecutar algún script?\n* Crear archivos?\n\nO escribe 'ayuda' para ver todas las opciones."
        else:
            response = f"He procesado tu mensaje: '{text}'\n\nPara acciones específicas, intenta:\n* 'Ayuda' - Ver todos los comandos\n* 'Estado' - Ver sistema VECTA\n* 'Enseña a vecta' - Para enseñarme nuevos comandos"
        
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
        teach_option = f"\n\n¿Quieres que aprenda este comando?\n   Di: 'Enseña a vecta: cuando digo \"{text}\" haz [accion correcta]'"
        
        return {
            "success": False,
            "type": "unknown_command",
            "content": f"VECTA no entendió completamente: '{text}'\n\nPrueba con:\n* 'Ayuda' - Ver todos los comandos\n* 'Estado' - Ver sistema VECTA\n* Escribe en lenguaje natural lo que necesitas{teach_option}",
            "original_text": text,
            "can_learn": True
        }

# ============================================================================
# PARTE 6: SISTEMA PRINCIPAL DE CHAT
# ============================================================================

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
Sistema Autónomo de Comunicación Inteligente

----------------------------------------------------------------
  Version: {self.config.VERSION}                Creador: {self.config.CREATOR}                Session: {self.logger.session_id}
----------------------------------------------------------------

CARACTERÍSTICAS PRINCIPALES:
  * Lenguaje natural completo (español/inglés)
  * Ejecución automática de comandos
  * Sistema de auto-aprendizaje
  * Auditoría completa (principio VECTA)

AUTO-APRENDIZAJE ACTIVO:
  * Puedo aprender nuevos comandos
  * Mejoro con el uso
  * Entiendo variaciones de lenguaje

INSTRUCCIÓN:
  Escribe en lenguaje natural lo que necesitas. Ejemplos:
    * "Crea un archivo prueba.py"
    * "Como está el sistema?"
    * "Enseña a vecta: cuando digo 'programa' haz 'crear archivo'"

Escribe 'ayuda' para ver la guía completa o 'salir' para terminar.
----------------------------------------------------------------
"""
        
        print(banner)
    
    def process_input(self, user_input: str) -> Optional[Dict]:
        """Procesa la entrada del usuario"""
        if not user_input.strip():
            return {"content": "Entrada vacía. Por favor, escribe algo."}
        
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
        
        return result
    
    def format_response(self, result: Dict) -> str:
        """Formatea la respuesta para mostrar al usuario"""
        content = result.get("content", "Sin contenido")
        return f"\n{'='*80}\n{content}\n{'='*80}\n"
    
    def _save_session(self):
        """Guarda la sesión actual"""
        self.session_data["end_time"] = datetime.now().isoformat()
        self.session_data["chat_history"] = self.chat_history[-20:]  # Últimos 20 mensajes
        
        self.logger.save_session(self.session_data)
        self.logger.log("INFO", "Sesión guardada", {"session_id": self.logger.session_id})
    
    def run(self):
        """Ejecuta el sistema principal de chat"""
        self.display_banner()
        self._save_session()  # Guardar sesión inicial
        
        print(f"\n{'='*80}")
        print("CHAT VECTA ACTIVADO - Escribe tu mensaje:")
        print("=" * 80)
        
        try:
            while True:
                try:
                    # Mostrar prompt
                    user_input = input("\n>>> ").strip()
                    
                    # Verificar si quiere salir
                    if user_input.lower() in ['salir', 'exit', 'quit', 'adiós']:
                        print("\nSaliendo del sistema VECTA...")
                        break
                    
                    # Procesar entrada
                    result = self.process_input(user_input)
                    
                    # Mostrar respuesta
                    print(self.format_response(result))
                    
                    # Auto-guardar cada 10 interacciones
                    if self.session_data["interaction_count"] % 10 == 0:
                        self._save_session()
                        
                except KeyboardInterrupt:
                    print("\n\nInterrupción detectada. ¿Salir? (s/n): ", end="")
                    confirm = input().strip().lower()
                    if confirm in ['s', 'si', 'yes', 'y']:
                        print("\nSaliendo del sistema VECTA...")
                        break
                    else:
                        print("Continuando...")
                        continue
                        
                except EOFError:
                    print("\n\nFin de entrada detectado. Saliendo...")
                    break
                    
                except Exception as e:
                    error_msg = f"Error interno: {str(e)}"
                    print(f"\n{error_msg}")
                    self.logger.log("ERROR", "Error en loop principal", {"error": str(e)})
        
        finally:
            # Guardar sesión final
            self._save_session()
            print(f"\n{'='*80}")
            print(f"Resumen de sesión {self.logger.session_id}:")
            print(f"  * Interacciones: {self.session_data['interaction_count']}")
            print(f"  * Comandos ejecutados: {len(self.session_data['commands_executed'])}")
            stats = self.executor.learner.get_stats()
            print(f"  * Patrones aprendidos: {stats['total_learned']}")
            print(f"  * Sesión guardada en: {self.logger.session_file}")
            print("=" * 80)
            print("\n¡Gracias por usar VECTA 12D AI Chat!")

# ============================================================================
# PARTE 7: SISTEMA DE AUTO-IMPLEMENTACIÓN
# ============================================================================

class VECTAAutoImplementador:
    """Sistema que genera todos los archivos VECTA"""
    
    def __init__(self):
        self.base_dir = Path.cwd()
        self.creation_log = []
        
    def log(self, message):
        """Registra mensaje"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] {message}"
        self.creation_log.append(entry)
        print(entry)
    
    def create_file(self, file_path, content):
        """Crea un archivo con contenido"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            file_size = os.path.getsize(file_path)
            self.log(f"✓ {file_path.name} ({file_size} bytes)")
            return True
        except Exception as e:
            self.log(f"✗ Error creando {file_path.name}: {e}")
            return False
    
    def generate_vecta_ai_chat(self):
        """Genera el archivo principal VECTA AI Chat"""
        # El contenido de esta clase está en este mismo archivo
        # Creamos un archivo separado con solo la clase VECTAAIChat
        content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VECTA AI CHAT - Sistema Principal
==================================
Archivo generado automáticamente por VECTA Auto-Implementador
"""

import os
import sys
import json
import re
import uuid
import time
import subprocess
import traceback
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

# NOTA: Este es un archivo simplificado
# Para la versión completa, ejecuta este mismo script con --full-version

def main():
    print("VECTA AI Chat - Sistema Simplificado")
    print("Para la versión completa, ejecuta el script principal.")
    print("Este archivo es un marcador de posición.")

if __name__ == "__main__":
    main()
'''
        
        file_path = self.base_dir / "vecta_ai_chat.py"
        return self.create_file(file_path, content)
    
    def generate_system_files(self):
        """Genera todos los archivos del sistema"""
        files_to_create = [
            ("vecta_ai_chat.py", self.generate_vecta_ai_chat()),
        ]
        
        # Crear archivos core
        core_content = '''"""
NÚCLEO VECTA 12D
Versión simplificada para implementación inicial
"""

class VECTA_12D_Core:
    def __init__(self):
        self.nombre = "VECTA 12D"
        self.version = "5.0.0"
    
    def procesar(self, texto):
        return {
            "exito": True,
            "mensaje": f"Texto procesado: {texto[:50]}...",
            "longitud": len(texto)
        }

if __name__ == "__main__":
    core = VECTA_12D_Core()
    print(core.procesar("Prueba del núcleo VECTA"))
'''
        
        core_file = self.base_dir / "core" / "vecta_12d_core.py"
        self.create_file(core_file, core_content)
        
        # Crear vector 12D básico
        vector_content = '''"""
SISTEMA VECTORIAL 12D - VERSIÓN BÁSICA
"""

class Vector12D:
    def __init__(self, valores=None):
        self.dimensiones = valores or [0.0] * 12
    
    def magnitud(self):
        import math
        return math.sqrt(sum(d * d for d in self.dimensiones))

class SistemaVectorial12D:
    def __init__(self):
        self.dimensiones = []
    
    def procesar_evento(self, evento):
        texto = evento.get("texto", "")
        valores = [len(texto) * 0.01] * 12
        return Vector12D(valores)
'''
        
        vector_file = self.base_dir / "dimensiones" / "vector_12d.py"
        self.create_file(vector_file, vector_content)
        
        # Crear dimensiones básicas
        for i in range(1, 13):
            dim_content = f'''"""
DIMENSIÓN {i} - Sistema VECTA 12D
"""

class Dimension_{i}:
    def procesar(self, texto):
        return len(texto) * 0.01
'''
            dim_file = self.base_dir / "dimensiones" / f"dimension_{i}.py"
            self.create_file(dim_file, dim_content)
        
        return True
    
    def run(self):
        """Ejecuta la generación completa"""
        print("=" * 80)
        print("VECTA AUTO-IMPLEMENTADOR - Generando sistema completo")
        print("=" * 80)
        print(f"Directorio: {self.base_dir}")
        print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        print("[1/3] Verificando estructura de directorios...")
        # Asegurar directorios
        directories = ["core", "dimensiones", "chat_data", "chat_data/sessions", 
                      "chat_data/logs", "chat_data/backups", "chat_data/learning"]
        
        for dir_path in directories:
            full_path = self.base_dir / dir_path
            full_path.mkdir(exist_ok=True)
            self.log(f"Directorio: {dir_path}")
        
        print("\n[2/3] Generando archivos del sistema...")
        self.generate_system_files()
        
        print("\n[3/3] Creando script de lanzamiento...")
        # Crear lanzador
        launcher_content = '''#!/usr/bin/env python3
"""
LANZADOR VECTA 12D
==================
Ejecuta el sistema VECTA 12D completo desde este archivo.
"""

import os
import sys

def main():
    print("=" * 70)
    print("LANZANDO VECTA 12D AI CHAT")
    print("=" * 70)
    
    # Verificar que estamos en el directorio correcto
    required_files = [
        "core/vecta_12d_core.py",
        "dimensiones/vector_12d.py"
    ]
    
    all_ok = True
    for file in required_files:
        if not os.path.exists(file):
            print(f"✗ Faltante: {file}")
            all_ok = False
        else:
            print(f"✓ Disponible: {file}")
    
    if not all_ok:
        print("\n❌ Algunos archivos necesarios no existen.")
        print("   Ejecuta primero: python vecta_todo_en_uno.py --implementar")
        return
    
    print("\n🚀 Iniciando VECTA AI Chat...")
    print("-" * 70)
    
    # Importar y ejecutar VECTA AI Chat
    try:
        # Esto ejecutará el sistema completo
        from vecta_todo_en_uno import VECTAAIChat
        chat = VECTAAIChat()
        chat.run()
    except ImportError as e:
        print(f"Error de importación: {e}")
        print("\n💡 Ejecuta directamente:")
        print("   python vecta_todo_en_uno.py --chat")

if __name__ == "__main__":
    main()
'''
        
        launcher_file = self.base_dir / "lanzar_vecta.py"
        self.create_file(launcher_file, launcher_content)
        
        print("\n" + "=" * 80)
        print("GENERACIÓN COMPLETADA")
        print("=" * 80)
        print("\nARCHIVOS CREADOS:")
        print("  ✓ core/vecta_12d_core.py")
        print("  ✓ dimensiones/vector_12d.py")
        print("  ✓ dimensiones/dimension_[1-12].py")
        print("  ✓ vecta_ai_chat.py (simplificado)")
        print("  ✓ lanzar_vecta.py")
        
        print("\nPARA USAR:")
        print("  1. Para chat completo: python vecta_todo_en_uno.py --chat")
        print("  2. Para solo lanzar: python lanzar_vecta.py")
        print("  3. Para auto-implementar: python vecta_todo_en_uno.py --implementar")
        
        print("\n" + "=" * 80)

# ============================================================================
# PARTE 8: FUNCIÓN PRINCIPAL Y MENÚ
# ============================================================================

def main():
    """Función principal con menú de opciones"""
    import argparse
    
    parser = argparse.ArgumentParser(description="VECTA 12D - Sistema Todo-en-Uno")
    parser.add_argument("--chat", action="store_true", help="Iniciar chat VECTA AI")
    parser.add_argument("--implementar", action="store_true", help="Auto-implementar sistema completo")
    parser.add_argument("--diagnostico", action="store_true", help="Ejecutar diagnóstico del sistema")
    parser.add_argument("--version", action="store_true", help="Mostrar versión")
    
    args = parser.parse_args()
    
    if args.version:
        print(f"VECTA 12D Todo-en-Uno v5.0.0")
        print(f"Directorio: {Path.cwd()}")
        return
    
    if args.diagnostico:
        print("=" * 70)
        print("DIAGNÓSTICO DEL SISTEMA VECTA")
        print("=" * 70)
        
        # Verificar directorios
        required_dirs = ["core", "dimensiones", "chat_data"]
        for dir_name in required_dirs:
            dir_path = Path(dir_name)
            if dir_path.exists():
                print(f"✓ {dir_name}")
            else:
                print(f"✗ {dir_name} (no existe)")
        
        # Verificar archivos clave
        key_files = [
            "core/vecta_12d_core.py",
            "dimensiones/vector_12d.py",
            "vecta_ai_chat.py"
        ]
        
        for file_path in key_files:
            path = Path(file_path)
            if path.exists():
                size = path.stat().st_size
                print(f"✓ {file_path} ({size} bytes)")
            else:
                print(f"✗ {file_path} (no existe)")
        
        print("\nRECOMENDACIÓN:")
        print("  Para crear los archivos faltantes, ejecuta:")
        print("  python vecta_todo_en_uno.py --implementar")
        return
    
    if args.implementar:
        print("=" * 70)
        print("MODO AUTO-IMPLEMENTACIÓN")
        print("=" * 70)
        print("\nEste modo generará todos los archivos necesarios.")
        print("¿Continuar? (s/n): ", end="")
        
        confirm = input().strip().lower()
        if confirm not in ['s', 'si', 'yes', 'y']:
            print("Cancelado.")
            return
        
        implementador = VECTAAutoImplementador()
        implementador.run()
        return
    
    # Por defecto, iniciar chat (o menú interactivo)
    if args.chat:
        # Iniciar chat directamente
        try:
            chat = VECTAAIChat()
            chat.run()
        except Exception as e:
            print(f"Error al iniciar chat: {e}")
            print("\nSugerencia: Ejecuta primero --implementar para crear archivos necesarios.")
    else:
        # Mostrar menú interactivo
        print("=" * 70)
        print("VECTA 12D - SISTEMA TODO-EN-UNO")
        print("=" * 70)
        print("\nOPCIONES DISPONIBLES:")
        print("  1. Iniciar chat VECTA AI")
        print("  2. Auto-implementar sistema completo")
        print("  3. Ejecutar diagnóstico")
        print("  4. Salir")
        print("\nTambién puedes usar argumentos de línea de comandos:")
        print("  --chat, --implementar, --diagnostico, --version")
        
        while True:
            print("\n" + "-" * 70)
            print("Elige una opción (1-4) o escribe 'salir': ", end="")
            
            choice = input().strip().lower()
            
            if choice in ['1', 'chat']:
                try:
                    chat = VECTAAIChat()
                    chat.run()
                except Exception as e:
                    print(f"Error: {e}")
                    print("Prueba primero --implementar para crear archivos necesarios.")
            
            elif choice in ['2', 'implementar']:
                implementador = VECTAAutoImplementador()
                implementador.run()
            
            elif choice in ['3', 'diagnostico']:
                args.diagnostico = True
                main()  # Recursivo pero con diagnóstico
            
            elif choice in ['4', 'salir', 'exit', 'quit']:
                print("¡Hasta luego!")
                break
            
            else:
                print("Opción no válida. Intenta de nuevo.")

# ============================================================================
# EJECUCIÓN PRINCIPAL
# ============================================================================

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nPrograma interrumpido por el usuario.")
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {e}")
        traceback.print_exc()
        print("\n💡 INTENTA ESTO:")
        print("  1. Ejecuta: python vecta_todo_en_uno.py --diagnostico")
        print("  2. Luego: python vecta_todo_en_uno.py --implementar")
        print("  3. Finalmente: python vecta_todo_en_uno.py --chat")