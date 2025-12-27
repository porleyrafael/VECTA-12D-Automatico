"""
PAQUETE DIMENSIONES VECTA 12D
Exporta todas las dimensiones para importacion correcta
"""

# Exportar dimensiones base
from .dimension_base import DimensionBase, ResultadoDimension, EstadoDimension

# Exportar dimensiones especificas
try:
    from .dimension_1 import Dimension1
except ImportError:
    Dimension1 = None

try:
    from .dimension_2 import Dimension2
except ImportError:
    Dimension2 = None

try:
    from .dimension_3 import Dimension3
except ImportError:
    Dimension3 = None

try:
    from .dimension_4 import Dimension4
except ImportError:
    Dimension4 = None

try:
    from .dimension_5 import Dimension5
except ImportError:
    Dimension5 = None

try:
    from .dimension_6 import Dimension6
except ImportError:
    Dimension6 = None

try:
    from .dimension_7 import Dimension7
except ImportError:
    Dimension7 = None

try:
    from .dimension_8 import Dimension8
except ImportError:
    Dimension8 = None

try:
    from .dimension_9 import Dimension9
except ImportError:
    Dimension9 = None

try:
    from .dimension_10 import Dimension10
except ImportError:
    Dimension10 = None

try:
    from .dimension_11 import Dimension11
except ImportError:
    Dimension11 = None

try:
    from .dimension_12 import Dimension12
except ImportError:
    Dimension12 = None

# Lista de dimensiones disponibles
dimensiones_disponibles = [
    Dimension1, Dimension2, Dimension3, Dimension4, Dimension5, Dimension6,
    Dimension7, Dimension8, Dimension9, Dimension10, Dimension11, Dimension12
]

__all__ = [
    'DimensionBase', 'ResultadoDimension', 'EstadoDimension',
    'Dimension1', 'Dimension2', 'Dimension3', 'Dimension4', 'Dimension5', 'Dimension6',
    'Dimension7', 'Dimension8', 'Dimension9', 'Dimension10', 'Dimension11', 'Dimension12',
    'dimensiones_disponibles'
]
