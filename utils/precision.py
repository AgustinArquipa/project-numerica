"""
Módulo para control de precisión en cálculos numéricos.

Este módulo permite simular el comportamiento de calculadoras científicas
con mantisa y exponente controlados, útil para comparar resultados
con implementaciones manuales.
"""

import math
from decimal import Decimal, getcontext, ROUND_HALF_EVEN
from typing import Union, Callable


def redondear_significativos(x: float, n_sig: int = 9) -> float:
    """
    Redondea x a n_sig cifras significativas.
    
    Args:
        x: Número a redondear
        n_sig: Número de cifras significativas (por defecto 9)
        
    Returns:
        Número redondeado a n_sig cifras significativas
        
    Examples:
        >>> redondear_significativos(3.14159265359, 4)
        3.142
        >>> redondear_significativos(0.00123456789, 3)
        0.00123
        >>> redondear_significativos(1234567.89, 5)
        1234600.0
    """
    if x == 0:
        return 0.0
    
    # Manejar números negativos
    signo = -1 if x < 0 else 1
    x_abs = abs(x)
    
    # Calcular el exponente
    if x_abs >= 1:
        exponent = int(math.floor(math.log10(x_abs)))
    else:
        exponent = int(math.floor(math.log10(x_abs)))
    
    # Factor para redondear a n_sig cifras significativas
    factor = 10**(n_sig - 1 - exponent)
    
    # Redondear y restaurar
    resultado = round(x_abs * factor) / factor * signo
    
    return resultado


def formato_exponencial_legible(x: float, n_sig: int = 9) -> str:
    """
    Convierte un número a formato exponencial legible (ej: 4.47x10^-5).
    
    Args:
        x: Número a formatear
        n_sig: Número de cifras significativas
        
    Returns:
        String con formato exponencial legible
        
    Examples:
        >>> formato_exponencial_legible(4.46583412e-05)
        "4.47x10^-5"
        >>> formato_exponencial_legible(1.23e-08)
        "1.23x10^-8"
        >>> formato_exponencial_legible(1.23456789e+03)
        "1.23x10^3"
    """
    if x == 0:
        return "0"
    
    # Redondear a n_sig cifras significativas
    x_redondeado = redondear_significativos(x, n_sig)
    
    # Calcular exponente
    x_abs = abs(x_redondeado)
    exponent = int(math.floor(math.log10(x_abs)))
    
    # Calcular mantisa
    mantisa = x_redondeado / (10 ** exponent)
    
    # Formatear mantisa con el número correcto de dígitos
    if n_sig <= 3:
        mantisa_str = f"{mantisa:.2f}"
    elif n_sig <= 6:
        mantisa_str = f"{mantisa:.3f}"
    else:
        # Para n_sig > 6, mostrar 3 dígitos después del punto decimal
        mantisa_str = f"{mantisa:.3f}"
    
    # Eliminar ceros finales innecesarios
    mantisa_str = mantisa_str.rstrip('0').rstrip('.')
    
    # Formatear exponente
    exp_str = f"x10^{exponent}"
    
    return f"{mantisa_str}{exp_str}"


def aplicar_formato_calculadora(x: float, usar_exponencial: bool = True, n_sig: int = 9) -> str:
    """
    Aplica formato de calculadora científica con opción de exponencial legible.
    
    Args:
        x: Número a formatear
        usar_exponencial: Si usar formato exponencial legible para números muy pequeños/grandes
        n_sig: Número de cifras significativas
        
    Returns:
        String formateado para calculadora científica
    """
    if x == 0:
        return "0"
    
    x_abs = abs(x)
    
    # Determinar si usar formato exponencial
    if usar_exponencial and (x_abs < 1e-3 or x_abs > 1e6):
        return formato_exponencial_legible(x, n_sig)
    else:
        # Formato normal con redondeo
        resultado = redondear_significativos(x, n_sig)
        return f"{resultado}"


def configurar_decimal_precision(precision: int = 9, exponente_max: int = 999, exponente_min: int = -999):
    """
    Configura la precisión del módulo decimal para simular calculadora científica.
    
    Args:
        precision: Número de dígitos en la mantisa (por defecto 9)
        exponente_max: Exponente máximo (por defecto 999)
        exponente_min: Exponente mínimo (por defecto -999)
    """
    getcontext().prec = precision
    getcontext().Emax = exponente_max
    getcontext().Emin = exponente_min
    getcontext().rounding = ROUND_HALF_EVEN


def redondear_decimal(x: Union[float, Decimal], precision: int = 9) -> Decimal:
    """
    Convierte un número a Decimal con precisión controlada.
    
    Args:
        x: Número a convertir
        precision: Precisión deseada
        
    Returns:
        Decimal con la precisión especificada
    """
    configurar_decimal_precision(precision)
    return Decimal(str(x))


