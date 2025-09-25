#!/usr/bin/env python3
"""
Ejemplo simple de uso de precisión de calculadora científica.

Este ejemplo muestra cómo exportar con precisión controlada
para comparar con calculadora manual.
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from cerrados import biseccion
from utils import exportar_iteraciones_csv, redondear_significativos


def ejemplo_simple_precision():
    """Ejemplo simple de precisión de calculadora"""
    print("🧮 Ejemplo Simple: Precisión de Calculadora Científica")
    print("=" * 60)
    
    # Definir función
    def f(x):
        return x**3 - x - 1
    
    print("Función: f(x) = x³ - x - 1")
    print("Intervalo: [1, 2]")
    print("Precisión: 9 cifras significativas (calculadora científica)")
    print()
    
    # Ejecutar método
    raiz, iteraciones, convergencia, historial = biseccion(
        f, 1, 2, tolerancia=1e-6, mostrar_iteraciones=False
    )
    
    print(f"✓ Raíz encontrada: {raiz:.10f}")
    print(f"✓ Iteraciones: {iteraciones}")
    print()
    
    # Mostrar cómo se ve la raíz con diferentes precisiones
    print("📊 Comparación de precisiones para la raíz:")
    print(f"  Precisión completa: {raiz}")
    print(f"  9 cifras significativas: {redondear_significativos(raiz, 9)}")
    print(f"  8 cifras significativas: {redondear_significativos(raiz, 8)}")
    print(f"  6 cifras significativas: {redondear_significativos(raiz, 6)}")
    print()
    
    # Exportar sin precisión controlada
    print("📁 Exportando sin precisión controlada...")
    archivo_normal = exportar_iteraciones_csv(
        historial=historial,
        nombre_archivo="ejemplo_normal.csv",
        precision_calculadora=None  # Sin límite
    )
    print(f"✅ Archivo: {os.path.basename(archivo_normal)}")
    
    # Exportar con precisión de calculadora
    print("\n📁 Exportando con precisión de calculadora (9 cifras)...")
    archivo_calculadora = exportar_iteraciones_csv(
        historial=historial,
        nombre_archivo="ejemplo_calculadora.csv",
        precision_calculadora=9  # Mantisa de 9 dígitos
    )
    print(f"✅ Archivo: {os.path.basename(archivo_calculadora)}")
    
    print()
    print("🎯 ¡Listo! Ahora puedes comparar:")
    print("   - ejemplo_normal.csv: Precisión completa de Python")
    print("   - ejemplo_calculadora.csv: Precisión de calculadora (9 cifras)")
    print()
    print("💡 Los valores en el archivo 'calculadora' simulan")
    print("   exactamente lo que verías en una calculadora científica real")


if __name__ == "__main__":
    ejemplo_simple_precision()
