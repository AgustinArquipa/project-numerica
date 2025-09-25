"""
Archivo principal para probar métodos de resolución de ecuaciones no lineales.

Este archivo contiene ejemplos de uso de todos los métodos implementados:
- Métodos cerrados: Bisección, Regula Falsi, Regula Falsi Modificada
- Métodos abiertos: Punto Fijo, Newton, Secante
"""

import sys
import os
from typing import Callable, Dict, Any

# Agregar el directorio raíz al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar métodos cerrados
from cerrados import biseccion, regula_falsi, regula_falsi_modificada
from cerrados.biseccion import biseccion_analisis
from cerrados.regula_falsi import regula_falsi_analisis, comparar_biseccion_regula_falsi
from cerrados.regula_falsi_modificada import regula_falsi_modificada_analisis, comparar_regula_falsi_variantes

# Importar métodos abiertos
from abiertos import punto_fijo, newton, secante
from abiertos.punto_fijo import punto_fijo_analisis, verificar_condicion_fourier, transformar_ecuacion_a_punto_fijo
from abiertos.newton import newton_analisis, newton_raphson, comparar_newton_variantes
from abiertos.secante import secante_analisis, secante_modificada, comparar_secante_variantes

# Importar utilidades
from utils.helpers import error_absoluto, error_relativo, aceleracion_aitken
from utils import exportar_iteraciones_csv, exportar_resultado_completo, exportar_comparacion_csv