def aplicar_precision_calculadora(valor: float, mantisa: int = 9) -> float:
    """
    Aplica precisión de calculadora científica (mantisa de 9 dígitos, exponente de 3).
    
    Args:
        valor: Valor a procesar
        mantisa: Número de dígitos en la mantisa
        
    Returns:
        Valor con precisión de calculadora científica
    """
    return redondear_significativos(valor, mantisa)


def procesar_iteracion_con_precision(
    iteracion_data: dict, 
    precision: int = 9,
    usar_decimal: bool = False
) -> dict:
    """
    Procesa los datos de una iteración aplicando precisión controlada.
    
    Args:
        iteracion_data: Diccionario con datos de la iteración
        precision: Precisión deseada
        usar_decimal: Si usar Decimal en lugar de float redondeado
        
    Returns:
        Diccionario con valores procesados con precisión controlada
    """
    resultado = {}
    
    for clave, valor in iteracion_data.items():
        if isinstance(valor, (int, float)) and valor != 0:
            if usar_decimal:
                resultado[clave] = redondear_decimal(valor, precision)
            else:
                resultado[clave] = redondear_significativos(valor, precision)
        else:
            resultado[clave] = valor
    
    return resultado


def procesar_historial_con_precision(
    historial: list, 
    precision: int = 9,
    usar_decimal: bool = False
) -> list:
    """
    Procesa todo el historial aplicando precisión controlada.
    
    Args:
        historial: Lista de diccionarios con datos de iteraciones
        precision: Precisión deseada
        usar_decimal: Si usar Decimal en lugar de float redondeado
        
    Returns:
        Lista con historial procesado con precisión controlada
    """
    return [procesar_iteracion_con_precision(iteracion, precision, usar_decimal) 
            for iteracion in historial]


def comparar_precisiones(valor: float, precisiones: list = [6, 8, 9, 10, 12]) -> dict:
    """
    Compara cómo se ve un valor con diferentes precisiones.
    
    Args:
        valor: Valor a comparar
        precisiones: Lista de precisiones a probar
        
    Returns:
        Diccionario con el valor redondeado a cada precisión
    """
    return {f"precisión_{p}": redondear_significativos(valor, p) for p in precisiones}


def simular_calculadora_cientifica(
    funcion: Callable[[float], float],
    valores: list,
    precision: int = 9
) -> dict:
    """
    Simula el comportamiento de una calculadora científica.
    
    Args:
        funcion: Función a evaluar
        valores: Lista de valores a evaluar
        precision: Precisión de la calculadora
        
    Returns:
        Diccionario con valores evaluados con precisión de calculadora
    """
    resultados = {}
    
    for valor in valores:
        # Evaluar función
        resultado = funcion(valor)
        
        # Aplicar precisión de calculadora
        valor_redondeado = redondear_significativos(valor, precision)
        resultado_redondeado = redondear_significativos(resultado, precision)
        
        resultados[f"f({valor_redondeado})"] = resultado_redondeado
    
    return resultados


def mostrar_precision_analysis(valor: float):
    """
    Muestra un análisis de cómo se ve un valor con diferentes precisiones.
    
    Args:
        valor: Valor a analizar
    """
    print(f"Valor original: {valor}")
    print(f"Valor original (formato científico): {valor:.10e}")
    print()
    
    precisiones = [6, 7, 8, 9, 10, 12]
    print("Precisiones diferentes:")
    for p in precisiones:
        redondeado = redondear_significativos(valor, p)
        print(f"  {p} cifras significativas: {redondeado}")
    
    print()
    print("Comparación con calculadora científica (9 cifras):")
    calc_valor = redondear_significativos(valor, 9)
    print(f"  Calculadora: {calc_valor}")


# Ejemplo de uso
if __name__ == "__main__":
    # Ejemplo con π
    pi = 3.141592653589793
    print("Análisis de precisión para π:")
    mostrar_precision_analysis(pi)
    
    print("\n" + "="*50)
    
    # Ejemplo con un número grande
    numero_grande = 1234567.123456789
    print(f"Análisis de precisión para {numero_grande}:")
    mostrar_precision_analysis(numero_grande)
    
    print("\n" + "="*50)
    
    # Ejemplo con un número pequeño
    numero_pequeno = 0.000123456789
    print(f"Análisis de precisión para {numero_pequeno}:")
    mostrar_precision_analysis(numero_pequeno)
    
    print("\n" + "="*50)
    
    # Simular calculadora científica
    def f(x):
        return x**3 - x - 1
    
    valores = [1.0, 1.5, 2.0]
    print("Simulación de calculadora científica:")
    resultados = simular_calculadora_cientifica(f, valores, 9)
    for clave, valor in resultados.items():
        print(f"  {clave} = {valor}")
