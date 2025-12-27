#!/usr/bin/env python3
"""
DASHBOARD WEB VECTA 12D - MONITOR EN TIEMPO REAL
Sistema que refleja automaticamente la carpeta VECTA 12D Automatico
"""

import os
import sys
import json
import time
import threading
import webbrowser
from datetime import datetime
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler

# Intentar importar watchdog
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False
    print("ADVERTENCIA: watchdog no instalado. El monitoreo en tiempo real no funcionara.")
    print("Instala con: pip install watchdog")

class VECTAChangeHandler:
    """Manejador de cambios en los archivos VECTA (version simplificada si no hay watchdog)"""
    
    def __init__(self, dashboard):
        self.dashboard = dashboard
        self.change_log = []
        self.last_check = time.time()
        self.file_states = {}
        
    def check_for_changes(self):
        """Verifica cambios manualmente (usado si watchdog no esta disponible)"""
        current_time = time.time()
        
        # Verificar cada 2 segundos
        if current_time - self.last_check < 2:
            return
        
        self.last_check = current_time
        
        # Escanear todos los archivos
        for root, dirs, files in os.walk(self.dashboard.base_dir):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    stat = os.stat(file_path)
                    mod_time = stat.st_mtime
                    file_key = os.path.relpath(file_path, self.dashboard.base_dir)
                    
                    if file_key not in self.file_states:
                        # Archivo nuevo
                        self._log_change("CREADO", file_path)
                        self.file_states[file_key] = mod_time
                    elif self.file_states[file_key] != mod_time:
                        # Archivo modificado
                        self._log_change("MODIFICADO", file_path)
                        self.file_states[file_key] = mod_time
                        
                except Exception:
                    continue
        
        # Verificar archivos eliminados
        current_files = set()
        for root, dirs, files in os.walk(self.dashboard.base_dir):
            for file in files:
                file_path = os.path.join(root, file)
                file_key = os.path.relpath(file_path, self.dashboard.base_dir)
                current_files.add(file_key)
        
        # Encontrar archivos que estaban antes pero ya no estan
        for file_key in list(self.file_states.keys()):
            if file_key not in current_files:
                file_path = os.path.join(self.dashboard.base_dir, file_key)
                self._log_change("ELIMINADO", file_path)
                del self.file_states[file_key]
    
    def _log_change(self, action, path):
        """Registra un cambio manteniendo solo los ultimos 3"""
        try:
            rel_path = os.path.relpath(path, self.dashboard.base_dir)
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            change = {
                "timestamp": timestamp,
                "action": action,
                "path": rel_path,
                "full_path": path
            }
            
            self.change_log.insert(0, change)
            # Mantener solo ultimos 3 cambios
            self.change_log = self.change_log[:3]
            
            print(f"[{timestamp}] {action}: {rel_path}")
            self.dashboard.last_changes = self.change_log
            self.dashboard.update_html()
        except Exception as e:
            print(f"Error registrando cambio: {e}")

