#!/usr/bin/env python3
"""
Ejemplo simple de exportación a CSV.

Este es un ejemplo mínimo que muestra cómo exportar resultados
de un método numérico a CSV de manera muy sencilla.
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from cerrados import biseccion
from utils import exportar_iteraciones_csv


def ejemplo_simple():
    """Ejemplo muy simple de exportación"""
    print("🔢 Ejemplo Simple: Exportar Bisección a CSV")
    print("=" * 50)
    
    # Definir función
    def f(x):
        return x**3 - x - 1
    
    print("Función: f(x) = x³ - x - 1")
    print("Ejecutando método de bisección...")
    
    # Ejecutar método
    raiz, iteraciones, convergencia, historial = biseccion(
        f, 1, 2, tolerancia=1e-6, mostrar_iteraciones=False
    )
    
    print(f"✓ Raíz encontrada: {raiz:.6f}")
    print(f"✓ Iteraciones: {iteraciones}")
    print()
    
    # Exportar a CSV
    print("📊 Exportando a CSV...")
    archivo = exportar_iteraciones_csv(
        historial=historial,
        nombre_archivo="ejemplo_simple.csv"
    )
    
    print(f"✅ ¡Listo! Archivo generado: {archivo}")
    print()
    print("💡 Puedes abrir el archivo CSV en:")
    print("   - Excel o Google Sheets")
    print("   - Cualquier editor de texto")
    print("   - Python con pandas: pd.read_csv('resultados/ejemplo_simple.csv')")


if __name__ == "__main__":
    ejemplo_simple()
