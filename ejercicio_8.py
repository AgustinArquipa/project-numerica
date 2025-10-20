"""
Ejercicio N° 8: Método de Bisección para f(x) = x - cos(x)

1. Estudiar la convergencia del método de bisección
2. Determinar el número de iteraciones para asegurar t dígitos decimales de precisión
3. Calcular iteraciones necesarias para 4 decimales de precisión
4. Encontrar la raíz usando bisección
5. Indicar cuántas iteraciones realizó el método
"""

import sys
import os
import math
from typing import Callable

# Agregar el directorio raíz al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar método de bisección
from cerrados import biseccion
from utils import exportar_iteraciones_csv


def ejercicio_8():
    """Resuelve el Ejercicio N° 8 con método de bisección"""
    print("=" * 80)
    print("EJERCICIO N° 8: MÉTODO DE BISECCIÓN")
    print("=" * 80)
    print("Función: f(x) = x - cos(x)")
    print("Intervalo: [0, 1]")
    print("Precisión objetivo: 4 decimales")
    print()
    
    # Definir la función
    def f(x):
        return x - math.cos(x)
    
    # Intervalo de búsqueda
    a, b = 0.0, 1.0
    
    print("📋 Función: f(x) = x - cos(x)")
    print("📋 Primera derivada: f'(x) = 1 + sen(x)")
    print("📋 Intervalo: [0, 1]")
    print()
    
    # ========================================
    # ANÁLISIS TEÓRICO DE CONVERGENCIA
    # ========================================
    print("=" * 60)
    print("1) ESTUDIO DE LA CONVERGENCIA DEL MÉTODO DE BISECCIÓN")
    print("=" * 60)
    
    print("📐 FÓRMULA DE CONVERGENCIA:")
    print("   |x_n - x*| ≤ (b - a) / 2^n")
    print("   donde:")
    print("   • x_n = aproximación en la iteración n")
    print("   • x* = raíz exacta")
    print("   • [a, b] = intervalo inicial")
    print("   • n = número de iteraciones")
    print()
    
    print("🔍 CONDICIONES PARA CONVERGENCIA:")
    print("   ✅ f(x) es continua en [a, b]")
    print("   ✅ f(a) · f(b) < 0 (cambio de signo)")
    print("   ✅ La raíz es única en el intervalo")
    print()
    
    # Verificar condiciones
    f_a = f(a)
    f_b = f(b)
    print(f"📊 Verificación de condiciones:")
    print(f"   • f(0) = {f_a:.6f}")
    print(f"   • f(1) = {f_b:.6f}")
    print(f"   • f(0) · f(1) = {f_a * f_b:.6f}")
    
    if f_a * f_b < 0:
        print("   ✅ Condición de cambio de signo: CUMPLE")
    else:
        print("   ❌ Condición de cambio de signo: NO CUMPLE")
        return
    
    print()
    
    # ========================================
    # CÁLCULO TEÓRICO DE ITERACIONES
    # ========================================
    print("=" * 60)
    print("2) CÁLCULO DEL NÚMERO DE ITERACIONES PARA t DÍGITOS DECIMALES")
    print("=" * 60)
    
    print("📐 FÓRMULA GENERAL:")
    print("   Para asegurar t dígitos decimales de precisión:")
    print("   |x_n - x*| ≤ 0.5 × 10^(-t)")
    print()
    print("   Igualando con la fórmula de bisección:")
    print("   (b - a) / 2^n ≤ 0.5 × 10^(-t)")
    print("   (b - a) / (0.5 × 10^(-t)) ≤ 2^n")
    print("   log₂((b - a) / (0.5 × 10^(-t))) ≤ n")
    print()
    
    # Calcular para diferentes precisiones
    precisiones = [1, 2, 3, 4, 5, 6]
    print("📊 ITERACIONES NECESARIAS PARA DIFERENTES PRECISIONES:")
    print("Precisión (t) | Tolerancia | Iteraciones Teóricas")
    print("-" * 50)
    
    for t in precisiones:
        tolerancia = 0.5 * 10**(-t)
        iteraciones_teoricas = math.ceil(math.log2((b - a) / tolerancia))
        print(f"     {t:2d}       | {tolerancia:10.0e} | {iteraciones_teoricas:18d}")
    
    print()
    
    # ========================================
    # APLICACIÓN ESPECÍFICA PARA 4 DECIMALES
    # ========================================
    print("=" * 60)
    print("3) APLICACIÓN PARA f(x) = x - cos(x) CON 4 DECIMALES")
    print("=" * 60)
    
    t = 4  # 4 decimales de precisión
    tolerancia_4_decimales = 0.5 * 10**(-t)
    iteraciones_teoricas_4 = math.ceil(math.log2((b - a) / tolerancia_4_decimales))
    
    print(f"🎯 Precisión objetivo: {t} decimales")
    print(f"📊 Tolerancia requerida: {tolerancia_4_decimales:.0e}")
    print(f"📐 Iteraciones teóricas: {iteraciones_teoricas_4}")
    print()
    
    print("📋 CÁLCULO DETALLADO:")
    print(f"   • Intervalo inicial: [{a}, {b}]")
    print(f"   • Longitud inicial: {b - a}")
    print(f"   • Tolerancia: {tolerancia_4_decimales:.0e}")
    print(f"   • Cálculo: log₂({b - a} / {tolerancia_4_decimales:.0e}) = {math.log2((b - a) / tolerancia_4_decimales):.2f}")
    print(f"   • Redondeado hacia arriba: {iteraciones_teoricas_4}")
    print()
    
    # ========================================
    # IMPLEMENTACIÓN DEL MÉTODO DE BISECCIÓN
    # ========================================
    print("=" * 60)
    print("4) IMPLEMENTACIÓN DEL MÉTODO DE BISECCIÓN")
    print("=" * 60)
    
    print(f"📍 Punto inicial: a = {a}, b = {b}")
    print(f"🎯 Tolerancia: {tolerancia_4_decimales:.0e}")
    print(f"🔄 Máximo de iteraciones: {iteraciones_teoricas_4 + 5}")
    print()
    
    # Ejecutar método de bisección
    raiz, iteraciones, convergencia, historial = biseccion(
        f, a, b, 
        tolerancia=tolerancia_4_decimales, 
        max_iteraciones=iteraciones_teoricas_4 + 5,
        mostrar_iteraciones=False
    )
    
    if convergencia and raiz is not None:
        print(f"✅ Convergencia alcanzada en {iteraciones} iteraciones")
        print(f"🎯 Raíz aproximada: {raiz:.6f}")
        print(f"🔍 f(raíz) = {f(raiz):.2e}")
        print(f"📊 Error absoluto estimado: {tolerancia_4_decimales/2:.2e}")
        print()
        
        # Verificar si coincide con la predicción teórica
        if iteraciones == iteraciones_teoricas_4:
            print("✅ CONFIRMADO: Iteraciones reales = Iteraciones teóricas")
        elif iteraciones < iteraciones_teoricas_4:
            print(f"📊 Iteraciones reales ({iteraciones}) < Iteraciones teóricas ({iteraciones_teoricas_4})")
            print("💡 El método convergió antes de lo esperado")
        else:
            print(f"📊 Iteraciones reales ({iteraciones}) > Iteraciones teóricas ({iteraciones_teoricas_4})")
            print("⚠️  El método necesitó más iteraciones de lo esperado")
        
        print()
        
        # Mostrar las primeras iteraciones
        print("📊 PRIMERAS 5 ITERACIONES:")
        print("Iteración | a        | b        | c = (a+b)/2 | f(c)      | |b-a|/2")
        print("-" * 70)
        
        for i, iter_info in enumerate(historial[:5], 1):
            a_val = iter_info['a']
            b_val = iter_info['b']
            c_val = iter_info['c']
            f_c = iter_info['f(c)']
            error_estimado = iter_info['longitud_intervalo'] / 2
            
            print(f"   {i:2d}    | {a_val:.6f} | {b_val:.6f} | {c_val:.6f} | {f_c:8.2e} | {error_estimado:.2e}")
        
        print()
        
        # Mostrar las últimas iteraciones
        print("📊 ÚLTIMAS 5 ITERACIONES:")
        print("Iteración | a        | b        | c = (a+b)/2 | f(c)      | |b-a|/2")
        print("-" * 70)
        
        for i, iter_info in enumerate(historial[-5:], len(historial)-4):
            a_val = iter_info['a']
            b_val = iter_info['b']
            c_val = iter_info['c']
            f_c = iter_info['f(c)']
            error_estimado = iter_info['longitud_intervalo'] / 2
            
            print(f"   {i:2d}    | {a_val:.6f} | {b_val:.6f} | {c_val:.6f} | {f_c:8.2e} | {error_estimado:.2e}")
        
        print()
        
        # Exportar historial completo
        print("📁 Exportando historial completo...")
        archivo_csv = exportar_iteraciones_csv(
            historial, "ejercicio8_biseccion.csv", "resultados", precision_calculadora=9
        )
        print(f"✅ Historial exportado: {os.path.basename(archivo_csv)}")
        
    else:
        print("❌ No se alcanzó convergencia")
        print("🔍 Posibles causas:")
        print("   • Intervalo inicial incorrecto")
        print("   • Función no tiene cambio de signo")
        print("   • Máximo de iteraciones insuficiente")
    
    print()
    
    # ========================================
    # ANÁLISIS DE PRECISIÓN ALCANZADA
    # ========================================
    print("=" * 60)
    print("5) ANÁLISIS DE PRECISIÓN ALCANZADA")
    print("=" * 60)
    
    if raiz is not None:
        # La raíz exacta de x = cos(x) es aproximadamente 0.7390851332
        raiz_exacta = 0.7390851332
        
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
        
        # Comparar con el error teórico
        error_teorico = (b - a) / (2**iteraciones)
        print(f"📐 Error teórico máximo: {error_teorico:.2e}")
        print(f"📊 Error real: {error_absoluto:.2e}")
        print(f"📊 Relación error_real/error_teorico: {error_absoluto/error_teorico:.2f}")
    
    print()
    
    # ========================================
    # COMPARACIÓN CON OTROS MÉTODOS
    # ========================================
    print("=" * 60)
    print("6) COMPARACIÓN CON OTROS MÉTODOS")
    print("=" * 60)
    
    print("📊 COMPARACIÓN DE EFICIENCIA:")
    print("   • Bisección: Convergencia lineal (orden 1)")
    print("   • Newton: Convergencia cuadrática (orden 2)")
    print("   • Punto Fijo: Convergencia lineal (orden 1)")
    print("   • Halley: Convergencia cúbica (orden 3)")
    print()
    
    print("💡 VENTAJAS DEL MÉTODO DE BISECCIÓN:")
    print("   ✅ Garantiza convergencia si hay cambio de signo")
    print("   ✅ Simple de implementar")
    print("   ✅ Estable numéricamente")
    print("   ✅ No requiere derivadas")
    print()
    
    print("⚠️  DESVENTAJAS:")
    print("   ❌ Convergencia lenta (lineal)")
    print("   ❌ Requiere intervalo con cambio de signo")
    print("   ❌ No aprovecha información de la función")
    
    print()
    
    # ========================================
    # CONCLUSIONES FINALES
    # ========================================
    print("=" * 80)
    print("CONCLUSIONES FINALES")
    print("=" * 80)
    
    print("🔍 ANÁLISIS DE LA FUNCIÓN f(x) = x - cos(x):")
    print("   • Función continua en [0, 1]")
    print("   • Cambio de signo: f(0) < 0, f(1) > 0")
    print("   • Raíz única en el intervalo")
    print("   • Raíz exacta: x ≈ 0.7390851332")
    print()
    
    print("📊 RESULTADOS DEL MÉTODO DE BISECCIÓN:")
    if raiz is not None:
        print(f"   • Iteraciones teóricas: {iteraciones_teoricas_4}")
        print(f"   • Iteraciones reales: {iteraciones}")
        print(f"   • Raíz aproximada: {raiz:.6f}")
        print(f"   • Precisión alcanzada: {decimales_exactos} decimales exactos")
        print(f"   • Convergencia: {'Sí' if convergencia else 'No'}")
    
    print()
    print("💡 FÓRMULA GENERAL PARA BISECCIÓN:")
    print("   n ≥ log₂((b-a) / (0.5 × 10^(-t)))")
    print("   donde n = iteraciones, t = dígitos decimales")
    print()
    
    print("🎯 EJERCICIO COMPLETADO")
    print("📁 Revisa la carpeta 'resultados/' para ver el archivo CSV")
    
    return {
        'iteraciones_teoricas': iteraciones_teoricas_4,
        'iteraciones_reales': iteraciones if raiz is not None else None,
        'raiz': raiz,
        'convergencia': convergencia,
        'decimales_exactos': decimales_exactos if raiz is not None else None
    }


if __name__ == "__main__":
    ejercicio_8()
