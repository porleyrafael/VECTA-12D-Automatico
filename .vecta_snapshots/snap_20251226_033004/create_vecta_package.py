"""
Crea el paquete .pkg con todos los archivos de VECTA 12D
Versión simplificada para evitar errores de sintaxis
"""
import os
import zipfile
import json

def create_pkg_file(output_file="paquete_vecta.pkg"):
    """Crea el archivo .pkg con todos los archivos"""
    
    # Archivos esenciales para VECTA 12D
    package_files = {
        # Archivos raíz
        "README.txt": "VECTA 12D - Sistema Autoprogramable de 12 Dimensiones\n\nInstalación: Ejecuta INSTALAR.bat como administrador\nUso: Haz doble clic en VECTA 12D del escritorio",
        
        "LICENSE.txt": "LICENCIA VECTA 12D - Software libre para uso personal",
        
        "config.json": json.dumps({
            "version": "12D.1.0.0",
            "dimensions": 12,
            "auto_update": True
        }, indent=2),
        
        # Core del sistema
        "core/__init__.py": "# Paquete core de VECTA 12D\n",
        
        "core/vecta_12d_core.py": '''# vecta_12d_core.py - Núcleo principal
import sys
import os

class VECTA_12D_Core:
    def __init__(self):
        self.mode = "local"
    
    def process(self, input_text):
        return f"VECTA 12D: Procesando '{input_text}' en modo {self.mode}"
    
    def start_gui(self):
        try:
            from interfaz.vecta_gui_secure import VECTA_GUI
            import tkinter as tk
            root = tk.Tk()
            app = VECTA_GUI(root)
            root.mainloop()
        except:
            print("GUI no disponible, usando consola")
            self._start_console()
    
    def _start_console(self):
        print("Modo consola 12D activado")
        while True:
            cmd = input("12D> ")
            if cmd.lower() in ['exit', 'quit', 'salir']:
                break
            print(self.process(cmd))''',
        
        # Interfaz gráfica básica
        "interfaz/__init__.py": "# Interfaz de usuario\n",
        
        "interfaz/vecta_gui_secure.py": '''# vecta_gui_secure.py - GUI principal
import tkinter as tk
from tkinter import ttk, scrolledtext

class VECTA_GUI:
    def __init__(self, root):
        self.root = root
        self.setup_gui()
    
    def setup_gui(self):
        self.root.title("VECTA 12D")
        self.root.geometry("800x600")
        
        # Área de chat
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD)
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Entrada
        self.input_frame = ttk.Frame(self.root)
        self.input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.input_var = tk.StringVar()
        self.input_entry = ttk.Entry(self.input_frame, textvariable=self.input_var)
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        self.send_btn = ttk.Button(self.input_frame, text="Enviar", command=self.send_message)
        self.send_btn.pack(side=tk.RIGHT)
        
        self.input_entry.bind("<Return>", lambda e: self.send_message())
        
        self.text_area.insert(tk.END, "🌀 VECTA 12D iniciado\\n")
        self.text_area.insert(tk.END, "Escribe 'hola' para comenzar\\n\\n")
    
    def send_message(self):
        message = self.input_var.get()
        if message:
            self.text_area.insert(tk.END, f"Tú: {message}\\n")
            self.input_var.set("")
            
            # Procesar mensaje
            if message.lower() == 'hola':
                response = "¡Hola! Soy VECTA 12D, tu sistema autoprogramable"
            elif '12d' in message.lower():
                response = "Sistema de 12 Dimensiones Vectoriales activo"
            else:
                response = f"Procesando: {message}"
            
            self.text_area.insert(tk.END, f"VECTA: {response}\\n\\n")
            self.text_area.see(tk.END)

def main():
    root = tk.Tk()
    app = VECTA_GUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()''',
        
        # Dimensiones básicas
        "dimensiones/__init__.py": "# Paquete de dimensiones 12D\n",
        
        "dimensiones/d1_temporal.py": "# Dimensión 1: Temporal\\nclass TemporalDimension:\\n    def process(self, data):\\n        return {'dimension': 1}",
        
        "dimensiones/d2_espacial.py": "# Dimensión 2: Espacial\\nclass SpatialDimension:\\n    def process(self, data):\\n        return {'dimension': 2}",
        
        # Scripts
        "scripts/__init__.py": "# Scripts auxiliares\n",
        
        "scripts/initial_setup.py": '''# initial_setup.py
import json
import os

def run_setup():
    print("Configuración inicial VECTA 12D")
    os.makedirs("data", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    config = {"setup_complete": True}
    with open("data/setup.json", 'w') as f:
        json.dump(config, f, indent=2)
    
    print("✅ Configuración completada")

if __name__ == "__main__":
    run_setup()''',
        
        # Datos básicos
        "data/local_knowledge.json": json.dumps({
            "greetings": ["Hola", "Buenos días", "¿Cómo estás?"]
        }, indent=2),
    }
    
    # Crear archivo ZIP
    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for filepath, content in package_files.items():
            zipf.writestr(filepath, content)
    
    size_mb = os.path.getsize(output_file) / 1024 / 1024
    print(f"✅ Paquete creado: {output_file}")
    print(f"📦 Tamaño: {size_mb:.2f} MB")
    print(f"📁 Archivos incluidos: {len(package_files)}")
    print(f"📍 Ubicación: {os.path.abspath(output_file)}")

if __name__ == "__main__":
    create_pkg_file()