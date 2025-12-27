"""
VECTA 12D - GENERADOR DE REPORTES COMPLETOS
Crea reportes detallados para compartir en otros chats
"""

import os
import json
import datetime
from pathlib import Path

def generar_reporte_completo():
    """Genera un reporte completo del sistema VECTA"""
    
    base_dir = Path.cwd()
    reporte = []
    
    # Encabezado
    reporte.append("VECTA 12D - REPORTE COMPLETO DEL SISTEMA")
    reporte.append("=" * 60)
    reporte.append(f"Fecha: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    reporte.append(f"Directorio: {base_dir}")
    reporte.append("=" * 60)
    reporte.append("")
    
    # 1. ESTRUCTURA DEL PROYECTO
    reporte.append("1. ESTRUCTURA DEL PROYECTO:")
    reporte.append("-" * 40)
    
    estructura = []
    for item in base_dir.rglob("*"):
        if ".vecta_snapshots" in str(item):
            continue
            
        rel_path = str(item.relative_to(base_dir))
        if item.is_file():
            size = item.stat().st_size
            ext = item.suffix.lower()
            if ext in ['.py', '.json', '.txt', '.md', '.bat', '.pkg']:
                estructura.append(f"📄 {rel_path} ({size} bytes)")
        elif item.is_dir():
            estructura.append(f"📁 {rel_path}/")
    
    # Ordenar y limitar a 50 elementos
    estructura.sort()
    for item in estructura[:50]:
        reporte.append(item)
    
    if len(estructura) > 50:
        reporte.append(f"... y {len(estructura) - 50} más")
    
    reporte.append("")
    
    # 2. ARCHIVOS PRINCIPALES Y SU CONTENIDO
    reporte.append("2. CONTENIDO DE ARCHIVOS PRINCIPALES:")
    reporte.append("-" * 40)
    
    archivos_importantes = [
        "vecta_launcher.py",
        "core/vecta_12d_core.py",
        "core/meta_vecta.py",
        "dimensiones/vector_12d.py",
        "core/config_manager.py"
    ]
    
    for archivo in archivos_importantes:
        ruta = base_dir / archivo
        if ruta.exists():
            reporte.append(f"\n--- {archivo} ---")
            try:
                with open(ruta, 'r', encoding='utf-8') as f:
                    contenido = f.read(2000)  # Primeros 2000 caracteres
                    reporte.append(contenido)
                    if len(contenido) == 2000:
                        reporte.append("[... el archivo continúa ...]")
            except:
                reporte.append("[No se pudo leer el contenido]")
        else:
            reporte.append(f"\n--- {archivo} (NO ENCONTRADO) ---")
    
    reporte.append("")
    
    # 3. DIMENSIONES DISPONIBLES
    reporte.append("3. DIMENSIONES DEL SISTEMA:")
    reporte.append("-" * 40)
    
    dimensiones_encontradas = 0
    for i in range(1, 13):
        dim_file = base_dir / f"dimensiones/dimension_{i}.py"
        if dim_file.exists():
            dimensiones_encontradas += 1
            try:
                with open(dim_file, 'r', encoding='utf-8') as f:
                    primera_linea = f.readline().strip()
                    reporte.append(f"Dimensión {i}: {primera_linea}")
            except:
                reporte.append(f"Dimensión {i}: Existe")
        else:
            reporte.append(f"Dimensión {i}: FALTANTE")
    
    reporte.append(f"\nTotal dimensiones: {dimensiones_encontradas}/12")
    reporte.append("")
    
    # 4. SISTEMA DE SNAPSHOTS
    reporte.append("4. SISTEMA DE SNAPSHOTS:")
    reporte.append("-" * 40)
    
    snapshots_dir = base_dir / ".vecta_snapshots"
    if snapshots_dir.exists():
        snapshots = list(snapshots_dir.glob("snap_*"))
        reporte.append(f"Snapshots disponibles: {len(snapshots)}")
        for snap in sorted(snapshots)[-5:]:  # Últimos 5
            reporte.append(f"- {snap.name}")
            
            # Leer metadata si existe
            metadata_file = snap / "metadata.json"
            if metadata_file.exists():
                try:
                    with open(metadata_file, 'r') as f:
                        metadata = json.load(f)
                        reporte.append(f"  Razón: {metadata.get('reason', 'N/A')}")
                        reporte.append(f"  Fecha: {metadata.get('created', 'N/A')}")
                except:
                    pass
    else:
        reporte.append("No hay sistema de snapshots activo")
    
    reporte.append("")
    
    # 5. ESTADO DEL SISTEMA
    reporte.append("5. ESTADO GENERAL:")
    reporte.append("-" * 40)
    
    # Contar archivos por tipo
    contador = {
        '.py': 0,
        '.json': 0,
        '.txt': 0,
        '.md': 0,
        '.bat': 0
    }
    
    for ext in contador.keys():
        contador[ext] = len(list(base_dir.rglob(f"*{ext}")))
    
    reporte.append("Archivos por tipo:")
    for ext, count in contador.items():
        if count > 0:
            reporte.append(f"- {ext}: {count}")
    
    # Verificar componentes críticos
    reporte.append("\nComponentes críticos:")
    criticos = {
        "Lanzador principal": base_dir / "vecta_launcher.py",
        "Núcleo VECTA 12D": base_dir / "core/vecta_12d_core.py",
        "META-VECTA": base_dir / "core/meta_vecta.py",
        "Sistema vectorial": base_dir / "dimensiones/vector_12d.py",
        "Instalador": base_dir / "INSTALAR.bat"
    }
    
    for nombre, ruta in criticos.items():
        if ruta.exists():
            size_kb = ruta.stat().st_size / 1024
            reporte.append(f"✅ {nombre}: {size_kb:.1f} KB")
        else:
            reporte.append(f"❌ {nombre}: NO ENCONTRADO")
    
    reporte.append("")
    
    # 6. INSTRUCCIONES
    reporte.append("6. INSTRUCCIONES PARA EL ASISTENTE:")
    reporte.append("-" * 40)
    reporte.append("Este es el sistema VECTA 12D creado por Rafael Porley.")
    reporte.append("Es un sistema de 12 dimensiones vectoriales con núcleo META-VECTA.")
    reporte.append("")
    reporte.append("Para continuar el trabajo:")
    reporte.append("1. Revisar la estructura del proyecto")
    reporte.append("2. Verificar que todas las dimensiones estén presentes")
    reporte.append("3. Probar el lanzador principal: python vecta_launcher.py")
    reporte.append("4. Si hay errores, revisar los archivos de log")
    reporte.append("")
    reporte.append("ARCHIVOS IMPORTANTES A REVISAR:")
    reporte.append("- vecta_launcher.py: Punto de entrada")
    reporte.append("- core/meta_vecta.py: Núcleo filosófico")
    reporte.append("- dimensiones/vector_12d.py: Sistema vectorial")
    reporte.append("- INSTALAR.bat: Instalador Windows")
    
    # 7. PROBLEMAS COMUNES
    reporte.append("")
    reporte.append("7. PROBLEMAS COMUNES:")
    reporte.append("-" * 40)
    
    problemas = []
    
    # Verificar dimensiones faltantes
    if dimensiones_encontradas < 12:
        problemas.append(f"Faltan {12 - dimensiones_encontradas} dimensiones")
    
    # Verificar archivos .pyc
    pyc_files = list(base_dir.rglob("*.pyc"))
    if pyc_files:
        problemas.append(f"Hay {len(pyc_files)} archivos .pyc (pueden eliminarse)")
    
    if problemas:
        for prob in problemas:
            reporte.append(f"• {prob}")
    else:
        reporte.append("No se detectaron problemas comunes")
    
    reporte.append("")
    reporte.append("=" * 60)
    reporte.append("FIN DEL REPORTE")
    reporte.append("Para más detalles, revisar los archivos individuales.")
    reporte.append("=" * 60)
    
    return "\n".join(reporte)

def guardar_y_mostrar_reporte():
    """Guarda el reporte y muestra cómo copiarlo"""
    
    reporte = generar_reporte_completo()
    
    # Guardar en archivo
    nombre_archivo = f"reporte_vecta_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(nombre_archivo, 'w', encoding='utf-8') as f:
        f.write(reporte)
    
    print(f"✅ Reporte guardado como: {nombre_archivo}")
    print("\n" + "="*60)
    print("📋 PARA COPIAR Y PEGAR EN OTRO CHAT:")
    print("="*60)
    
    # Mostrar las primeras 50 líneas como preview
    lineas = reporte.split('\n')
    for i, linea in enumerate(lineas[:50]):
        print(linea)
        if i == 49:
            print("\n[... el reporte continúa en el archivo ...]")
    
    print("\n" + "="*60)
    print("📋 INSTRUCCIONES PARA COPIAR:")
    print("="*60)
    print("1. Abre el archivo: notepad " + nombre_archivo)
    print("2. En el Bloc de Notas: Ctrl+A (seleccionar todo)")
    print("3. Ctrl+C (copiar)")
    print("4. Ir al nuevo chat y Ctrl+V (pegar)")
    print("="*60)
    
    # También crear versión compacta
    version_compacta = "\n".join(lineas[:100]) + "\n[... ver archivo completo para más detalles ...]"
    with open("reporte_compacto.txt", 'w', encoding='utf-8') as f:
        f.write(version_compacta)
    
    print(f"\n✅ También se creó: reporte_compacto.txt (versión más corta)")

def main():
    """Función principal"""
    print("\n" + "="*60)
    print("VECTA 12D - GENERADOR DE REPORTES PARA OTROS CHATS")
    print("="*60)
    print("Este sistema creará un reporte COMPLETO con toda la")
    print("información que necesita otro asistente para ayudarte.")
    print("="*60)
    
    input("\nPresiona Enter para comenzar...")
    
    guardar_y_mostrar_reporte()
    
    print("\n" + "="*60)
    print("✅ PROCESO COMPLETADO")
    print("="*60)
    print("\nAhora puedes:")
    print("1. Abrir reporte_vecta_XXXXXXXX.txt para copiar TODO")
    print("2. O usar reporte_compacto.txt si es muy largo")
    print("3. Pegar el contenido en un NUEVO chat")
    print("\nEl reporte incluye:")
    print("- Estructura completa del proyecto")
    print("- Contenido de archivos importantes")
    print("- Estado de las dimensiones")
    print("- Problemas detectados")
    print("- Instrucciones para continuar")
    print("="*60)

if __name__ == "__main__":
    try:
        main()
        input("\nPresiona Enter para salir...")
    except Exception as e:
        print(f"Error: {e}")
        input("\nPresiona Enter para salir...")