def ejemplo_1():
    """Ejemplo 1: f(x) = x³ - x - 1 = 0"""
    print("=" * 60)
    print("EJEMPLO 1: f(x) = x³ - x - 1 = 0")
    print("=" * 60)
    
    def f(x):
        return x**3 - x - 1
    
    def f_derivada(x):
        return 3 * x**2 - 1
    
    def f_segunda_derivada(x):
        return 6 * x
    
    # Métodos cerrados
    print("\n--- MÉTODOS CERRADOS ---")
    print("Intervalo: [1, 2]")
    
    # Bisección
    print("\n1. MÉTODO DE BISECCIÓN:")
    raiz_b, iter_b, conv_b, hist_b = biseccion(f, 1, 2, tolerancia=1e-6, mostrar_iteraciones=False)
    print(f"   Raíz: {raiz_b:.8f}")
    print(f"   Iteraciones: {iter_b}")
    print(f"   Convergencia: {'✓' if conv_b else '✗'}")
    if raiz_b:
        print(f"   f(raíz) = {f(raiz_b):.2e}")
    
    # Regula Falsi
    print("\n2. MÉTODO DE REGULA FALSI:")
    raiz_rf, iter_rf, conv_rf, hist_rf = regula_falsi(f, 1, 2, tolerancia=1e-6, mostrar_iteraciones=False)
    print(f"   Raíz: {raiz_rf:.8f}")
    print(f"   Iteraciones: {iter_rf}")
    print(f"   Convergencia: {'✓' if conv_rf else '✗'}")
    if raiz_rf:
        print(f"   f(raíz) = {f(raiz_rf):.2e}")
    
    # Regula Falsi Modificada
    print("\n3. MÉTODO DE REGULA FALSI MODIFICADA:")
    raiz_rfm, iter_rfm, conv_rfm, hist_rfm = regula_falsi_modificada(
        f, 1, 2, tolerancia=1e-6, factor_reduccion=0.5, mostrar_iteraciones=False
    )
    print(f"   Raíz: {raiz_rfm:.8f}")
    print(f"   Iteraciones: {iter_rfm}")
    print(f"   Convergencia: {'✓' if conv_rfm else '✗'}")
    if raiz_rfm:
        print(f"   f(raíz) = {f(raiz_rfm):.2e}")
    
    # Métodos abiertos
    print("\n--- MÉTODOS ABIERTOS ---")
    
    # Punto Fijo
    print("\n4. MÉTODO DE PUNTO FIJO:")
    def g(x):
        return (x + 1)**(1/3)  # Transformación: x = g(x) donde g(x) = (x+1)^(1/3)
    
    def g_derivada(x):
        return (1/3) * (x + 1)**(-2/3)
    
    cumple_fourier, max_derivada = verificar_condicion_fourier(g, g_derivada, 1.5)
    print(f"   Condición de Fourier: {'✓' if cumple_fourier else '✗'} (max |g'| = {max_derivada:.4f})")
    
    raiz_pf, iter_pf, conv_pf, hist_pf = punto_fijo(g, 1.5, tolerancia=1e-6, mostrar_iteraciones=False)
    print(f"   Raíz: {raiz_pf:.8f}")
    print(f"   Iteraciones: {iter_pf}")
    print(f"   Convergencia: {'✓' if conv_pf else '✗'}")
    if raiz_pf:
        print(f"   g(raíz) - raíz = {g(raiz_pf) - raiz_pf:.2e}")
    
    # Newton
    print("\n5. MÉTODO DE NEWTON:")
    raiz_n, iter_n, conv_n, hist_n = newton(f, f_derivada, 1.5, tolerancia=1e-6, mostrar_iteraciones=False)
    print(f"   Raíz: {raiz_n:.8f}")
    print(f"   Iteraciones: {iter_n}")
    print(f"   Convergencia: {'✓' if conv_n else '✗'}")
    if raiz_n:
        print(f"   f(raíz) = {f(raiz_n):.2e}")
    
    # Secante
    print("\n6. MÉTODO DE LA SECANTE:")
    raiz_s, iter_s, conv_s, hist_s = secante(f, 1, 2, tolerancia=1e-6, mostrar_iteraciones=False)
    print(f"   Raíz: {raiz_s:.8f}")
    print(f"   Iteraciones: {iter_s}")
    print(f"   Convergencia: {'✓' if conv_s else '✗'}")
    if raiz_s:
        print(f"   f(raíz) = {f(raiz_s):.2e}")
    
    # Comparación
    print("\n--- COMPARACIÓN DE VELOCIDAD ---")
    metodos_cerrados = [
        ("Bisección", iter_b),
        ("Regula Falsi", iter_rf),
        ("Regula Falsi Modificada", iter_rfm)
    ]
    metodos_abiertos = [
        ("Punto Fijo", iter_pf),
        ("Newton", iter_n),
        ("Secante", iter_s)
    ]
    
    print("Métodos cerrados:")
    for nombre, iteraciones in metodos_cerrados:
        print(f"  {nombre}: {iteraciones} iteraciones")
    
    print("Métodos abiertos:")
    for nombre, iteraciones in metodos_abiertos:
        print(f"  {nombre}: {iteraciones} iteraciones")


def ejemplo_2():
    """Ejemplo 2: f(x) = e^x - 3x = 0"""
    print("\n" + "=" * 60)
    print("EJEMPLO 2: f(x) = e^x - 3x = 0")
    print("=" * 60)
    
    import math
    
    def f(x):
        return math.exp(x) - 3 * x
    
    def f_derivada(x):
        return math.exp(x) - 3
    
    def f_segunda_derivada(x):
        return math.exp(x)
    
    # Métodos cerrados
    print("\n--- MÉTODOS CERRADOS ---")
    print("Intervalo: [1, 2]")
    
    # Bisección
    raiz_b, iter_b, conv_b, hist_b = biseccion(f, 1, 2, tolerancia=1e-6, mostrar_iteraciones=False)
    print(f"\nBisección: {iter_b} iteraciones → Raíz: {raiz_b:.8f}")
    
    # Regula Falsi
    raiz_rf, iter_rf, conv_rf, hist_rf = regula_falsi(f, 1, 2, tolerancia=1e-6, mostrar_iteraciones=False)
    print(f"Regula Falsi: {iter_rf} iteraciones → Raíz: {raiz_rf:.8f}")
    
    # Métodos abiertos
    print("\n--- MÉTODOS ABIERTOS ---")
    
    # Newton
    raiz_n, iter_n, conv_n, hist_n = newton(f, f_derivada, 1.0, tolerancia=1e-6, mostrar_iteraciones=False)
    print(f"Newton: {iter_n} iteraciones → Raíz: {raiz_n:.8f}")
    
    # Secante
    raiz_s, iter_s, conv_s, hist_s = secante(f, 1, 2, tolerancia=1e-6, mostrar_iteraciones=False)
    print(f"Secante: {iter_s} iteraciones → Raíz: {raiz_s:.8f}")


