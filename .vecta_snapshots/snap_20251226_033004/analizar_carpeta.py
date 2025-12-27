import os
import json
import sys
from pathlib import Path
from datetime import datetime

def analizar_carpeta(ruta_carpeta, max_contenido_chars=5000):
    """
    Analiza una carpeta y genera un reporte estructurado
    """
    ruta = Path(ruta_carpeta)
    
    if not ruta.exists():
        return {"error": f"La carpeta no existe: {ruta_carpeta}"}
    
    if not ruta.is_dir():
        return {"error": f"La ruta no es una carpeta: {ruta_carpeta}"}
    
    reporte = {
        "fecha_analisis": datetime.now().isoformat(),
        "ruta_carpeta": str(ruta.absolute()),
        "estructura": {},
        "estadisticas": {
            "total_archivos": 0,
            "total_carpetas": 0,
            "tamano_total_bytes": 0,
            "extensiones": {}
        },
        "contenidos_importantes": {}
    }
    
    # Función recursiva para analizar
    def analizar_recursivo(directorio, nivel_max=3, nivel_actual=0):
        if nivel_actual >= nivel_max:
            return {"_profundidad_maxima": f"Profundidad máxima ({nivel_max}) alcanzada"}
        
        estructura = {}
        
        try:
            items = list(directorio.iterdir())
            for item in sorted(items, key=lambda x: (not x.is_dir(), x.name.lower())):
                nombre = item.name
                
                if item.is_dir():
                    reporte["estadisticas"]["total_carpetas"] += 1
                    estructura[nombre] = {
                        "tipo": "carpeta",
                        "ruta": str(item.relative_to(ruta)),
                        "contenido": analizar_recursivo(item, nivel_max, nivel_actual + 1)
                    }
                else:
                    reporte["estadisticas"]["total_archivos"] += 1
                    
                    # Obtener extensión
                    ext = item.suffix.lower() if item.suffix else "sin_extension"
                    reporte["estadisticas"]["extensiones"][ext] = reporte["estadisticas"]["extensiones"].get(ext, 0) + 1
                    
                    # Obtener tamaño
                    tamano = item.stat().st_size
                    reporte["estadisticas"]["tamano_total_bytes"] += tamano
                    
                    # Leer contenido de archivos de texto pequeños
                    contenido = ""
                    if tamano < 100000:  # Archivos menores a 100KB
                        try:
                            if ext in ['.txt', '.py', '.js', '.json', '.xml', '.html', '.css', '.md', '.csv', '.log', '.ps1', '.bat', '.cmd', '.ini', '.config', '.inf', '.cfg']:
                                with open(item, 'r', encoding='utf-8', errors='ignore') as f:
                                    contenido_preview = f.read(5000)
                                    if contenido_preview.strip():
                                        contenido = contenido_preview
                        except:
                            contenido = "[No se pudo leer el contenido]"
                    
                    estructura[nombre] = {
                        "tipo": "archivo",
                        "extension": ext,
                        "tamano_bytes": tamano,
                        "tamano_humano": f"{tamano / 1024:.2f} KB" if tamano < 1024*1024 else f"{tamano / (1024*1024):.2f} MB",
                        "ruta": str(item.relative_to(ruta)),
                        "contenido_preview": contenido if contenido else None
                    }
                    
        except PermissionError:
            estructura["_error"] = "Permiso denegado"
        except Exception as e:
            estructura["_error"] = str(e)
        
        return estructura
    
    # Analizar la carpeta principal
    reporte["estructura"] = analizar_recursivo(ruta)
    
    return reporte

