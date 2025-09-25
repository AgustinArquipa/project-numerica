#!/usr/bin/env python3
"""
Ejemplo de uso de precisión de calculadora científica.

Este ejemplo demuestra cómo exportar resultados con precisión controlada
para simular el comportamiento de una calculadora científica con mantisa
de 9 dígitos y exponente de 3.
"""

import sys
import os
import math

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from cerrados import biseccion, regula_falsi
from utils import (
    exportar_iteraciones_csv, 
    redondear_significativos,
    mostrar_precision_analysis,
    simular_calculadora_cientifica
)


def ejemplo_precision_calculadora():
    """Ejemplo completo de precisión de calculadora científica"""
    print("=" * 80)
    print("EJEMPLO: PRECISIÓN DE CALCULADORA CIENTÍFICA")
    print("=" * 80)
    print("Simulando calculadora con mantisa de 9 dígitos y exponente de 3")
    print()
    
    # Definir función
    def f(x):
        return x**3 - x - 1
    
    print("📋 Función: f(x) = x³ - x - 1")
    print("📋 Intervalo: [1, 2]")
    print()
    
    # Ejecutar método de bisección
    print("🔄 Ejecutando método de bisección...")
    raiz, iteraciones, convergencia, historial = biseccion(
        f, 1, 2, tolerancia=1e-6, mostrar_iteraciones=False
    )
    
    print(f"✅ Raíz encontrada: {raiz:.10f}")
    print(f"✅ Iteraciones: {iteraciones}")
    print()
    
    # Mostrar análisis de precisión para la raíz
    print("📊 ANÁLISIS DE PRECISIÓN PARA LA RAÍZ:")
    mostrar_precision_analysis(raiz)
    print()
    
    # Exportar sin precisión controlada (precisión completa de Python)
    print("📁 Exportando con precisión completa de Python...")
    archivo_precision_completa = exportar_iteraciones_csv(
        historial=historial,
        nombre_archivo="precision_completa.csv",
        directorio="resultados",
        precision_calculadora=None  # Sin límite de precisión
    )
    print(f"✅ Archivo generado: {os.path.basename(archivo_precision_completa)}")
    print()
    
    # Exportar con precisión de calculadora (9 cifras significativas)
    print("📁 Exportando con precisión de calculadora (9 cifras significativas)...")
    archivo_calculadora = exportar_iteraciones_csv(
        historial=historial,
        nombre_archivo="precision_calculadora.csv",
        directorio="resultados",
        precision_calculadora=9,  # Mantisa de 9 dígitos
        usar_decimal=False
    )
    print(f"✅ Archivo generado: {os.path.basename(archivo_calculadora)}")
    print()
    
    # Exportar con precisión de calculadora usando Decimal
    print("📁 Exportando con precisión Decimal (9 cifras significativas)...")
    archivo_decimal = exportar_iteraciones_csv(
        historial=historial,
        nombre_archivo="precision_decimal.csv",
        directorio="resultados",
        precision_calculadora=9,
        usar_decimal=True
    )
    print(f"✅ Archivo generado: {os.path.basename(archivo_decimal)}")
    print()
    
    # Comparar diferentes precisiones
    print("📊 COMPARACIÓN DE PRECISIONES:")
    precisiones = [6, 8, 9, 10, 12]
    
    for precision in precisiones:
        print(f"\n🎯 Exportando con {precision} cifras significativas...")
        archivo = exportar_iteraciones_csv(
            historial=historial,
            nombre_archivo=f"precision_{precision}.csv",
            directorio="resultados",
            precision_calculadora=precision
        )
        print(f"✅ Archivo: {os.path.basename(archivo)}")
    
    print()
    
    # Simular calculadora científica
    print("🧮 SIMULACIÓN DE CALCULADORA CIENTÍFICA:")
    valores_ejemplo = [1.0, 1.5, 2.0, raiz]
    resultados_calc = simular_calculadora_cientifica(f, valores_ejemplo, 9)
    
    print("Evaluación de función con precisión de calculadora:")
    for clave, valor in resultados_calc.items():
        print(f"  {clave} = {valor}")
    
    print()
    print("✅ Ejemplo completado!")
    print("📁 Revisa la carpeta 'resultados/' para ver los archivos con diferentes precisiones")


def comparar_archivos_precision():
    """Compara algunos valores de los archivos generados"""
    print("\n" + "=" * 80)
    print("COMPARACIÓN DE ARCHIVOS CON DIFERENTES PRECISIONES")
    print("=" * 80)
    
    # Leer algunas líneas de cada archivo para comparar
    archivos = [
        "precision_completa.csv",
        "precision_calculadora.csv", 
        "precision_decimal.csv"
    ]
    
    for archivo in archivos:
        ruta = os.path.join("resultados", archivo)
        if os.path.exists(ruta):
            print(f"\n📄 {archivo}:")
            with open(ruta, 'r') as f:
                lineas = f.readlines()[:10]  # Primeras 10 líneas
                for i, linea in enumerate(lineas):
                    if i < 6:  # Mostrar solo las primeras 6 líneas
                        print(f"  {linea.strip()}")
                    elif i == 6:
                        print("  ...")
                        break


def ejemplo_redondeo_manual():
    """Ejemplo de redondeo manual para comparar con calculadora"""
    print("\n" + "=" * 80)
    print("EJEMPLO DE REDONDEO MANUAL")
    print("=" * 80)
    
    # Valores de ejemplo
    valores = [
        3.141592653589793,  # π
        2.718281828459045,  # e
        1.4142135623730951, # √2
        1.324717957244746,  # Raíz de x³ - x - 1
        0.000123456789,     # Número pequeño
        1234567.123456789   # Número grande
    ]
    
    nombres = ["π", "e", "√2", "Raíz x³-x-1", "Número pequeño", "Número grande"]
    
    print("Comparación de valores con diferentes precisiones:")
    print()
    print(f"{'Valor':<15} {'Original':<20} {'6 cifras':<15} {'8 cifras':<15} {'9 cifras':<15}")
    print("-" * 90)
    
    for valor, nombre in zip(valores, nombres):
        original = f"{valor:.15f}"
        p6 = redondear_significativos(valor, 6)
        p8 = redondear_significativos(valor, 8)
        p9 = redondear_significativos(valor, 9)
        
        print(f"{nombre:<15} {original:<20} {p6:<15} {p8:<15} {p9:<15}")


if __name__ == "__main__":
    ejemplo_precision_calculadora()
    comparar_archivos_precision()
    ejemplo_redondeo_manual()
    
    print("\n🎯 RESUMEN:")
    print("✅ Se generaron archivos CSV con diferentes precisiones")
    print("✅ Precisión de calculadora: 9 cifras significativas")
    print("✅ Comparación entre float redondeado y Decimal")
    print("✅ Archivos listos para comparar con calculadora manual")
    print()
    print("💡 Los archivos con precisión de calculadora simulan")
    print("   el comportamiento de una calculadora científica real")
