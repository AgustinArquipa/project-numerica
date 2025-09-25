"""
Módulo para exportar resultados de métodos numéricos a diferentes formatos.

Este módulo permite exportar el historial de iteraciones a CSV, JSON y otros formatos
para análisis posterior y visualización de resultados.
"""

import csv
import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional, Union
from .precision import procesar_historial_con_precision, aplicar_precision_calculadora


def exportar_iteraciones_csv(
    historial: List[Dict],
    nombre_archivo: str = "iteraciones.csv",
    directorio: str = "resultados",
    incluir_metadata: bool = True,
    precision_calculadora: Optional[int] = None,
    usar_decimal: bool = False
) -> str:
    """
    Exporta el historial de iteraciones a un archivo CSV.
    
    Args:
        historial: Lista de diccionarios con los valores de cada iteración
        nombre_archivo: Nombre del archivo CSV a generar
        directorio: Directorio donde guardar el archivo
        incluir_metadata: Si incluir información adicional en comentarios
        precision_calculadora: Precisión de calculadora científica (ej: 9 para mantisa de 9 dígitos)
        usar_decimal: Si usar Decimal en lugar de float redondeado
        
    Returns:
        Ruta completa del archivo generado
        
    Raises:
        ValueError: Si el historial está vacío
    """
    if not historial:
        raise ValueError("El historial está vacío. No se puede exportar.")
    
    # Crear directorio si no existe
    if not os.path.exists(directorio):
        os.makedirs(directorio)
    
    # Generar nombre de archivo con timestamp si no se especifica
    if nombre_archivo == "iteraciones.csv":
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"iteraciones_{timestamp}.csv"
    
    ruta_completa = os.path.join(directorio, nombre_archivo)
    
    # Aplicar precisión de calculadora si se especifica
    if precision_calculadora is not None:
        historial_procesado = procesar_historial_con_precision(
            historial, precision_calculadora, usar_decimal
        )
    else:
        historial_procesado = historial
    
    # Encabezados: usar las claves del primer diccionario
    campos = list(historial_procesado[0].keys())
    
    with open(ruta_completa, mode="w", newline="", encoding="utf-8") as archivo:
        # Escribir comentarios de metadata si se solicita
        if incluir_metadata:
            archivo.write(f"# Archivo generado el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            archivo.write(f"# Total de iteraciones: {len(historial)}\n")
            archivo.write(f"# Columnas: {', '.join(campos)}\n")
            if precision_calculadora is not None:
                archivo.write(f"# Precisión de calculadora: {precision_calculadora} cifras significativas\n")
                if usar_decimal:
                    archivo.write("# Tipo de precisión: Decimal\n")
                else:
                    archivo.write("# Tipo de precisión: Float redondeado\n")
            archivo.write("#\n")
        
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(historial_procesado)
    
    print(f"✅ Archivo CSV generado: {ruta_completa}")
    return ruta_completa


def exportar_resultado_completo(
    metodo: str,
    funcion: str,
    parametros: Dict[str, Any],
    resultado: Dict[str, Any],
    historial: List[Dict],
    nombre_archivo: Optional[str] = None,
    directorio: str = "resultados"
) -> str:
    """
    Exporta un resultado completo incluyendo metadata, parámetros y historial.
    
    Args:
        metodo: Nombre del método utilizado
        funcion: Descripción de la función
        parametros: Parámetros utilizados en el método
        resultado: Resultado del método (raíz, iteraciones, convergencia)
        historial: Historial de iteraciones
        nombre_archivo: Nombre base del archivo (se generará automáticamente si es None)
        directorio: Directorio donde guardar los archivos
        
    Returns:
        Ruta del archivo CSV generado
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if nombre_archivo is None:
        nombre_archivo = f"{metodo.lower()}_{timestamp}.csv"
    else:
        nombre_archivo = f"{nombre_archivo}_{timestamp}.csv"
    
    # Crear directorio si no existe
    if not os.path.exists(directorio):
        os.makedirs(directorio)
    
    ruta_completa = os.path.join(directorio, nombre_archivo)
    
    # Encabezados: usar las claves del primer diccionario del historial
    campos = list(historial[0].keys()) if historial else []
    
    with open(ruta_completa, mode="w", newline="", encoding="utf-8") as archivo:
        # Escribir metadata completa
        archivo.write(f"# ================================================\n")
        archivo.write(f"# RESULTADO DE MÉTODO NUMÉRICO\n")
        archivo.write(f"# ================================================\n")
        archivo.write(f"# Método: {metodo}\n")
        archivo.write(f"# Función: {funcion}\n")
        archivo.write(f"# Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        archivo.write(f"#\n")
        
        # Parámetros utilizados
        archivo.write(f"# PARÁMETROS:\n")
        for clave, valor in parametros.items():
            archivo.write(f"# {clave}: {valor}\n")
        archivo.write(f"#\n")
        
        # Resultado obtenido
        archivo.write(f"# RESULTADO:\n")
        for clave, valor in resultado.items():
            archivo.write(f"# {clave}: {valor}\n")
        archivo.write(f"#\n")
        archivo.write(f"# TOTAL DE ITERACIONES: {len(historial)}\n")
        archivo.write(f"# ================================================\n")
        archivo.write(f"#\n")
        
        # Escribir datos
        if campos:
            escritor = csv.DictWriter(archivo, fieldnames=campos)
            escritor.writeheader()
            escritor.writerows(historial)
    
    print(f"✅ Archivo CSV completo generado: {ruta_completa}")
    return ruta_completa


def exportar_comparacion_csv(
    comparacion: Dict[str, Any],
    nombre_archivo: str = "comparacion_metodos.csv",
    directorio: str = "resultados"
) -> str:
    """
    Exporta una comparación de métodos a CSV.
    
    Args:
        comparacion: Diccionario con la comparación de métodos
        nombre_archivo: Nombre del archivo CSV
        directorio: Directorio donde guardar el archivo
        
    Returns:
        Ruta del archivo generado
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"comparacion_{timestamp}.csv" if nombre_archivo == "comparacion_metodos.csv" else nombre_archivo
    
    # Crear directorio si no existe
    if not os.path.exists(directorio):
        os.makedirs(directorio)
    
    ruta_completa = os.path.join(directorio, nombre_archivo)
    
    with open(ruta_completa, mode="w", newline="", encoding="utf-8") as archivo:
        archivo.write(f"# Comparación de métodos numéricos\n")
        archivo.write(f"# Generado el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        archivo.write(f"#\n")
        
        # Escribir comparación como CSV
        writer = csv.writer(archivo)
        writer.writerow(["Método", "Raíz", "Iteraciones", "Convergencia"])
        
        for metodo, datos in comparacion.items():
            if isinstance(datos, dict) and 'raiz' in datos:
                writer.writerow([
                    metodo,
                    datos.get('raiz', 'N/A'),
                    datos.get('iteraciones', 'N/A'),
                    datos.get('convergencia', 'N/A')
                ])
    
    print(f"✅ Archivo de comparación generado: {ruta_completa}")
    return ruta_completa


def exportar_a_json(
    data: Union[Dict, List],
    nombre_archivo: str = "resultados.json",
    directorio: str = "resultados",
    indent: int = 2
) -> str:
    """
    Exporta datos a formato JSON.
    
    Args:
        data: Datos a exportar (diccionario o lista)
        nombre_archivo: Nombre del archivo JSON
        directorio: Directorio donde guardar el archivo
        indent: Indentación para el JSON
        
    Returns:
        Ruta del archivo generado
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"resultados_{timestamp}.json" if nombre_archivo == "resultados.json" else nombre_archivo
    
    # Crear directorio si no existe
    if not os.path.exists(directorio):
        os.makedirs(directorio)
    
    ruta_completa = os.path.join(directorio, nombre_archivo)
    
    # Agregar metadata
    if isinstance(data, dict):
        data_con_metadata = {
            "metadata": {
                "fecha_generacion": datetime.now().isoformat(),
                "version": "1.0"
            },
            "datos": data
        }
    else:
        data_con_metadata = {
            "metadata": {
                "fecha_generacion": datetime.now().isoformat(),
                "version": "1.0"
            },
            "datos": data
        }
    
    with open(ruta_completa, mode="w", encoding="utf-8") as archivo:
        json.dump(data_con_metadata, archivo, indent=indent, ensure_ascii=False)
    
    print(f"✅ Archivo JSON generado: {ruta_completa}")
    return ruta_completa


def crear_tabla_resumen(
    resultados: List[Dict[str, Any]],
    nombre_archivo: str = "resumen_metodos.csv",
    directorio: str = "resultados"
) -> str:
    """
    Crea una tabla resumen con los resultados de múltiples métodos.
    
    Args:
        resultados: Lista de diccionarios con resultados de métodos
        nombre_archivo: Nombre del archivo CSV
        directorio: Directorio donde guardar el archivo
        
    Returns:
        Ruta del archivo generado
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"resumen_{timestamp}.csv" if nombre_archivo == "resumen_metodos.csv" else nombre_archivo
    
    # Crear directorio si no existe
    if not os.path.exists(directorio):
        os.makedirs(directorio)
    
    ruta_completa = os.path.join(directorio, nombre_archivo)
    
    with open(ruta_completa, mode="w", newline="", encoding="utf-8") as archivo:
        archivo.write(f"# Resumen de métodos numéricos\n")
        archivo.write(f"# Generado el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        archivo.write(f"#\n")
        
        writer = csv.writer(archivo)
        writer.writerow([
            "Método", 
            "Tipo", 
            "Raíz", 
            "Iteraciones", 
            "Convergencia", 
            "Error Final",
            "Tiempo (s)"
        ])
        
        for resultado in resultados:
            writer.writerow([
                resultado.get('metodo', 'N/A'),
                resultado.get('tipo', 'N/A'),
                resultado.get('raiz', 'N/A'),
                resultado.get('iteraciones', 'N/A'),
                resultado.get('convergencia', 'N/A'),
                resultado.get('error_final', 'N/A'),
                resultado.get('tiempo', 'N/A')
            ])
    
    print(f"✅ Tabla resumen generada: {ruta_completa}")
    return ruta_completa


def listar_archivos_generados(directorio: str = "resultados") -> List[str]:
    """
    Lista todos los archivos generados en el directorio de resultados.
    
    Args:
        directorio: Directorio a revisar
        
    Returns:
        Lista de archivos encontrados
    """
    if not os.path.exists(directorio):
        return []
    
    archivos = []
    for archivo in os.listdir(directorio):
        if archivo.endswith(('.csv', '.json')):
            ruta_completa = os.path.join(directorio, archivo)
            tamaño = os.path.getsize(ruta_completa)
            fecha = datetime.fromtimestamp(os.path.getmtime(ruta_completa))
            archivos.append({
                'nombre': archivo,
                'ruta': ruta_completa,
                'tamaño': tamaño,
                'fecha': fecha.strftime('%Y-%m-%d %H:%M:%S')
            })
    
    return sorted(archivos, key=lambda x: x['fecha'], reverse=True)


def limpiar_archivos_antiguos(directorio: str = "resultados", dias: int = 7) -> int:
    """
    Elimina archivos más antiguos que el número de días especificado.
    
    Args:
        directorio: Directorio a limpiar
        dias: Número de días de antigüedad
        
    Returns:
        Número de archivos eliminados
    """
    if not os.path.exists(directorio):
        return 0
    
    from datetime import timedelta
    fecha_limite = datetime.now() - timedelta(days=dias)
    archivos_eliminados = 0
    
    for archivo in os.listdir(directorio):
        ruta_completa = os.path.join(directorio, archivo)
        if os.path.isfile(ruta_completa):
            fecha_modificacion = datetime.fromtimestamp(os.path.getmtime(ruta_completa))
            if fecha_modificacion < fecha_limite:
                os.remove(ruta_completa)
                archivos_eliminados += 1
    
    print(f"🧹 Se eliminaron {archivos_eliminados} archivos antiguos")
    return archivos_eliminados


# Ejemplo de uso
if __name__ == "__main__":
    # Ejemplo de historial de iteraciones
    historial_ejemplo = [
        {'iteracion': 1, 'a': 1.0, 'b': 2.0, 'c': 1.5, 'f(a)': -1.0, 'f(b)': 5.0, 'f(c)': 0.875, 'error_relativo': None},
        {'iteracion': 2, 'a': 1.0, 'b': 1.5, 'c': 1.25, 'f(a)': -1.0, 'f(b)': 0.875, 'f(c)': -0.296875, 'error_relativo': 0.2},
        {'iteracion': 3, 'a': 1.25, 'b': 1.5, 'c': 1.375, 'f(a)': -0.296875, 'f(b)': 0.875, 'f(c)': 0.224609, 'error_relativo': 0.090909}
    ]
    
    # Exportar historial simple
    exportar_iteraciones_csv(historial_ejemplo, "ejemplo_biseccion.csv")
    
    # Exportar resultado completo
    exportar_resultado_completo(
        metodo="Bisección",
        funcion="f(x) = x³ - x - 1",
        parametros={"a": 1.0, "b": 2.0, "tolerancia": 1e-6},
        resultado={"raiz": 1.32471796, "iteraciones": 20, "convergencia": True},
        historial=historial_ejemplo,
        nombre_archivo="ejemplo_completo"
    )
    
    # Listar archivos generados
    archivos = listar_archivos_generados()
    print(f"\nArchivos generados: {len(archivos)}")
    for archivo in archivos:
        print(f"  - {archivo['nombre']} ({archivo['fecha']})")