def generar_reporte_html(reporte, archivo_salida="reporte_carpeta.html"):
    """Genera un reporte HTML legible"""
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Reporte de Carpeta: {reporte['ruta_carpeta']}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .seccion {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; }}
            .archivo {{ margin: 5px 0; padding: 5px; background: #f5f5f5; }}
            .carpeta {{ margin: 10px 0; padding: 10px; background: #e8f4fc; }}
            .contenido {{ background: #fff8dc; padding: 10px; margin: 5px 0; font-family: monospace; }}
            .estadisticas {{ background: #f0f0f0; padding: 15px; }}
        </style>
    </head>
    <body>
        <h1>📁 Reporte de Carpeta</h1>
        <div class="seccion">
            <h2>📊 Información General</h2>
            <p><strong>Ruta:</strong> {reporte['ruta_carpeta']}</p>
            <p><strong>Fecha de análisis:</strong> {reporte['fecha_analisis']}</p>
        </div>
        
        <div class="seccion estadisticas">
            <h2>📈 Estadísticas</h2>
            <p>📂 Carpetas: {reporte['estadisticas']['total_carpetas']}</p>
            <p>📄 Archivos: {reporte['estadisticas']['total_archivos']}</p>
            <p>💾 Tamaño total: {reporte['estadisticas']['tamano_total_bytes'] / (1024*1024):.2f} MB</p>
            
            <h3>Extensiones de archivo:</h3>
            <ul>
    """
    
    for ext, count in reporte['estadisticas']['extensiones'].items():
        html += f"<li>{ext}: {count} archivos</li>"
    
    html += """
            </ul>
        </div>
        
        <div class="seccion">
            <h2>🌳 Estructura de Carpetas</h2>
    """
    
    def generar_html_estructura(estructura, nivel=0):
        html = ""
        for nombre, info in estructura.items():
            if nombre.startswith('_'):
                continue
                
            if info['tipo'] == 'carpeta':
                html += f'<div class="carpeta" style="margin-left: {nivel * 20}px;">'
                html += f'<strong>📁 {nombre}/</strong>'
                if 'contenido' in info:
                    html += generar_html_estructura(info['contenido'], nivel + 1)
                html += '</div>'
            else:
                html += f'<div class="archivo" style="margin-left: {nivel * 20}px;">'
                html += f'📄 <strong>{nombre}</strong> ({info["tamano_humano"]})'
                if info.get('contenido_preview'):
                    html += f'<div class="contenido"><strong>Contenido (preview):</strong><br>{info["contenido_preview"]}</div>'
                html += '</div>'
        return html
    
    html += generar_html_estructura(reporte['estructura'])
    html += """
        </div>
    </body>
    </html>
    """
    
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return archivo_salida

if __name__ == "__main__":
    # Preguntar al usuario por la carpeta a analizar
    if len(sys.argv) > 1:
        carpeta = sys.argv[1]
    else:
        # Si no se proporciona argumento, usar la carpeta actual
        carpeta = os.getcwd()
        print(f"⚠️  No se proporcionó carpeta. Usando carpeta actual: {carpeta}")
        respuesta = input("¿Continuar? (s/n): ").lower()
        if respuesta != 's':
            sys.exit(0)
    
    print(f"🔍 Analizando carpeta: {carpeta}")
    
    # Analizar la carpeta
    reporte = analizar_carpeta(carpeta)
    
    if "error" in reporte:
        print(f"❌ Error: {reporte['error']}")
        input("Presiona Enter para salir...")
        sys.exit(1)
    
    # Guardar reporte en JSON
    json_file = "reporte_carpeta.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(reporte, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Reporte JSON guardado como '{json_file}'")
    
    # Generar reporte HTML
    try:
        html_file = generar_reporte_html(reporte)
        print(f"📊 Reporte HTML guardado como '{html_file}'")
    except Exception as e:
        print(f"⚠️  No se pudo generar HTML: {e}")
    
    # Mostrar resumen en consola
    print("\n" + "="*50)
    print("📋 RESUMEN DEL ANÁLISIS")
    print("="*50)
    print(f"📂 Ruta analizada: {reporte['ruta_carpeta']}")
    print(f"📊 Total carpetas: {reporte['estadisticas']['total_carpetas']}")
    print(f"📄 Total archivos: {reporte['estadisticas']['total_archivos']}")
    print(f"💾 Tamaño total: {reporte['estadisticas']['tamano_total_bytes'] / (1024*1024):.2f} MB")
    print("\n📈 Extensiones encontradas:")
    for ext, count in sorted(reporte['estadisticas']['extensiones'].items()):
        print(f"  {ext}: {count}")
    
    print("\n" + "="*50)
    print("📁 Para compartir conmigo:")
    print(f"1. Copia el contenido de '{json_file}'")
    print("2. O pégalo aquí directamente")
    print("="*50)
    
    # Mostrar vista previa del JSON
    preview = input("\n¿Mostrar vista previa del JSON? (s/n): ").lower()
    if preview == 's':
        print("\n" + "="*50)
        print("VISTA PREVIA DEL JSON (primeros 2000 caracteres):")
        print("="*50)
        with open(json_file, 'r', encoding='utf-8') as f:
            contenido = f.read(2000)
            print(contenido)
            if len(contenido) == 2000:
                print("... [continúa en el archivo]")
    
    input("\nPresiona Enter para terminar...")