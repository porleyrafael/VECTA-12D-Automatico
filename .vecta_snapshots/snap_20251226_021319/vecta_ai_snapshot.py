#!/usr/bin/env python3
"""
VECTA 12D - AI SNAPSHOT MANAGER
================================
Sistema automático de puntos de restauración con documentación integrada.
CARACTERÍSTICAS:
1. Se ejecuta automáticamente detectando cambios
2. Mantiene solo los últimos X estados relevantes
3. Genera documentación automáticamente
4. Permite revertir a cualquier punto anterior
5. Elimina automáticamente estados obsoletos
"""
import os
import sys
import json
import time
import shutil
import hashlib
import datetime
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import difflib
from typing import Dict, List, Optional, Tuple
import threading
import zipfile

class VECTA_AISnapshot:
    """Sistema de snapshots inteligentes para VECTA 12D"""
    
    def __init__(self, max_snapshots=3, auto_mode=True):
        self.base_dir = Path.cwd()
        self.snapshots_dir = self.base_dir / ".ai_snapshots"
        self.max_snapshots = max_snapshots  # Solo guardar los últimos N relevantes
        self.auto_mode = auto_mode
        self.config_file = self.snapshots_dir / "config.json"
        self.current_hash = None
        self.lock = threading.Lock()
        
        # Inicializar sistema
        self._setup_system()
    
    def _setup_system(self):
        """Configura el sistema de snapshots"""
        self.snapshots_dir.mkdir(exist_ok=True)
        
        # Configuración inicial
        if not self.config_file.exists():
            config = {
                "version": "1.0",
                "created": datetime.datetime.now().isoformat(),
                "total_snapshots": 0,
                "active_snapshots": [],
                "auto_cleanup": True,
                "tracked_extensions": [".py", ".json", ".md", ".txt", ".bat", ".pkg"],
                "ignored_patterns": [".pyc", "__pycache__", ".git", ".ai_snapshots"]
            }
            self._save_config(config)
        
        # Iniciar monitoreo automático si está activado
        if self.auto_mode:
            self._start_monitoring()
    
    def _save_config(self, config=None):
        """Guarda la configuración"""
        if config is None:
            config = self._load_config()
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    
    def _load_config(self):
        """Carga la configuración"""
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _calculate_project_hash(self, specific_files=None) -> str:
        """
        Calcula un hash único del proyecto o archivos específicos
        Ignora archivos temporales y de sistema
        """
        hasher = hashlib.sha256()
        config = self._load_config()
        
        files_to_hash = []
        if specific_files:
            files_to_hash = specific_files
        else:
            for ext in config.get("tracked_extensions", [".py"]):
                files_to_hash.extend(self.base_dir.rglob(f"*{ext}"))
        
        # Filtrar archivos ignorados
        ignored = config.get("ignored_patterns", [])
        filtered_files = []
        for f in files_to_hash:
            if isinstance(f, str):
                f = Path(f)
            if any(pattern in str(f) for pattern in ignored):
                continue
            if f.exists() and f.is_file():
                filtered_files.append(f)
        
        # Ordenar para consistencia y calcular hash
        filtered_files.sort(key=lambda x: str(x))
        
        for file_path in filtered_files:
            # Incluir ruta relativa
            rel_path = str(file_path.relative_to(self.base_dir))
            hasher.update(rel_path.encode())
            
            # Incluir contenido
            try:
                with open(file_path, 'rb') as f:
                    content = f.read()
                    hasher.update(content)
                    # También incluir metadatos (tamaño, modificación)
                    stat = file_path.stat()
                    hasher.update(str(stat.st_size).encode())
                    hasher.update(str(stat.st_mtime).encode())
            except:
                # Si no se puede leer, usar solo el nombre
                hasher.update(b"unreadable")
        
        return hasher.hexdigest()
    
    def _is_significant_change(self, old_hash: str, new_hash: str, changed_files: List[str]) -> bool:
        """
        Determina si los cambios son significativos
        para evitar snapshots por cambios triviales
        """
        if old_hash != new_hash:
            # Analizar tipos de archivos cambiados
            config = self._load_config()
            important_exts = ['.py', '.json']
            
            # Contar archivos importantes cambiados
            important_changes = 0
            for file in changed_files:
                if any(file.endswith(ext) for ext in important_exts):
                    important_changes += 1
            
            # Solo crear snapshot si hay cambios en archivos importantes
            # o muchos cambios en archivos menores
            return important_changes > 0 or len(changed_files) > 5
        
        return False
    
    def create_snapshot(self, reason: str = "Auto-snapshot", force: bool = False) -> Optional[str]:
        """
        Crea un snapshot inteligente del proyecto
        Returns: ID del snapshot o None si no es necesario
        """
        with self.lock:
            try:
                # Calcular hash actual
                current_hash = self._calculate_project_hash()
                
                # Verificar si hay cambios desde el último snapshot
                config = self._load_config()
                last_snapshot = config.get("active_snapshots", [])[-1] if config.get("active_snapshots") else None
                
                if last_snapshot:
                    last_hash = last_snapshot.get("hash", "")
                    if current_hash == last_hash and not force:
                        print("🔄 Sin cambios significativos desde el último snapshot")
                        return None
                
                # Generar ID único con timestamp
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                snapshot_id = f"ai_snap_{timestamp}_{current_hash[:8]}"
                snapshot_path = self.snapshots_dir / snapshot_id
                
                # Crear directorio del snapshot
                snapshot_path.mkdir(exist_ok=True)
                
                print(f"📸 Creando snapshot: {snapshot_id}")
                print(f"   Razón: {reason}")
                
                # 1. Guardar archivos esenciales
                files_dir = snapshot_path / "files"
                files_dir.mkdir(exist_ok=True)
                
                files_copied = self._copy_essential_files(files_dir)
                
                # 2. Generar documentación automática
                doc_content = self._generate_smart_documentation(files_dir)
                doc_file = snapshot_path / "DOCUMENTACION.md"
                with open(doc_file, 'w', encoding='utf-8') as f:
                    f.write(doc_content)
                
                # 3. Crear metadatos
                metadata = {
                    "id": snapshot_id,
                    "created": datetime.datetime.now().isoformat(),
                    "reason": reason,
                    "hash": current_hash,
                    "files_copied": files_copied,
                    "project_size_mb": self._get_project_size() / (1024*1024),
                    "documentation": "DOCUMENTACION.md"
                }
                
                metadata_file = snapshot_path / "metadata.json"
                with open(metadata_file, 'w', encoding='utf-8') as f:
                    json.dump(metadata, f, indent=2, ensure_ascii=False)
                
                # 4. Actualizar configuración
                config["active_snapshots"].append({
                    "id": snapshot_id,
                    "created": metadata["created"],
                    "reason": reason,
                    "hash": current_hash,
                    "size_kb": sum(f.stat().st_size for f in snapshot_path.rglob('*') if f.is_file()) / 1024
                })
                
                # Mantener solo los últimos N snapshots
                if len(config["active_snapshots"]) > self.max_snapshots:
                    self._auto_cleanup(config)
                
                config["total_snapshots"] = len(config["active_snapshots"])
                self._save_config(config)
                
                print(f"✅ Snapshot creado: {snapshot_id}")
                print(f"📊 Snapshots activos: {len(config['active_snapshots'])}/{self.max_snapshots}")
                
                # Generar reporte para chat
                chat_report = self._generate_chat_report(snapshot_id)
                with open(snapshot_path / "CHAT_REPORT.txt", 'w', encoding='utf-8') as f:
                    f.write(chat_report)
                
                print(f"📋 Reporte para chat generado")
                
                return snapshot_id
                
            except Exception as e:
                print(f"❌ Error creando snapshot: {e}")
                return None
    
    def _copy_essential_files(self, target_dir: Path) -> int:
        """Copia solo archivos esenciales (no todo)"""
        config = self._load_config()
        extensions = config.get("tracked_extensions", [".py", ".json"])
        ignored = config.get("ignored_patterns", [])
        
        files_copied = 0
        
        for ext in extensions:
            for source_file in self.base_dir.rglob(f"*{ext}"):
                # Ignorar patrones
                if any(pattern in str(source_file) for pattern in ignored):
                    continue
                
                if source_file.is_file():
                    rel_path = source_file.relative_to(self.base_dir)
                    target_file = target_dir / rel_path
                    
                    # Crear directorios padres
                    target_file.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Copiar archivo
                    shutil.copy2(source_file, target_file)
                    files_copied += 1
        
        return files_copied
    
    def _generate_smart_documentation(self, files_dir: Path) -> str:
        """Genera documentación inteligente basada en el contenido"""
        lines = []
        
        lines.append("# 🌀 VECTA 12D - SNAPSHOT INTELIGENTE")
        lines.append(f"*Generado: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        lines.append("")
        
        # Análisis automático de estructura
        lines.append("## 📊 ANÁLISIS AUTOMÁTICO")
        
        # Contar archivos por tipo
        file_counts = {}
        for ext in ['.py', '.json', '.md', '.txt', '.bat']:
            count = len(list(files_dir.rglob(f"*{ext}")))
            if count > 0:
                file_counts[ext] = count
        
        lines.append("### Archivos por tipo:")
        for ext, count in file_counts.items():
            lines.append(f"- `{ext}`: {count} archivos")
        
        # Verificar componentes críticos
        lines.append("\n### Componentes críticos:")
        critical_files = [
            ("vecta_launcher.py", "Lanzador principal"),
            ("core/meta_vecta.py", "Núcleo META-VECTA"),
            ("core/vecta_12d_core.py", "Núcleo 12D"),
            ("dimensiones/vector_12d.py", "Sistema vectorial"),
            ("INSTALAR.bat", "Instalador Windows")
        ]
        
        for file, desc in critical_files:
            if (files_dir / file).exists():
                lines.append(f"- ✅ `{file}`: {desc}")
            else:
                lines.append(f"- ❌ `{file}`: {desc} (FALTANTE)")
        
        # Analizar dimensiones
        dimension_files = list(files_dir.rglob("dimensiones/dimension_*.py"))
        lines.append(f"\n### Sistema de dimensiones: {len(dimension_files)}/12")
        
        # Detectar versiones
        lines.append("\n### Versiones detectadas:")
        version_files = [files_dir / "core/meta_vecta.py", files_dir / "vecta_launcher.py"]
        for vfile in version_files:
            if vfile.exists():
                try:
                    content = vfile.read_text(encoding='utf-8')
                    for line in content.split('\n'):
                        if 'version' in line.lower() and '=' in line:
                            lines.append(f"- `{vfile.relative_to(files_dir)}`: {line.strip()}")
                            break
                except:
                    pass
        
        lines.append("\n---")
        lines.append("*Documentación generada automáticamente por AI Snapshot Manager*")
        
        return '\n'.join(lines)
    
    def _generate_chat_report(self, snapshot_id: str) -> str:
        """Genera reporte optimizado para chat"""
        snapshot_path = self.snapshots_dir / snapshot_id
        metadata_file = snapshot_path / "metadata.json"
        
        if metadata_file.exists():
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
        
        # Reporte compacto para chat
        report = [
            "# 🌀 VECTA 12D - ESTADO ACTUAL",
            f"*Snapshot ID: {snapshot_id}*",
            f"*Fecha: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
            "",
            "## 📊 RESUMEN RÁPIDO",
            f"- Hash del proyecto: `{metadata.get('hash', 'N/A')[:16]}...`",
            f"- Archivos guardados: {metadata.get('files_copied', 0)}",
            f"- Tamaño: {metadata.get('project_size_mb', 0):.2f} MB",
            "",
            "## 🚀 COMANDOS PARA CONTINUAR",
            "```bash",
            "# Para restaurar este estado:",
            f"python vecta_ai_snapshot.py restore {snapshot_id}",
            "",
            "# Para iniciar VECTA:",
            "python vecta_launcher.py",
            "",
            "# Para reparar sistema:",
            "python reparar_vecta.py",
            "```",
            "",
            "## 📁 ARCHIVOS PRINCIPALES",
            self._get_key_files_list(snapshot_path),
            "",
            "---",
            "*Para detalles completos, ver DOCUMENTACION.md en el snapshot*"
        ]
        
        return '\n'.join(report)
    
    def _get_key_files_list(self, snapshot_path: Path) -> str:
        """Lista archivos clave formateados"""
        key_files = []
        important_patterns = [
            "vecta_launcher.py",
            "core/meta_vecta.py",
            "core/vecta_12d_core.py",
            "dimensiones/vector_12d.py",
            "vecta_auto_build.py",
            "INSTALAR.bat"
        ]
        
        for pattern in important_patterns:
            file_path = snapshot_path / "files" / pattern
            if file_path.exists():
                size_kb = file_path.stat().st_size / 1024
                key_files.append(f"- ✅ `{pattern}` ({size_kb:.1f} KB)")
            else:
                key_files.append(f"- ❌ `{pattern}` (NO ENCONTRADO)")
        
        return '\n'.join(key_files)
    
    def _auto_cleanup(self, config):
        """Limpia snapshots antiguos automáticamente"""
        if not config.get("auto_cleanup", True):
            return
        
        # Mantener solo los últimos max_snapshots
        while len(config["active_snapshots"]) > self.max_snapshots:
            oldest = config["active_snapshots"].pop(0)
            self._delete_snapshot(oldest["id"])
            print(f"🗑️  Auto-eliminado snapshot antiguo: {oldest['id']}")
    
    def _delete_snapshot(self, snapshot_id: str):
        """Elimina un snapshot"""
        snapshot_path = self.snapshots_dir / snapshot_id
        if snapshot_path.exists():
            shutil.rmtree(snapshot_path)
    
    def list_snapshots(self) -> List[Dict]:
        """Lista snapshots disponibles"""
        config = self._load_config()
        return config.get("active_snapshots", [])
    
    def restore_snapshot(self, snapshot_id: str) -> bool:
        """Restaura el proyecto a un snapshot anterior"""
        try:
            snapshot_path = self.snapshots_dir / snapshot_id
            if not snapshot_path.exists():
                print(f"❌ Snapshot no encontrado: {snapshot_id}")
                return False
            
            files_dir = snapshot_path / "files"
            
            print(f"🔄 Restaurando: {snapshot_id}")
            
            # Primero hacer backup del estado actual
            current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            temp_backup = self.snapshots_dir / f"temp_backup_{current_time}"
            if self.base_dir.exists():
                shutil.copytree(self.base_dir, temp_backup, 
                              ignore=shutil.ignore_patterns('.ai_snapshots', '__pycache__', '*.pyc'))
            
            # Limpiar directorio actual (excepto snapshots)
            for item in self.base_dir.iterdir():
                if item.name != '.ai_snapshots' and item.name != temp_backup.name:
                    if item.is_dir():
                        shutil.rmtree(item)
                    else:
                        item.unlink()
            
            # Restaurar archivos
            shutil.copytree(files_dir, self.base_dir, dirs_exist_ok=True)
            
            # Eliminar backup temporal
            shutil.rmtree(temp_backup)
            
            print(f"✅ Restauración completada: {snapshot_id}")
            
            # Mostrar reporte del snapshot
            chat_report_file = snapshot_path / "CHAT_REPORT.txt"
            if chat_report_file.exists():
                with open(chat_report_file, 'r', encoding='utf-8') as f:
                    print("\n" + "="*60)
                    print("📋 REPORTE DEL SNAPSHOT:")
                    print("="*60)
                    content = f.read()
                    # Mostrar solo primeras 30 líneas
                    lines = content.split('\n')[:30]
                    print('\n'.join(lines))
                    if len(content.split('\n')) > 30:
                        print("... [continúa en el archivo]")
            
            return True
            
        except Exception as e:
            print(f"❌ Error en restauración: {e}")
            return False
    
    def get_status_report(self) -> str:
        """Genera reporte de estado actual del sistema"""
        config = self._load_config()
        current_hash = self._calculate_project_hash()
        
        report = [
            "🔄 VECTA 12D - SISTEMA DE SNAPSHOTS AI",
            "="*40,
            f"Estado: {'🟢 ACTIVO' if self.auto_mode else '🟡 MANUAL'}",
            f"Snapshots activos: {len(config.get('active_snapshots', []))}/{self.max_snapshots}",
            f"Hash actual: {current_hash[:16]}...",
            f"Auto-limpieza: {'✅ ACTIVADA' if config.get('auto_cleanup', True) else '❌ DESACTIVADA'}",
            "",
            "Últimos snapshots:"
        ]
        
        snapshots = config.get("active_snapshots", [])
        for snap in snapshots[-3:]:  # Mostrar solo los 3 últimos
            report.append(f"  • {snap['id']} - {snap['reason']}")
        
        report.append("")
        report.append("📊 Para crear snapshot ahora:")
        report.append("  python vecta_ai_snapshot.py snapshot")
        report.append("")
        report.append("📋 Para ver reporte de chat del último estado:")
        report.append("  python vecta_ai_snapshot.py chat")
        
        return '\n'.join(report)
    
    def _get_project_size(self) -> int:
        """Calcula tamaño del proyecto en bytes"""
        total = 0
        for path in self.base_dir.rglob("*"):
            if path.is_file():
                # Ignorar directorio de snapshots
                if '.ai_snapshots' not in str(path):
                    total += path.stat().st_size
        return total
    
    def _start_monitoring(self):
        """Inicia monitoreo automático (simplificado)"""
        print("🔍 Sistema de monitoreo automático iniciado")
        print("   Los snapshots se crearán automáticamente después de cambios significativos")
        
        # Crear snapshot inicial si no existe ninguno
        config = self._load_config()
        if not config.get("active_snapshots"):
            self.create_snapshot("Snapshot inicial del sistema", force=True)


# ====================================================
# SISTEMA DE INTEGRACIÓN AUTOMÁTICA CON VECTA
# ====================================================

class VECTA_AutoIntegrator:
    """Integra el sistema de snapshots con VECTA automáticamente"""
    
    @staticmethod
    def patch_vecta_files():
        """Parchea archivos de VECTA para integración automática"""
        
        # 1. Parchear vecta_launcher.py
        launcher_path = Path("vecta_launcher.py")
        if launcher_path.exists():
            content = launcher_path.read_text(encoding='utf-8')
            
            # Añadir import y creación de snapshot al inicio
            if "from vecta_ai_snapshot import" not in content:
                patch_code = """
# ============================================================================
# AUTO-SNAPSHOT INTEGRATION (Added by VECTA AI Snapshot System)
# ============================================================================
try:
    from vecta_ai_snapshot import VECTA_AISnapshot
    snapshot_system = VECTA_AISnapshot(auto_mode=True)
    snapshot_system.create_snapshot("VECTA launcher ejecutado")
except ImportError as e:
    print(f"⚠️  AI Snapshot System not available: {e}")
except Exception as e:
    print(f"⚠️  Error in AI Snapshot System: {e}")
# ============================================================================
"""
                
                # Insertar después de los imports
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if 'import' in line and 'def ' not in lines[i+1] and 'class ' not in lines[i+1]:
                        continue
                    if 'def ' in line or 'class ' in line:
                        lines.insert(i, patch_code)
                        break
                
                launcher_path.write_text('\n'.join(lines))
                print("✅ vecta_launcher.py parcheado para auto-snapshots")
        
        # 2. Crear script de activación automática
        auto_script = """
#!/usr/bin/env python3
"""
        
        auto_path = Path("vecta_auto_snapshot.py")
        if not auto_path.exists():
            auto_path.write_text(auto_script)
            print("✅ Script de auto-snapshot creado")


# ====================================================
# INTERFAZ DE USUARIO SIMPLE
# ====================================================

def main():
    """Interfaz principal de usuario"""
    
    print("\n" + "="*60)
    print("🌀 VECTA 12D - AI SNAPSHOT MANAGER")
    print("="*60)
    
    # Argumentos de línea de comandos
    if len(sys.argv) > 1:
        command = sys.argv[1]
        manager = VECTA_AISnapshot()
        
        if command == "snapshot":
            reason = sys.argv[2] if len(sys.argv) > 2 else "Comando manual"
            manager.create_snapshot(reason, force=True)
            
        elif command == "restore":
            if len(sys.argv) > 2:
                manager.restore_snapshot(sys.argv[2])
            else:
                snapshots = manager.list_snapshots()
                if snapshots:
                    print("Snapshots disponibles:")
                    for i, snap in enumerate(snapshots, 1):
                        print(f"{i}. {snap['id']} - {snap['reason']}")
                    choice = input("\nNúmero a restaurar: ")
                    if choice.isdigit():
                        idx = int(choice) - 1
                        if 0 <= idx < len(snapshots):
                            manager.restore_snapshot(snapshots[idx]["id"])
                else:
                    print("❌ No hay snapshots disponibles")
            
        elif command == "list":
            snapshots = manager.list_snapshots()
            print("\n📋 SNAPSHOTS ACTIVOS:")
            print("-" * 50)
            for snap in snapshots:
                print(f"• {snap['id']}")
                print(f"  Razón: {snap['reason']}")
                print(f"  Creado: {snap['created']}")
                print(f"  Tamaño: {snap.get('size_kb', 0):.1f} KB")
                print()
            
        elif command == "chat":
            # Generar reporte para chat del último estado
            snapshots = manager.list_snapshots()
            if snapshots:
                last_snapshot = snapshots[-1]
                snapshot_path = Path(".ai_snapshots") / last_snapshot["id"]
                chat_file = snapshot_path / "CHAT_REPORT.txt"
                
                if chat_file.exists():
                    with open(chat_file, 'r', encoding='utf-8') as f:
                        print("\n📋 COPIA ESTO EN EL CHAT:")
                        print("="*60)
                        print(f.read())
                        print("="*60)
                        print("\n💡 Presiona Ctrl+A, Ctrl+C para copiar todo")
                else:
                    print("❌ No se encontró reporte de chat")
            else:
                print("❌ No hay snapshots disponibles")
            
        elif command == "status":
            print(manager.get_status_report())
            
        elif command == "auto":
            # Activar modo automático permanente
            config = manager._load_config()
            config["auto_mode"] = True
            manager._save_config(config)
            print("✅ Modo automático activado permanentemente")
            
        elif command == "manual":
            # Desactivar modo automático
            config = manager._load_config()
            config["auto_mode"] = False
            manager._save_config(config)
            print("✅ Modo manual activado")
            
        elif command == "integrate":
            # Integrar con VECTA
            VECTA_AutoIntegrator.patch_vecta_files()
            print("✅ Integración completada")
            
        elif command == "clean":
            # Limpiar snapshots antiguos
            config = manager._load_config()
            while len(config.get("active_snapshots", [])) > 3:
                oldest = config["active_snapshots"].pop(0)
                manager._delete_snapshot(oldest["id"])
                print(f"🗑️  Eliminado: {oldest['id']}")
            manager._save_config(config)
            print("✅ Limpieza completada")
            
        else:
            print(f"❌ Comando desconocido: {command}")
    
    else:
        # Modo interactivo
        manager = VECTA_AISnapshot()
        
        while True:
            print("\n" + manager.get_status_report())
            print("\nOpciones:")
            print("1. Crear snapshot ahora")
            print("2. Restaurar snapshot anterior")
            print("3. Ver lista de snapshots")
            print("4. Generar reporte para chat")
            print("5. Integrar con VECTA (auto-snapshots)")
            print("6. Limpiar snapshots antiguos")
            print("7. Salir")
            
            try:
                choice = input("\nSelección [1-7]: ").strip()
            except KeyboardInterrupt:
                print("\n👋 Saliendo...")
                break
            
            if choice == "1":
                reason = input("Razón (opcional): ").strip()
                if not reason:
                    reason = "Snapshot manual"
                manager.create_snapshot(reason, force=True)
                
            elif choice == "2":
                snapshots = manager.list_snapshots()
                if snapshots:
                    print("\nSnapshots disponibles:")
                    for i, snap in enumerate(snapshots, 1):
                        print(f"{i}. {snap['id']} - {snap['reason']}")
                    
                    try:
                        sel = input("\nNúmero a restaurar (0 para cancelar): ").strip()
                        if sel.isdigit():
                            idx = int(sel) - 1
                            if 0 <= idx < len(snapshots):
                                confirm = input(f"¿Restaurar {snapshots[idx]['id']}? (s/N): ").lower()
                                if confirm == 's':
                                    manager.restore_snapshot(snapshots[idx]["id"])
                    except:
                        print("❌ Selección inválida")
                else:
                    print("❌ No hay snapshots disponibles")
                    
            elif choice == "3":
                snapshots = manager.list_snapshots()
                if snapshots:
                    print("\n📋 SNAPSHOTS ACTIVOS:")
                    for snap in snapshots:
                        print(f"• {snap['id']} - {snap['reason']}")
                else:
                    print("❌ No hay snapshots disponibles")
                    
            elif choice == "4":
                snapshots = manager.list_snapshots()
                if snapshots:
                    last_snapshot = snapshots[-1]
                    snapshot_path = Path(".ai_snapshots") / last_snapshot["id"]
                    chat_file = snapshot_path / "CHAT_REPORT.txt"
                    
                    if chat_file.exists():
                        with open(chat_file, 'r', encoding='utf-8') as f:
                            print("\n" + "="*60)
                            print("📋 COPIA TODO ESTO EN EL NUEVO CHAT:")
                            print("="*60)
                            print(f.read())
                            print("="*60)
                            print("\n💡 Presiona Ctrl+A, Ctrl+C para copiar todo")
                    else:
                        print("❌ Generando reporte...")
                        manager._generate_chat_report(last_snapshot["id"])
                else:
                    print("❌ Crea un snapshot primero")
                    
            elif choice == "5":
                VECTA_AutoIntegrator.patch_vecta_files()
                
            elif choice == "6":
                config = manager._load_config()
                current_count = len(config.get("active_snapshots", []))
                if current_count > 3:
                    while len(config["active_snapshots"]) > 3:
                        oldest = config["active_snapshots"].pop(0)
                        manager._delete_snapshot(oldest["id"])
                        print(f"🗑️  Eliminado: {oldest['id']}")
                    manager._save_config(config)
                    print(f"✅ Limpieza completada. Mantenidos: 3/{current_count}")
                else:
                    print(f"✅ Ya tienes solo {current_count} snapshots (mínimo: 3)")
                    
            elif choice == "7":
                print("👋 Saliendo del AI Snapshot Manager")
                break
            
            else:
                print("❌ Opción inválida")


if __name__ == "__main__":
    # Guardar este script como archivo permanente
    current_file = Path(__file__)
    if current_file.name != "vecta_ai_snapshot.py":
        target_file = Path("vecta_ai_snapshot.py")
        shutil.copy2(current_file, target_file)
        print(f"📄 Script guardado como: {target_file}")
    
    main()