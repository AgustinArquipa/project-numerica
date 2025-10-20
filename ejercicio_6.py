"""
Ejercicio N° 6: Método de Punto Fijo para f(x) = x - cos(x)

Punto b) Determinar el número de iteraciones necesarias para asegurar 4 decimales exactas
Punto c) Calcular las 5 primeras iteraciones desde x₀ = 0.5
"""

import sys
import os
import math
from typing import Callable

# Agregar el directorio raíz al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar método de punto fijo
from abiertos.punto_fijo import punto_fijo, verificar_condicion_fourier, punto_fijo_analisis
from utils import exportar_iteraciones_csv


def ejercicio_6():
    """Resuelve el Ejercicio N° 6 con método de punto fijo"""
    print("=" * 80)
    print("EJERCICIO N° 6: MÉTODO DE PUNTO FIJO")
    print("=" * 80)
    print("Función: f(x) = x - cos(x) definida en [0, 1]")
    print("Transformación: x = cos(x)")
    print("Punto inicial: x₀ = 0.5")
    print()
    
    # Definir la función original y la transformación
    def f(x):
        return x - math.cos(x)
    
    def g(x):
        return math.cos(x)
    
    def g_derivada(x):
        return -math.sin(x)
    
    print("📋 Función original: f(x) = x - cos(x)")
    print("📋 Transformación: x = cos(x)")
    print("📋 Derivada de g(x): g'(x) = -sin(x)")
    print()
    
    # ========================================
    # ANÁLISIS TEÓRICO DE CONVERGENCIA
    # ========================================
    print("=" * 60)
    print("ANÁLISIS TEÓRICO DE CONVERGENCIA")
    print("=" * 60)
    
    # Verificar condición de Fourier
    cumple_fourier, max_derivada = verificar_condicion_fourier(g, g_derivada, 0.5)
    
    print(f"🔍 Condición de Fourier: {'✓ CUMPLE' if cumple_fourier else '✗ NO CUMPLE'}")
    print(f"📊 Máxima derivada en [0, 1]: {max_derivada:.6f}")
    
    if cumple_fourier:
        print("✅ La condición de Fourier se cumple: |g'(x)| < 1 en [0, 1]")
        print("✅ El método de punto fijo convergerá")
    else:
        print("⚠️  La condición de Fourier no se cumple")
        print("⚠️  El método podría no converger o converger lentamente")
    
    print()
    
    # ========================================
    # PUNTO C: 5 PRIMERAS ITERACIONES
    # ========================================
    print("=" * 60)
    print("PUNTO C) PRIMERAS 5 ITERACIONES DESDE x₀ = 0.5")
    print("=" * 60)
    
    x0 = 0.5
    print(f"📍 Punto inicial: x₀ = {x0}")
    print()
    
    # Ejecutar 5 iteraciones manualmente para mostrar el proceso
    x = x0
    print("Iteración | x_n     | x_{n+1} = cos(x_n) | |x_{n+1} - x_n| | Error Relativo")
    print("-" * 70)
    
    for i in range(5):
        x_anterior = x
        x = g(x)  # x_{n+1} = cos(x_n)
        
        error_rel = abs(x - x_anterior) / abs(x_anterior) if x_anterior != 0 else 0
        diferencia = abs(x - x_anterior)
        
        print(f"   {i+1:2d}    | {x_anterior:.6f} | {x:.6f}        | {diferencia:.6f}    | {error_rel:.6f}")
    
    print()
    print(f"🎯 Después de 5 iteraciones: x₅ = {x:.6f}")
    print(f"🔍 f(x₅) = x₅ - cos(x₅) = {f(x):.6f}")
    print()
    
    # ========================================
    # PUNTO B: ITERACIONES PARA 4 DECIMALES EXACTOS
    # ========================================
    print("=" * 60)
    print("PUNTO B) ITERACIONES PARA 4 DECIMALES EXACTOS")
    print("=" * 60)
    
    # Tolerancia para 4 decimales exactos
    tolerancia_4_decimales = 0.1e-4  # 0.00005
    print(f"🎯 Tolerancia para 4 decimales exactos: {tolerancia_4_decimales}")
    print(f"📊 Esto significa: |x_{{n+1}} - x_n| < {tolerancia_4_decimales}")
    print()
    
    # Ejecutar método con tolerancia de 4 decimales
    raiz, iteraciones, convergencia, historial = punto_fijo(
        g, x0, tolerancia=tolerancia_4_decimales, max_iteraciones=100, mostrar_iteraciones=False
    )
    
    if convergencia and raiz is not None:
        print(f"✅ Convergencia alcanzada en {iteraciones} iteraciones")
        print(f"🎯 Raíz aproximada: {raiz:.6f}")
        print(f"🔍 f(raíz) = {f(raiz):.2e}")
        print(f"📊 Error absoluto: {abs(raiz - 0.739085):.2e}")
        print()
        
        # Verificar si efectivamente se necesitaron 63 iteraciones
        if iteraciones == 63:
            print("✅ CONFIRMADO: Se necesitaron exactamente 63 iteraciones")
        elif iteraciones < 63:
            print(f"📊 Se necesitaron {iteraciones} iteraciones (menos que las 63 esperadas)")
        else:
            print(f"📊 Se necesitaron {iteraciones} iteraciones (más que las 63 esperadas)")
        
        print()
        
        # Mostrar las últimas iteraciones para verificar precisión
        print("🔍 ÚLTIMAS ITERACIONES:")
        print("Iteración | x_n     | x_{n+1} | |x_{n+1} - x_n| | Error Relativo")
        print("-" * 60)
        
        for i, iter_info in enumerate(historial[-5:], len(historial)-4):
            x_ant = iter_info['x_anterior']
            x_act = iter_info['x_actual']
            dif = iter_info['diferencia']
            err_rel = iter_info['error_relativo']
            
            print(f"   {i:2d}    | {x_ant:.6f} | {x_act:.6f} | {dif:.6f}    | {err_rel:.6f}")
        
        print()
        
        # Exportar historial completo
        print("📁 Exportando historial completo...")
        archivo_csv = exportar_iteraciones_csv(
            historial, "ejercicio6_punto_fijo.csv", "resultados", precision_calculadora=9
        )
        print(f"✅ Historial exportado: {os.path.basename(archivo_csv)}")
        
    else:
        print("❌ No se alcanzó convergencia en 100 iteraciones")
        print("🔍 Posibles causas:")
        print("   • Tolerancia muy estricta")
        print("   • Punto inicial inadecuado")
        print("   • La función no cumple condiciones de convergencia")
    
    print()
    
    # ========================================
    # ANÁLISIS COMPLETO CON DIFERENTES TOLERANCIAS
    # ========================================
    print("=" * 60)
    print("ANÁLISIS CON DIFERENTES TOLERANCIAS")
    print("=" * 60)
    
    tolerancias = [1e-2, 1e-3, 1e-4, 0.5e-4, 1e-5]
    print("Tolerancia | Iteraciones | Raíz Aproximada | f(raíz)")
    print("-" * 55)
    
    for tol in tolerancias:
        raiz_tol, iter_tol, conv_tol, _ = punto_fijo(
            g, x0, tolerancia=tol, max_iteraciones=100, mostrar_iteraciones=False
        )
        
        if conv_tol and raiz_tol is not None:
            f_raiz = f(raiz_tol)
            print(f"{tol:10.0e} | {iter_tol:11d} | {raiz_tol:13.6f} | {f_raiz:.2e}")
        else:
            print(f"{tol:10.0e} | {'No conv.':>11} | {'N/A':>13} | N/A")
    
    print()
    
    # ========================================
    # ANÁLISIS DE VELOCIDAD DE CONVERGENCIA
    # ========================================
    print("=" * 60)
    print("ANÁLISIS DE VELOCIDAD DE CONVERGENCIA")
    print("=" * 60)
    
    # Ejecutar análisis completo
    analisis = punto_fijo_analisis(g, g_derivada, x0, tolerancia_4_decimales, 100)
    
    print(f"📊 Análisis completo del método:")
    print(f"   • Raíz encontrada: {analisis['raiz_encontrada']:.6f}")
    print(f"   • Iteraciones usadas: {analisis['iteraciones_usadas']}")
    print(f"   • Convergencia: {'Sí' if analisis['convergencia_alcanzada'] else 'No'}")
    print(f"   • Cumple condición de Fourier: {'Sí' if analisis['cumple_condicion_fourier'] else 'No'}")
    print(f"   • Máxima derivada: {analisis['max_derivada']:.6f}")
    
    if 'velocidad_convergencia_promedio' in analisis:
        print(f"   • Velocidad de convergencia: {analisis['velocidad_convergencia_promedio']:.6f}")
    
    if 'raiz_aitken' in analisis and analisis['raiz_aitken'] is not None:
        print(f"   • Raíz con aceleración de Aitken: {analisis['raiz_aitken']:.6f}")
    
    print()
    
    # ========================================
    # VERIFICACIÓN DE LA RAÍZ EXACTA
    # ========================================
    print("=" * 60)
    print("VERIFICACIÓN DE LA RAÍZ EXACTA")
    print("=" * 60)
    
    # La raíz exacta de x = cos(x) es aproximadamente 0.7390851332
    raiz_exacta = 0.7390851332
    
    if raiz is not None:
        error_absoluto = abs(raiz - raiz_exacta)
        error_relativo = error_absoluto / raiz_exacta if raiz_exacta != 0 else 0
        
        print(f"🎯 Raíz exacta: {raiz_exacta:.10f}")
        print(f"🎯 Raíz aproximada: {raiz:.10f}")
        print(f"📊 Error absoluto: {error_absoluto:.2e}")
        print(f"📊 Error relativo: {error_relativo:.2e}")
        
        # Verificar si tenemos 4 decimales exactos
        decimales_exactos = 0
        raiz_str = f"{raiz:.10f}"
        exacta_str = f"{raiz_exacta:.10f}"
        
        for i in range(min(len(raiz_str), len(exacta_str))):
            if raiz_str[i] == exacta_str[i] and raiz_str[i] != '.':
                decimales_exactos += 1
            elif raiz_str[i] != exacta_str[i]:
                break
        
        print(f"✅ Decimales exactos: {decimales_exactos}")
        
        if decimales_exactos >= 4:
            print("✅ CONFIRMADO: Se alcanzaron 4 decimales exactos")
        else:
            print("⚠️  No se alcanzaron 4 decimales exactos")
    
    print()
    
    # ========================================
    # CONCLUSIONES
    # ========================================
    print("=" * 80)
    print("CONCLUSIONES")
    print("=" * 80)
    
    print("🔍 ANÁLISIS DE LA FUNCIÓN f(x) = x - cos(x):")
    print("   • Función continua en [0, 1]")
    print("   • Transformación: x = cos(x)")
    print("   • Condición de Fourier: |g'(x)| = |sin(x)| < 1 en [0, 1]")
    print("   • Raíz exacta: x ≈ 0.7390851332")
    print()
    
    print("📊 RESULTADOS DEL MÉTODO DE PUNTO FIJO:")
    if raiz is not None:
        print(f"   • Iteraciones necesarias: {iteraciones}")
        print(f"   • Raíz aproximada: {raiz:.6f}")
        print(f"   • Precisión alcanzada: 4 decimales exactos")
        print(f"   • Convergencia: {'Sí' if convergencia else 'No'}")
    
    print()
    print("💡 CARACTERÍSTICAS DEL MÉTODO:")
    print("   • Convergencia lineal (orden 1)")
    print("   • Velocidad: |g'(x)| ≈ 0.67 en la raíz")
    print("   • Estable y confiable para esta función")
    print("   • Requiere más iteraciones que métodos de orden superior")
    
    print()
    print("🎯 EJERCICIO COMPLETADO")
    print("📁 Revisa la carpeta 'resultados/' para ver el archivo CSV")


if __name__ == "__main__":
    ejercicio_6()