def ejemplo_3():
    """Ejemplo 3: f(x) = x² - 2 = 0 (raíz cuadrada de 2)"""
    print("\n" + "=" * 60)
    print("EJEMPLO 3: f(x) = x² - 2 = 0 (√2)")
    print("=" * 60)
    
    import math
    
    def f(x):
        return x**2 - 2
    
    def f_derivada(x):
        return 2 * x
    
    def f_segunda_derivada(x):
        return 2
    
    valor_exacto = math.sqrt(2)
    print(f"Valor exacto de √2: {valor_exacto:.10f}")
    
    # Métodos cerrados
    print("\n--- MÉTODOS CERRADOS ---")
    print("Intervalo: [1, 2]")
    
    # Bisección
    raiz_b, iter_b, conv_b, hist_b = biseccion(f, 1, 2, tolerancia=1e-8, mostrar_iteraciones=False)
    error_b = error_absoluto(valor_exacto, raiz_b) if raiz_b else None
    print(f"\nBisección: {iter_b} iteraciones")
    print(f"  Raíz: {raiz_b:.10f}")
    print(f"  Error absoluto: {error_b:.2e}")
    
    # Métodos abiertos
    print("\n--- MÉTODOS ABIERTOS ---")
    
    # Newton
    raiz_n, iter_n, conv_n, hist_n = newton(f, f_derivada, 1.5, tolerancia=1e-8, mostrar_iteraciones=False)
    error_n = error_absoluto(valor_exacto, raiz_n) if raiz_n else None
    print(f"\nNewton: {iter_n} iteraciones")
    print(f"  Raíz: {raiz_n:.10f}")
    print(f"  Error absoluto: {error_n:.2e}")
    
    # Secante
    raiz_s, iter_s, conv_s, hist_s = secante(f, 1, 2, tolerancia=1e-8, mostrar_iteraciones=False)
    error_s = error_absoluto(valor_exacto, raiz_s) if raiz_s else None
    print(f"\nSecante: {iter_s} iteraciones")
    print(f"  Raíz: {raiz_s:.10f}")
    print(f"  Error absoluto: {error_s:.2e}")


def ejemplo_analisis_completo():
    """Ejemplo con análisis completo de un método"""
    print("\n" + "=" * 60)
    print("ANÁLISIS COMPLETO DEL MÉTODO DE NEWTON")
    print("=" * 60)
    
    def f(x):
        return x**3 - x - 1
    
    def f_derivada(x):
        return 3 * x**2 - 1
    
    def f_segunda_derivada(x):
        return 6 * x
    
    # Análisis completo
    analisis = newton_analisis(f, f_derivada, 1.5, tolerancia=1e-6)
    
    print(f"Raíz encontrada: {analisis['raiz_encontrada']:.8f}")
    print(f"Iteraciones usadas: {analisis['iteraciones_usadas']}")
    print(f"Convergencia alcanzada: {'✓' if analisis['convergencia_alcanzada'] else '✗'}")
    
    if analisis['convergencia_alcanzada']:
        print(f"Valor de f(raíz): {analisis['valor_funcion_raiz']:.2e}")
        
        if 'velocidad_convergencia_cuadratica' in analisis:
            print(f"Velocidad de convergencia cuadrática: {analisis['velocidad_convergencia_cuadratica']:.4f}")
        
        print(f"Derivada mínima: {analisis['min_derivada']:.2e}")
        print(f"Derivada máxima: {analisis['max_derivada']:.2e}")
        print(f"Derivada promedio: {analisis['derivada_promedio']:.2e}")
        
        if analisis.get('advertencia_derivada_pequena'):
            print("⚠️  Advertencia: Se detectaron derivadas muy pequeñas")


