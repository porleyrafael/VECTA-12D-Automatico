#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VECTA 12D TODO-EN-UNO CORREGIDO
================================
Versión corregida sin errores de indentación.
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
# CONFIGURACIÓN BÁSICA
# ============================================================================

class VECTAConfig:
    def __init__(self, base_dir=None):
        self.BASE_DIR = Path(base_dir) if base_dir else Path.cwd()
        self.CORE_DIR = self.BASE_DIR / "core"
        self.DIMENSIONS_DIR = self.BASE_DIR / "dimensiones"
        self.CHAT_DATA_DIR = self.BASE_DIR / "chat_data"
        self.CHAT_SESSIONS_DIR = self.CHAT_DATA_DIR / "sessions"
        self.CHAT_LOGS_DIR = self.CHAT_DATA_DIR / "logs"
        self.CHAT_BACKUPS_DIR = self.CHAT_DATA_DIR / "backups"
        self.LEARNING_DATA_DIR = self.CHAT_DATA_DIR / "learning"
        
        self._create_directories()
        
        self.VERSION = "5.0.0"
        self.CREATOR = "Rafael Porley"
        self.AUTO_EXECUTE = True
        self.MAX_HISTORY = 1000
        self.COMMAND_TIMEOUT = 60
        
        self.VECTA_PRINCIPLES = [
            "ALWAYS_DECIDE",
            "FINITE_TIME_COLLAPSE", 
            "NO_COMPLEXITY_WITHOUT_GAIN",
            "FULL_AUDITABILITY",
            "SEPARATION_OF_LAYERS"
        ]
        
        self.NLP_PATTERNS = self._load_nlp_patterns()
    
    def _create_directories(self):
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
        return {
            "system_status": {
                "patterns": [
                    r"(?:estado|status|situacion|condicion)(?: del sistema)?",
                    r"como esta (?:el sistema|vecta)",
                    r"que pasa con vecta"
                ],
                "action": "system_status"
            },
            "show_help": {
                "patterns": [
                    r"ayuda|help|comandos|instrucciones",
                    r"que puedes hacer",
                    r"como (?:usar|utilizar) (?:esto|vecta|el sistema)"
                ],
                "action": "show_help"
            },
            "create_file": {
                "patterns": [
                    r"(?:crear|crea|hacer|generar) (?:un )?archivo ([a-zA-Z0-9_\.\-]+)",
                    r"crea (?:archivo|fichero|modulo|script) ([a-zA-Z0-9_\.\-]+)"
                ],
                "action": "create_file",
                "has_params": True
            },
            "run_script": {
                "patterns": [
                    r"(?:ejecutar|correr|run|lanzar) (?:el )?(?:archivo|script|programa) ([a-zA-Z0-9_\.\-]+\.py)",
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
# LOGGER
# ============================================================================

class VECTALogger:
    def __init__(self, config: VECTAConfig):
        self.config = config
        self.session_id = str(uuid.uuid4())[:8]
        self.log_file = config.CHAT_LOGS_DIR / f"vecta_chat_{datetime.now().strftime('%Y%m%d')}.log"
        self.session_file = config.CHAT_SESSIONS_DIR / f"session_{self.session_id}.json"
    
    def log(self, level: str, message: str, data: Dict = None):
        timestamp = datetime.now().isoformat()
        log_entry = {
            "timestamp": timestamp,
            "session_id": self.session_id,
            "level": level,
            "message": message,
            "data": data or {}
        }
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
        
        if level in ["ERROR", "WARNING", "ACTION", "LEARNING"]:
            print(f"[{level}] {message}")

# ============================================================================
# NLP
# ============================================================================

class VECTANLP:
    def __init__(self, config: VECTAConfig):
        self.config = config
    
    def extract_intent(self, text: str) -> Tuple[str, Dict, float]:
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
        
        for intent_name, intent_data in self.config.NLP_PATTERNS.items():
            if intent_data.get("default"):
                return intent_data["action"], {"original_text": text}, 0.1
        
        return "unknown", {"original_text": text}, 0.0
    
    def _extract_parameters(self, intent_data: Dict, text: str, match=None) -> Dict:
        params = {"original_text": text}
        
        if intent_data.get("has_params") and match:
            if match.groups():
                for i, group in enumerate(match.groups(), 1):
                    if group:
                        params[f"param_{i}"] = group
        
        file_match = re.search(r'([a-zA-Z0-9_\.\-]+\.py)', text)
        if file_match:
            params["file_name"] = file_match.group(1)
        
        return params

# ============================================================================
# LEARNER
# ============================================================================

class VECTALearner:
    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = "chat_data/learning/learned_patterns.json"
        
        self.config_path = Path(config_path)
        self.learned_patterns = self._load_learned_patterns()
    
    def _load_learned_patterns(self) -> Dict:
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
        return text.lower().replace('"', '').replace("'", "").strip()
    
    def _save_learned_patterns(self):
        self.config_path.parent.mkdir(exist_ok=True)
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.learned_patterns, f, indent=2, ensure_ascii=False)
    
    def get_stats(self) -> Dict:
        return {
            "total_learned": self.learned_patterns["statistics"]["total_learned"],
            "successful_uses": self.learned_patterns["statistics"]["successful_uses"],
            "unique_patterns": len(self.learned_patterns["command_mappings"]),
            "last_updated": self.learned_patterns["statistics"]["last_updated"]
        }

# ============================================================================
# ACTION EXECUTOR
# ============================================================================

class VECTAActionExecutor:
    def __init__(self, config: VECTAConfig, logger: VECTALogger):
        self.config = config
        self.logger = logger
        self.learner = VECTALearner()
    
    def execute(self, action: str, params: Dict) -> Dict:
        start_time = time.time()
        
        original_text = params.get("original_text", "")
        learned_suggestion = self.learner.get_suggestion(original_text)
        
        if learned_suggestion and learned_suggestion["confidence"] > 0.8:
            old_action = action
            action = learned_suggestion["action"]
            params.update(learned_suggestion["params"])
            self.logger.log("LEARNING", f"Usando aprendizaje: '{original_text}' -> {action} (antes: {old_action})")
        
        self.logger.log("ACTION", f"Iniciando accion: {action}", params)
        
        try:
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
            
            exec_time = time.time() - start_time
            if exec_time > self.config.COMMAND_TIMEOUT:
                result["warning"] = f"Accion tardo {exec_time:.2f}s"
            
            result["vecta_metadata"] = {
                "execution_time": exec_time,
                "action": action,
                "timestamp": datetime.now().isoformat()
            }
            
            self.logger.log("INFO", f"Accion {action} completada", {
                "time": exec_time,
                "success": result.get("success", True)
            })
            
            return result
            
        except Exception as e:
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
                teach_suggestion = f"\nQuieres enseñarme este comando?\n   Di: 'ensena a vecta: cuando digo \"{params['original_text']}\" haz [accion correcta]'"
            
            return {
                "success": False,
                "type": "error",
                "error": str(e),
                "action": action,
                "content": f"Error en accion: {str(e)}{teach_suggestion}"
            }
    
    def _action_system_status(self) -> Dict:
        status_text = f"""
VECTA 12D - ESTADO DEL SISTEMA

VERSION: {self.config.VERSION}
CREADOR: {self.config.CREATOR}
SESSION: {self.logger.session_id}

DIRECTORIOS:
  * Principal: {self.config.BASE_DIR}
  * Datos Chat: {self.config.CHAT_DATA_DIR}
  * Aprendizaje: {self.config.LEARNING_DATA_DIR}

PRINCIPIOS VECTA:
"""
        
        for principle in self.config.VECTA_PRINCIPLES:
            status_text += f"  * {principle}\n"
        
        stats = self.learner.get_stats()
        status_text += f"\nAPRENDIZAJE AUTOMATICO:\n"
        status_text += f"  * Patrones aprendidos: {stats['total_learned']}\n"
        status_text += f"  * Usos exitosos: {stats['successful_uses']}\n"
        
        return {
            "success": True,
            "type": "system_status",
            "content": status_text
        }
    
    def _action_show_help(self) -> Dict:
        help_text = f"""
VECTA AI CHAT - AYUDA v{self.config.VERSION}

COMANDOS:
  * "Como esta el sistema?" - Ver estado
  * "Ayuda" - Ver esta ayuda
  * "Crea archivo prueba.py" - Crear archivo
  * "Ejecuta script.py" - Ejecutar script
  * "Analiza con VECTA: [texto]" - Analizar texto

AUTO-APRENDIZAJE:
  * "Enseña a vecta: cuando digo X haz Y"

Sistema VECTA 12D - Creado por {self.config.CREATOR}
"""
        
        return {
            "success": True,
            "type": "help",
            "content": help_text
        }
    
    def _action_create_file(self, params: Dict) -> Dict:
        file_name = params.get("file_name") or params.get("param_1")
        
        if not file_name:
            return {
                "success": False,
                "type": "file_creation",
                "content": "No se especifico nombre de archivo\nEjemplo: 'Crea un archivo test.py'",
                "error": "No filename specified"
            }
        
        if not '.' in file_name and not file_name.endswith('.py'):
            file_name += '.py'
        
        file_path = self.config.BASE_DIR / file_name
        
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
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
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
        script_name = params.get("file_name") or params.get("param_1")
        
        if not script_name:
            return {
                "success": False,
                "type": "script_execution",
                "content": "No se especifico archivo a ejecutar\nEjemplo: 'Ejecuta prueba.py'",
                "error": "No script specified"
            }
        
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
  * Codigo de salida: {result.returncode}

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
    
    def _action_analyze_with_vecta(self, params: Dict) -> Dict:
        text = params.get("original_text", "")
        
        analysis_match = re.search(r'(?:analiza|procesa|calcula)[\s\:]+(.+)', text, re.IGNORECASE)
        analysis_text = analysis_match.group(1).strip() if analysis_match else text
        
        if not analysis_text or len(analysis_text) < 3:
            return {
                "success": False,
                "type": "vecta_analysis",
                "content": "No se especifico texto para analizar\nEjemplo: 'Analiza con VECTA: Este es un proyecto importante'",
                "error": "No text provided"
            }
        
        word_count = len(analysis_text.split())
        char_count = len(analysis_text)
        avg_word_length = char_count / max(word_count, 1)
        
        content = f"""
Analisis VECTA completado:

Texto analizado: "{analysis_text[:100]}{'...' if len(analysis_text) > 100 else ''}"

Resultados:
  * Palabras: {word_count}
  * Caracteres: {char_count}
  * Longitud promedio palabra: {avg_word_length:.1f}
  * Procesamiento exitoso
"""
        
        return {
            "success": True,
            "type": "vecta_analysis",
            "content": content,
            "text_analyzed": analysis_text
        }
    
    def _action_general_query(self, params: Dict) -> Dict:
        text = params.get("original_text", "")
        
        if any(word in text.lower() for word in ['hola', 'hello', 'hi', 'buenas']):
            response = f"Hola! Soy VECTA AI Chat v{self.config.VERSION}\n¿En que puedo ayudarte hoy?"
        elif any(word in text.lower() for word in ['gracias', 'thanks', 'thank you']):
            response = "De nada! Siempre estoy aqui para ayudarte con VECTA 12D."
        elif '?' in text:
            response = f"Interesante pregunta.\n\nPuedo ayudarte mejor si me dices que quieres hacer:\n* Consultar el estado del sistema?\n* Ejecutar algun script?\n* Crear archivos?\n\nO escribe 'ayuda' para ver todas las opciones."
        else:
            response = f"He procesado tu mensaje: '{text}'\n\nPara acciones especificas, intenta:\n* 'Ayuda' - Ver todos los comandos\n* 'Estado' - Ver sistema VECTA\n* 'Enseña a vecta' - Para enseñarme nuevos comandos"
        
        return {
            "success": True,
            "type": "general_response",
            "content": response,
            "original_text": text
        }
    
    def _action_unknown(self, params: Dict) -> Dict:
        text = params.get("original_text", "N/A")
        
        teach_option = f"\n\n¿Quieres que aprenda este comando?\n   Di: 'Enseña a vecta: cuando digo \"{text}\" haz [accion correcta]'"
        
        return {
            "success": False,
            "type": "unknown_command",
            "content": f"VECTA no entendio completamente: '{text}'\n\nPrueba con:\n* 'Ayuda' - Ver todos los comandos\n* 'Estado' - Ver sistema VECTA\n* Escribe en lenguaje natural lo que necesitas{teach_option}",
            "original_text": text,
            "can_learn": True
        }

# ============================================================================
# MAIN CHAT SYSTEM
# ============================================================================

class VECTAAIChat:
    def __init__(self):
        self.config = VECTAConfig()
        self.logger = VECTALogger(self.config)
        self.nlp = VECTANLP(self.config)
        self.executor = VECTAActionExecutor(self.config, self.logger)
        
        self.chat_history = []
        self.max_history = self.config.MAX_HISTORY
        
        self.session_data = {
            "session_id": self.logger.session_id,
            "start_time": datetime.now().isoformat(),
            "interaction_count": 0,
            "commands_executed": []
        }
    
    def display_banner(self):
        banner = f"""
VECTA 12D - AI CHAT INTERFACE
Sistema Autonomo de Comunicacion Inteligente

----------------------------------------------------------------
  Version: {self.config.VERSION}                Creador: {self.config.CREATOR}                Session: {self.logger.session_id}
----------------------------------------------------------------

CARACTERISTICAS PRINCIPALES:
  * Lenguaje natural completo (espanol/ingles)
  * Ejecucion automatica de comandos
  * Sistema de auto-aprendizaje
  * Auditoria completa (principio VECTA)

INSTRUCCION:
  Escribe en lenguaje natural lo que necesitas. Ejemplos:
    * "Crea un archivo prueba.py"
    * "Como esta el sistema?"
    * "Enseña a vecta: cuando digo 'programa' haz 'crear archivo'"

Escribe 'ayuda' para ver la guia completa o 'salir' para terminar.
----------------------------------------------------------------
"""
        
        print(banner)
    
    def process_input(self, user_input: str) -> Optional[Dict]:
        if not user_input.strip():
            return {"content": "Entrada vacia. Por favor, escribe algo."}
        
        self.session_data["interaction_count"] += 1
        
        self.chat_history.append({
            "type": "user",
            "content": user_input,
            "timestamp": datetime.now().isoformat()
        })
        
        action, params, confidence = self.nlp.extract_intent(user_input)
        
        self.logger.log("INFO", f"Intencion detectada: {action} (confianza: {confidence:.2f})", {
            "input": user_input,
            "params": params,
            "confidence": confidence
        })
        
        result = self.executor.execute(action, params)
        
        self.session_data["commands_executed"].append({
            "action": action,
            "input": user_input,
            "timestamp": datetime.now().isoformat(),
            "success": result.get("success", False)
        })
        
        self.chat_history.append({
            "type": "vecta",
            "content": result.get("content", "Sin respuesta"),
            "action": action,
            "timestamp": datetime.now().isoformat(),
            "success": result.get("success", False)
        })
        
        if len(self.chat_history) > self.max_history * 2:
            self.chat_history = self.chat_history[-self.max_history*2:]
        
        return result
    
    def format_response(self, result: Dict) -> str:
        content = result.get("content", "Sin contenido")
        return f"\n{'='*80}\n{content}\n{'='*80}\n"
    
    def _save_session(self):
        self.session_data["end_time"] = datetime.now().isoformat()
        self.session_data["chat_history"] = self.chat_history[-20:]
        
        self.logger.save_session(self.session_data)
        self.logger.log("INFO", "Sesion guardada", {"session_id": self.logger.session_id})
    
    def run(self):
        self.display_banner()
        self._save_session()
        
        print(f"\n{'='*80}")
        print("CHAT VECTA ACTIVADO - Escribe tu mensaje:")
        print("=" * 80)
        
        try:
            while True:
                try:
                    user_input = input("\n>>> ").strip()
                    
                    if user_input.lower() in ['salir', 'exit', 'quit', 'adios']:
                        print("\nSaliendo del sistema VECTA...")
                        break
                    
                    result = self.process_input(user_input)
                    
                    print(self.format_response(result))
                    
                    if self.session_data["interaction_count"] % 10 == 0:
                        self._save_session()
                        
                except KeyboardInterrupt:
                    print("\n\nInterrupcion detectada. ¿Salir? (s/n): ", end="")
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
            self._save_session()
            print(f"\n{'='*80}")
            print(f"Resumen de sesion {self.logger.session_id}:")
            print(f"  * Interacciones: {self.session_data['interaction_count']}")
            print(f"  * Comandos ejecutados: {len(self.session_data['commands_executed'])}")
            stats = self.executor.learner.get_stats()
            print(f"  * Patrones aprendidos: {stats['total_learned']}")
            print(f"  * Sesion guardada en: {self.logger.session_file}")
            print("=" * 80)
            print("\n¡Gracias por usar VECTA 12D AI Chat!")

# ============================================================================
# AUTO-IMPLEMENTATION
# ============================================================================

class VECTAAutoImplementador:
    def __init__(self):
        self.base_dir = Path.cwd()
        self.creation_log = []
    
    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] {message}"
        self.creation_log.append(entry)
        print(entry)
    
    def create_file(self, file_path, content):
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            file_size = os.path.getsize(file_path)
            self.log(f"✓ {file_path.name} ({file_size} bytes)")
            return True
        except Exception as e:
            self.log(f"✗ Error creando {file_path.name}: {e}")
            return False
    
    def generate_system_files(self):
        # Crear vecta_ai_chat.py standalone
        chat_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VECTA AI CHAT - Sistema Principal
==================================
Versión standalone generada automáticamente
"""

print("VECTA AI Chat - Sistema listo para usar")
print("Para la versión completa, ejecuta vecta_todo_en_uno_corregido.py --chat")
'''
        
        file_path = self.base_dir / "vecta_ai_chat.py"
        self.create_file(file_path, chat_content)
        
        # Crear archivos core
        core_content = '''"""
NÚCLEO VECTA 12D
"""

class VECTA_12D_Core:
    def __init__(self):
        self.nombre = "VECTA 12D"
        self.version = "5.0.0"
    
    def procesar(self, texto):
        return {
            "exito": True,
            "mensaje": f"Texto procesado: {texto[:50]}..."
        }
'''
        
        core_file = self.base_dir / "core" / "vecta_12d_core.py"
        self.create_file(core_file, core_content)
        
        # Crear vector 12D
        vector_content = '''"""
SISTEMA VECTORIAL 12D
"""

class Vector12D:
    def __init__(self, valores=None):
        self.dimensiones = valores or [0.0] * 12

class SistemaVectorial12D:
    def procesar_evento(self, evento):
        texto = evento.get("texto", "")
        return Vector12D([len(texto) * 0.01] * 12)
'''
        
        vector_file = self.base_dir / "dimensiones" / "vector_12d.py"
        self.create_file(vector_file, vector_content)
        
        # Crear dimensiones básicas
        for i in range(1, 13):
            dim_content = f'''"""
DIMENSIÓN {i}
"""

class Dimension_{i}:
    def procesar(self, texto):
        return len(texto) * 0.01
'''
            dim_file = self.base_dir / "dimensiones" / f"dimension_{i}.py"
            self.create_file(dim_file, dim_content)
        
        return True
    
    def run(self):
        print("=" * 80)
        print("VECTA AUTO-IMPLEMENTADOR")
        print("=" * 80)
        print(f"Directorio: {self.base_dir}")
        print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        print("[1/3] Verificando directorios...")
        directories = ["core", "dimensiones", "chat_data", "chat_data/sessions", 
                      "chat_data/logs", "chat_data/backups", "chat_data/learning"]
        
        for dir_path in directories:
            full_path = self.base_dir / dir_path
            full_path.mkdir(exist_ok=True)
            self.log(f"Directorio: {dir_path}")
        
        print("\n[2/3] Generando archivos...")
        self.generate_system_files()
        
        print("\n[3/3] Creando lanzador...")
        launcher_content = '''#!/usr/bin/env python3
"""
LANZADOR VECTA
"""

print("=" * 70)
print("VECTA 12D - Sistema listo")
print("=" * 70)
print()
print("Para iniciar el chat VECTA:")
print("   python vecta_todo_en_uno_corregido.py --chat")
print()
print("Para auto-implementar todo:")
print("   python vecta_todo_en_uno_corregido.py --implementar")
'''
        
        launcher_file = self.base_dir / "lanzar_vecta.py"
        self.create_file(launcher_file, launcher_content)
        
        print("\n" + "=" * 80)
        print("COMPLETADO")
        print("=" * 80)
        print("\nARCHIVOS CREADOS:")
        print("  ✓ core/vecta_12d_core.py")
        print("  ✓ dimensiones/vector_12d.py")
        print("  ✓ dimensiones/dimension_[1-12].py")
        print("  ✓ vecta_ai_chat.py")
        print("  ✓ lanzar_vecta.py")
        
        print("\nPARA USAR:")
        print("  1. Chat: python vecta_todo_en_uno_corregido.py --chat")
        print("  2. Auto-implementar: python vecta_todo_en_uno_corregido.py --implementar")
        
        print("\n" + "=" * 80)

# ============================================================================
# MAIN FUNCTION
# ============================================================================

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="VECTA 12D - Sistema Corregido")
    parser.add_argument("--chat", action="store_true", help="Iniciar chat VECTA")
    parser.add_argument("--implementar", action="store_true", help="Auto-implementar sistema")
    parser.add_argument("--diagnostico", action="store_true", help="Ejecutar diagnostico")
    parser.add_argument("--version", action="store_true", help="Mostrar version")
    
    args = parser.parse_args()
    
    if args.version:
        print("VECTA 12D Todo-en-Uno Corregido v5.0.0")
        return
    
    if args.diagnostico:
        print("=" * 70)
        print("DIAGNOSTICO DEL SISTEMA")
        print("=" * 70)
        
        required_dirs = ["core", "dimensiones", "chat_data"]
        for dir_name in required_dirs:
            dir_path = Path(dir_name)
            if dir_path.exists():
                print(f"✓ {dir_name}")
            else:
                print(f"✗ {dir_name}")
        
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
                print(f"✗ {file_path}")
        
        print("\nPara crear archivos faltantes:")
        print("  python vecta_todo_en_uno_corregido.py --implementar")
        return
    
    if args.implementar:
        print("=" * 70)
        print("MODO AUTO-IMPLEMENTACION")
        print("=" * 70)
        print("\n¿Continuar? (s/n): ", end="")
        
        confirm = input().strip().lower()
        if confirm not in ['s', 'si', 'yes', 'y']:
            print("Cancelado.")
            return
        
        implementador = VECTAAutoImplementador()
        implementador.run()
        return
    
    if args.chat:
        try:
            chat = VECTAAIChat()
            chat.run()
        except Exception as e:
            print(f"Error: {e}")
            print("\nPrimero ejecuta: python vecta_todo_en_uno_corregido.py --implementar")
    else:
        print("=" * 70)
        print("VECTA 12D - SISTEMA CORREGIDO")
        print("=" * 70)
        print("\nOPCIONES:")
        print("  1. Iniciar chat VECTA (--chat)")
        print("  2. Auto-implementar sistema (--implementar)")
        print("  3. Diagnóstico (--diagnostico)")
        print("  4. Salir")
        print("\nEjemplo: python vecta_todo_en_uno_corregido.py --chat")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrumpido por el usuario.")
    except Exception as e:
        print(f"\nERROR: {e}")
        print("\nIntenta: python vecta_todo_en_uno_corregido.py --diagnostico")