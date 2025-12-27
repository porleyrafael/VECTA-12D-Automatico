"""
VECTA 12D - SISTEMA DE SNAPSHOTS AUTOMATICO
Version: 1.0
Este sistema crea puntos de restauracion automaticos de tu proyecto VECTA
"""
import os
import sys
import json
import shutil
import hashlib
import datetime
from pathlib import Path
import threading

class VECTA_SnapshotSystem:
    def __init__(self):
        self.base_dir = Path.cwd()
        self.snapshots_dir = self.base_dir / ".vecta_snapshots"
        self.max_snapshots = 3
        self.config_file = self.snapshots_dir / "config.json"
        self._setup()
    
    def _setup(self):
        """Configura el sistema"""
        self.snapshots_dir.mkdir(exist_ok=True)
        if not self.config_file.exists():
            config = {
                "version": "1.0",
                "created": datetime.datetime.now().isoformat(),
                "total_snapshots": 0,
                "active_snapshots": [],
                "tracked_files": [".py", ".json", ".txt", ".md", ".bat"]
            }
            self._save_config(config)
    
    def _save_config(self, config):
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
    
    def _load_config(self):
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {}
    
    def create_snapshot(self, reason="Auto-snapshot"):
        """Crea un nuevo snapshot"""
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            snapshot_id = f"snap_{timestamp}"
            snapshot_path = self.snapshots_dir / snapshot_id
            
            snapshot_path.mkdir(exist_ok=True)
            
            print(f"Creando snapshot: {snapshot_id}")
            print(f"Razon: {reason}")
            
            files_copied = 0
            config = self._load_config()
            
            for ext in config.get("tracked_files", [".py"]):
                for source_file in self.base_dir.rglob(f"*{ext}"):
                    if source_file.is_file() and ".vecta_snapshots" not in str(source_file):
                        rel_path = source_file.relative_to(self.base_dir)
                        target_file = snapshot_path / rel_path
                        target_file.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(source_file, target_file)
                        files_copied += 1
            
            metadata = {
                "id": snapshot_id,
                "created": datetime.datetime.now().isoformat(),
                "reason": reason,
                "files_copied": files_copied
            }
            
            metadata_file = snapshot_path / "metadata.json"
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            config["active_snapshots"].append(metadata)
            
            while len(config["active_snapshots"]) > self.max_snapshots:
                old = config["active_snapshots"].pop(0)
                old_path = self.snapshots_dir / old["id"]
                if old_path.exists():
                    shutil.rmtree(old_path)
            
            config["total_snapshots"] = len(config["active_snapshots"])
            self._save_config(config)
            
            print(f"Snapshot creado: {snapshot_id}")
            print(f"Archivos copiados: {files_copied}")
            
            return snapshot_id
            
        except Exception as e:
            print(f"Error creando snapshot: {e}")
            return None
    
    def restore_snapshot(self, snapshot_id):
        """Restaura un snapshot"""
        try:
            snapshot_path = self.snapshots_dir / snapshot_id
            if not snapshot_path.exists():
                print(f"Snapshot no encontrado: {snapshot_id}")
                return False
            
            print(f"Restaurando snapshot: {snapshot_id}")
            
            for source_file in snapshot_path.rglob("*"):
                if source_file.is_file() and source_file.name != "metadata.json":
                    rel_path = source_file.relative_to(snapshot_path)
                    target_file = self.base_dir / rel_path
                    target_file.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source_file, target_file)
            
            print(f"Snapshot restaurado: {snapshot_id}")
            return True
            
        except Exception as e:
            print(f"Error restaurando snapshot: {e}")
            return False
    
    def list_snapshots(self):
        """Lista todos los snapshots disponibles"""
        config = self._load_config()
        return config.get("active_snapshots", [])
    
    def generate_chat_report(self):
        """Genera reporte para compartir en chat"""
        try:
            report_lines = []
            report_lines.append("VECTA 12D - ESTADO DEL SISTEMA")
            report_lines.append("="*50)
            report_lines.append(f"Fecha: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report_lines.append(f"Directorio: {self.base_dir}")
            report_lines.append("")
            
            snapshots = self.list_snapshots()
            report_lines.append(f"Snapshots disponibles: {len(snapshots)}")
            for snap in snapshots:
                report_lines.append(f"- {snap['id']}: {snap['reason']}")
            
            report_lines.append("")
            report_lines.append("ARCHIVOS PRINCIPALES:")
            
            important_files = [
                "vecta_launcher.py",
                "core/vecta_12d_core.py",
                "core/meta_vecta.py",
                "dimensiones/vector_12d.py"
            ]
            
            for file in important_files:
                file_path = self.base_dir / file
                if file_path.exists():
                    size_kb = file_path.stat().st_size / 1024
                    report_lines.append(f"- {file} ({size_kb:.1f} KB)")
                else:
                    report_lines.append(f"- {file} (NO ENCONTRADO)")
            
            report_lines.append("")
            report_lines.append("PARA RESTAURAR:")
            report_lines.append("python vecta_snapshot_system.py restore SNAPSHOT_ID")
            report_lines.append("")
            report_lines.append("PARA CREAR NUEVO SNAPSHOT:")
            report_lines.append("python vecta_snapshot_system.py snapshot 'Razon'")
            
            return "\n".join(report_lines)
            
        except Exception as e:
            return f"Error generando reporte: {e}"

def main():
    if len(sys.argv) < 2:
        print("Uso: python vecta_snapshot_system.py [comando]")
        print("Comandos:")
        print("  snapshot [razon]  - Crea nuevo snapshot")
        print("  restore [id]      - Restaura snapshot")
        print("  list              - Lista snapshots")
        print("  report            - Genera reporte para chat")
        return
    
    sistema = VECTA_SnapshotSystem()
    comando = sys.argv[1]
    
    if comando == "snapshot":
        razon = sys.argv[2] if len(sys.argv) > 2 else "Snapshot automatico"
        sistema.create_snapshot(razon)
    
    elif comando == "restore":
        if len(sys.argv) > 2:
            sistema.restore_snapshot(sys.argv[2])
        else:
            print("Debe especificar ID del snapshot")
    
    elif comando == "list":
        snapshots = sistema.list_snapshots()
        print("Snapshots disponibles:")
        for snap in snapshots:
            print(f"- {snap['id']}: {snap['reason']}")
    
    elif comando == "report":
        reporte = sistema.generate_chat_report()
        print(reporte)
        print("\n" + "="*50)
        print("COPIAR TODO ESTE TEXTO Y PEGARLO EN EL CHAT")
    
    else:
        print(f"Comando desconocido: {comando}")

if __name__ == "__main__":
    main()
