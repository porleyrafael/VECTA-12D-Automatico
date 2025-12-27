"""
DIMENSION 11: Conectividad-Red
"""


class DimensionConectividadRed:
    def __init__(self):
        self.nombre = "Conectividad-Red"
        self.magnitud = 0.0
    
    def procesar(self, datos):
        return {"dimension": self.nombre, "magnitud": 0.6}
