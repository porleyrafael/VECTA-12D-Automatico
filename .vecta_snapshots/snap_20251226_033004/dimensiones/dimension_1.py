"""
DIMENSION 1: Tiempo-Entropia
"""


class DimensionTiempoEntropia:
    def __init__(self):
        self.nombre = "Tiempo-Entropia"
        self.magnitud = 0.0
    
    def procesar(self, datos):
        import time
        return {"dimension": self.nombre, "magnitud": 0.5, "timestamp": time.time()}
