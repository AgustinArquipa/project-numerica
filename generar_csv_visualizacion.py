#!/usr/bin/env python3
"""
Generador de archivos CSV optimizados para visualización en VS Code/Cursor.

Este script genera archivos CSV con formato optimizado para la extensión CSV
que permite visualización interactiva con celdas, colores y edición.
"""

import sys
import os
import math
from datetime import datetime

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from cerrados import biseccion, regula_falsi, regula_falsi_modificada
from abiertos import newton, secante
from utils import exportar_iteraciones_csv, redondear_significativos


def generar_csv_visualizacion_completo():
    """Genera archivos CSV optimizados para visualización interactiva"""
    print("=" * 80)
    print("GENERADOR DE CSV PARA VISUALIZACIÓN INTERACTIVA")
    print("=" * 80)
    print("Optimizado para la extensión CSV de VS Code/Cursor")
    print("📊 Características: Celdas editables, colores por tipo de dato, headers fijos")
    print()
    
    # Definir función del ejercicio 2
    def f(x):
        return math.exp(x) - x**2 + 1
    
    def f_derivada(x):
        return math.exp(x) - 2*x
    
    print("📋 Función: f(x) = eˣ - x² + 1")
    print("🎯 Tolerancia: 1e-6 (seis cifras de precisión)")
    print()
    
    # Encontrar intervalo
    a, b = -5, 0  # Intervalo donde hay cambio de signo
    print(f"📍 Intervalo: [{a}, {b}]")
    print(f"   f({a}) = {f(a):.6f}")
    print(f"   f({b}) = {f(b):.6f}")
    print()
    
    # Configuración
    tolerancia = 1e-6
    max_iteraciones = 100
    
    # ========================================
    # 1. BISECCIÓN CON VISUALIZACIÓN MEJORADA
    # ========================================
    print("🔄 Generando CSV de Bisección...")
    raiz_b, iter_b, conv_b, hist_b = biseccion(
        f, a, b, tolerancia=tolerancia, max_iteraciones=max_iteraciones, mostrar_iteraciones=False
    )
    
    # Crear CSV optimizado para visualización
    crear_csv_visualizacion_biseccion(hist_b, "visualizacion_biseccion.csv")
    print("✅ Archivo: visualizacion_biseccion.csv")
    
    # ========================================
    # 2. REGULA FALSI CON VISUALIZACIÓN MEJORADA
    # ========================================
    print("🔄 Generando CSV de Regula Falsi...")
    raiz_rf, iter_rf, conv_rf, hist_rf = regula_falsi(
        f, a, b, tolerancia=tolerancia, max_iteraciones=max_iteraciones, mostrar_iteraciones=False
    )
    
    crear_csv_visualizacion_regula_falsi(hist_rf, "visualizacion_regula_falsi.csv")
    print("✅ Archivo: visualizacion_regula_falsi.csv")
    
    # ========================================
    # 3. NEWTON CON VISUALIZACIÓN MEJORADA
    # ========================================
    print("🔄 Generando CSV de Newton...")
    x0 = (a + b) / 2
    raiz_n, iter_n, conv_n, hist_n = newton(
        f, f_derivada, x0, tolerancia=tolerancia, max_iteraciones=max_iteraciones, mostrar_iteraciones=False
    )
    
    crear_csv_visualizacion_newton(hist_n, "visualizacion_newton.csv")
    print("✅ Archivo: visualizacion_newton.csv")
    
    # ========================================
    # 4. COMPARACIÓN VISUAL
    # ========================================
    print("🔄 Generando tabla comparativa...")
    crear_tabla_comparativa_visual([
        ("Bisección", raiz_b, iter_b, conv_b),
        ("Regula Falsi", raiz_rf, iter_rf, conv_rf),
        ("Newton", raiz_n, iter_n, conv_n)
    ], "comparacion_visual.csv")
    print("✅ Archivo: comparacion_visual.csv")
    
    # ========================================
    # 5. ANÁLISIS DE CONVERGENCIA
    # ========================================
    print("🔄 Generando análisis de convergencia...")
    crear_analisis_convergencia([
        ("Bisección", hist_b, "Lineal"),
        ("Regula Falsi", hist_rf, "Superlineal"),
        ("Newton", hist_n, "Cuadrática")
    ], "analisis_convergencia.csv")
    print("✅ Archivo: analisis_convergencia.csv")
    
    print()
    print("🎯 ARCHIVOS GENERADOS PARA VISUALIZACIÓN:")
    print("📁 Abre estos archivos CSV en VS Code/Cursor para ver la visualización interactiva:")
    print("   • visualizacion_biseccion.csv")
    print("   • visualizacion_regula_falsi.csv") 
    print("   • visualizacion_newton.csv")
    print("   • comparacion_visual.csv")
    print("   • analisis_convergencia.csv")
    print()
    print("💡 Características de la extensión CSV:")
    print("   • Haz clic en cualquier celda para editarla")
    print("   • Usa las flechas del teclado para navegar")
    print("   • Los headers permanecen visibles al hacer scroll")
    print("   • Los números se colorean automáticamente")
    print("   • Selecciona múltiples celdas con Shift+Click")


