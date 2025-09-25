#!/usr/bin/env python3
"""
Generador de archivos CSV con formato exponencial legible.

Este script genera archivos CSV con números en formato exponencial legible
(como 4.47x10^-5) optimizado para la extensión CSV de VS Code/Cursor.
"""

import sys
import os
import math
from datetime import datetime

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from cerrados import biseccion, regula_falsi, regula_falsi_modificada
from abiertos import newton
from utils import formato_exponencial_legible, aplicar_formato_calculadora


def generar_csv_exponencial():
    """Genera archivos CSV con formato exponencial legible"""
    print("=" * 80)
    print("GENERADOR DE CSV CON FORMATO EXPONENCIAL LEGIBLE")
    print("=" * 80)
    print("Formato: 4.47x10^-5 (en lugar de 4.46583412e-05)")
    print("Optimizado para extensión CSV de VS Code/Cursor")
    print()
    
    # Definir función
    def f(x):
        return math.exp(x) - x**2 + 1
    
    def f_derivada(x):
        return math.exp(x) - 2*x
    
    print("📋 Función: f(x) = eˣ - x² + 1")
    print("📍 Intervalo inicial: a = -5.0, b = 0.0")
    print("🎯 Tolerancia: 1e-6")
    print()
    
    # Configuración
    a, b = -5.0, 0.0
    tolerancia = 1e-6
    max_iteraciones = 100
    
    # Verificar cambio de signo
    print(f"🔍 Verificando cambio de signo:")
    print(f"   f({a}) = {f(a):.6f}")
    print(f"   f({b}) = {f(b):.6f}")
    print(f"   f({a}) × f({b}) = {f(a) * f(b):.6f} {'< 0' if f(a) * f(b) < 0 else '≥ 0'}")
    print()
    
    # ========================================
    # REGULA FALSI MODIFICADA CON FORMATO EXPONENCIAL
    # ========================================
    print("🔄 Generando Regula Falsi Modificada con formato exponencial...")
    raiz_rfm, iter_rfm, conv_rfm, hist_rfm = regula_falsi_modificada(
        f, a, b, tolerancia=tolerancia, max_iteraciones=max_iteraciones, 
        factor_reduccion=0.5, mostrar_iteraciones=False
    )
    
    if conv_rfm and raiz_rfm:
        print(f"✅ Convergencia alcanzada en {iter_rfm} iteraciones")
        print(f"🎯 Raíz aproximada: {raiz_rfm:.10f}")
        print(f"🔍 f(raíz) = {f(raiz_rfm):.2e}")
        
        # Crear CSV con formato exponencial
        crear_csv_exponencial_regula_falsi_modificada(hist_rfm, "regula_falsi_modificada_exponencial.csv")
        print("✅ Archivo generado: regula_falsi_modificada_exponencial.csv")
    else:
        print("❌ No se alcanzó convergencia")
    
    print()
    
    # ========================================
    # NEWTON CON FORMATO EXPONENCIAL
    # ========================================
    print("🔄 Generando Newton con formato exponencial...")
    x0 = (a + b) / 2
    raiz_n, iter_n, conv_n, hist_n = newton(
        f, f_derivada, x0, tolerancia=tolerancia, max_iteraciones=max_iteraciones, mostrar_iteraciones=False
    )
    
    if conv_n and raiz_n:
        print(f"✅ Convergencia alcanzada en {iter_n} iteraciones")
        print(f"🎯 Raíz aproximada: {raiz_n:.10f}")
        print(f"🔍 f(raíz) = {f(raiz_n):.2e}")
        
        # Crear CSV con formato exponencial
        crear_csv_exponencial_newton(hist_n, "newton_exponencial.csv")
        print("✅ Archivo generado: newton_exponencial.csv")
    
    print()
    
    # ========================================
    # DEMOSTRACIÓN DEL FORMATO EXPONENCIAL
    # ========================================
    print("📊 DEMOSTRACIÓN DEL FORMATO EXPONENCIAL:")
    valores_demo = [
        4.46583412e-05,
        1.15737986e-06,
        1.86318279e-07,
        8.88e-16,
        3.57e-07,
        0.00123456789,
        1234567.89
    ]
    
    print("Valor original → Formato exponencial legible")
    print("-" * 50)
    for valor in valores_demo:
        formato_legible = formato_exponencial_legible(valor, 9)
        print(f"{valor:15.2e} → {formato_legible}")
    
    print()
    print("🎯 ARCHIVOS GENERADOS:")
    print("📁 regula_falsi_modificada_exponencial.csv")
    print("📁 newton_exponencial.csv")
    print()
    print("💡 Los números muy pequeños ahora se muestran como:")
    print("   • 4.46583412e-05 → 4.47x10^-5")
    print("   • 1.15737986e-06 → 1.16x10^-6")
    print("   • 1.86318279e-07 → 1.86x10^-7")
    print()
    print("📊 Abre estos archivos en VS Code/Cursor para ver la visualización interactiva!")


