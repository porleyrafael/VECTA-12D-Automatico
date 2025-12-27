"""
DIMENSION 4: Informacion-Entropia
"""


class DimensionInformacionEntropia:
    def __init__(self):
        self.nombre = "Informacion-Entropia"
        self.magnitud = 0.0
    
    def procesar(self, datos):
        return {"dimension": self.nombre, "magnitud": 0.4}
