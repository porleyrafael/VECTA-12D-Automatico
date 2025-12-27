"""
DIMENSION 9: Ejecucion-Accion
"""


class DimensionEjecucionAccion:
    def __init__(self):
        self.nombre = "Ejecucion-Accion"
        self.magnitud = 0.0
    
    def procesar(self, datos):
        return {"dimension": self.nombre, "magnitud": 0.9}
