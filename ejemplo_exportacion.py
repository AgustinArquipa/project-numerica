"""
Ejemplo de uso de la funcionalidad de exportación a CSV.

Este archivo demuestra cómo exportar resultados de métodos numéricos
a diferentes formatos para análisis posterior.
"""

import sys
import os
from typing import Dict, Any

# Agregar el directorio raíz al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar métodos
from cerrados import biseccion, regula_falsi
from abiertos import newton, secante
from utils import exportar_iteraciones_csv, exportar_resultado_completo, exportar_comparacion_csv


def ejemplo_biseccion_con_exportacion():
    """Ejemplo de bisección con exportación automática a CSV"""
    print("=" * 60)
    print("EJEMPLO: BISECCIÓN CON EXPORTACIÓN A CSV")
    print("=" * 60)
    
    def f(x):
        return x**3 - x - 1
    
    print("Función: f(x) = x³ - x - 1")
    print("Intervalo: [1, 2]")
    print()
    
    # Ejecutar método de bisección
    raiz, iteraciones, convergencia, historial = biseccion(
        f, 1, 2, tolerancia=1e-6, mostrar_iteraciones=False
    )
    
    print(f"Resultado:")
    print(f"  Raíz: {raiz:.8f}")
    print(f"  Iteraciones: {iteraciones}")
    print(f"  Convergencia: {'✓' if convergencia else '✗'}")
    print()
    
    # Exportar historial simple a CSV
    print("📊 Exportando historial a CSV...")
    archivo_csv = exportar_iteraciones_csv(
        historial=historial,
        nombre_archivo="biseccion_ejemplo.csv",
        directorio="resultados"
    )
    print()
    
    # Exportar resultado completo con metadata
    print("📋 Exportando resultado completo...")
    archivo_completo = exportar_resultado_completo(
        metodo="Bisección",
        funcion="f(x) = x³ - x - 1",
        parametros={
            "a": 1.0,
            "b": 2.0,
            "tolerancia": 1e-6,
            "max_iteraciones": 100
        },
        resultado={
            "raiz": raiz,
            "iteraciones": iteraciones,
            "convergencia": convergencia,
            "valor_funcion_raiz": f(raiz) if raiz else None
        },
        historial=historial,
        nombre_archivo="biseccion_completo"
    )
    print()
    
    return raiz, iteraciones, historial


def ejemplo_comparacion_metodos():
    """Ejemplo de comparación de métodos con exportación"""
    print("=" * 60)
    print("EJEMPLO: COMPARACIÓN DE MÉTODOS CON EXPORTACIÓN")
    print("=" * 60)
    
    def f(x):
        return x**3 - x - 1
    
    def f_derivada(x):
        return 3 * x**2 - 1
    
    print("Función: f(x) = x³ - x - 1")
    print()
    
    # Ejecutar diferentes métodos
    print("🔄 Ejecutando métodos...")
    
    # Bisección
    raiz_b, iter_b, conv_b, hist_b = biseccion(f, 1, 2, tolerancia=1e-6, mostrar_iteraciones=False)
    print(f"  Bisección: {iter_b} iteraciones → {raiz_b:.8f}")
    
    # Regula Falsi
    raiz_rf, iter_rf, conv_rf, hist_rf = regula_falsi(f, 1, 2, tolerancia=1e-6, mostrar_iteraciones=False)
    print(f"  Regula Falsi: {iter_rf} iteraciones → {raiz_rf:.8f}")
    
    # Newton
    raiz_n, iter_n, conv_n, hist_n = newton(f, f_derivada, 1.5, tolerancia=1e-6, mostrar_iteraciones=False)
    print(f"  Newton: {iter_n} iteraciones → {raiz_n:.8f}")
    
    # Secante
    raiz_s, iter_s, conv_s, hist_s = secante(f, 1, 2, tolerancia=1e-6, mostrar_iteraciones=False)
    print(f"  Secante: {iter_s} iteraciones → {raiz_s:.8f}")
    
    print()
    
    # Crear diccionario de comparación
    comparacion = {
        "biseccion": {
            "raiz": raiz_b,
            "iteraciones": iter_b,
            "convergencia": conv_b,
            "historial": hist_b
        },
        "regula_falsi": {
            "raiz": raiz_rf,
            "iteraciones": iter_rf,
            "convergencia": conv_rf,
            "historial": hist_rf
        },
        "newton": {
            "raiz": raiz_n,
            "iteraciones": iter_n,
            "convergencia": conv_n,
            "historial": hist_n
        },
        "secante": {
            "raiz": raiz_s,
            "iteraciones": iter_s,
            "convergencia": conv_s,
            "historial": hist_s
        }
    }
    
    # Exportar comparación
    print("📊 Exportando comparación de métodos...")
    archivo_comparacion = exportar_comparacion_csv(
        comparacion=comparacion,
        nombre_archivo="comparacion_metodos_ejemplo.csv",
        directorio="resultados"
    )
    print()
    
    # Exportar historiales individuales
    print("📋 Exportando historiales individuales...")
    
    exportar_iteraciones_csv(hist_b, "biseccion_historial.csv", "resultados")
    exportar_iteraciones_csv(hist_rf, "regula_falsi_historial.csv", "resultados")
    exportar_iteraciones_csv(hist_n, "newton_historial.csv", "resultados")
    exportar_iteraciones_csv(hist_s, "secante_historial.csv", "resultados")
    
    print()
    return comparacion


