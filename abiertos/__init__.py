"""
Métodos abiertos para resolución de ecuaciones no lineales.

Este módulo contiene implementaciones de métodos abiertos:
- Iteración de Punto Fijo
- Método de Newton
- Método de la Secante
"""

from .punto_fijo import punto_fijo
from .newton import newton
from .secante import secante

__all__ = ['punto_fijo', 'newton', 'secante']
