"""
Métodos cerrados para resolución de ecuaciones no lineales.

Este módulo contiene implementaciones de métodos cerrados:
- Bisección
- Regula Falsi
- Regula Falsi Modificada
"""

from .biseccion import biseccion
from .regula_falsi import regula_falsi
from .regula_falsi_modificada import regula_falsi_modificada

__all__ = ['biseccion', 'regula_falsi', 'regula_falsi_modificada']