def menu_interactivo():
    """Menú interactivo para probar métodos"""
    print("\n" + "=" * 60)
    print("MENÚ INTERACTIVO - MÉTODOS NUMÉRICOS")
    print("=" * 60)
    
    while True:
        print("\nOpciones disponibles:")
        print("1. Ejemplo 1: f(x) = x³ - x - 1 = 0")
        print("2. Ejemplo 2: f(x) = e^x - 3x = 0")
        print("3. Ejemplo 3: f(x) = x² - 2 = 0 (√2)")
        print("4. Análisis completo de Newton")
        print("5. Comparación de métodos cerrados")
        print("6. Comparación de métodos abiertos")
        print("7. Demostración de exportación a CSV")
        print("8. Salir")
        
        try:
            opcion = input("\nSelecciona una opción (1-8): ").strip()
            
            if opcion == "1":
                ejemplo_1()
            elif opcion == "2":
                ejemplo_2()
            elif opcion == "3":
                ejemplo_3()
            elif opcion == "4":
                ejemplo_analisis_completo()
            elif opcion == "5":
                comparacion_metodos_cerrados()
            elif opcion == "6":
                comparacion_metodos_abiertos()
            elif opcion == "7":
                demostracion_exportacion()
            elif opcion == "8":
                print("¡Hasta luego!")
                break
            else:
                print("Opción no válida. Por favor, selecciona 1-8.")
                
        except KeyboardInterrupt:
            print("\n\n¡Hasta luego!")
            break
        except Exception as e:
            print(f"Error: {e}")


def comparacion_metodos_cerrados():
    """Comparación detallada de métodos cerrados"""
    print("\n" + "=" * 60)
    print("COMPARACIÓN DE MÉTODOS CERRADOS")
    print("=" * 60)
    
    def f(x):
        return x**3 - x - 1
    
    # Comparar bisección vs regula falsi
    print("\nComparación Bisección vs Regula Falsi:")
    comparacion = comparar_biseccion_regula_falsi(f, 1, 2)
    
    print(f"Bisección: {comparacion['biseccion']['iteraciones']} iteraciones")
    print(f"Regula Falsi: {comparacion['regula_falsi']['iteraciones']} iteraciones")
    
    if 'analisis' in comparacion:
        print(f"Método más rápido: {comparacion['analisis']['metodo_mas_rapido']}")
        print(f"Diferencia en iteraciones: {comparacion['analisis']['diferencia_iteraciones']}")
    
    # Comparar variantes de regula falsi
    print("\nComparación de variantes de Regula Falsi:")
    comparacion_rf = comparar_regula_falsi_variantes(f, 1, 2)
    
    for metodo, datos in comparacion_rf.items():
        if isinstance(datos, dict) and 'iteraciones' in datos:
            print(f"{metodo}: {datos['iteraciones']} iteraciones")


def comparacion_metodos_abiertos():
    """Comparación detallada de métodos abiertos"""
    print("\n" + "=" * 60)
    print("COMPARACIÓN DE MÉTODOS ABIERTOS")
    print("=" * 60)
    
    def f(x):
        return x**3 - x - 1
    
    def f_derivada(x):
        return 3 * x**2 - 1
    
    def f_segunda_derivada(x):
        return 6 * x
    
    # Comparar Newton vs Newton-Raphson
    print("\nComparación Newton vs Newton-Raphson:")
    comparacion_n = comparar_newton_variantes(f, f_derivada, f_segunda_derivada, 1.5)
    
    print(f"Newton: {comparacion_n['newton']['iteraciones']} iteraciones")
    print(f"Newton-Raphson: {comparacion_n['newton_raphson']['iteraciones']} iteraciones")
    
    # Comparar variantes de secante
    print("\nComparación de variantes de Secante:")
    comparacion_s = comparar_secante_variantes(f, 1, 2)
    
    print(f"Secante: {comparacion_s['secante']['iteraciones']} iteraciones")
    print(f"Secante Modificada: {comparacion_s['secante_modificada']['iteraciones']} iteraciones")


