#!/usr/bin/env python3
"""
VECTA LEARNER - Sistema de auto-aprendizaje para VECTA 12D
Versión: 2.0.0
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
        
        return f"✅ Aprendido: '{user_input}' → {correct_action}"
    
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
            for pattern, data in list(self.learned_patterns["command_mappings"].items())[:10]:
                report.append(f"  • '{pattern}' → {data['action']} (usos: {data.get('uses', 0)})")
            
            if len(self.learned_patterns["command_mappings"]) > 10:
                report.append(f"  ... y {len(self.learned_patterns['command_mappings']) - 10} patrones más")
        else:
            report.append("  Aún no hay patrones aprendidos")
        
        return "\n".join(report)

# Instancia global para importación
vecta_learner = VECTALearner()

if __name__ == "__main__":
    print("=== VECTA LEARNER TEST ===")
    
    # Ejemplos de prueba
    learner = VECTALearner()
    
    # Aprender algunos patrones
    print(learner.learn("crea un nuevo módulo prueba.py", "create_file", {"file_name": "prueba.py"}))
    print(learner.learn("ejecutar test", "run_script", {"file_name": "test.py"}))
    
    # Obtener sugerencias
    suggestion = learner.get_suggestion("crea módulo test.py")
    print(f"\nSugerencia para 'crea módulo test.py': {suggestion}")
    
    # Mostrar reporte
    print("\n" + learner.show_learning_report())