def ejemplo_exportacion_avanzada():
    """Ejemplo de exportación avanzada con múltiples formatos"""
    print("=" * 60)
    print("EJEMPLO: EXPORTACIÓN AVANZADA")
    print("=" * 60)
    
    from utils import exportar_a_json, crear_tabla_resumen
    
    def f(x):
        return x**2 - 2  # Para calcular √2
    
    def f_derivada(x):
        return 2 * x
    
    # Ejecutar métodos
    print("🔄 Ejecutando métodos para f(x) = x² - 2...")
    
    raiz_b, iter_b, conv_b, hist_b = biseccion(f, 1, 2, tolerancia=1e-8, mostrar_iteraciones=False)
    raiz_n, iter_n, conv_n, hist_n = newton(f, f_derivada, 1.5, tolerancia=1e-8, mostrar_iteraciones=False)
    
    print(f"  Bisección: {iter_b} iteraciones → √2 ≈ {raiz_b:.10f}")
    print(f"  Newton: {iter_n} iteraciones → √2 ≈ {raiz_n:.10f}")
    print()
    
    # Crear tabla resumen
    resultados = [
        {
            "metodo": "Bisección",
            "tipo": "Cerrado",
            "raiz": raiz_b,
            "iteraciones": iter_b,
            "convergencia": conv_b,
            "error_final": abs(raiz_b - 1.4142135623730951) if raiz_b else None,
            "tiempo": "N/A"
        },
        {
            "metodo": "Newton",
            "tipo": "Abierto",
            "raiz": raiz_n,
            "iteraciones": iter_n,
            "convergencia": conv_n,
            "error_final": abs(raiz_n - 1.4142135623730951) if raiz_n else None,
            "tiempo": "N/A"
        }
    ]
    
    # Exportar tabla resumen
    print("📊 Creando tabla resumen...")
    archivo_resumen = crear_tabla_resumen(
        resultados=resultados,
        nombre_archivo="resumen_calculo_raiz2.csv",
        directorio="resultados"
    )
    
    # Exportar a JSON
    print("📋 Exportando a JSON...")
    datos_json = {
        "funcion": "f(x) = x² - 2",
        "objetivo": "Calcular √2",
        "valor_exacto": 1.4142135623730951,
        "resultados": resultados,
        "historiales": {
            "biseccion": hist_b,
            "newton": hist_n
        }
    }
    
    archivo_json = exportar_a_json(
        data=datos_json,
        nombre_archivo="calculo_raiz2.json",
        directorio="resultados"
    )
    
    print()
    return datos_json


def mostrar_archivos_generados():
    """Muestra los archivos generados"""
    print("=" * 60)
    print("ARCHIVOS GENERADOS")
    print("=" * 60)
    
    from utils import listar_archivos_generados
    
    archivos = listar_archivos_generados("resultados")
    
    if not archivos:
        print("No se encontraron archivos generados.")
        return
    
    print(f"Se encontraron {len(archivos)} archivos:")
    print()
    
    for archivo in archivos:
        print(f"📄 {archivo['nombre']}")
        print(f"   📅 {archivo['fecha']}")
        print(f"   📏 {archivo['tamaño']} bytes")
        print(f"   📁 {archivo['ruta']}")
        print()


if __name__ == "__main__":
    print("PROYECTO NUMÉRICA - EJEMPLO DE EXPORTACIÓN")
    print("Demostración de funcionalidades de exportación a CSV y JSON")
    print()
    
    try:
        # Ejecutar ejemplos
        ejemplo_biseccion_con_exportacion()
        print()
        
        ejemplo_comparacion_metodos()
        print()
        
        ejemplo_exportacion_avanzada()
        print()
        
        mostrar_archivos_generados()
        
        print("✅ Todos los ejemplos se ejecutaron correctamente!")
        print("📁 Revisa la carpeta 'resultados/' para ver los archivos generados.")
        
    except Exception as e:
        print(f"❌ Error durante la ejecución: {e}")
        import traceback
        traceback.print_exc()
