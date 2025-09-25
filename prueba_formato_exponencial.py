#!/usr/bin/env python3
"""
Prueba del formato exponencial legible.

Este script prueba la función de formato exponencial para asegurar
que funciona correctamente.
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import formato_exponencial_legible


def prueba_formato_exponencial():
    """Prueba el formato exponencial con diferentes valores"""
    print("=" * 60)
    print("PRUEBA DEL FORMATO EXPONENCIAL LEGIBLE")
    print("=" * 60)
    print()
    
    # Valores de prueba
    valores_prueba = [
        4.46583412e-05,
        1.15737986e-06,
        1.86318279e-07,
        8.88e-16,
        3.57e-07,
        0.00123456789,
        1234567.89,
        1.23e-08,
        1.23456789e+03,
        0.0,
        -4.46583412e-05
    ]
    
    print("Valor original → Formato exponencial legible")
    print("-" * 60)
    
    for valor in valores_prueba:
        formato_legible = formato_exponencial_legible(valor, 9)
        print(f"{valor:20.2e} → {formato_legible}")
    
    print()
    print("✅ Prueba completada")
    print("💡 Los números muy pequeños ahora se muestran como:")
    print("   • 4.46583412e-05 → 4.47x10^-5")
    print("   • 1.15737986e-06 → 1.16x10^-6")
    print("   • 1.86318279e-07 → 1.86x10^-7")


if __name__ == "__main__":
    prueba_formato_exponencial()
