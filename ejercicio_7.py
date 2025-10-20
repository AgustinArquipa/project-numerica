"""
Ejercicio N° 7: Método de Iteración de Punto Fijo

Para cada ecuación f(x) = 0, encontrar la función de iteración g(x) adecuada,
verificar criterios de convergencia y determinar las raíces.
"""

import sys
import os
import math
from typing import Callable, Tuple, List, Dict

# Agregar el directorio raíz al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar método de punto fijo
from abiertos.punto_fijo import punto_fijo, verificar_condicion_fourier, punto_fijo_analisis
from utils import exportar_iteraciones_csv


def ejercicio_7():
    """Resuelve el Ejercicio N° 7 con método de punto fijo para 6 ecuaciones"""
    print("=" * 80)
    print("EJERCICIO N° 7: MÉTODO DE ITERACIÓN DE PUNTO FIJO")
    print("=" * 80)
    print("Objetivo: Elegir función de iteración adecuada, verificar convergencia y encontrar raíces")
    print()
    
    # ========================================
    # DEFINICIÓN DE LAS 6 ECUACIONES
    # ========================================
    
    ecuaciones = {
        'i': {
            'funcion': 'f(x) = x² - sen(x) - 1 = 0',
            'f': lambda x: x**2 - math.sin(x) - 1,
            'g_opciones': {
                'g1': lambda x: math.sqrt(math.sin(x) + 1),  # x = √(sen(x) + 1)
                'g2': lambda x: math.asin(x**2 - 1),         # x = arcsen(x² - 1)
                'g3': lambda x: x + (x**2 - math.sin(x) - 1) # x = x + f(x)
            },
            'g_derivadas': {
                'g1': lambda x: math.cos(x) / (2 * math.sqrt(math.sin(x) + 1)),
                'g2': lambda x: 2*x / math.sqrt(1 - (x**2 - 1)**2),
                'g3': lambda x: 1 + 2*x - math.cos(x)
            },
            'intervalo': (0, 2),
            'punto_inicial': 1.0
        },
        'ii': {
            'funcion': 'f(x) = ln(x) - 1 - 1/x = 0',
            'f': lambda x: math.log(x) - 1 - 1/x,
            'g_opciones': {
                'g1': lambda x: math.exp(1 + 1/x),           # x = e^(1 + 1/x)
                'g2': lambda x: 1 / (math.log(x) - 1),       # x = 1/(ln(x) - 1)
                'g3': lambda x: x + (math.log(x) - 1 - 1/x)  # x = x + f(x)
            },
            'g_derivadas': {
                'g1': lambda x: -math.exp(1 + 1/x) / x**2,
                'g2': lambda x: -1 / (x * (math.log(x) - 1)**2),
                'g3': lambda x: 1 + 1/x + 1/x**2
            },
            'intervalo': (1, 5),
            'punto_inicial': 2.0
        },
        'iii': {
            'funcion': 'f(x) = x + 1/x - e^x = 0',
            'f': lambda x: x + 1/x - math.exp(x),
            'g_opciones': {
                'g1': lambda x: math.exp(x) - 1/x,           # x = e^x - 1/x
                'g2': lambda x: 1 / (math.exp(x) - x),       # x = 1/(e^x - x)
                'g3': lambda x: x + (x + 1/x - math.exp(x))  # x = x + f(x)
            },
            'g_derivadas': {
                'g1': lambda x: math.exp(x) + 1/x**2,
                'g2': lambda x: -(math.exp(x) - 1) / (math.exp(x) - x)**2,
                'g3': lambda x: 1 + 1 - 1/x**2 - math.exp(x)
            },
            'intervalo': (0.5, 2),
            'punto_inicial': 1.0
        },
        'iv': {
            'funcion': 'f(x) = x² - 5x + 3 = 0',
            'f': lambda x: x**2 - 5*x + 3,
            'g_opciones': {
                'g1': lambda x: (x**2 + 3) / 5,              # x = (x² + 3)/5
                'g2': lambda x: math.sqrt(5*x - 3),          # x = √(5x - 3)
                'g3': lambda x: x + (x**2 - 5*x + 3)         # x = x + f(x)
            },
            'g_derivadas': {
                'g1': lambda x: 2*x / 5,
                'g2': lambda x: 5 / (2 * math.sqrt(5*x - 3)),
                'g3': lambda x: 1 + 2*x - 5
            },
            'intervalo': (0, 5),
            'punto_inicial': 1.0
        },
        'v': {
            'funcion': 'f(x) = cos(x) - 3x = 0',
            'f': lambda x: math.cos(x) - 3*x,
            'g_opciones': {
                'g1': lambda x: math.cos(x) / 3,             # x = cos(x)/3
                'g2': lambda x: math.acos(3*x),              # x = arccos(3x)
                'g3': lambda x: x + (math.cos(x) - 3*x)      # x = x + f(x)
            },
            'g_derivadas': {
                'g1': lambda x: -math.sin(x) / 3,
                'g2': lambda x: -3 / math.sqrt(1 - (3*x)**2),
                'g3': lambda x: 1 - math.sin(x) - 3
            },
            'intervalo': (0, 1),
            'punto_inicial': 0.3
        },
        'vi': {
            'funcion': 'f(x) = x·e^x - 1 = 0',
            'f': lambda x: x * math.exp(x) - 1,
            'g_opciones': {
                'g1': lambda x: 1 / math.exp(x),             # x = 1/e^x
                'g2': lambda x: math.exp(-x),                # x = e^(-x)
                'g3': lambda x: x + (x * math.exp(x) - 1)    # x = x + f(x)
            },
            'g_derivadas': {
                'g1': lambda x: -1 / math.exp(x),
                'g2': lambda x: -math.exp(-x),
                'g3': lambda x: 1 + math.exp(x) + x * math.exp(x)
            },
            'intervalo': (0, 1),
            'punto_inicial': 0.5
        }
    }
    
    # ========================================
    # PROCESAR CADA ECUACIÓN
    # ========================================
    
    resultados_totales = {}
    
    for letra, datos in ecuaciones.items():
        print("=" * 80)
        print(f"ECUACIÓN {letra.upper()}: {datos['funcion']}")
        print("=" * 80)
        
        # Mostrar opciones de transformación
        print("📋 OPCIONES DE TRANSFORMACIÓN:")
        print("   g1: Primera opción")
        print("   g2: Segunda opción") 
        print("   g3: Método de suma (x = x + f(x))")
        print()
        
        # Probar cada opción de g(x)
        mejor_opcion = None
        mejor_resultado = None
        mejor_convergencia = False
        
        for g_nombre, g_func in datos['g_opciones'].items():
            print(f"🔍 Probando {g_nombre}:")
            
            try:
                # Verificar condición de Fourier
                g_derivada = datos['g_derivadas'][g_nombre]
                cumple_fourier, max_derivada = verificar_condicion_fourier(
                    g_func, g_derivada, datos['punto_inicial']
                )
                
                print(f"   Condición de Fourier: {'✓' if cumple_fourier else '✗'}")
                print(f"   Máxima derivada: {max_derivada:.4f}")
                
                # Ejecutar método de punto fijo
                raiz, iteraciones, convergencia, historial = punto_fijo(
                    g_func, datos['punto_inicial'], 
                    tolerancia=1e-6, max_iteraciones=50, mostrar_iteraciones=False
                )
                
                if convergencia and raiz is not None:
                    f_raiz = datos['f'](raiz)
                    print(f"   ✅ Convergencia: {iteraciones} iteraciones")
                    print(f"   🎯 Raíz: {raiz:.6f}")
                    print(f"   🔍 f(raíz): {f_raiz:.2e}")
                    
                    # Guardar mejor opción
                    if mejor_opcion is None or (convergencia and iteraciones < mejor_resultado[1]):
                        mejor_opcion = g_nombre
                        mejor_resultado = (raiz, iteraciones, convergencia, historial)
                        mejor_convergencia = True
                else:
                    print(f"   ❌ No convergió en 50 iteraciones")
                
            except (ValueError, ZeroDivisionError, OverflowError) as e:
                print(f"   ❌ Error: {str(e)}")
            
            print()
        
        # Mostrar mejor resultado
        if mejor_convergencia and mejor_resultado:
            raiz, iteraciones, convergencia, historial = mejor_resultado
            print(f"🏆 MEJOR OPCIÓN: {mejor_opcion}")
            print(f"   • Raíz encontrada: {raiz:.6f}")
            print(f"   • Iteraciones: {iteraciones}")
            print(f"   • f(raíz): {datos['f'](raiz):.2e}")
            
            # Mostrar primeras iteraciones
            print(f"\n📊 PRIMERAS 5 ITERACIONES:")
            print("Iteración | x_n     | x_{n+1} | |x_{n+1} - x_n| | Error Relativo")
            print("-" * 60)
            
            for i, iter_info in enumerate(historial[:5], 1):
                x_ant = iter_info['x_anterior']
                x_act = iter_info['x_actual']
                dif = iter_info['diferencia']
                err_rel = iter_info['error_relativo']
                
                print(f"   {i:2d}    | {x_ant:.6f} | {x_act:.6f} | {dif:.6f}    | {err_rel:.6f}")
            
            # Exportar historial
            archivo_csv = exportar_iteraciones_csv(
                historial, f"ejercicio7_{letra}_{mejor_opcion}.csv", "resultados", precision_calculadora=9
            )
            print(f"\n📁 Historial exportado: {os.path.basename(archivo_csv)}")
            
            # Guardar resultado
            resultados_totales[letra] = {
                'ecuacion': datos['funcion'],
                'mejor_g': mejor_opcion,
                'raiz': raiz,
                'iteraciones': iteraciones,
                'convergencia': convergencia,
                'archivo': archivo_csv
            }
            
        else:
            print("❌ NINGUNA OPCIÓN CONVERGIÓ")
            resultados_totales[letra] = {
                'ecuacion': datos['funcion'],
                'mejor_g': None,
                'raiz': None,
                'iteraciones': 0,
                'convergencia': False,
                'archivo': None
            }
        
        print()
    
    # ========================================
    # RESUMEN FINAL
    # ========================================
    print("=" * 80)
    print("RESUMEN FINAL - EJERCICIO 7")
    print("=" * 80)
    
    print("📊 RESULTADOS POR ECUACIÓN:")
    print()
    print("Ecuación | Función de Iteración | Raíz Aproximada | Iteraciones | Convergencia")
    print("-" * 80)
    
    for letra, resultado in resultados_totales.items():
        ecuacion = resultado['ecuacion'].split('=')[0].strip()
        mejor_g = resultado['mejor_g'] if resultado['mejor_g'] else 'N/A'
        raiz = f"{resultado['raiz']:.6f}" if resultado['raiz'] else 'N/A'
        iteraciones = resultado['iteraciones']
        convergencia = 'Sí' if resultado['convergencia'] else 'No'
        
        print(f"   {letra.upper()}    | {mejor_g:>20} | {raiz:>14} | {iteraciones:>11} | {convergencia}")
    
    print()
    
    # Estadísticas
    convergentes = sum(1 for r in resultados_totales.values() if r['convergencia'])
    total = len(resultados_totales)
    
    print(f"📈 ESTADÍSTICAS:")
    print(f"   • Ecuaciones procesadas: {total}")
    print(f"   • Ecuaciones convergentes: {convergentes}")
    print(f"   • Tasa de éxito: {convergentes/total*100:.1f}%")
    
    if convergentes > 0:
        iteraciones_promedio = sum(r['iteraciones'] for r in resultados_totales.values() if r['convergencia']) / convergentes
        print(f"   • Iteraciones promedio: {iteraciones_promedio:.1f}")
    
    print()
    print("🎯 EJERCICIO COMPLETADO")
    print("📁 Revisa la carpeta 'resultados/' para ver todos los archivos CSV")
    
    return resultados_totales


if __name__ == "__main__":
    ejercicio_7()
