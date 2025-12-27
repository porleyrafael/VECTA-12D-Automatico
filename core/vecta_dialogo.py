#!/usr/bin/env python3
"""
MÓDULO DE DIÁLOGO VECTA-IA
Registra la interacción autoprogramable entre VECTA y asistentes IA
"""

import json
import os
from datetime import datetime
from pathlib import Path

class DialogoVECTA:
    """Gestiona el diálogo entre VECTA y asistentes IA"""
    
    def __init__(self):
        # Rutas
        self.base_dir = Path(__file__).parent.parent
        self.logs_dir = self.base_dir / "logs"
        self.historial_path = self.logs_dir / "dialogo_vecta.json"
        
        # Asegurar que existe el directorio logs
        self.logs_dir.mkdir(exist_ok=True)
        
        # Estado actual de VECTA
        self.estado_vecta = {
            "sistema": "VECTA 12D",
            "version": "1.0",
            "dimensiones_completas": 3,
            "dimensiones_totales": 12,
            "estado": "operativo",
            "ultima_actualizacion": datetime.now().isoformat()
        }
        
        print(f"✅ Diálogo VECTA inicializado. Historial en: {self.historial_path}")
    
    def registrar_interaccion(self, tipo, contenido, fuente="VECTA"):
        """
        Registra una interacción en el diálogo
        
        Args:
            tipo: "consulta", "sugerencia", "implementacion", "reporte"
            contenido: Texto de la interacción
            fuente: "VECTA" o "IA"
        """
        # Crear entrada
        entrada = {
            "id": self._generar_id(),
            "timestamp": datetime.now().isoformat(),
            "fuente": fuente,
            "tipo": tipo,
            "contenido": contenido,
            "estado_vecta_en_ese_momento": self.estado_vecta.copy()
        }
        
        # Cargar historial existente
        historial = self.cargar_historial()
        historial.append(entrada)
        
        # Guardar (máximo 1000 entradas para no sobrecargar)
        if len(historial) > 1000:
            historial = historial[-1000:]
        
        try:
            with open(self.historial_path, 'w', encoding='utf-8') as f:
                json.dump(historial, f, indent=2, ensure_ascii=False)
            
            print(f"📝 Registrada interacción: {fuente} - {tipo}")
            return True
            
        except Exception as e:
            print(f"❌ Error guardando interacción: {e}")
            return False
    
    def _generar_id(self):
        """Genera un ID único para cada interacción"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"INT_{timestamp}"
    
    def cargar_historial(self):
        """Carga el historial de diálogos desde archivo"""
        if self.historial_path.exists():
            try:
                with open(self.historial_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("⚠️  Historial corrupto, creando nuevo")
                return []
            except Exception as e:
                print(f"⚠️  Error cargando historial: {e}")
                return []
        return []
    
    def actualizar_estado_vecta(self, nuevos_datos):
        """Actualiza el estado de VECTA"""
        self.estado_vecta.update(nuevos_datos)
        self.estado_vecta["ultima_actualizacion"] = datetime.now().isoformat()
        
        # Registrar automáticamente cambios importantes
        if "dimensiones_completas" in nuevos_datos:
            self.registrar_interaccion(
                "reporte",
                f"Actualizadas dimensiones completas: {nuevos_datos['dimensiones_completas']}/12",
                "VECTA"
            )
    
    def generar_reporte_diario(self):
        """Genera un reporte del progreso"""
        historial = self.cargar_historial()
        
        # Filtrar interacciones de hoy
        hoy = datetime.now().date().isoformat()
        interacciones_hoy = [
            h for h in historial 
            if h["timestamp"].startswith(hoy)
        ]
        
        reporte = {
            "fecha": hoy,
            "total_interacciones": len(interacciones_hoy),
            "consultas_vecta": sum(1 for h in interacciones_hoy 
                                 if h["fuente"] == "VECTA" and h["tipo"] == "consulta"),
            "sugerencias_ia": sum(1 for h in interacciones_hoy 
                                 if h["fuente"] == "IA" and h["tipo"] == "sugerencia"),
            "implementaciones": sum(1 for h in interacciones_hoy 
                                   if h["tipo"] == "implementacion"),
            "estado_actual": self.estado_vecta
        }
        
        return reporte
    
    def mostrar_historial_reciente(self, cantidad=5):
        """Muestra las interacciones más recientes"""
        historial = self.cargar_historial()
        
        if not historial:
            print("📭 No hay historial de diálogo aún.")
            return
        
        print(f"\n📜 ÚLTIMAS {cantidad} INTERACCIONES:")
        print("=" * 60)
        
        for entrada in historial[-cantidad:]:
            tiempo = entrada["timestamp"][11:19]  # Solo hora:minuto:segundo
            fuente = entrada["fuente"]
            tipo = entrada["tipo"]
            contenido = entrada["contenido"][:80] + "..." if len(entrada["contenido"]) > 80 else entrada["contenido"]
            
            # Iconos según fuente y tipo
            if fuente == "VECTA":
                icono = "🔄"
            else:
                icono = "🤖"
            
            if tipo == "sugerencia":
                icono += "💡"
            elif tipo == "implementacion":
                icono += "⚡"
            
            print(f"{icono} [{tiempo}] {fuente}: {contenido}")
            print("-" * 60)
    
    def exportar_historial_texto(self, archivo_salida="dialogo_completo.txt"):
        """Exporta todo el historial a un archivo de texto legible"""
        historial = self.cargar_historial()
        
        if not historial:
            return "No hay historial para exportar"
        
        texto = f"# HISTORIAL COMPLETO DIÁLOGO VECTA-IA\n"
        texto += f"# Generado: {datetime.now().isoformat()}\n"
        texto += f"# Total interacciones: {len(historial)}\n\n"
        
        for entrada in historial:
            fecha = entrada["timestamp"][:10]
            hora = entrada["timestamp"][11:19]
            fuente = entrada["fuente"]
            tipo = entrada["tipo"]
            contenido = entrada["contenido"]
            
            texto += f"[{fecha} {hora}] {fuente} ({tipo}):\n"
            texto += f"{contenido}\n"
            texto += f"{'-'*50}\n\n"
        
        # Guardar archivo
        archivo_path = self.logs_dir / archivo_salida
        try:
            with open(archivo_path, 'w', encoding='utf-8') as f:
                f.write(texto)
            return f"Historial exportado a: {archivo_path}"
        except Exception as e:
            return f"Error exportando: {e}"

# ============================================================================
# FUNCIONES DE CONVENIENCIA PARA USO RÁPIDO
# ============================================================================

# Crear instancia global
_dialogo_instance = None

def obtener_dialogo():
    """Obtiene o crea la instancia global del diálogo"""
    global _dialogo_instance
    if _dialogo_instance is None:
        _dialogo_instance = DialogoVECTA()
    return _dialogo_instance

def registrar_consulta_vecta(pregunta):
    """Registra una consulta de VECTA a IA"""
    dialogo = obtener_dialogo()
    return dialogo.registrar_interaccion("consulta", pregunta, "VECTA")

def registrar_sugerencia_ia(sugerencia):
    """Registra una sugerencia de IA a VECTA"""
    dialogo = obtener_dialogo()
    return dialogo.registrar_interaccion("sugerencia", sugerencia, "IA")

def registrar_implementacion_vecta(descripcion):
    """Registra una implementación realizada por VECTA"""
    dialogo = obtener_dialogo()
    return dialogo.registrar_interaccion("implementacion", descripcion, "VECTA")

def actualizar_progreso_vecta(dimensiones_completas=None, **kwargs):
    """Actualiza el progreso de VECTA"""
    dialogo = obtener_dialogo()
    
    datos_actualizacion = {}
    if dimensiones_completas is not None:
        datos_actualizacion["dimensiones_completas"] = dimensiones_completas
    
    datos_actualizacion.update(kwargs)
    dialogo.actualizar_estado_vecta(datos_actualizacion)
    
    return dialogo.estado_vecta

# ============================================================================
# PRUEBA DEL MÓDULO
# ============================================================================

if __name__ == "__main__":
    print("🧪 PROBANDO MÓDULO DE DIÁLOGO VECTA-IA")
    print("=" * 60)
    
    # Crear instancia
    dialogo = DialogoVECTA()
    
    # Registrar algunas interacciones de ejemplo
    dialogo.registrar_interaccion(
        "consulta",
        "He completado 3 dimensiones. ¿Cómo puedo avanzar con la dimensión 4?",
        "VECTA"
    )
    
    dialogo.registrar_interaccion(
        "sugerencia",
        "Sugiero implementar la dimensión 4 (Temporalidad) usando ciclos filosóficos y métricas de evolución.",
        "IA"
    )
    
    dialogo.registrar_interaccion(
        "implementacion",
        "Implementando dimensión 4: Sistema de ciclos temporales con 3 fases (Pasado, Presente, Futuro).",
        "VECTA"
    )
    
    # Actualizar progreso
    dialogo.actualizar_estado_vecta({"dimensiones_completas": 4})
    
    # Mostrar historial reciente
    dialogo.mostrar_historial_reciente(3)
    
    # Generar reporte
    reporte = dialogo.generar_reporte_diario()
    print(f"\n📊 REPORTE DIARIO:")
    print(f"   Interacciones hoy: {reporte['total_interacciones']}")
    print(f"   Dimensiones completas: {reporte['estado_actual']['dimensiones_completas']}/12")
    
    # Exportar historial
    resultado = dialogo.exportar_historial_texto()
    print(f"\n{resultado}")
    
    print("\n✅ Módulo de diálogo funcionando correctamente.")
    print("   Para usar en tu código:")
    print("   from core.vecta_dialogo import registrar_consulta_vecta, registrar_sugerencia_ia")