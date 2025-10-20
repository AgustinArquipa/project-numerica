"""
Funciones de exportación específicas para el método de Halley con notación científica.
"""

import os
from datetime import datetime
from .precision import formato_exponencial_legible


def exportar_halley_csv_cientifico(
    historial: list,
    nombre_archivo: str,
    directorio: str = "resultados",
    precision_calculadora: int = 9
) -> str:
    """
    Exporta el historial del método de Halley a CSV con notación científica.
    
    Args:
        historial: Lista con el historial de iteraciones
        nombre_archivo: Nombre del archivo CSV
        directorio: Directorio donde guardar el archivo
        precision_calculadora: Número de cifras significativas
        
    Returns:
        Ruta del archivo generado
    """
    
    # Crear directorio si no existe
    if not os.path.exists(directorio):
        os.makedirs(directorio)
    
    ruta = os.path.join(directorio, nombre_archivo)
    
    with open(ruta, 'w', newline='', encoding='utf-8') as archivo:
        # Escribir encabezado
        archivo.write(f"# Método de Halley - Historial de Iteraciones\n")
        archivo.write(f"# Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        archivo.write(f"# Total de iteraciones: {len(historial)}\n")
        archivo.write(f"# Notación científica: 4.47x10^-5\n")
        archivo.write(f"# Precisión de calculadora: {precision_calculadora} cifras significativas\n")
        archivo.write("#\n")
        
        # Escribir encabezados de columnas
        archivo.write("Iteración,x_anterior,f(x),f'(x),f''(x),Denominador,Delta_x,x_actual,Error_Relativo,Diferencia,Estado\n")
        
        for i, iteracion in enumerate(historial):
            # Formatear valores normales
            x_ant = f"{iteracion['x_anterior']:.9f}"
            
            # Formatear f(x) con notación científica si es muy pequeño
            fx_valor = iteracion['f(x)']
            if abs(fx_valor) < 1e-3:
                fx = formato_exponencial_legible(fx_valor, precision_calculadora)
            else:
                fx = f"{fx_valor:.9f}"
            
            # Formatear f'(x) con notación científica si es muy pequeño
            fpx_valor = iteracion['f\'(x)']
            if abs(fpx_valor) < 1e-3:
                fpx = formato_exponencial_legible(fpx_valor, precision_calculadora)
            else:
                fpx = f"{fpx_valor:.9f}"
            
            # Formatear f''(x) con notación científica si es muy pequeño
            fppx_valor = iteracion['f\'\'(x)']
            if abs(fppx_valor) < 1e-3:
                fppx = formato_exponencial_legible(fppx_valor, precision_calculadora)
            else:
                fppx = f"{fppx_valor:.9f}"
            
            # Formatear denominador con notación científica si es muy pequeño
            denominador_valor = iteracion['denominador']
            if abs(denominador_valor) < 1e-3:
                denominador = formato_exponencial_legible(denominador_valor, precision_calculadora)
            else:
                denominador = f"{denominador_valor:.9f}"
            
            # Formatear delta_x con notación científica si es muy pequeño
            delta_x_valor = iteracion['delta_x']
            if abs(delta_x_valor) < 1e-3:
                delta_x = formato_exponencial_legible(delta_x_valor, precision_calculadora)
            else:
                delta_x = f"{delta_x_valor:.9f}"
            
            # Formatear x_actual
            x_actual = f"{iteracion['x_actual']:.9f}"
            
            # Formatear error relativo con notación científica
            error_rel = iteracion.get('error_relativo')
            if error_rel is not None:
                if abs(error_rel) < 1e-3:
                    error_rel_str = formato_exponencial_legible(error_rel, precision_calculadora)
                else:
                    error_rel_str = f"{error_rel:.9f}"
            else:
                error_rel_str = ""
            
            # Formatear diferencia
            diferencia = f"{iteracion['diferencia']:.9f}"
            
            # Estado
            if abs(fx_valor) < 1e-6:
                estado = "Convergido"
            elif error_rel is not None and error_rel < 1e-6:
                estado = "Convergido"
            elif i == len(historial) - 1:
                estado = "Final"
            else:
                estado = "Activo"
            
            archivo.write(f"{iteracion['iteracion']},{x_ant},{fx},{fpx},{fppx},{denominador},{delta_x},{x_actual},{error_rel_str},{diferencia},{estado}\n")
    
    return ruta


def exportar_comparacion_halley_csv(
    resultados: dict,
    nombre_archivo: str,
    directorio: str = "resultados"
) -> str:
    """
    Exporta una comparación de métodos incluyendo Halley a CSV.
    
    Args:
        resultados: Diccionario con resultados de diferentes métodos
        nombre_archivo: Nombre del archivo CSV
        directorio: Directorio donde guardar el archivo
        
    Returns:
        Ruta del archivo generado
    """
    
    # Crear directorio si no existe
    if not os.path.exists(directorio):
        os.makedirs(directorio)
    
    ruta = os.path.join(directorio, nombre_archivo)
    
    with open(ruta, 'w', newline='', encoding='utf-8') as archivo:
        # Escribir encabezado
        archivo.write(f"# Comparación de métodos numéricos (incluyendo Halley)\n")
        archivo.write(f"# Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        archivo.write("#\n")
        
        # Escribir encabezados de columnas
        archivo.write("Método,Raíz,Iteraciones,Convergencia,Error_Absoluto,Precisión\n")
        
        for metodo, datos in resultados.items():
            if datos['convergencia'] and datos['raiz'] is not None:
                raiz = datos['raiz']
                iteraciones = datos['iteraciones']
                convergencia = "Sí" if datos['convergencia'] else "No"
                error_abs = datos.get('error_absoluto', 0)
                precision = f"{error_abs:.2e}" if error_abs > 0 else "Exacta"
                
                archivo.write(f"{metodo},{raiz:.10f},{iteraciones},{convergencia},{error_abs:.2e},{precision}\n")
            else:
                archivo.write(f"{metodo},No convergió,{datos['iteraciones']},No,N/A,N/A\n")
    
    return ruta


def crear_analisis_halley(
    historial: list,
    raiz: float,
    iteraciones: int,
    convergencia: bool
) -> dict:
    """
    Crea un análisis detallado del método de Halley.
    
    Args:
        historial: Historial de iteraciones
        raiz: Raíz encontrada
        iteraciones: Número de iteraciones
        convergencia: Si convergió o no
        
    Returns:
        Diccionario con análisis detallado
    """
    
    if not historial:
        return {
            'convergencia': convergencia,
            'iteraciones': iteraciones,
            'raiz': raiz,
            'analisis': 'Sin datos suficientes para análisis'
        }
    
    # Análisis de convergencia
    errores_relativos = [iter['error_relativo'] for iter in historial if iter['error_relativo'] is not None]
    
    analisis = {
        'convergencia': convergencia,
        'iteraciones': iteraciones,
        'raiz': raiz,
        'total_iteraciones': len(historial),
        'errores_relativos': errores_relativos
    }
    
    if len(errores_relativos) > 2:
        # Calcular velocidad de convergencia (cúbica para Halley)
        cocientes = []
        for i in range(1, len(errores_relativos)):
            if errores_relativos[i-1] != 0:
                cocientes.append(errores_relativos[i] / errores_relativos[i-1])
        
        if cocientes:
            analisis['velocidad_convergencia_promedio'] = sum(cocientes) / len(cocientes)
            analisis['velocidad_esperada_halley'] = 1.84  # Orden cúbico
    
    # Análisis de estabilidad
    denominadores = [abs(iter['denominador']) for iter in historial]
    analisis['min_denominador'] = min(denominadores)
    analisis['max_denominador'] = max(denominadores)
    analisis['denominador_promedio'] = sum(denominadores) / len(denominadores)
    
    # Verificar si hay problemas de estabilidad
    if analisis['min_denominador'] < 1e-10:
        analisis['advertencia_denominador_pequeno'] = True
    
    # Análisis de la función en la raíz
    if raiz is not None:
        # Esto se calculará en el código principal
        analisis['valor_funcion_raiz'] = None
    
    return analisis