class VECTADashboard:
    """Dashboard principal de VECTA 12D"""
    
    def __init__(self, base_dir, port=8080):
        self.base_dir = base_dir
        self.port = port
        self.last_changes = []
        self.file_tree = []
        self.vecta_info = {}
        self.server = None
        self.observer = None
        self.change_handler = None
        
    def scan_directory(self):
        """Escanea recursivamente la estructura de directorios"""
        self.file_tree = []
        
        try:
            for root, dirs, files in os.walk(self.base_dir):
                # Calcular nivel de profundidad
                rel_root = os.path.relpath(root, self.base_dir)
                if rel_root == ".":
                    level = 0
                else:
                    level = len(rel_root.split(os.sep))
                
                # Agregar directorio
                dir_name = os.path.basename(root)
                if dir_name:
                    self.file_tree.append({
                        "type": "directory",
                        "name": dir_name,
                        "path": rel_root,
                        "level": level,
                        "items": len(files) + len(dirs)
                    })
                
                # Agregar archivos
                for file in files:
                    try:
                        file_path = os.path.join(root, file)
                        rel_path = os.path.relpath(file_path, self.base_dir)
                        size = os.path.getsize(file_path)
                        mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                        
                        self.file_tree.append({
                            "type": "file",
                            "name": file,
                            "path": rel_path,
                            "level": level + 1,
                            "size": self._format_size(size),
                            "modified": mod_time.strftime("%Y-%m-%d %H:%M:%S"),
                            "extension": os.path.splitext(file)[1].lower()
                        })
                    except Exception:
                        continue
        except Exception as e:
            print(f"Error escaneando directorio: {e}")
    
    def _format_size(self, size):
        """Formatea el tamaño del archivo"""
        try:
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024.0:
                    return f"{size:.1f} {unit}"
                size /= 1024.0
            return f"{size:.1f} TB"
        except:
            return "0 B"
    
    def get_vecta_info(self):
        """Obtiene informacion del sistema VECTA"""
        info = {
            "nombre": "VECTA 12D Automatico",
            "directorio": self.base_dir,
            "fecha_actual": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_archivos": 0,
            "total_directorios": 0,
            "tamano_total": 0
        }
        
        try:
            for root, dirs, files in os.walk(self.base_dir):
                info["total_directorios"] += len(dirs)
                info["total_archivos"] += len(files)
                for file in files:
                    try:
                        file_path = os.path.join(root, file)
                        info["tamano_total"] += os.path.getsize(file_path)
                    except:
                        pass
        except Exception:
            pass
        
        info["tamano_total"] = self._format_size(info["tamano_total"])
        
        # Verificar componentes principales
        componentes = {
            "vecta_launcher.py": os.path.exists(os.path.join(self.base_dir, "vecta_launcher.py")),
            "core/meta_vecta.py": os.path.exists(os.path.join(self.base_dir, "core", "meta_vecta.py")),
            "dimensiones/vector_12d.py": os.path.exists(os.path.join(self.base_dir, "dimensiones", "vector_12d.py")),
            "dimensiones/dimension_1.py": os.path.exists(os.path.join(self.base_dir, "dimensiones", "dimension_1.py"))
        }
        
        info["componentes"] = componentes
        info["componentes_activos"] = sum(1 for v in componentes.values() if v)
        info["componentes_totales"] = len(componentes)
        
        return info
    
    def generate_html(self):
        """Genera el HTML del dashboard"""
        self.scan_directory()
        self.vecta_info = self.get_vecta_info()
        
        # Generar HTML para los cambios
        changes_html = ""
        if self.last_changes:
            for change in self.last_changes:
                action_class = {
                    "CREADO": "change-added",
                    "MODIFICADO": "change-modified", 
                    "ELIMINADO": "change-deleted"
                }.get(change["action"], "change-modified")
                
                action_icon = {
                    "CREADO": "+",
                    "MODIFICADO": "~",
                    "ELIMINADO": "x"
                }.get(change["action"], "~")
                
                changes_html += f'''
                <div class="change-item {action_class}">
                    <div class="change-time">{change['timestamp']}</div>
                    <div>
                        <span class="change-action">{action_icon} {change['action']}</span>
                        <span class="change-path">{change['path']}</span>
                    </div>
                </div>'''
        else:
            changes_html = '''
            <div class="change-item change-modified">
                <div class="change-time">Esperando cambios...</div>
                <div>
                    <span class="change-action">Sin cambios recientes</span>
                    <span class="change-path">El sistema esta monitoreando la carpeta</span>
                </div>
            </div>'''
        
        # Generar HTML para archivos
        files_html = ""
        for item in self.file_tree:
            level_class = f"level-{min(item['level'], 10)}"
            
            if item["type"] == "directory":
                icon = "📁"
                file_class = "folder"
                details = f"({item['items']} items)"
            else:
                icon = self._get_file_icon(item["extension"])
                file_class = self._get_file_class(item["extension"])
                details = f"{item['size']} | {item['modified']}"
            
            files_html += f'''
            <div class="file-item {level_class}">
                <span class="file-icon {file_class}">{icon}</span>
                <div style="flex: 1;">
                    <div style="color: white; font-weight: 500;">{item['name']}</div>
                    <div style="color: #888; font-size: 0.9em;">{details}</div>
                </div>
            </div>'''
        
        html = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard VECTA 12D</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: Arial, sans-serif; 
            background: #0f2027;
            color: #e0e0e0; 
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{ 
            max-width: 1400px; 
            margin: 0 auto; 
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }}
        .header {{ 
            grid-column: 1 / -1;
            background: rgba(0, 0, 0, 0.3); 
            padding: 20px; 
            border-radius: 10px;
            margin-bottom: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
        .header h1 {{ 
            color: #00d4ff; 
            font-size: 2em; 
            margin-bottom: 10px;
        }}
        .header p {{ 
            color: #a0a0a0; 
        }}
        .card {{ 
            background: rgba(20, 30, 40, 0.7); 
            border-radius: 10px; 
            padding: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
        .card h2 {{ 
            color: #00ff88; 
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 1px solid rgba(0, 255, 136, 0.3);
        }}
        .card h3 {{ 
            color: #00d4ff; 
            margin: 10px 0;
        }}
        .status-grid {{ 
            display: grid; 
            grid-template-columns: repeat(2, 1fr); 
            gap: 10px;
        }}
        .status-item {{ 
            background: rgba(0, 0, 0, 0.2); 
            padding: 10px; 
            border-radius: 5px;
            border-left: 3px solid #00d4ff;
        }}
        .status-label {{ 
            color: #a0a0a0; 
            font-size: 0.8em; 
            margin-bottom: 5px;
        }}
        .status-value {{ 
            color: #ffffff; 
            font-size: 1em; 
        }}
        .file-tree {{ 
            max-height: 400px; 
            overflow-y: auto;
            background: rgba(0, 0, 0, 0.2);
            border-radius: 5px;
            padding: 10px;
        }}
        .file-item {{ 
            padding: 5px 10px; 
            margin: 2px 0; 
            border-radius: 3px;
            display: flex;
            align-items: center;
        }}
        .file-item:hover {{ 
            background: rgba(255, 255, 255, 0.05);
        }}
        .file-icon {{ 
            margin-right: 8px; 
        }}
        .folder {{ color: #00d4ff; }}
        .python {{ color: #00ff88; }}
        .json {{ color: #ffaa00; }}
        .txt {{ color: #a0a0ff; }}
        .bat {{ color: #ff5555; }}
        .changes-list {{ 
            list-style: none;
        }}
        .change-item {{ 
            background: rgba(0, 0, 0, 0.2); 
            padding: 10px; 
            margin: 5px 0;
            border-radius: 5px;
            border-left: 3px solid;
        }}
        .change-added {{ border-left-color: #00ff88; }}
        .change-modified {{ border-left-color: #00d4ff; }}
        .change-deleted {{ border-left-color: #ff5555; }}
        .change-time {{ 
            color: #a0a0a0; 
            font-size: 0.8em; 
            margin-bottom: 5px;
        }}
        .change-action {{ 
            color: #ffffff; 
            font-weight: bold; 
            margin-right: 10px;
        }}
        .change-path {{ 
            color: #cccccc; 
            font-family: monospace;
            word-break: break-all;
        }}
        .auto-refresh {{ 
            background: rgba(0, 212, 255, 0.1); 
            padding: 8px; 
            border-radius: 5px;
            margin-top: 15px;
            text-align: center;
            font-size: 0.8em;
            color: #00d4ff;
        }}
        .footer {{ 
            grid-column: 1 / -1;
            text-align: center; 
            padding: 15px; 
            color: #666; 
            font-size: 0.8em;
            margin-top: 20px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }}
        .level-1 {{ margin-left: 10px; }}
        .level-2 {{ margin-left: 20px; }}
        .level-3 {{ margin-left: 30px; }}
        .level-4 {{ margin-left: 40px; }}
        .level-5 {{ margin-left: 50px; }}
        .level-6 {{ margin-left: 60px; }}
        .level-7 {{ margin-left: 70px; }}
        .level-8 {{ margin-left: 80px; }}
        .level-9 {{ margin-left: 90px; }}
        .level-10 {{ margin-left: 100px; }}
        .warning {{ 
            background: rgba(255, 100, 0, 0.2); 
            padding: 10px; 
            border-radius: 5px;
            border: 1px solid #ff6400;
            margin-bottom: 15px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>VECTA 12D - DASHBOARD EN TIEMPO REAL</h1>
            <p>Monitoreo automatico del sistema de 12 dimensiones vectoriales | Ultima actualizacion: {self.vecta_info['fecha_actual']}</p>
        </div>
        
        <div class="card">
            <h2>ESTADO DEL SISTEMA</h2>
            <div class="status-grid">
                <div class="status-item">
                    <div class="status-label">Directorio Actual</div>
                    <div class="status-value">{os.path.basename(self.base_dir)}</div>
                </div>
                <div class="status-item">
                    <div class="status-label">Total Archivos</div>
                    <div class="status-value">{self.vecta_info['total_archivos']}</div>
                </div>
                <div class="status-item">
                    <div class="status-label">Total Carpetas</div>
                    <div class="status-value">{self.vecta_info['total_directorios']}</div>
                </div>
                <div class="status-item">
                    <div class="status-label">Tamaño Total</div>
                    <div class="status-value">{self.vecta_info['tamano_total']}</div>
                </div>
            </div>
            
            <h3>Componentes Principales</h3>
            <div class="status-grid">
                <div class="status-item" style="border-left-color: {'#00ff88' if self.vecta_info['componentes']['vecta_launcher.py'] else '#ff5555'}">
                    <div class="status-label">Lanzador Principal</div>
                    <div class="status-value">{'Activo' if self.vecta_info['componentes']['vecta_launcher.py'] else 'No encontrado'}</div>
                </div>
                <div class="status-item" style="border-left-color: {'#00ff88' if self.vecta_info['componentes']['core/meta_vecta.py'] else '#ff5555'}">
                    <div class="status-label">Nucleo META-VECTA</div>
                    <div class="status-value">{'Activo' if self.vecta_info['componentes']['core/meta_vecta.py'] else 'No encontrado'}</div>
                </div>
                <div class="status-item" style="border-left-color: {'#00ff88' if self.vecta_info['componentes']['dimensiones/vector_12d.py'] else '#ff5555'}">
                    <div class="status-label">Sistema Vectorial</div>
                    <div class="status-value">{'Activo' if self.vecta_info['componentes']['dimensiones/vector_12d.py'] else 'No encontrado'}</div>
                </div>
                <div class="status-item" style="border-left-color: {'#00ff88' if self.vecta_info['componentes']['dimensiones/dimension_1.py'] else '#ff5555'}">
                    <div class="status-label">Dimension 1</div>
                    <div class="status-value">{'Activa' if self.vecta_info['componentes']['dimensiones/dimension_1.py'] else 'No encontrada'}</div>
                </div>
            </div>
        </div>
        
        <div class="card">
            <h2>ULTIMOS 3 CAMBIOS</h2>
            <div class="changes-list">
                {changes_html}
            </div>
            
            <div class="auto-refresh">
                Auto-refresh en 5 segundos | Cambios detectados en tiempo real
            </div>
        </div>
        
        <div class="card" style="grid-column: 1 / -1;">
            <h2>ESTRUCTURA DE ARCHIVOS</h2>
            <p style="margin-bottom: 10px; color: #a0a0a0;">
                Directorio base: {self.base_dir} | Total items: {len(self.file_tree)}
            </p>
            <div class="file-tree">
                {files_html}
            </div>
        </div>
        
        <div class="footer">
            <p>VECTA 12D Dashboard v1.0 | Sistema de monitoreo en tiempo real</p>
            <p>Desarrollado para Rafael Porley | {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        </div>
    </div>
    
    <script>
        // Auto-refresh cada 5 segundos
        setTimeout(function() {{
            window.location.reload();
        }}, 5000);
    </script>
</body>
</html>'''
        
        return html
    
    def _get_file_icon(self, extension):
        """Obtiene icono segun extension"""
        icons = {
            '.py': '🐍', '.json': '📊', '.txt': '📄', '.md': '📝',
            '.bat': '⚙️', '.html': '🌐', '.css': '🎨', '.js': '📜',
            '.png': '🖼️', '.jpg': '🖼️', '.ico': '🖼️', '.exe': '⚡'
        }
        return icons.get(extension, '📄')
    
    def _get_file_class(self, extension):
        """Obtiene clase CSS segun extension"""
        classes = {
            '.py': 'python', '.json': 'json', '.txt': 'txt', 
            '.md': 'txt', '.bat': 'bat', '.html': 'other',
            '.css': 'other', '.js': 'other', '.exe': 'other'
        }
        return classes.get(extension, 'other')
    
    def update_html(self):
        """Actualiza el archivo HTML"""
        try:
            html_content = self.generate_html()
            html_path = os.path.join(self.base_dir, "dashboard_vecta.html")
            
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            
            print(f"Dashboard actualizado: {html_path}")
        except Exception as e:
            print(f"Error actualizando dashboard: {e}")
    
    def start_monitoring(self):
        """Inicia el monitoreo de archivos"""
        self.change_handler = VECTAChangeHandler(self)
        
        if WATCHDOG_AVAILABLE:
            # Usar watchdog si esta disponible
            event_handler = type('EventHandler', (FileSystemEventHandler,), {
                'on_modified': lambda self, event: self._on_event('MODIFICADO', event),
                'on_created': lambda self, event: self._on_event('CREADO', event),
                'on_deleted': lambda self, event: self._on_event('ELIMINADO', event),
                '_on_event': lambda self, action, event: self._log_event(action, event) if not event.is_directory else None,
                '_log_event': lambda self, action, event: self.dashboard.change_handler._log_change(action, event.src_path),
                'dashboard': self
            })()
            
            self.observer = Observer()
            self.observer.schedule(event_handler, self.base_dir, recursive=True)
            self.observer.start()
            print(f"Monitoreo con watchdog iniciado en: {self.base_dir}")
        else:
            # Modo manual sin watchdog
            print(f"Monitoreo manual iniciado en: {self.base_dir}")
            print("Nota: Para monitoreo en tiempo real, instala: pip install watchdog")
    
    def start_server(self):
        """Inicia el servidor web"""
        os.chdir(self.base_dir)
        
        class DashboardHandler(SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=self.base_dir, **kwargs)
            
            def log_message(self, format, *args):
                # Silenciar logs normales
                pass
            
            def do_GET(self):
                # Redirigir / al dashboard
                if self.path == "/":
                    self.path = "/dashboard_vecta.html"
                return super().do_GET()
        
        self.server = HTTPServer(("localhost", self.port), DashboardHandler)
        server_thread = threading.Thread(target=self.server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        
        print(f"Servidor iniciado en: http://localhost:{self.port}")
        print(f"Dashboard disponible en: http://localhost:{self.port}/")
        
        # Abrir navegador automaticamente
        try:
            webbrowser.open(f"http://localhost:{self.port}")
        except:
            print("No se pudo abrir el navegador automaticamente. Abre manualmente:")
            print(f"  http://localhost:{self.port}")
    
    def run(self):
        """Ejecuta el dashboard completo"""
        print("=" * 70)
        print("INICIANDO DASHBOARD VECTA 12D EN TIEMPO REAL")
        print("=" * 70)
        
        # Crear HTML inicial
        self.update_html()
        
        # Iniciar monitoreo
        self.start_monitoring()
        
        # Iniciar servidor
        self.start_server()
        
        print("\nDASHBOARD INICIADO CORRECTAMENTE")
        print("   - Monitoreando cambios en la carpeta")
        print("   - Servidor web en ejecucion")
        print("   - Navegador abierto automaticamente")
        print("\nCOMANDOS:")
        print("   - Ctrl+C para detener el dashboard")
        print("   - Recarga la pagina para ver cambios")
        print("=" * 70)
        
        try:
            # Mantener el script ejecutandose
            while True:
                if not WATCHDOG_AVAILABLE and self.change_handler:
                    # Modo manual: verificar cambios periodicamente
                    self.change_handler.check_for_changes()
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nDeteniendo dashboard...")
            if self.observer:
                self.observer.stop()
                self.observer.join()
            if self.server:
                self.server.shutdown()
            print("Dashboard detenido correctamente")

def main():
    """Funcion principal"""
    # Configuracion
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    PORT = 8080
    
    # Crear y ejecutar dashboard
    dashboard = VECTADashboard(BASE_DIR, PORT)
    dashboard.run()

if __name__ == "__main__":
    main()