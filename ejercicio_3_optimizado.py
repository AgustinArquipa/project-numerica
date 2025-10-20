"""
Ejercicio N° 3 OPTIMIZADO: Resolución de f(x) = (x-1)²

Hallar la raíz de f(x) = (x-1)² con 4 cifras de precisión decimal usando:
i) Método de Newton
ii) Método de Secante (con puntos iniciales optimizados)

Comparar diferentes combinaciones de puntos iniciales para la Secante.
"""

import sys
import os
import math
from typing import Callable

# Agregar el directorio raíz al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar métodos
from abiertos import newton, secante
from utils import exportar_iteraciones_csv, exportar_comparacion_csv, error_absoluto, error_relativo


def ejercicio_3_optimizado():
    """Resuelve el Ejercicio N° 3 con puntos iniciales optimizados"""
    print("=" * 80)
    print("EJERCICIO N° 3 OPTIMIZADO: f(x) = (x-1)²")
    print("=" * 80)
    print("Hallar la raíz con 4 cifras de precisión decimal")
    print("Métodos a usar: Newton y Secante (con puntos optimizados)")
    print("📊 Los archivos CSV se exportan con notación decimal para números largos")
    print()
    
    # Definir la función y su derivada
    def f(x):
        return (x - 1)**2
    
    def f_derivada(x):
        return 2 * (x - 1)
    
    print("📋 Función: f(x) = (x-1)²")
    print("📋 Derivada: f'(x) = 2(x-1)")
    print("🎯 Raíz exacta: x = 1")
    print()
    
    # Configuración para 4 cifras de precisión decimal
    tolerancia = 1e-4  # 4 cifras de precisión decimal
    max_iteraciones = 100
    
    print(f"🎯 Tolerancia: {tolerancia} (4 cifras de precisión decimal)")
    print(f"🔄 Máximo de iteraciones: {max_iteraciones}")
    print()
    
    # Almacenar resultados para comparación
    resultados = {}
    
    # ========================================
    # i) MÉTODO DE NEWTON
    # ========================================
    print("=" * 60)
    print("i) MÉTODO DE NEWTON")
    print("=" * 60)
    
    # Punto inicial cerca de la raíz
    x0 = 1.1
    print(f"📍 Punto inicial: x₀ = {x0}")
    print(f"🔍 f(x₀) = f({x0}) = {f(x0):.6f}")
    print(f"🔍 f'(x₀) = f'({x0}) = {f_derivada(x0):.6f}")
    print()
    
    raiz_n, iter_n, conv_n, hist_n = newton(
        f, f_derivada, x0, tolerancia=tolerancia, max_iteraciones=max_iteraciones, mostrar_iteraciones=False
    )
    
    if conv_n and raiz_n:
        print(f"✅ Convergencia alcanzada en {iter_n} iteraciones")
        print(f"🎯 Raíz aproximada: {raiz_n:.10f}")
        print(f"🔍 f(raíz) = {f(raiz_n):.2e}")
        print(f"📊 Error absoluto: {abs(raiz_n - 1):.2e}")
        print(f"📊 Error relativo: {abs(raiz_n - 1)/1:.2e}")
        
        # Exportar historial con notación decimal
        archivo_newton = exportar_iteraciones_csv(
            hist_n, "ejercicio3_optimizado_newton.csv", "resultados", 
            precision_calculadora=9
        )
        print(f"📁 Historial exportado: {os.path.basename(archivo_newton)}")
        
        resultados['newton'] = {
            'raiz': raiz_n,
            'iteraciones': iter_n,
            'convergencia': conv_n,
            'historial': hist_n
        }
    else:
        print("❌ No se alcanzó convergencia")
        resultados['newton'] = {'raiz': None, 'iteraciones': iter_n, 'convergencia': conv_n}
    
    print()
    
    # ========================================
    # ii) MÉTODO DE SECANTE - MÚLTIPLES COMBINACIONES
    # ========================================
    print("=" * 60)
    print("ii) MÉTODO DE SECANTE - COMPARACIÓN DE PUNTOS INICIALES")
    print("=" * 60)
    
    # Diferentes combinaciones de puntos iniciales para probar
    combinaciones_secante = [
        # (x0, x1, descripcion)
        (0.0, 1.2, "Original: x₀=0.0, x₁=1.2"),
        (0.0, 2.0, "Simétricos: x₀=0.0, x₁=2.0"),
        (0.5, 1.5, "Cerca simétricos: x₀=0.5, x₁=1.5"),
        (0.0, 1.5, "Uno lejos, uno cerca: x₀=0.0, x₁=1.5"),
        (0.8, 1.3, "Ambos cerca: x₀=0.8, x₁=1.3"),
        (-1.0, 2.0, "Muy separados: x₀=-1.0, x₁=2.0"),
        (0.9, 1.1, "Muy cerca de la raíz: x₀=0.9, x₁=1.1"),
        (0.0, 1.0, "Uno es la raíz: x₀=0.0, x₁=1.0"),
    ]
    
    resultados_secante = []
    
    for i, (x0_sec, x1_sec, descripcion) in enumerate(combinaciones_secante, 1):
        print(f"🔄 Prueba {i}: {descripcion}")
        print(f"   Puntos: x₀ = {x0_sec}, x₁ = {x1_sec}")
        print(f"   f(x₀) = {f(x0_sec):.6f}, f(x₁) = {f(x1_sec):.6f}")
        
        # Verificar si f(x0) != f(x1) para evitar división por cero
        if abs(f(x0_sec) - f(x1_sec)) < 1e-15:
            print(f"   ⚠️  f(x₀) = f(x₁), saltando esta combinación...")
            print()
            continue
        
        raiz_s, iter_s, conv_s, hist_s = secante(
            f, x0_sec, x1_sec, tolerancia=tolerancia, max_iteraciones=max_iteraciones, mostrar_iteraciones=False
        )
        
        if conv_s and raiz_s:
            error_abs = abs(raiz_s - 1)
            print(f"   ✅ Convergencia en {iter_s} iteraciones")
            print(f"   🎯 Raíz: {raiz_s:.10f}, Error: {error_abs:.2e}")
            
            resultado_secante = {
                'descripcion': descripcion,
                'x0': x0_sec,
                'x1': x1_sec,
                'raiz': raiz_s,
                'iteraciones': iter_s,
                'error_absoluto': error_abs,
                'convergencia': conv_s,
                'historial': hist_s
            }
            resultados_secante.append(resultado_secante)
        else:
            print(f"   ❌ No convergió")
        
        print()
    
    # Ordenar por número de iteraciones
    resultados_secante.sort(key=lambda x: x['iteraciones'])
    
    # Mostrar resumen de resultados de Secante
    print("📊 RESUMEN DE RESULTADOS DE SECANTE:")
    print("-" * 100)
    print(f"{'Rank':<4} {'Descripción':<30} {'x₀':<6} {'x₁':<6} {'Iter.':<6} {'Raíz':<12} {'Error':<12}")
    print("-" * 100)
    
    for i, resultado in enumerate(resultados_secante, 1):
        print(f"{i:<4} {resultado['descripcion']:<30} "
              f"{resultado['x0']:<6.1f} {resultado['x1']:<6.1f} "
              f"{resultado['iteraciones']:<6} {resultado['raiz']:<12.8f} "
              f"{resultado['error_absoluto']:<12.2e}")
    
    print()
    
    # Usar el mejor resultado de Secante para la comparación general
    if resultados_secante:
        mejor_secante = resultados_secante[0]
        print(f"🥇 MEJOR COMBINACIÓN DE SECANTE:")
        print(f"   {mejor_secante['descripcion']}")
        print(f"   Iteraciones: {mejor_secante['iteraciones']}")
        print(f"   Raíz: {mejor_secante['raiz']:.10f}")
        print()
        
        # Exportar historial del mejor resultado
        archivo_secante = exportar_iteraciones_csv(
            mejor_secante['historial'], "ejercicio3_optimizado_secante.csv", "resultados",
            precision_calculadora=9
        )
        print(f"📁 Historial del mejor resultado exportado: {os.path.basename(archivo_secante)}")
        
        resultados['secante'] = {
            'raiz': mejor_secante['raiz'],
            'iteraciones': mejor_secante['iteraciones'],
            'convergencia': mejor_secante['convergencia'],
            'historial': mejor_secante['historial'],
            'puntos_iniciales': (mejor_secante['x0'], mejor_secante['x1']),
            'descripcion': mejor_secante['descripcion']
        }
    else:
        print("❌ No se encontraron combinaciones exitosas para Secante")
        resultados['secante'] = {'raiz': None, 'iteraciones': 0, 'convergencia': False}
    
    print()
    
    # ========================================
    # COMPARACIÓN DE RESULTADOS
    # ========================================
    print("=" * 80)
    print("COMPARACIÓN DE RESULTADOS")
    print("=" * 80)
    
    # Crear tabla comparativa
    print(f"{'Método':<25} {'Raíz':<15} {'Iteraciones':<12} {'f(raíz)':<12} {'Error Abs.':<12} {'Puntos Iniciales'}")
    print("-" * 110)
    
    metodos_nombres = {
        'newton': 'i) Newton',
        'secante': 'ii) Secante (óptimo)'
    }
    
    for metodo, datos in resultados.items():
        nombre = metodos_nombres[metodo]
        if datos['convergencia'] and datos['raiz'] is not None:
            raiz = datos['raiz']
            iteraciones = datos['iteraciones']
            f_raiz = f(raiz)
            error_abs = abs(raiz - 1)
            convergencia = "✓"
            
            # Mostrar puntos iniciales si están disponibles
            puntos_str = ""
            if 'puntos_iniciales' in datos:
                x0, x1 = datos['puntos_iniciales']
                puntos_str = f"({x0}, {x1})"
            else:
                puntos_str = f"({x0})"  # Para Newton
            
            print(f"{nombre:<25} {raiz:<15.10f} {iteraciones:<12} {f_raiz:<12.2e} {error_abs:<12.2e} {puntos_str}")
        else:
            print(f"{nombre:<25} {'No convergió':<15} {datos['iteraciones']:<12} {'N/A':<12} {'N/A':<12} {'N/A'}")
    
    print()
    
    # Análisis de diferencias
    raices_validas = [(metodo, datos['raiz']) for metodo, datos in resultados.items() 
                     if datos['convergencia'] and datos['raiz'] is not None]
    
    if len(raices_validas) > 1:
        print("📊 ANÁLISIS DE PRECISIÓN:")
        print()
        
        # Calcular diferencias entre raíces
        for i, (metodo1, raiz1) in enumerate(raices_validas):
            for metodo2, raiz2 in raices_validas[i+1:]:
                diferencia = abs(raiz1 - raiz2)
                print(f"   {metodos_nombres[metodo1]} vs {metodos_nombres[metodo2]}: {diferencia:.2e}")
        
        print()
        
        # Método más eficiente
        metodos_convergentes = [(metodo, datos) for metodo, datos in resultados.items() 
                               if datos['convergencia'] and datos['raiz'] is not None]
        
        if metodos_convergentes:
            metodo_rapido = min(metodos_convergentes, key=lambda x: x[1]['iteraciones'])
            print(f"🏆 MÉTODO MÁS EFICIENTE: {metodos_nombres[metodo_rapido[0]]} ({metodo_rapido[1]['iteraciones']} iteraciones)")
            
            metodo_lento = max(metodos_convergentes, key=lambda x: x[1]['iteraciones'])
            print(f"🐌 MÉTODO MÁS LENTO: {metodos_nombres[metodo_lento[0]]} ({metodo_lento[1]['iteraciones']} iteraciones)")
    
    print()
    
    # ========================================
    # CONCLUSIONES ESPECÍFICAS
    # ========================================
    print("=" * 80)
    print("CONCLUSIONES")
    print("=" * 80)
    
    print("🔍 ANÁLISIS DE LA FUNCIÓN f(x) = (x-1)²:")
    print("   • Raíz exacta: x = 1")
    print("   • Derivada: f'(x) = 2(x-1)")
    print("   • En x = 1: f(1) = 0 y f'(1) = 0")
    print("   • ⚠️  PROBLEMA: La derivada se anula en la raíz (raíz múltiple)")
    print()
    
    print("📊 COMPORTAMIENTO OBSERVADO:")
    print("   • Newton: Convergencia rápida y estable")
    print("   • Secante: Muy sensible a la elección de puntos iniciales")
    print("   • Puntos simétricos respecto a la raíz causan división por cero")
    print("   • La mejor estrategia es usar puntos con valores diferentes de f(x)")
    print()
    
    if resultados_secante:
        print("🎯 MEJORES ESTRATEGIAS PARA SECANTE:")
        print("   • Evitar puntos simétricos: f(x₀) ≠ f(x₁)")
        print("   • Usar un punto lejos y otro cerca de la raíz")
        print("   • La combinación óptima depende de la función específica")
        print()
    
    # Exportar comparación
    print("📁 Exportando comparación completa...")
    archivo_comparacion = exportar_comparacion_csv(
        resultados, "ejercicio3_optimizado_comparacion.csv", "resultados"
    )
    print(f"✅ Comparación exportada: {os.path.basename(archivo_comparacion)}")
    
    print()
    print("🎯 EJERCICIO COMPLETADO")
    print("📁 Revisa la carpeta 'resultados/' para ver todos los archivos CSV generados")
    print("💡 La optimización de puntos iniciales puede mejorar significativamente la eficiencia")


if __name__ == "__main__":
    ejercicio_3_optimizado()