def crear_csv_exponencial_regula_falsi_modificada(historial, nombre_archivo):
    """Crea CSV de Regula Falsi Modificada con formato exponencial legible"""
    ruta = os.path.join("resultados", nombre_archivo)
    
    with open(ruta, 'w', newline='', encoding='utf-8') as archivo:
        archivo.write(f"# Regula Falsi Modificada - f(x) = eˣ - x² + 1\n")
        archivo.write(f"# Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        archivo.write(f"# Intervalo inicial: a = -5.0, b = 0.0\n")
        archivo.write(f"# Tolerancia: 1e-6, Factor reducción: 0.5\n")
        archivo.write(f"# Formato exponencial: 4.47x10^-5\n")
        archivo.write(f"# Total iteraciones: {len(historial)}\n")
        archivo.write("#\n")
        
        archivo.write("Iteración,Extremo_a,Extremo_b,Aproximación_c,f(a),f(b),f(c),Error_Relativo,Longitud_Intervalo,Contador_a,Contador_b,Reducción_Aplicada,Estado\n")
        
        for i, iteracion in enumerate(historial):
            # Formatear valores normales
            a = f"{iteracion['a']:.9f}"
            b = f"{iteracion['b']:.9f}"
            c = f"{iteracion['c']:.9f}"
            fa = f"{iteracion['f(a)']:.9f}"
            fb = f"{iteracion['f(b)']:.9f}"
            
            # Formatear f(c) con exponencial si es muy pequeño
            fc_valor = iteracion['f(c)']
            if abs(fc_valor) < 1e-3:
                fc = formato_exponencial_legible(fc_valor, 9)
            else:
                fc = f"{fc_valor:.9f}"
            
            # Formatear error relativo con exponencial
            error_rel = iteracion.get('error_relativo')
            if error_rel is not None:
                if abs(error_rel) < 1e-3:
                    error_str = formato_exponencial_legible(error_rel, 9)
                else:
                    error_str = f"{error_rel:.9f}"
            else:
                error_str = ""
            
            # Formatear longitud del intervalo
            longitud = f"{iteracion['longitud_intervalo']:.9f}"
            
            # Contadores
            contador_a = int(iteracion['contador_a'])
            contador_b = int(iteracion['contador_b'])
            reduccion = "Sí" if iteracion['reduccion_aplicada'] else "No"
            
            # Estado
            if abs(fc_valor) < 1e-6:
                estado = "Convergido"
            elif error_rel is not None and error_rel < 1e-6:
                estado = "Convergido"
            elif i == len(historial) - 1:
                estado = "Final"
            else:
                estado = "Activo"
            
            archivo.write(f"{i+1},{a},{b},{c},{fa},{fb},{fc},{error_str},{longitud},{contador_a},{contador_b},{reduccion},{estado}\n")


def crear_csv_exponencial_newton(historial, nombre_archivo):
    """Crea CSV de Newton con formato exponencial legible"""
    ruta = os.path.join("resultados", nombre_archivo)
    
    with open(ruta, 'w', newline='', encoding='utf-8') as archivo:
        archivo.write(f"# Método de Newton - f(x) = eˣ - x² + 1\n")
        archivo.write(f"# Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        archivo.write(f"# Punto inicial: -2.5, Tolerancia: 1e-6\n")
        archivo.write(f"# Formato exponencial: 8.88x10^-16\n")
        archivo.write(f"# Total iteraciones: {len(historial)}\n")
        archivo.write("#\n")
        
        archivo.write("Iteración,x_anterior,f(x),f'(x),x_nuevo,Error_Relativo,Error_Cuadrático,Estado\n")
        
        for i, iteracion in enumerate(historial):
            # Formatear valores normales
            x_ant = f"{iteracion['x_anterior']:.9f}"
            
            # Formatear f(x) con exponencial si es muy pequeño
            fx_valor = iteracion['f(x_anterior)']
            if abs(fx_valor) < 1e-3:
                fx = formato_exponencial_legible(fx_valor, 9)
            else:
                fx = f"{fx_valor:.9f}"
            
            # Formatear f'(x)
            fpx = f"{iteracion['f\'(x_anterior)']:.9f}"
            
            # Formatear x_nuevo
            x_nuevo = f"{iteracion['x_actual']:.9f}"
            
            # Formatear error relativo con exponencial
            error_rel = iteracion.get('error_relativo')
            if error_rel is not None:
                if abs(error_rel) < 1e-3:
                    error_rel_str = formato_exponencial_legible(error_rel, 9)
                else:
                    error_rel_str = f"{error_rel:.9f}"
            else:
                error_rel_str = ""
            
            # Formatear error cuadrático con exponencial
            error_cuad = iteracion.get('error_cuadratico')
            if error_cuad is not None:
                if abs(error_cuad) < 1e-3:
                    error_cuad_str = formato_exponencial_legible(error_cuad, 9)
                else:
                    error_cuad_str = f"{error_cuad:.9f}"
            else:
                error_cuad_str = ""
            
            # Estado
            if abs(fx_valor) < 1e-6:
                estado = "Convergido"
            elif error_rel is not None and error_rel < 1e-6:
                estado = "Convergido"
            elif i == len(historial) - 1:
                estado = "Final"
            else:
                estado = "Activo"
            
            archivo.write(f"{i+1},{x_ant},{fx},{fpx},{x_nuevo},{error_rel_str},{error_cuad_str},{estado}\n")


if __name__ == "__main__":
    generar_csv_exponencial()
