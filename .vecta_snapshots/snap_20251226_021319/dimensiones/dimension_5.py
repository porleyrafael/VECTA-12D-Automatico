"""
DIMENSION 5: Conciencia-Atencion
"""


class DimensionConcienciaAtencion:
    def __init__(self):
        self.nombre = "Conciencia-Atencion"
        self.magnitud = 0.0
    
    def procesar(self, datos):
        return {"dimension": self.nombre, "magnitud": 0.2}
