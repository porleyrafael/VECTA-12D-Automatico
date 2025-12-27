#!/usr/bin/env python3
"""
🧹 LIMPIADOR VECTA 12D - COMPLETO Y SEGURO
Elimina archivos obsoletos manteniendo la integridad del proyecto
"""

import os
import sys
import glob
import shutil
import json
from datetime import datetime
from pathlib import Path

class LimpiadorVECTA:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.log_file = self.base_dir / "logs" / "limpieza.log"
        self.config_file = self.base_dir / "config_limpieza.json"
        
        # Archivos ESENCIALES que NUNCA se deben tocar
        self.esenciales = {
            # NÚCLEO VECTA
            "core/meta_vecta.py",
            "core/vecta_12d_core.py",
            "core/__init__.py",
            
            # DIMENSIONES
            "dimensiones/vector_12d.py",
            "dimensiones/dimension_1.py",
            "dimensiones/dimension_2.py",
            "dimensiones/dimension_3.py", 
            "dimensiones/dimension_4.py",
            "dimensiones/__init__.py",
            
            # PRINCIPALES
            "vecta_launcher.py",
            "crear_dashboard_vecta.py",
            "dashboard_vecta.html",
            
            # CONFIGURACIÓN
            "README.md",
            ".gitignore",
            "github_config.json",
            "configurar_github.py",
            
            # UTILIDADES
            "auto_commit.py",
            "iniciar_sistema.bat",
            "git_help.bat",
            "limpiador_vecta.py"
        }
        
        # Carpetas PROTEGIDAS
        self.carpetas_protegidas = {
            "core",
            "dimensiones",
            ".git",
            "logs"
        }
        
        # Patrones de BASURA (se eliminan)
        self.patrones_basura = [
            # Python cache
            "**/__pycache__/**",
            "**/*.py[cod]",
            "**/*.py.class",
            "**/*.so",
            
            # Temporales y backups
            "**/*.tmp",
            "**/*.temp",
            "**/*.bak",
            "**/*.backup",
            "**/*~",
            
            # Sistema
            "**/Thumbs.db",
            "**/.DS_Store",
            "**/desktop.ini",
            
            # IDE/Editor
            "**/.vscode/settings.json",
            "**/.vscode/launch.json",
            "**/.idea/workspace.xml",
            "**/*.swp",
            "**/*.swo",
            
            # Logs viejos (más de 30 días)
            "**/*.log",
            
            # Build/Dist
            "**/build/**",
            "**/dist/**",
            "**/*.egg-info/**",
            "**/*.egg"
        ]
        
        self.eliminados = []
        self.errores = []
        self.espacio_liberado = 0

    def mostrar_banner(self):
        """Muestra banner del limpiador"""
        print("\n" + "="*70)
        print("🧹 LIMPIADOR VECTA 12D - VERSIÓN COMPLETA")
        print("="*70)
        print(f"📂 Directorio: {self.base_dir}")
        print(f"⏰ Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-"*70)

    def cargar_config(self):
        """Carga configuración desde archivo JSON"""
        config_default = {
            "modo_seguro": True,
            "eliminar_vacios": True,
            "dias_para_logs": 7,
            "tamano_max_mb": 100,
            "exclusiones": []
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return {**config_default, **json.load(f)}
            except:
                return config_default
        return config_default

    def es_archivo_esencial(self, ruta_relativa):
        """Verifica si un archivo es esencial y no debe eliminarse"""
        # Convertir a formato compatible
        ruta_str = str(ruta_relativa).replace('\\', '/')
        
        # Verificar en lista de esenciales
        if ruta_str in self.esenciales:
            return True
        
        # Verificar si está en carpeta protegida
        for carpeta in self.carpetas_protegidas:
            if ruta_str.startswith(carpeta + '/'):
                # Dentro de carpeta protegida, solo eliminar __pycache__
                if '__pycache__' in ruta_str:
                    return False
                return True
        
        return False

    def escanear_basura(self):
        """Escanea y retorna lista de archivos basura"""
        basura = []
        
        for patron in self.patrones_basura:
            for ruta_abs in glob.glob(str(self.base_dir / patron), recursive=True):
                ruta = Path(ruta_abs)
                ruta_rel = ruta.relative_to(self.base_dir)
                
                # Saltar si es esencial
                if self.es_archivo_esencial(ruta_rel):
                    continue
                
                # Saltar si no existe (por si acaso)
                if not ruta.exists():
                    continue
                
                # Verificar si es archivo .gitkeep (nunca eliminar)
                if ruta.name == '.gitkeep':
                    continue
                
                # Para logs, verificar antigüedad
                if ruta.suffix == '.log':
                    try:
                        mtime = ruta.stat().st_mtime
                        edad_dias = (datetime.now().timestamp() - mtime) / (60*60*24)
                        if edad_dias < 7:  # Logs menores a 7 días se conservan
                            continue
                    except:
                        pass
                
                basura.append(ruta)
        
        # Eliminar duplicados
        basura = list(set(basura))
        
        # Ordenar por profundidad (más profundo primero)
        basura.sort(key=lambda x: len(str(x)), reverse=True)
        
        return basura

    def escanear_carpetas_vacias(self):
        """Encuentra carpetas vacías (excepto protegidas)"""
        carpetas_vacias = []
        
        for ruta in self.base_dir.rglob('*'):
            if ruta.is_dir():
                # Saltar carpetas protegidas
                ruta_rel = ruta.relative_to(self.base_dir)
                if any(str(ruta_rel).startswith(cp) for cp in self.carpetas_protegidas):
                    continue
                
                # Saltar .git
                if '.git' in str(ruta):
                    continue
                
                # Verificar si está vacía
                try:
                    if not any(ruta.iterdir()):
                        carpetas_vacias.append(ruta)
                except:
                    pass
        
        # Ordenar por profundidad
        carpetas_vacias.sort(key=lambda x: len(str(x)), reverse=True)
        
        return carpetas_vacias

    def calcular_tamano(self, ruta):
        """Calcula tamaño de archivo o carpeta"""
        if ruta.is_file():
            return ruta.stat().st_size
        elif ruta.is_dir():
            total = 0
            for archivo in ruta.rglob('*'):
                if archivo.is_file():
                    total += archivo.stat().st_size
            return total
        return 0

    def formatear_tamano(self, bytes):
        """Formatea bytes a texto legible"""
        for unidad in ['B', 'KB', 'MB', 'GB']:
            if bytes < 1024.0:
                return f"{bytes:.1f} {unidad}"
            bytes /= 1024.0
        return f"{bytes:.1f} TB"

    def mostrar_resumen(self, archivos, carpetas):
        """Muestra resumen de lo encontrado"""
        print("\n📊 RESULTADO DEL ESCANEO:")
        print("-"*50)
        
        total_archivos = len(archivos)
        total_carpetas = len(carpetas)
        
        # Calcular espacio
        espacio_total = sum(self.calcular_tamano(a) for a in archivos)
        self.espacio_liberado = espacio_total
        
        print(f"📄 Archivos obsoletos: {total_archivos}")
        print(f"📁 Carpetas vacías: {total_carpetas}")
        print(f"💾 Espacio a liberar: {self.formatear_tamano(espacio_total)}")
        
        if total_archivos > 0:
            print("\n📋 Top 10 archivos a eliminar:")
            for i, archivo in enumerate(archivos[:10], 1):
                tam = self.calcular_tamano(archivo)
                rel = archivo.relative_to(self.base_dir)
                print(f"  {i:2d}. {rel} ({self.formatear_tamano(tam)})")
            
            if total_archivos > 10:
                print(f"  ... y {total_archivos - 10} más")
        
        if total_carpetas > 0:
            print("\n📂 Carpetas vacías:")
            for i, carpeta in enumerate(carpetas[:5], 1):
                rel = carpeta.relative_to(self.base_dir)
                print(f"  {i:2d}. {rel}/")
            
            if total_carpetas > 5:
                print(f"  ... y {total_carpetas - 5} más")

    def confirmar_eliminacion(self):
        """Pide confirmación al usuario"""
        print("\n⚠️  ADVERTENCIA: Esta acción no se puede deshacer.")
        print("   Se eliminarán archivos temporales y carpetas vacías.")
        
        while True:
            respuesta = input("\n¿Continuar con la limpieza? (sí/no/mostrar): ").strip().lower()
            
            if respuesta in ['si', 'sí', 's', 'yes', 'y']:
                return True
            elif respuesta in ['no', 'n']:
                return False
            elif respuesta in ['mostrar', 'm']:
                print("\n🔍 Archivos esenciales protegidos:")
                for i, esen in enumerate(sorted(self.esenciales)[:20], 1):
                    print(f"  {i:2d}. {esen}")
                if len(self.esenciales) > 20:
                    print(f"  ... y {len(self.esenciales) - 20} más")
            else:
                print("❌ Respuesta no válida. Escribe 'sí', 'no' o 'mostrar'.")

    def eliminar_archivos(self, archivos):
        """Elimina archivos de forma segura"""
        print("\n🗑️  Eliminando archivos...")
        
        for ruta in archivos:
            try:
                if ruta.is_file():
                    tamano = self.calcular_tamano(ruta)
                    ruta.unlink()  # Eliminar archivo
                    self.eliminados.append(("archivo", str(ruta), tamano))
                    
                    rel = ruta.relative_to(self.base_dir)
                    print(f"  ✓ {rel}")
                    
                elif ruta.is_dir():
                    tamano = self.calcular_tamano(ruta)
                    shutil.rmtree(ruta)  # Eliminar carpeta y contenido
                    self.eliminados.append(("carpeta", str(ruta), tamano))
                    
                    rel = ruta.relative_to(self.base_dir)
                    print(f"  📁 {rel}/")
                    
            except Exception as e:
                self.errores.append((str(ruta), str(e)))
                print(f"  ✗ Error con {ruta.name}: {e}")

    def guardar_log(self):
        """Guarda log de limpieza"""
        # Crear carpeta logs si no existe
        logs_dir = self.base_dir / "logs"
        logs_dir.mkdir(exist_ok=True)
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write("\n" + "="*60 + "\n")
            f.write(f"LIMPIEZA VECTA 12D - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*60 + "\n")
            
            if self.eliminados:
                f.write("\n📄 ELIMINADOS:\n")
                for tipo, ruta, tamano in self.eliminados:
                    f.write(f"  [{tipo.upper()}] {ruta} ({self.formatear_tamano(tamano)})\n")
            
            if self.errores:
                f.write("\n❌ ERRORES:\n")
                for ruta, error in self.errores:
                    f.write(f"  {ruta}: {error}\n")
            
            f.write(f"\n💾 ESPACIO LIBERADO: {self.formatear_tamano(self.espacio_liberado)}\n")
            f.write("="*60 + "\n")
        
        print(f"\n📝 Log guardado en: {self.log_file}")

    def mostrar_resultado_final(self):
        """Muestra resultado final de la limpieza"""
        print("\n" + "="*70)
        print("🎯 RESULTADO FINAL DE LA LIMPIEZA")
        print("="*70)
        
        if self.eliminados:
            total_archivos = sum(1 for t, _, _ in self.eliminados if t == "archivo")
            total_carpetas = sum(1 for t, _, _ in self.eliminados if t == "carpeta")
            
            print(f"✅ Archivos eliminados: {total_archivos}")
            print(f"✅ Carpetas eliminadas: {total_carpetas}")
            print(f"✅ Espacio liberado: {self.formatear_tamano(self.espacio_liberado)}")
            
            if self.errores:
                print(f"⚠️  Errores: {len(self.errores)}")
        else:
            print("✅ No se encontró basura para eliminar.")
        
        print("\n💡 RECOMENDACIONES:")
        print("   1. Ejecuta 'git status' para ver cambios")
        print("   2. Si quieres commit: 'git add .' y 'git commit -m \"Limpieza\"'")
        print("   3. Para limpieza automática, agrega al cron/tasks")
        print("="*70)

    def crear_config_ejemplo(self):
        """Crea archivo de configuración de ejemplo"""
        config_ejemplo = {
            "modo_seguro": True,
            "eliminar_vacios": True,
            "dias_para_logs": 7,
            "tamano_max_mb": 100,
            "exclusiones": [
                "mi_archivo_especial.txt",
                "backups/"
            ],
            "notas": "Configuración del limpiador VECTA 12D"
        }
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config_ejemplo, f, indent=2, ensure_ascii=False)
        
        print(f"\n⚙️  Configuración creada: {self.config_file}")

    def ejecutar(self):
        """Ejecuta el proceso completo de limpieza"""
        self.mostrar_banner()
        
        # Crear config si no existe
        if not self.config_file.exists():
            self.crear_config_ejemplo()
        
        # Cargar configuración
        config = self.cargar_config()
        print(f"⚙️  Modo seguro: {'Activado' if config['modo_seguro'] else 'Desactivado'}")
        
        # Escanear
        print("\n🔍 Escaneando archivos obsoletos...")
        archivos_basura = self.escanear_basura()
        
        print("🔍 Escaneando carpetas vacías...")
        carpetas_vacias = self.escanear_carpetas_vacias() if config['eliminar_vacios'] else []
        
        # Mostrar resumen
        self.mostrar_resumen(archivos_basura, carpetas_vacias)
        
        # Si no hay nada, terminar
        if not archivos_basura and not carpetas_vacias:
            print("\n🎉 ¡Todo limpio! No hay archivos obsoletos.")
            return
        
        # Pedir confirmación
        if config['modo_seguro'] and not self.confirmar_eliminacion():
            print("\n❌ Limpieza cancelada por el usuario.")
            return
        
        # Ejecutar limpieza
        todo = archivos_basura + carpetas_vacias
        self.eliminar_archivos(todo)
        
        # Guardar log
        if self.eliminados or self.errores:
            self.guardar_log()
        
        # Mostrar resultado
        self.mostrar_resultado_final()

def main():
    """Función principal"""
    try:
        limpiador = LimpiadorVECTA()
        limpiador.ejecutar()
        
        # Pausa para ver resultados
        if sys.platform == "win32":
            input("\nPresiona Enter para salir...")
            
    except KeyboardInterrupt:
        print("\n\n❌ Limpieza interrumpida por el usuario.")
    except Exception as e:
        print(f"\n⚠️  Error inesperado: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()