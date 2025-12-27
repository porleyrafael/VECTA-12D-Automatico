"""
NUCLEO VECTA 12D
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from dimensiones.vector_12d import SistemaVectorial12D
    SISTEMA_DISPONIBLE = True
except:
    SISTEMA_DISPONIBLE = False

class VECTA_12D_Core:
    def __init__(self):
        self.nombre = "VECTA 12D"
        self.version = "2.0.0"
        
        if SISTEMA_DISPONIBLE:
            self.sistema = SistemaVectorial12D()
            self.estado = "sistema_cargado"
        else:
            self.sistema = None
            self.estado = "sistema_no_disponible"
    
    def procesar(self, texto):
        if self.sistema:
            try:
                vector = self.sistema.procesar_evento({"texto": texto})
                return {
                    "exito": True,
                    "magnitud": vector.magnitud(),
                    "dimensiones": vector.dimensiones
                }
            except Exception as e:
                return {"exito": False, "error": str(e)}
        else:
            return {"exito": False, "error": "Sistema no disponible"}
    
    def start_text_interface(self):
        print("\n=== VECTA 12D ===")
        print("Escribe 'salir' para terminar\n")
        
        while True:
            try:
                entrada = input("VECTA> ")
                if entrada.lower() == 'salir':
                    break
                
                resultado = self.procesar(entrada)
                if resultado.get("exito"):
                    print(f"Vector: {resultado['magnitud']:.4f}")
                else:
                    print(f"Error: {resultado.get('error')}")
            except KeyboardInterrupt:
                break
