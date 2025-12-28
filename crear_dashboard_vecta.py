#!/usr/bin/env python3
"""
DASHBOARD VECTA 12D - CORREGIDO
Dashboard en tiempo real para monitorear las 12 dimensiones
"""

import http.server
import socketserver
import json
import os
import time
import webbrowser
import threading
from pathlib import Path
from datetime import datetime

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

BASE_DIR = Path(__file__).parent
DASHBOARD_HTML = BASE_DIR / "dashboard_vecta.html"

print("="*70)
print("INICIANDO DASHBOARD VECTA 12D EN TIEMPO REAL")
print("="*70)

# ============================================================================
# GENERAR DATOS DE LAS 12 DIMENSIONES
# ============================================================================

def cargar_dimensiones():
    """Carga información de las 12 dimensiones"""
    
    dimensiones = []
    
    # Nombres y descripciones filosóficas
    info_dimensiones = [
        {"id": 1, "nombre": "Intencionalidad", "color": "#4ECDC4", "completado": True},
        {"id": 2, "nombre": "Lógica", "color": "#FF6B6B", "completado": True},
        {"id": 3, "nombre": "Contexto", "color": "#45B7D1", "completado": True},
        {"id": 4, "nombre": "Temporalidad", "color": "#96CEB4", "completado": False},
        {"id": 5, "nombre": "Emergencia", "color": "#FFEAA7", "completado": False},
        {"id": 6, "nombre": "Recursividad", "color": "#DDA0DD", "completado": False},
        {"id": 7, "nombre": "Holismo", "color": "#98D8C8", "completado": False},
        {"id": 8, "nombre": "Singularidad", "color": "#F7DC6F", "completado": False},
        {"id": 9, "nombre": "Meta-cognición", "color": "#BB8FCE", "completado": False},
        {"id": 10, "nombre": "Transcendencia", "color": "#85C1E9", "completado": False},
        {"id": 11, "nombre": "Universalidad", "color": "#F8C471", "completado": False},
        {"id": 12, "nombre": "Autonomía", "color": "#82E0AA", "completado": False}
    ]
    
    # Verificar qué dimensiones realmente existen como archivos
    for dim in info_dimensiones:
        archivo_dim = BASE_DIR / "dimensiones" / f"{dim['nombre'].lower()}.py"
        dim["archivo_existe"] = archivo_dim.exists()
        
        # Si el archivo existe, intentar cargar más info
        if archivo_dim.exists():
            try:
                # Leer primeras líneas para ver si tiene contenido
                with open(archivo_dim, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                    lineas = len(contenido.split('\n'))
                    dim["lineas_codigo"] = lineas
                    dim["implementado"] = lineas > 50  # Si tiene más de 50 líneas, asumimos implementado
            except:
                dim["lineas_codigo"] = 0
                dim["implementado"] = False
        else:
            dim["lineas_codigo"] = 0
            dim["implementado"] = False
        
        dimensiones.append(dim)
    
    return dimensiones

def generar_datos_estado():
    """Genera datos actualizados del estado del sistema"""
    
    dimensiones = cargar_dimensiones()
    
    # Contar dimensiones completas vs pendientes
    completadas = sum(1 for d in dimensiones if d.get("implementado", False) or d.get("completado", False))
    total = len(dimensiones)
    
    # Calcular métricas
    porcentaje = (completadas / total) * 100 if total > 0 else 0
    
    # Obtener última actualización
    logs_dir = BASE_DIR / "logs"
    ultima_actualizacion = "Nunca"
    
    if logs_dir.exists():
        archivos_log = list(logs_dir.glob("*.json"))
        if archivos_log:
            # Tomar el archivo más reciente
            archivo_reciente = max(archivos_log, key=os.path.getctime)
            ultima_actualizacion = time.strftime('%Y-%m-%d %H:%M', 
                                                time.localtime(os.path.getctime(archivo_reciente)))
    
    # Estructura de datos para el dashboard
    datos = {
        "sistema": "VECTA 12D",
        "version": "2.0",
        "fecha_actualizacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "estado": "operativo" if completadas > 0 else "inactivo",
        "dimensiones": {
            "total": total,
            "completadas": completadas,
            "pendientes": total - completadas,
            "porcentaje": round(porcentaje, 1),
            "lista": dimensiones
        },
        "archivos": {
            "dimensiones_encontradas": len(list((BASE_DIR / "dimensiones").glob("*.py"))),
            "dashboard_activo": True,
            "ultima_actualizacion": ultima_actualizacion
        },
        "proxima_accion": "Completar dimensión 4: Temporalidad" if completadas < 12 else "Sistema completo"
    }
    
    return datos

# ============================================================================
# GENERAR HTML DEL DASHBOARD
# ============================================================================

def generar_html_dashboard(datos):
    """Genera el HTML del dashboard con los datos actualizados"""
    
    html = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VECTA 12D Dashboard</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        
        body {{
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            color: white;
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 40px;
            padding: 20px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
        
        .titulo {{
            font-size: 2.8em;
            background: linear-gradient(90deg, #4ECDC4, #FF6B6B);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            margin-bottom: 10px;
        }}
        
        .subtitulo {{
            color: #aaa;
            font-size: 1.2em;
        }}
        
        .estado-general {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        
        .tarjeta {{
            background: rgba(255, 255, 255, 0.07);
            padding: 25px;
            border-radius: 12px;
            border-left: 5px solid;
            transition: transform 0.3s, background 0.3s;
        }}
        
        .tarjeta:hover {{
            transform: translateY(-5px);
            background: rgba(255, 255, 255, 0.1);
        }}
        
        .tarjeta h3 {{
            font-size: 1.3em;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .valor {{
            font-size: 2.5em;
            font-weight: bold;
            margin: 10px 0;
        }}
        
        .progreso {{
            height: 8px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 4px;
            margin: 15px 0;
            overflow: hidden;
        }}
        
        .barra-progreso {{
            height: 100%;
            background: linear-gradient(90deg, #4ECDC4, #45B7D1);
            border-radius: 4px;
            transition: width 1s ease;
        }}
        
        .dimensiones-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }}
        
        .dimension-card {{
            background: rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s;
        }}
        
        .dimension-card:hover {{
            border-color: rgba(255, 255, 255, 0.3);
            background: rgba(255, 255, 255, 0.08);
        }}
        
        .dimension-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}
        
        .dimension-num {{
            background: rgba(255, 255, 255, 0.1);
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 1.2em;
        }}
        
        .dimension-estado {{
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: bold;
        }}
        
        .estado-completado {{
            background: rgba(78, 205, 196, 0.2);
            color: #4ECDC4;
        }}
        
        .estado-pendiente {{
            background: rgba(255, 107, 107, 0.2);
            color: #FF6B6B;
        }}
        
        .dimension-nombre {{
            font-size: 1.4em;
            margin: 10px 0;
        }}
        
        .dimension-desc {{
            color: #aaa;
            font-size: 0.9em;
            line-height: 1.5;
            margin-bottom: 15px;
        }}
        
        .dimension-metricas {{
            display: flex;
            justify-content: space-between;
            font-size: 0.85em;
            color: #888;
            margin-top: 10px;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 50px;
            padding: 20px;
            color: #666;
            font-size: 0.9em;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }}
        
        .actualizar-btn {{
            background: linear-gradient(90deg, #4ECDC4, #45B7D1);
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 8px;
            font-size: 1em;
            cursor: pointer;
            margin: 20px 0;
            transition: transform 0.2s;
        }}
        
        .actualizar-btn:hover {{
            transform: scale(1.05);
        }}
        
        .conexion-ia {{
            background: rgba(255, 107, 107, 0.1);
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
            border-left: 4px solid #FF6B6B;
        }}
        
        .timestamp {{
            color: #888;
            font-size: 0.8em;
            margin-top: 5px;
        }}
        
        @media (max-width: 768px) {{
            .dimensiones-grid {{
                grid-template-columns: 1fr;
            }}
            
            .estado-general {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 class="titulo">VECTA 12D DASHBOARD</h1>
            <p class="subtitulo">Sistema filosófico de 12 dimensiones vectoriales autoprogramables</p>
            <p class="timestamp">Actualizado: {datos['fecha_actualizacion']}</p>
        </div>
        
        <div class="estado-general">
            <div class="tarjeta" style="border-left-color: #4ECDC4;">
                <h3>📊 Progreso Total</h3>
                <div class="valor">{datos['dimensiones']['completadas']}/12</div>
                <div class="progreso">
                    <div class="barra-progreso" style="width: {datos['dimensiones']['porcentaje']}%"></div>
                </div>
                <p>{datos['dimensiones']['porcentaje']}% completado</p>
            </div>
            
            <div class="tarjeta" style="border-left-color: #FF6B6B;">
                <h3>🚀 Estado Sistema</h3>
                <div class="valor" style="color: {'#4ECDC4' if datos['estado'] == 'operativo' else '#FF6B6B'}">
                    {datos['estado'].upper()}
                </div>
                <p>{datos['dimensiones']['pendientes']} dimensiones pendientes</p>
            </div>
            
            <div class="tarjeta" style="border-left-color: #45B7D1;">
                <h3>📁 Archivos</h3>
                <div class="valor">{datos['archivos']['dimensiones_encontradas']}</div>
                <p>Dimensiones detectadas en código</p>
                <p class="timestamp">Última actualización: {datos['archivos']['ultima_actualizacion']}</p>
            </div>
        </div>
        
        <div class="conexion-ia">
            <h3>🤖 CONEXIÓN IA MENTOR ACTIVA</h3>
            <p>Próxima acción sugerida: <strong>{datos['proxima_accion']}</strong></p>
            <p class="timestamp">Usa mentor_ia_real.py para recibir sugerencias de mejora</p>
        </div>
        
        <button class="actualizar-btn" onclick="location.reload()">🔄 Actualizar Dashboard</button>
        
        <h2 style="margin: 40px 0 20px 0; color: #4ECDC4;">🎯 LAS 12 DIMENSIONES</h2>
        
        <div class="dimensiones-grid">
'''
    
    # Añadir tarjetas para cada dimensión
    for dim in datos['dimensiones']['lista']:
        estado = "COMPLETADA" if dim.get("implementado", False) or dim.get("completado", False) else "EN DESARROLLO"
        clase_estado = "estado-completado" if estado == "COMPLETADA" else "estado-pendiente"
        lineas = dim.get("lineas_codigo", 0)
        archivo_existe = "✅" if dim.get("archivo_existe", False) else "⏳"
        
        html += f'''
            <div class="dimension-card">
                <div class="dimension-header">
                    <div class="dimension-num" style="border: 2px solid {dim['color']};">{dim['id']}</div>
                    <div class="dimension-estado {clase_estado}">{estado}</div>
                </div>
                <h3 class="dimension-nombre">{dim['nombre']}</h3>
                <p class="dimension-desc">
                    Dimensión {dim['id']} del sistema VECTA 12D.
                    {"Implementada y funcionando." if estado == "COMPLETADA" else "En desarrollo. Pendiente de implementación completa."}
                </p>
                <div class="dimension-metricas">
                    <span>Archivo: {archivo_existe}</span>
                    <span>Líneas: {lineas}</span>
                    <span style="color: {dim['color']}">●</span>
                </div>
            </div>
'''
    
    html += f'''
        </div>
        
        <div class="footer">
            <p>VECTA 12D • Sistema de autoprogramación filosófica</p>
            <p>Dashboard generado automáticamente • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>Ejecutar: <code>python mentor_ia_real.py</code> para recibir sugerencias de IA</p>
        </div>
    </div>
    
    <script>
        // Actualizar automáticamente cada 30 segundos
        setTimeout(() => {{
            location.reload();
        }}, 30000);
        
        // Efectos de carga
        document.addEventListener('DOMContentLoaded', function() {{
            const cards = document.querySelectorAll('.dimension-card');
            cards.forEach((card, index) => {{
                card.style.opacity = '0';
                card.style.transform = 'translateY(20px)';
                
                setTimeout(() => {{
                    card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
                    card.style.opacity = '1';
                    card.style.transform = 'translateY(0)';
                }}, 100 * index);
            }});
        }});
    </script>
</body>
</html>
'''
    
    return html

def actualizar_dashboard():
    """Actualiza el archivo HTML del dashboard"""
    datos = generar_datos_estado()
    html = generar_html_dashboard(datos)
    
    with open(DASHBOARD_HTML, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"Dashboard actualizado: {DASHBOARD_HTML}")
    print(f"  • Dimensiones: {datos['dimensiones']['completadas']}/12 completadas")
    print(f"  • Progreso: {datos['dimensiones']['porcentaje']}%")
    print(f"  • Estado: {datos['estado']}")
    
    return datos

# ============================================================================
# SERVIDOR WEB
# ============================================================================

PORT = 8080

class VECTAHandler(http.server.SimpleHTTPRequestHandler):
    """Manejador personalizado para el servidor web"""
    
    def __init__(self, *args, **kwargs):
        # Asegurarse de que BASE_DIR esté definido
        super().__init__(*args, directory=str(BASE_DIR), **kwargs)
    
    def log_message(self, format, *args):
        """Silenciar logs normales"""
        pass
    
    def do_GET(self):
        """Manejar solicitudes GET"""
        if self.path == '/':
            # Actualizar dashboard y servir HTML
            actualizar_dashboard()
            self.path = '/dashboard_vecta.html'
        
        elif self.path == '/api/estado':
            # Endpoint API para estado JSON
            datos = generar_datos_estado()
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(datos, indent=2).encode())
            return
        
        elif self.path == '/api/actualizar':
            # Forzar actualización
            datos = actualizar_dashboard()
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "updated", "data": datos}, indent=2).encode())
            return
        
        # Servir archivos estáticos
        return super().do_GET()

# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def iniciar_dashboard():
    """Inicia el servidor web del dashboard"""
    
    # Actualizar dashboard por primera vez
    print("\n" + "="*70)
    print("GENERANDO DASHBOARD CON 12 DIMENSIONES...")
    print("="*70)
    
    datos = actualizar_dashboard()
    
    # Abrir navegador automáticamente
    try:
        webbrowser.open(f'http://localhost:{PORT}')
        print(f"✅ Navegador abierto en: http://localhost:{PORT}")
    except:
        print(f"⚠️  Abre manualmente: http://localhost:{PORT}")
    
    # Iniciar servidor
    with socketserver.TCPServer(("", PORT), VECTAHandler) as httpd:
        print(f"✅ Servidor iniciado en: http://localhost:{PORT}")
        print(f"📊 Dashboard disponible en: http://localhost:{PORT}/")
        print("\n" + "="*70)
        print("✅ DASHBOARD INICIADO CORRECTAMENTE")
        print("   - Monitoreando 12 dimensiones en tiempo real")
        print("   - Servidor web en ejecución")
        print(f"   - Progreso actual: {datos['dimensiones']['completadas']}/12 dimensiones")
        print("\n📝 COMANDOS:")
        print("   - Ctrl+C para detener el dashboard")
        print("   - Recarga la página para ver cambios")
        print("   - Visita http://localhost:{PORT}/api/estado para datos JSON")
        print("="*70)
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n⚠️  Dashboard detenido por el usuario")
            print("👋 Hasta pronto, VECTA seguirá evolucionando...")

# ============================================================================
# EJECUCIÓN
# ============================================================================

if __name__ == "__main__":
    iniciar_dashboard()