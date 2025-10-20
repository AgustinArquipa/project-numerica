"""
Ejercicio N° 3: Resolución de f(x) = (x-1)²

Hallar la raíz de f(x) = (x-1)² con 4 cifras de precisión decimal usando:
i) Método de Newton
ii) Método de Secante

Obtener conclusiones sobre el comportamiento de ambos métodos.
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


def ejercicio_3():
    """Resuelve el Ejercicio N° 3 completo"""
    print("=" * 80)
    print("EJERCICIO N° 3: f(x) = (x-1)²")
    print("=" * 80)
    print("Hallar la raíz con 4 cifras de precisión decimal")
    print("Métodos a usar: Newton y Secante")
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
    
    # Punto inicial cerca de la raíz (como sugeriste)
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
            hist_n, "ejercicio3_newton.csv", "resultados", 
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
    # ii) MÉTODO DE SECANTE
    # ========================================
    print("=" * 60)
    print("ii) MÉTODO DE SECANTE")
    print("=" * 60)
    
    # Puntos iniciales con valores diferentes de la función
    x0_sec = 0.0
    x1_sec = 1.2
    print(f"📍 Puntos iniciales: x₀ = {x0_sec}, x₁ = {x1_sec}")
    print(f"🔍 f(x₀) = f({x0_sec}) = {f(x0_sec):.6f}")
    print(f"🔍 f(x₁) = f({x1_sec}) = {f(x1_sec):.6f}")
    print()
    
    raiz_s, iter_s, conv_s, hist_s = secante(
        f, x0_sec, x1_sec, tolerancia=tolerancia, max_iteraciones=max_iteraciones, mostrar_iteraciones=False
    )
    
    if conv_s and raiz_s:
        print(f"✅ Convergencia alcanzada en {iter_s} iteraciones")
        print(f"🎯 Raíz aproximada: {raiz_s:.10f}")
        print(f"🔍 f(raíz) = {f(raiz_s):.2e}")
        print(f"📊 Error absoluto: {abs(raiz_s - 1):.2e}")
        print(f"📊 Error relativo: {abs(raiz_s - 1)/1:.2e}")
        
        # Exportar historial con notación decimal
        archivo_secante = exportar_iteraciones_csv(
            hist_s, "ejercicio3_secante.csv", "resultados",
            precision_calculadora=9
        )
        print(f"📁 Historial exportado: {os.path.basename(archivo_secante)}")
        
        resultados['secante'] = {
            'raiz': raiz_s,
            'iteraciones': iter_s,
            'convergencia': conv_s,
            'historial': hist_s
        }
    else:
        print("❌ No se alcanzó convergencia")
        resultados['secante'] = {'raiz': None, 'iteraciones': iter_s, 'convergencia': conv_s}
    
    print()
    
    # ========================================
    # COMPARACIÓN DE RESULTADOS
    # ========================================
    print("=" * 80)
    print("COMPARACIÓN DE RESULTADOS")
    print("=" * 80)
    
    # Crear tabla comparativa
    print(f"{'Método':<20} {'Raíz':<15} {'Iteraciones':<12} {'f(raíz)':<12} {'Error Abs.':<12} {'Convergencia'}")
    print("-" * 90)
    
    metodos_nombres = {
        'newton': 'i) Newton',
        'secante': 'ii) Secante'
    }
    
    for metodo, datos in resultados.items():
        nombre = metodos_nombres[metodo]
        if datos['convergencia'] and datos['raiz'] is not None:
            raiz = datos['raiz']
            iteraciones = datos['iteraciones']
            f_raiz = f(raiz)
            error_abs = abs(raiz - 1)
            convergencia = "✓"
            print(f"{nombre:<20} {raiz:<15.10f} {iteraciones:<12} {f_raiz:<12.2e} {error_abs:<12.2e} {convergencia}")
        else:
            print(f"{nombre:<20} {'No convergió':<15} {datos['iteraciones']:<12} {'N/A':<12} {'N/A':<12} {'✗'}")
    
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
    
    print("📊 COMPORTAMIENTO ESPERADO:")
    print("   • Newton: Puede tener convergencia lenta debido a la raíz múltiple")
    print("   • Secante: También puede verse afectado por la raíz múltiple")
    print("   • Ambos métodos deberían converger, pero con velocidad reducida")
    print()
    
    # Exportar comparación
    print("📁 Exportando comparación completa...")
    archivo_comparacion = exportar_comparacion_csv(
        resultados, "ejercicio3_comparacion.csv", "resultados"
    )
    print(f"✅ Comparación exportada: {os.path.basename(archivo_comparacion)}")
    
    print()
    print("🎯 EJERCICIO COMPLETADO")
    print("📁 Revisa la carpeta 'resultados/' para ver todos los archivos CSV generados")
    print("💡 Observa cómo la raíz múltiple afecta la velocidad de convergencia de ambos métodos")


if __name__ == "__main__":
    ejercicio_3()
