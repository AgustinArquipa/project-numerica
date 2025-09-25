"""
Ejercicio N° 2: Resolución de f(x) = eˣ - x² + 1

Hallar una raíz aproximada con seis cifras de precisión usando:
i) Bisección
ii) Regula Falsi
iii) Regula Falsi Modificada
iv) Método de Newton

Comparar los resultados
"""

import sys
import os
import math
from typing import Callable

# Agregar el directorio raíz al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar métodos
from cerrados import biseccion, regula_falsi, regula_falsi_modificada
from abiertos import newton
from utils import exportar_iteraciones_csv, exportar_comparacion_csv, error_absoluto, error_relativo


def ejercicio_2():
    """Resuelve el Ejercicio N° 2 completo"""
    print("=" * 80)
    print("EJERCICIO N° 2: f(x) = eˣ - x² + 1")
    print("=" * 80)
    print("Hallar una raíz aproximada con seis cifras de precisión")
    print("Métodos a usar: Bisección, Regula Falsi, Regula Falsi Modificada, Newton")
    print("Comparar los resultados")
    print("📊 Los archivos CSV se exportan con precisión de calculadora (9 cifras significativas)")
    print()
    
    # Definir la función
    def f(x):
        return math.exp(x) - x**2 + 1
    
    def f_derivada(x):
        return math.exp(x) - 2*x
    
    print("📋 Función: f(x) = eˣ - x² + 1")
    print("📋 Derivada: f'(x) = eˣ - 2x")
    print()
    
    # Especificar explícitamente el intervalo inicial
    print("📍 Intervalo inicial especificado:")
    a, b = -2.0, -1.0  # Valores iniciales explícitos
    print(f"   a = {a}")
    print(f"   b = {b}")
    print(f"   f(a) = f({a}) = {f(a):.6f}")
    print(f"   f(b) = f({b}) = {f(b):.6f}")
    
    # Verificar que hay cambio de signo
    if f(a) * f(b) >= 0:
        print("⚠️  Advertencia: No hay cambio de signo en el intervalo especificado")
        print("🔍 Buscando intervalo alternativo...")
        a, b = encontrar_intervalo(f)
        print(f"✅ Nuevo intervalo encontrado: [{a}, {b}]")
    else:
        print("✅ Cambio de signo confirmado en el intervalo especificado")
    print()
    
    # Configuración para seis cifras de precisión
    tolerancia = 1e-6
    max_iteraciones = 100
    
    print(f"🎯 Tolerancia: {tolerancia} (seis cifras de precisión)")
    print(f"🔄 Máximo de iteraciones: {max_iteraciones}")
    print()
    
    # Almacenar resultados para comparación
    resultados = {}
    
    # ========================================
    # i) MÉTODO DE BISECCIÓN
    # ========================================
    print("=" * 60)
    print("i) MÉTODO DE BISECCIÓN")
    print("=" * 60)
    
    raiz_b, iter_b, conv_b, hist_b = biseccion(
        f, a, b, tolerancia=tolerancia, max_iteraciones=max_iteraciones, mostrar_iteraciones=False
    )
    
    if conv_b and raiz_b:
        print(f"✅ Convergencia alcanzada en {iter_b} iteraciones")
        print(f"🎯 Raíz aproximada: {raiz_b:.10f}")
        print(f"🔍 f(raíz) = {f(raiz_b):.2e}")
        print(f"📊 Error absoluto estimado: {tolerancia/2:.2e}")
        
        # Exportar historial con precisión de calculadora (9 cifras significativas)
        archivo_biseccion = exportar_iteraciones_csv(
            hist_b, "ejercicio2_biseccion.csv", "resultados", 
            precision_calculadora=9
        )
        print(f"📁 Historial exportado: {os.path.basename(archivo_biseccion)}")
        
        resultados['biseccion'] = {
            'raiz': raiz_b,
            'iteraciones': iter_b,
            'convergencia': conv_b,
            'historial': hist_b
        }
    else:
        print("❌ No se alcanzó convergencia")
        resultados['biseccion'] = {'raiz': None, 'iteraciones': iter_b, 'convergencia': conv_b}
    
    print()
    
    # ========================================
    # ii) MÉTODO DE REGULA FALSI
    # ========================================
    print("=" * 60)
    print("ii) MÉTODO DE REGULA FALSI")
    print("=" * 60)
    
    raiz_rf, iter_rf, conv_rf, hist_rf = regula_falsi(
        f, a, b, tolerancia=tolerancia, max_iteraciones=max_iteraciones, mostrar_iteraciones=False
    )
    
    if conv_rf and raiz_rf:
        print(f"✅ Convergencia alcanzada en {iter_rf} iteraciones")
        print(f"🎯 Raíz aproximada: {raiz_rf:.10f}")
        print(f"🔍 f(raíz) = {f(raiz_rf):.2e}")
        
        # Exportar historial con precisión de calculadora (9 cifras significativas)
        archivo_regula_falsi = exportar_iteraciones_csv(
            hist_rf, "ejercicio2_regula_falsi.csv", "resultados",
            precision_calculadora=9
        )
        print(f"📁 Historial exportado: {os.path.basename(archivo_regula_falsi)}")
        
        resultados['regula_falsi'] = {
            'raiz': raiz_rf,
            'iteraciones': iter_rf,
            'convergencia': conv_rf,
            'historial': hist_rf
        }
    else:
        print("❌ No se alcanzó convergencia")
        resultados['regula_falsi'] = {'raiz': None, 'iteraciones': iter_rf, 'convergencia': conv_rf}
    
    print()
    
    # ========================================
    # iii) MÉTODO DE REGULA FALSI MODIFICADA
    # ========================================
    print("=" * 60)
    print("iii) MÉTODO DE REGULA FALSI MODIFICADA")
    print("=" * 60)
    
    raiz_rfm, iter_rfm, conv_rfm, hist_rfm = regula_falsi_modificada(
        f, a, b, tolerancia=tolerancia, max_iteraciones=max_iteraciones, 
        factor_reduccion=0.5, mostrar_iteraciones=False
    )
    
    if conv_rfm and raiz_rfm:
        print(f"✅ Convergencia alcanzada en {iter_rfm} iteraciones")
        print(f"🎯 Raíz aproximada: {raiz_rfm:.10f}")
        print(f"🔍 f(raíz) = {f(raiz_rfm):.2e}")
        
        # Exportar historial con precisión de calculadora (9 cifras significativas)
        archivo_regula_falsi_mod = exportar_iteraciones_csv(
            hist_rfm, "ejercicio2_regula_falsi_modificada.csv", "resultados",
            precision_calculadora=9
        )
        print(f"📁 Historial exportado: {os.path.basename(archivo_regula_falsi_mod)}")
        
        resultados['regula_falsi_modificada'] = {
            'raiz': raiz_rfm,
            'iteraciones': iter_rfm,
            'convergencia': conv_rfm,
            'historial': hist_rfm
        }
    else:
        print("❌ No se alcanzó convergencia")
        resultados['regula_falsi_modificada'] = {'raiz': None, 'iteraciones': iter_rfm, 'convergencia': conv_rfm}
    
    print()
    
    # ========================================
    # iv) MÉTODO DE NEWTON
    # ========================================
    print("=" * 60)
    print("iv) MÉTODO DE NEWTON")
    print("=" * 60)
    
    # Punto inicial: punto medio del intervalo
    x0 = (a + b) / 2
    print(f"📍 Punto inicial: x₀ = {x0:.6f}")
    
    raiz_n, iter_n, conv_n, hist_n = newton(
        f, f_derivada, x0, tolerancia=tolerancia, max_iteraciones=max_iteraciones, mostrar_iteraciones=False
    )
    
    if conv_n and raiz_n:
        print(f"✅ Convergencia alcanzada en {iter_n} iteraciones")
        print(f"🎯 Raíz aproximada: {raiz_n:.10f}")
        print(f"🔍 f(raíz) = {f(raiz_n):.2e}")
        
        # Exportar historial con precisión de calculadora (9 cifras significativas)
        archivo_newton = exportar_iteraciones_csv(
            hist_n, "ejercicio2_newton.csv", "resultados",
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
    # COMPARACIÓN DE RESULTADOS
    # ========================================
    print("=" * 80)
    print("COMPARACIÓN DE RESULTADOS")
    print("=" * 80)
    
    # Crear tabla comparativa
    print(f"{'Método':<25} {'Raíz':<15} {'Iteraciones':<12} {'f(raíz)':<12} {'Convergencia'}")
    print("-" * 80)
    
    metodos_nombres = {
        'biseccion': 'i) Bisección',
        'regula_falsi': 'ii) Regula Falsi',
        'regula_falsi_modificada': 'iii) Regula Falsi Modificada',
        'newton': 'iv) Newton'
    }
    
    for metodo, datos in resultados.items():
        nombre = metodos_nombres[metodo]
        if datos['convergencia'] and datos['raiz'] is not None:
            raiz = datos['raiz']
            iteraciones = datos['iteraciones']
            f_raiz = f(raiz)
            convergencia = "✓"
            print(f"{nombre:<25} {raiz:<15.10f} {iteraciones:<12} {f_raiz:<12.2e} {convergencia}")
        else:
            print(f"{nombre:<25} {'No convergió':<15} {datos['iteraciones']:<12} {'N/A':<12} {'✗'}")
    
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
    
    # Exportar comparación
    print("📁 Exportando comparación completa...")
    archivo_comparacion = exportar_comparacion_csv(
        resultados, "ejercicio2_comparacion.csv", "resultados"
    )
    print(f"✅ Comparación exportada: {os.path.basename(archivo_comparacion)}")
    
    print()
    print("🎯 EJERCICIO COMPLETADO")
    print("📁 Revisa la carpeta 'resultados/' para ver todos los archivos CSV generados")


def encontrar_intervalo(f: Callable[[float], float]) -> tuple[float, float]:
    """
    Encuentra un intervalo [a, b] donde f(x) cambie de signo.
    
    Args:
        f: Función a evaluar
        
    Returns:
        Tupla con (a, b) donde f(a) * f(b) < 0
    """
    # Buscar en varios rangos
    rangos = [(-5, 0), (-2, 2), (0, 3), (-10, 10)]
    
    for a, b in rangos:
        try:
            fa = f(a)
            fb = f(b)
            
            if fa * fb < 0:  # Cambio de signo encontrado
                return a, b
                
            # Si no hay cambio de signo, buscar más granularmente
            paso = (b - a) / 20
            for i in range(20):
                x1 = a + i * paso
                x2 = a + (i + 1) * paso
                try:
                    fx1 = f(x1)
                    fx2 = f(x2)
                    if fx1 * fx2 < 0:
                        return x1, x2
                except:
                    continue
        except:
            continue
    
    # Si no se encuentra cambio de signo, usar un intervalo por defecto
    print("⚠️  No se encontró cambio de signo automáticamente, usando intervalo [-2, 2]")
    return -2.0, 2.0


if __name__ == "__main__":
    ejercicio_2()
