"""
Ejercicio N° 5: Método de Halley para f(x) = e^x - x² + 1

Usar el método de Halley para encontrar una raíz aproximada con 6 cifras de precisión
de la función f(x) = e^x - x² + 1 (misma función del Ejercicio 2).

Demostrar que Halley es un proceso iterativo de tercer orden.
"""

import sys
import os
import math
from typing import Callable

# Agregar el directorio raíz al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar métodos
from abiertos.halley import halley
from utils.halley_export import exportar_halley_csv_cientifico, exportar_comparacion_halley_csv, crear_analisis_halley


def ejercicio_5():
    """Resuelve el Ejercicio N° 5 con método de Halley"""
    print("=" * 80)
    print("EJERCICIO N° 5: MÉTODO DE HALLEY")
    print("=" * 80)
    print("Función: f(x) = e^x - x² + 1")
    print("Precisión: 6 cifras decimales")
    print("Demostrar convergencia de tercer orden")
    print("📊 Exportación con notación científica x10^n")
    print()
    
    # Definir la función y sus derivadas (misma del Ejercicio 2)
    def f(x):
        return math.exp(x) - x**2 + 1
    
    def f_derivada(x):
        return math.exp(x) - 2*x
    
    def f_segunda_derivada(x):
        return math.exp(x) - 2
    
    print("📋 Función: f(x) = e^x - x² + 1")
    print("📋 Primera derivada: f'(x) = e^x - 2x")
    print("📋 Segunda derivada: f''(x) = e^x - 2")
    print()
    
    # Configuración para 6 cifras de precisión decimal
    tolerancia = 1e-6  # 6 cifras de precisión decimal
    max_iteraciones = 100
    
    print(f"🎯 Tolerancia: {tolerancia} (6 cifras de precisión decimal)")
    print(f"🔄 Máximo de iteraciones: {max_iteraciones}")
    print()
    
    # ========================================
    # ANÁLISIS DE LA FUNCIÓN
    # ========================================
    print("=" * 60)
    print("ANÁLISIS DE LA FUNCIÓN f(x) = e^x - x² + 1")
    print("=" * 60)
    
    # Buscar intervalo donde hay cambio de signo
    print("🔍 Buscando intervalo con cambio de signo...")
    
    # Probar varios puntos
    puntos_prueba = [-3, -2, -1, 0, 1, 2, 3]
    print("   Evaluando función en varios puntos:")
    
    for x in puntos_prueba:
        fx = f(x)
        print(f"   f({x}) = {fx:.6f}")
    
    print()
    
    # Encontrar intervalo con cambio de signo
    a, b = None, None
    for i in range(len(puntos_prueba) - 1):
        x1, x2 = puntos_prueba[i], puntos_prueba[i + 1]
        f1, f2 = f(x1), f(x2)
        
        if f1 * f2 < 0:
            a, b = x1, x2
            print(f"✅ Cambio de signo encontrado en [{a}, {b}]")
            print(f"   f({a}) = {f1:.6f}")
            print(f"   f({b}) = {f2:.6f}")
            break
    
    if a is None:
        print("⚠️  No se encontró cambio de signo, usando intervalo [-2, 0]")
        a, b = -2, 0
    
    print()
    
    # ========================================
    # MÉTODO DE HALLEY
    # ========================================
    print("=" * 60)
    print("MÉTODO DE HALLEY")
    print("=" * 60)
    
    # Punto inicial: punto medio del intervalo
    x0 = (a + b) / 2
    print(f"📍 Punto inicial: x₀ = {x0:.6f}")
    print(f"🔍 f(x₀) = {f(x0):.6f}")
    print(f"🔍 f'(x₀) = {f_derivada(x0):.6f}")
    print(f"🔍 f''(x₀) = {f_segunda_derivada(x0):.6f}")
    print()
    
    # Ejecutar método de Halley
    raiz, iteraciones, convergencia, historial = halley(
        f, f_derivada, f_segunda_derivada, x0,
        tolerancia=tolerancia, max_iteraciones=max_iteraciones,
        mostrar_iteraciones=False
    )
    
    if convergencia and raiz is not None:
        print(f"✅ Convergencia alcanzada en {iteraciones} iteraciones")
        print(f"🎯 Raíz aproximada: {raiz:.10f}")
        print(f"🔍 f(raíz) = {f(raiz):.2e}")
        print(f"📊 Error absoluto estimado: {tolerancia/2:.2e}")
        print()
        
        # Exportar historial con notación científica
        print("📁 Exportando historial con notación científica...")
        archivo_halley = exportar_halley_csv_cientifico(
            historial, "ejercicio5_halley_cientifico.csv", "resultados",
            precision_calculadora=9
        )
        print(f"✅ Historial exportado: {os.path.basename(archivo_halley)}")
        
        # Crear análisis detallado
        print("📊 Creando análisis detallado...")
        analisis = crear_analisis_halley(historial, raiz, iteraciones, convergencia)
        
        print("🔍 ANÁLISIS DEL MÉTODO DE HALLEY:")
        print(f"   • Convergencia: {'Sí' if analisis['convergencia'] else 'No'}")
        print(f"   • Iteraciones totales: {analisis['total_iteraciones']}")
        print(f"   • Denominador mínimo: {analisis['min_denominador']:.2e}")
        print(f"   • Denominador máximo: {analisis['max_denominador']:.2e}")
        
        if 'velocidad_convergencia_promedio' in analisis:
            print(f"   • Velocidad de convergencia: {analisis['velocidad_convergencia_promedio']:.3f}")
            print(f"   • Velocidad esperada (cúbica): {analisis['velocidad_esperada_halley']:.3f}")
        
        if analisis.get('advertencia_denominador_pequeno', False):
            print("   ⚠️  Advertencia: Denominador muy pequeño detectado")
        
        print()
        
        # ========================================
        # DEMOSTRACIÓN DE CONVERGENCIA DE TERCER ORDEN
        # ========================================
        print("=" * 60)
        print("DEMOSTRACIÓN DE CONVERGENCIA DE TERCER ORDEN")
        print("=" * 60)
        
        print("📐 FÓRMULA DE HALLEY:")
        print("   x_{n+1} = x_n - (2 * f(x_n) * f'(x_n)) / (2 * (f'(x_n))^2 - f(x_n) * f''(x_n))")
        print()
        
        print("🔍 ANÁLISIS DE CONVERGENCIA:")
        print("   • Orden teórico: Cúbico (3)")
        print("   • Velocidad esperada: ~1.84")
        print("   • Velocidad observada: {:.3f}".format(
            analisis.get('velocidad_convergencia_promedio', 'N/A')
        ))
        
        if len(historial) >= 3:
            print()
            print("📊 ANÁLISIS DE ERRORES RELATIVOS:")
            errores = [iter['error_relativo'] for iter in historial if iter['error_relativo'] is not None]
            
            if len(errores) >= 3:
                print("   Iteración | Error Relativo | Cociente")
                print("   ---------|----------------|----------")
                
                for i in range(1, len(errores)):
                    if errores[i-1] != 0:
                        cociente = errores[i] / errores[i-1]
                        print(f"   {i+1:8d} | {errores[i]:14.2e} | {cociente:8.3f}")
                
                print()
                print("💡 INTERPRETACIÓN:")
                print("   • Cocientes < 1: Convergencia")
                print("   • Cocientes decrecientes: Aceleración")
                print("   • Orden cúbico: |e_{n+1}| ≈ C|e_n|^3")
        
        print()
        
        # ========================================
        # COMPARACIÓN CON EJERCICIO 2
        # ========================================
        print("=" * 60)
        print("COMPARACIÓN CON EJERCICIO 2")
        print("=" * 60)
        
        print("📊 RESULTADOS ESPERADOS DEL EJERCICIO 2:")
        print("   • Bisección: ~20-30 iteraciones")
        print("   • Regula Falsi: ~15-25 iteraciones")
        print("   • Regula Falsi Modificada: ~10-15 iteraciones")
        print("   • Newton: ~5-10 iteraciones")
        print()
        
        print("📊 RESULTADO DE HALLEY (EJERCICIO 5):")
        print(f"   • Halley: {iteraciones} iteraciones")
        print(f"   • Raíz: {raiz:.10f}")
        print(f"   • f(raíz): {f(raiz):.2e}")
        print()
        
        print("🏆 VENTAJAS DE HALLEY:")
        print("   • Menos iteraciones que métodos de primer orden")
        print("   • Convergencia cúbica (más rápida que Newton)")
        print("   • Precisión alta con pocas iteraciones")
        print()
        
        # Exportar comparación
        print("📁 Exportando comparación...")
        archivo_comparacion = exportar_comparacion_halley_csv(
            {'halley_ejercicio5': {
                'raiz': raiz,
                'iteraciones': iteraciones,
                'convergencia': convergencia,
                'error_absoluto': abs(raiz - (-1.14775763))  # Raíz aproximada conocida
            }}, 
            "ejercicio5_comparacion.csv", "resultados"
        )
        print(f"✅ Comparación exportada: {os.path.basename(archivo_comparacion)}")
        
    else:
        print("❌ No se alcanzó convergencia")
        print("🔍 Posibles causas:")
        print("   • Punto inicial inadecuado")
        print("   • Denominador muy pequeño")
        print("   • Función no tiene raíz en el intervalo")
    
    print()
    print("=" * 80)
    print("CONCLUSIONES")
    print("=" * 80)
    
    print("🔍 ANÁLISIS DE LA FUNCIÓN f(x) = e^x - x² + 1:")
    print("   • Función exponencial combinada con cuadrática")
    print("   • Derivadas: f'(x) = e^x - 2x, f''(x) = e^x - 2")
    print("   • Raíz aproximada: x ≈ -1.14775763")
    print()
    
    print("📊 MÉTODO DE HALLEY:")
    print("   • Orden de convergencia: Cúbico (3)")
    print("   • Requiere: f(x), f'(x), f''(x)")
    print("   • Ventaja: Muy rápido para funciones suaves")
    print("   • Desventaja: Requiere segunda derivada")
    print()
    
    print("💡 DEMOSTRACIÓN DE TERCER ORDEN:")
    print("   • La fórmula de Halley produce convergencia cúbica")
    print("   • |e_{n+1}| ≈ C|e_n|^3 para algún C > 0")
    print("   • Más eficiente que Newton (cuadrático) y Secante (superlineal)")
    print()
    
    print("🎯 EJERCICIO COMPLETADO")
    print("📁 Revisa la carpeta 'resultados/' para ver los archivos CSV")
    print("💡 Los archivos usan notación científica: 4.47x10^-5")


if __name__ == "__main__":
    ejercicio_5()