def crear_csv_visualizacion_biseccion(historial, nombre_archivo):
    """Crea CSV de bisección optimizado para visualización"""
    ruta = os.path.join("resultados", nombre_archivo)
    
    with open(ruta, 'w', newline='', encoding='utf-8') as archivo:
        # Escribir metadata como comentarios
        archivo.write(f"# Método de Bisección - f(x) = eˣ - x² + 1\n")
        archivo.write(f"# Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        archivo.write(f"# Intervalo: [-5, 0], Tolerancia: 1e-6\n")
        archivo.write(f"# Total iteraciones: {len(historial)}\n")
        archivo.write("#\n")
        
        # Escribir encabezados optimizados para visualización
        archivo.write("Iteración,Extremo_a,Extremo_b,Punto_medio_c,f(a),f(b),f(c),Error_Relativo,Longitud_Intervalo,Estado\n")
        
        # Escribir datos con formato mejorado
        for i, iteracion in enumerate(historial):
            # Redondear a 9 cifras significativas para mejor visualización
            a = redondear_significativos(iteracion['a'], 9)
            b = redondear_significativos(iteracion['b'], 9)
            c = redondear_significativos(iteracion['c'], 9)
            fa = redondear_significativos(iteracion['f(a)'], 9)
            fb = redondear_significativos(iteracion['f(b)'], 9)
            fc = redondear_significativos(iteracion['f(c)'], 9)
            error_rel = iteracion['error_relativo']
            longitud = redondear_significativos(iteracion['longitud_intervalo'], 9)
            
            # Determinar estado de la iteración
            if abs(fc) < 1e-6:
                estado = "Convergido"
            elif error_rel is not None and error_rel < 1e-6:
                estado = "Convergido"
            elif i == len(historial) - 1:
                estado = "Final"
            else:
                estado = "Activo"
            
            # Formatear error relativo
            if error_rel is not None:
                error_str = f"{error_rel:.2e}"
            else:
                error_str = ""
            
            archivo.write(f"{i+1},{a},{b},{c},{fa},{fb},{fc},{error_str},{longitud},{estado}\n")


def crear_csv_visualizacion_regula_falsi(historial, nombre_archivo):
    """Crea CSV de Regula Falsi optimizado para visualización"""
    ruta = os.path.join("resultados", nombre_archivo)
    
    with open(ruta, 'w', newline='', encoding='utf-8') as archivo:
        archivo.write(f"# Método de Regula Falsi - f(x) = eˣ - x² + 1\n")
        archivo.write(f"# Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        archivo.write(f"# Intervalo: [-5, 0], Tolerancia: 1e-6\n")
        archivo.write(f"# Total iteraciones: {len(historial)}\n")
        archivo.write("#\n")
        
        archivo.write("Iteración,Extremo_a,Extremo_b,Aproximación_c,f(a),f(b),f(c),Error_Relativo,Longitud_Intervalo,Estado\n")
        
        for i, iteracion in enumerate(historial):
            a = redondear_significativos(iteracion['a'], 9)
            b = redondear_significativos(iteracion['b'], 9)
            c = redondear_significativos(iteracion['c'], 9)
            fa = redondear_significativos(iteracion['f(a)'], 9)
            fb = redondear_significativos(iteracion['f(b)'], 9)
            fc = redondear_significativos(iteracion['f(c)'], 9)
            error_rel = iteracion['error_relativo']
            longitud = redondear_significativos(iteracion['longitud_intervalo'], 9)
            
            if abs(fc) < 1e-6:
                estado = "Convergido"
            elif error_rel is not None and error_rel < 1e-6:
                estado = "Convergido"
            elif i == len(historial) - 1:
                estado = "Final"
            else:
                estado = "Activo"
            
            error_str = f"{error_rel:.2e}" if error_rel is not None else ""
            archivo.write(f"{i+1},{a},{b},{c},{fa},{fb},{fc},{error_str},{longitud},{estado}\n")


def crear_csv_visualizacion_newton(historial, nombre_archivo):
    """Crea CSV de Newton optimizado para visualización"""
    ruta = os.path.join("resultados", nombre_archivo)
    
    with open(ruta, 'w', newline='', encoding='utf-8') as archivo:
        archivo.write(f"# Método de Newton - f(x) = eˣ - x² + 1\n")
        archivo.write(f"# Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        archivo.write(f"# Punto inicial: -2.5, Tolerancia: 1e-6\n")
        archivo.write(f"# Total iteraciones: {len(historial)}\n")
        archivo.write("#\n")
        
        archivo.write("Iteración,x_anterior,f(x),f'(x),x_nuevo,Error_Relativo,Error_Cuadrático,Estado\n")
        
        for i, iteracion in enumerate(historial):
            x_ant = redondear_significativos(iteracion['x_anterior'], 9)
            fx = redondear_significativos(iteracion['f(x_anterior)'], 9)
            fpx = redondear_significativos(iteracion['f\'(x_anterior)'], 9)
            x_nuevo = redondear_significativos(iteracion['x_actual'], 9)
            error_rel = iteracion['error_relativo']
            error_cuad = iteracion['error_cuadratico']
            
            if abs(fx) < 1e-6:
                estado = "Convergido"
            elif error_rel is not None and error_rel < 1e-6:
                estado = "Convergido"
            elif i == len(historial) - 1:
                estado = "Final"
            else:
                estado = "Activo"
            
            error_rel_str = f"{error_rel:.2e}" if error_rel is not None else ""
            error_cuad_str = f"{error_cuad:.2e}" if error_cuad is not None else ""
            
            archivo.write(f"{i+1},{x_ant},{fx},{fpx},{x_nuevo},{error_rel_str},{error_cuad_str},{estado}\n")


def crear_tabla_comparativa_visual(resultados, nombre_archivo):
    """Crea tabla comparativa optimizada para visualización"""
    ruta = os.path.join("resultados", nombre_archivo)
    
    with open(ruta, 'w', newline='', encoding='utf-8') as archivo:
        archivo.write(f"# Comparación de Métodos Numéricos - f(x) = eˣ - x² + 1\n")
        archivo.write(f"# Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        archivo.write("#\n")
        
        archivo.write("Método,Raíz_Encontrada,Iteraciones,Convergencia,Precisión_f(raíz),Tipo_Convergencia,Eficiencia\n")
        
        for metodo, raiz, iteraciones, convergencia in resultados:
            if convergencia and raiz is not None:
                def f(x):
                    return math.exp(x) - x**2 + 1
                
                precision = abs(f(raiz))
                precision_str = f"{precision:.2e}"
                
                if metodo == "Bisección":
                    tipo_conv = "Lineal"
                    eficiencia = "Baja"
                elif metodo == "Regula Falsi":
                    tipo_conv = "Superlineal"
                    eficiencia = "Media"
                elif metodo == "Newton":
                    tipo_conv = "Cuadrática"
                    eficiencia = "Alta"
                else:
                    tipo_conv = "Desconocida"
                    eficiencia = "Media"
                
                archivo.write(f"{metodo},{raiz:.9f},{iteraciones},Sí,{precision_str},{tipo_conv},{eficiencia}\n")
            else:
                archivo.write(f"{metodo},No convergió,{iteraciones},No,N/A,N/A,N/A\n")


def crear_analisis_convergencia(metodos_historial, nombre_archivo):
    """Crea análisis de convergencia optimizado para visualización"""
    ruta = os.path.join("resultados", nombre_archivo)
    
    with open(ruta, 'w', newline='', encoding='utf-8') as archivo:
        archivo.write(f"# Análisis de Convergencia - f(x) = eˣ - x² + 1\n")
        archivo.write(f"# Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        archivo.write("#\n")
        
        archivo.write("Método,Iteración,Valor_Actual,Error_Relativo,Reducción_Error,Tipo_Convergencia\n")
        
        for metodo, historial, tipo_conv in metodos_historial:
            for i, iteracion in enumerate(historial):
                if 'x_actual' in iteracion:  # Newton
                    valor = redondear_significativos(iteracion['x_actual'], 9)
                elif 'c' in iteracion:  # Bisección/Regula Falsi
                    valor = redondear_significativos(iteracion['c'], 9)
                else:
                    continue
                
                error_rel = iteracion.get('error_relativo')
                error_str = f"{error_rel:.2e}" if error_rel is not None else ""
                
                # Calcular reducción de error
                if i > 0 and error_rel is not None:
                    error_anterior = historial[i-1].get('error_relativo')
                    if error_anterior is not None and error_anterior != 0:
                        reduccion = error_rel / error_anterior
                        reduccion_str = f"{reduccion:.4f}"
                    else:
                        reduccion_str = "N/A"
                else:
                    reduccion_str = "N/A"
                
                archivo.write(f"{metodo},{i+1},{valor},{error_str},{reduccion_str},{tipo_conv}\n")


if __name__ == "__main__":
    generar_csv_visualizacion_completo()