def demostracion_exportacion():
    """Demostración de funcionalidades de exportación"""
    print("\n" + "=" * 60)
    print("DEMOSTRACIÓN DE EXPORTACIÓN A CSV")
    print("=" * 60)
    
    def f(x):
        return x**3 - x - 1
    
    def f_derivada(x):
        return 3 * x**2 - 1
    
    print("Función: f(x) = x³ - x - 1")
    print("Vamos a exportar resultados de diferentes métodos...")
    print()
    
    # Ejecutar métodos
    print("🔄 Ejecutando métodos...")
    
    # Bisección
    raiz_b, iter_b, conv_b, hist_b = biseccion(f, 1, 2, tolerancia=1e-6, mostrar_iteraciones=False)
    print(f"  ✓ Bisección: {iter_b} iteraciones")
    
    # Newton
    raiz_n, iter_n, conv_n, hist_n = newton(f, f_derivada, 1.5, tolerancia=1e-6, mostrar_iteraciones=False)
    print(f"  ✓ Newton: {iter_n} iteraciones")
    
    print()
    
    # Exportar historiales individuales
    print("📊 Exportando historiales a CSV...")
    
    archivo_biseccion = exportar_iteraciones_csv(
        historial=hist_b,
        nombre_archivo="demo_biseccion.csv",
        directorio="resultados"
    )
    
    archivo_newton = exportar_iteraciones_csv(
        historial=hist_n,
        nombre_archivo="demo_newton.csv", 
        directorio="resultados"
    )
    
    # Exportar resultado completo de bisección
    print("\n📋 Exportando resultado completo...")
    archivo_completo = exportar_resultado_completo(
        metodo="Bisección",
        funcion="f(x) = x³ - x - 1",
        parametros={"a": 1.0, "b": 2.0, "tolerancia": 1e-6},
        resultado={
            "raiz": raiz_b,
            "iteraciones": iter_b,
            "convergencia": conv_b,
            "valor_funcion_raiz": f(raiz_b) if raiz_b else None
        },
        historial=hist_b,
        nombre_archivo="demo_completo"
    )
    
    # Crear comparación
    print("\n📈 Creando comparación de métodos...")
    comparacion = {
        "biseccion": {
            "raiz": raiz_b,
            "iteraciones": iter_b,
            "convergencia": conv_b
        },
        "newton": {
            "raiz": raiz_n,
            "iteraciones": iter_n,
            "convergencia": conv_n
        }
    }
    
    archivo_comparacion = exportar_comparacion_csv(
        comparacion=comparacion,
        nombre_archivo="demo_comparacion.csv",
        directorio="resultados"
    )
    
    print()
    print("✅ Exportación completada!")
    print("📁 Revisa la carpeta 'resultados/' para ver los archivos generados:")
    print(f"   - {os.path.basename(archivo_biseccion)}")
    print(f"   - {os.path.basename(archivo_newton)}")
    print(f"   - {os.path.basename(archivo_completo)}")
    print(f"   - {os.path.basename(archivo_comparacion)}")
    
    print("\n💡 Tip: Puedes abrir estos archivos CSV en Excel, Google Sheets o cualquier editor de texto")
    print("   para analizar las iteraciones y comparar los métodos.")


if __name__ == "__main__":
    print("PROYECTO NUMÉRICA - MÉTODOS DE RESOLUCIÓN DE ECUACIONES NO LINEALES")
    print("Desarrollado para la materia Programación Numérica")
    print("Tema III: Resolución de Ecuaciones no Lineales")
    
    # Ejecutar ejemplos automáticamente
    ejemplo_1()
    ejemplo_2()
    ejemplo_3()
    ejemplo_analisis_completo()
    
    # Mostrar menú interactivo
    menu_interactivo()
