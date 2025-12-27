#!/usr/bin/env python3
"""
DASHBOARD WEB VECTA 12D - MONITOR EN TIEMPO REAL
Sistema que refleja automáticamente la carpeta VECTA 12D Automatico
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
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class VECTAChangeHandler(FileSystemEventHandler):
    """Manejador de cambios en los archivos VECTA"""
    
    def __init__(self, dashboard):
        self.dashboard = dashboard
        self.change_log = []
        
    def on_modified(self, event):
        if not event.is_directory:
            self._log_change("MODIFICADO", event.src_path)
            
    def on_created(self, event):
        if not event.is_directory:
            self._log_change("CREADO", event.src_path)
            
    def on_deleted(self, event):
        if not event.is_directory:
            self._log_change("ELIMINADO", event.src_path)
            
    def _log_change(self, action, path):
        """Registra un cambio manteniendo solo los últimos 3"""
        rel_path = os.path.relpath(path, self.dashboard.base_dir)
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        change = {
            "timestamp": timestamp,
            "action": action,
            "path": rel_path,
            "full_path": path
        }
        
        self.change_log.insert(0, change)
        # Mantener solo últimos 3 cambios
        self.change_log = self.change_log[:3]
        
        print(f"[{timestamp}] {action}: {rel_path}")
        self.dashboard.last_changes = self.change_log
        self.dashboard.update_html()

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
        
    def scan_directory(self):
        """Escanea recursivamente la estructura de directorios"""
        self.file_tree = []
        
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
    
    def _format_size(self, size):
        """Formatea el tamaño del archivo"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
    
    def get_vecta_info(self):
        """Obtiene información del sistema VECTA"""
        info = {
            "nombre": "VECTA 12D Automatico",
            "directorio": self.base_dir,
            "fecha_actual": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_archivos": 0,
            "total_directorios": 0,
            "tamano_total": 0
        }
        
        for root, dirs, files in os.walk(self.base_dir):
            info["total_directorios"] += len(dirs)
            info["total_archivos"] += len(files)
            for file in files:
                try:
                    file_path = os.path.join(root, file)
                    info["tamano_total"] += os.path.getsize(file_path)
                except:
                    pass
        
        info["tamano_total"] = self._format_size(info["tamano_total"])
        
        # Verificar componentes principales
        componentes = {
            "vecta_launcher.py": os.path.exists(os.path.join(self.base_dir, "vecta_launcher.py")),
            "core/meta_vecta.py": os.path.exists(os.path.join(self.base_dir, "core/meta_vecta.py")),
            "dimensiones/vector_12d.py": os.path.exists(os.path.join(self.base_dir, "dimensiones/vector_12d.py")),
            "dimensiones/dimension_1.py": os.path.exists(os.path.join(self.base_dir, "dimensiones/dimension_1.py"))
        }
        
        info["componentes"] = componentes
        info["componentes_activos"] = sum(1 for v in componentes.values() if v)
        info["componentes_totales"] = len(componentes)
        
        return info
    
    def generate_html(self):
        """Genera el HTML del dashboard"""
        self.scan_directory()
        self.vecta_info = self.get_vecta_info()
        
        html = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard VECTA 12D</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
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
            padding: 25px; 
            border-radius: 12px;
            margin-bottom: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }}
        .header h1 {{ 
            color: #00d4ff; 
            font-size: 2.5em; 
            margin-bottom: 10px;
            text-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
        }}
        .header p {{ 
            color: #a0a0a0; 
            font-size: 1.1em;
        }}
        .card {{ 
            background: rgba(20, 30, 40, 0.7); 
            border-radius: 12px; 
            padding: 25px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
            transition: transform 0.3s, box-shadow 0.3s;
        }}
        .card:hover {{ 
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
        }}
        .card h2 {{ 
            color: #00ff88; 
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid rgba(0, 255, 136, 0.3);
        }}
        .card h3 {{ 
            color: #00d4ff; 
            margin: 15px 0 10px 0;
        }}
        .status-grid {{ 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
            gap: 15px;
        }}
        .status-item {{ 
            background: rgba(0, 0, 0, 0.2); 
            padding: 15px; 
            border-radius: 8px;
            border-left: 4px solid #00d4ff;
        }}
        .status-label {{ 
            color: #a0a0a0; 
            font-size: 0.9em; 
            margin-bottom: 5px;
        }}
        .status-value {{ 
            color: #ffffff; 
            font-size: 1.2em; 
            font-weight: bold;
        }}
        .file-tree {{ 
            max-height: 500px; 
            overflow-y: auto;
            background: rgba(0, 0, 0, 0.2);
            border-radius: 8px;
            padding: 15px;
        }}
        .file-item {{ 
            padding: 8px 12px; 
            margin: 4px 0; 
            border-radius: 6px;
            display: flex;
            align-items: center;
            transition: background 0.2s;
        }}
        .file-item:hover {{ 
            background: rgba(255, 255, 255, 0.05);
        }}
        .file-icon {{ 
            margin-right: 10px; 
            font-size: 1.2em;
        }}
        .folder {{ color: #00d4ff; }}
        .python {{ color: #00ff88; }}
        .json {{ color: #ffaa00; }}
        .txt {{ color: #a0a0ff; }}
        .bat {{ color: #ff5555; }}
        .other {{ color: #a0a0a0; }}
        .changes-list {{ 
            list-style: none;
        }}
        .change-item {{ 
            background: rgba(0, 0, 0, 0.2); 
            padding: 15px; 
            margin: 10px 0;
            border-radius: 8px;
            border-left: 4px solid;
            animation: slideIn 0.5s ease-out;
        }}
        @keyframes slideIn {{
            from {{ transform: translateX(-20px); opacity: 0; }}
            to {{ transform: translateX(0); opacity: 1; }}
        }}
        .change-added {{ border-left-color: #00ff88; }}
        .change-modified {{ border-left-color: #00d4ff; }}
        .change-deleted {{ border-left-color: #ff5555; }}
        .change-time {{ 
            color: #a0a0a0; 
            font-size: 0.9em; 
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
            padding: 10px; 
            border-radius: 6px;
            margin-top: 20px;
            text-align: center;
            font-size: 0.9em;
            color: #00d4ff;
        }}
        .footer {{ 
            grid-column: 1 / -1;
            text-align: center; 
            padding: 20px; 
            color: #666; 
            font-size: 0.9em;
            margin-top: 20px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }}
        .level-1 {{ margin-left: 10px; }}
        .level-2 {{ margin-left: 30px; }}
        .level-3 {{ margin-left: 50px; }}
        .level-4 {{ margin-left: 70px; }}
        .level-5 {{ margin-left: 90px; }}
        .level-6 {{ margin-left: 110px; }}
        .level-7 {{ margin-left: 130px; }}
        .level-8 {{ margin-left: 150px; }}
        .level-9 {{ margin-left: 170px; }}
        .level-10 {{ margin-left: 190px; }}
    </style>
    <script>
        // Auto-refresh cada 5 segundos
        setTimeout(function() {{
            window.location.reload();
        }}, 5000);
        
        // Resaltar archivos por extensión
        function getFileIcon(extension) {{
            const icons = {{
                '.py': '🐍', '.json': '📊', '.txt': '📄', '.md': '📝',
                '.bat': '⚙️', '.html': '🌐', '.css': '🎨', '.js': '📜',
                '.png': '🖼️', '.jpg': '🖼️', '.ico': '🖼️'
            }};
            return icons[extension] || '📄';
        }}
        
        function getFileClass(extension) {{
            const classes = {{
                '.py': 'python', '.json': 'json', '.txt': 'txt', 
                '.md': 'txt', '.bat': 'bat', '.html': 'other',
                '.css': 'other', '.js': 'other'
            }};
            return classes[extension] || 'other';
        }}
    </script>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 VECTA 12D - DASHBOARD EN TIEMPO REAL</h1>
            <p>Monitoreo automático del sistema de 12 dimensiones vectoriales | Última actualización: {self.vecta_info['fecha_actual']}</p>
        </div>
        
        <div class="card">
            <h2>📊 ESTADO DEL SISTEMA</h2>
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
                <div class="status-item">
                    <div class="status-label">Componentes Activos</div>
                    <div class="status-value">{self.vecta_info['componentes_activos']}/{self.vecta_info['componentes_totales']}</div>
                </div>
            </div>
            
            <h3>✅ Componentes Principales</h3>
            <div class="status-grid">
                <div class="status-item" style="border-left-color: {'#00ff88' if self.vecta_info['componentes']['vecta_launcher.py'] else '#ff5555'}">
                    <div class="status-label">Lanzador Principal</div>
                    <div class="status-value">{'✓ Activo' if self.vecta_info['componentes']['vecta_launcher.py'] else '✗ No encontrado'}</div>
                </div>
                <div class="status-item" style="border-left-color: {'#00ff88' if self.vecta_info['componentes']['core/meta_vecta.py'] else '#ff5555'}">
                    <div class="status-label">Núcleo META-VECTA</div>
                    <div class="status-value">{'✓ Activo' if self.vecta_info['componentes']['core/meta_vecta.py'] else '✗ No encontrado'}</div>
                </div>
                <div class="status-item" style="border-left-color: {'#00ff88' if self.vecta_info['componentes']['dimensiones/vector_12d.py'] else '#ff5555'}">
                    <div class="status-label">Sistema Vectorial</div>
                    <div class="status-value">{'✓ Activo' if self.vecta_info['componentes']['dimensiones/vector_12d.py'] else '✗ No encontrado'}</div>
                </div>
                <div class="status-item" style="border-left-color: {'#00ff88' if self.vecta_info['componentes']['dimensiones/dimension_1.py'] else '#ff5555'}">
                    <div class="status-label">Dimensión 1</div>
                    <div class="status-value">{'✓ Activa' if self.vecta_info['componentes']['dimensiones/dimension_1.py'] else '✗ No encontrada'}</div>
                </div>
            </div>
        </div>
        
        <div class="card">
            <h2>🔄 ÚLTIMOS 3 CAMBIOS</h2>
            <div class="changes-list">
                {"".join(self._generate_change_html(change) for change in self.last_changes)}
                {self._get_no_changes_html()}
            </div>
            
            <div class="auto-refresh">
                ⏱️ Auto-refresh en 5 segundos | Cambios detectados en tiempo real
            </div>
        </div>
        
        <div class="card" style="grid-column: 1 / -1;">
            <h2>📁 ESTRUCTURA DE ARCHIVOS</h2>
            <p style="margin-bottom: 15px; color: #a0a0a0;">
                Directorio base: {self.base_dir} | Total items: {len(self.file_tree)}
            </p>
            <div class="file-tree">
                {"".join(self._generate_file_html(item) for item in self.file_tree)}
            </div>
        </div>
        
        <div class="footer">
            <p>VECTA 12D Dashboard v1.0 | Sistema de monitoreo en tiempo real</p>
            <p>Desarrollado para Rafael Porley | {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        </div>
    </div>
</body>
</html>'''
        
        return html
    
    def _generate_change_html(self, change):
        """Genera HTML para un cambio"""
        action_class = {
            "CREADO": "change-added",
            "MODIFICADO": "change-modified", 
            "ELIMINADO": "change-deleted"
        }.get(change["action"], "change-modified")
        
        action_icon = {
            "CREADO": "🆕",
            "MODIFICADO": "✏️",
            "ELIMINADO": "🗑️"
        }.get(change["action"], "✏️")
        
        return f'''
        <div class="change-item {action_class}">
            <div class="change-time">{change['timestamp']}</div>
            <div>
                <span class="change-action">{action_icon} {change['action']}</span>
                <span class="change-path">{change['path']}</span>
            </div>
        </div>'''
    
    def _get_no_changes_html(self):
        """HTML cuando no hay cambios"""
        if not self.last_changes:
            return '''
            <div class="change-item change-modified">
                <div class="change-time">Esperando cambios...</div>
                <div>
                    <span class="change-action">👀 Sin cambios recientes</span>
                    <span class="change-path">El sistema está monitoreando la carpeta</span>
                </div>
            </div>'''
        return ""
    
    def _generate_file_html(self, item):
        """Genera HTML para un archivo o directorio"""
        level_class = f"level-{min(item['level'], 10)}"
        
        if item["type"] == "directory":
            icon = "📁"
            file_class = "folder"
            details = f"({item['items']} items)"
        else:
            icon = self._get_file_icon(item["extension"])
            file_class = self._get_file_class(item["extension"])
            details = f"{item['size']} | {item['modified']}"
        
        return f'''
        <div class="file-item {level_class}">
            <span class="file-icon {file_class}">{icon}</span>
            <div style="flex: 1;">
                <div style="color: white; font-weight: 500;">{item['name']}</div>
                <div style="color: #888; font-size: 0.9em;">{details}</div>
            </div>
        </div>'''
    
    def _get_file_icon(self, extension):
        """Obtiene icono según extensión"""
        icons = {
            '.py': '🐍', '.json': '📊', '.txt': '📄', '.md': '📝',
            '.bat': '⚙️', '.html': '🌐', '.css': '🎨', '.js': '📜',
            '.png': '🖼️', '.jpg': '🖼️', '.ico': '🖼️', '.exe': '⚡'
        }
        return icons.get(extension, '📄')
    
    def _get_file_class(self, extension):
        """Obtiene clase CSS según extensión"""
        classes = {
            '.py': 'python', '.json': 'json', '.txt': 'txt', 
            '.md': 'txt', '.bat': 'bat', '.html': 'other',
            '.css': 'other', '.js': 'other', '.exe': 'other'
        }
        return classes.get(extension, 'other')
    
    def update_html(self):
        """Actualiza el archivo HTML"""
        html_content = self.generate_html()
        html_path = os.path.join(self.base_dir, "dashboard_vecta.html")
        
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        print(f"Dashboard actualizado: {html_path}")
    
    def start_monitoring(self):
        """Inicia el monitoreo de archivos"""
        event_handler = VECTAChangeHandler(self)
        self.observer = Observer()
        self.observer.schedule(event_handler, self.base_dir, recursive=True)
        self.observer.start()
        
        print(f"Monitoreo iniciado en: {self.base_dir}")
    
    def start_server(self):
        """Inicia el servidor web"""
        os.chdir(self.base_dir)
        
        class DashboardHandler(SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                    super().__init__(*args, directory=base_dir, **kwargs)
            
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
        
        # Abrir navegador automáticamente
        webbrowser.open(f"http://localhost:{self.port}")
    
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
        
        print("\n✅ DASHBOARD INICIADO CORRECTAMENTE")
        print("   - Monitoreando cambios en la carpeta")
        print("   - Servidor web en ejecución")
        print("   - Navegador abierto automáticamente")
        print("\n📝 COMANDOS:")
        print("   - Ctrl+C para detener el dashboard")
        print("   - Recarga la página para ver cambios")
        print("=" * 70)
        
        try:
            # Mantener el script ejecutándose
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Deteniendo dashboard...")
            if self.observer:
                self.observer.stop()
                self.observer.join()
            if self.server:
                self.server.shutdown()
            print("✅ Dashboard detenido correctamente")

def main():
    """Función principal"""
    # Configuración
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    PORT = 8080
    
    # Verificar dependencias
    try:
        from watchdog.observers import Observer
    except ImportError:
        print("❌ Error: watchdog no está instalado")
        print("Instala con: pip install watchdog")
        return
    
    # Crear y ejecutar dashboard
    dashboard = VECTADashboard(BASE_DIR, PORT)
    dashboard.run()

if __name__ == "__main__":
    main()