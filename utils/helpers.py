"""
Funciones auxiliares para métodos numéricos.

Este módulo contiene utilidades comunes para el cálculo de errores,
validaciones y técnicas de aceleración de convergencia.
"""

import math
from typing import Callable, Tuple, Optional


def error_absoluto(valor_real: float, valor_aproximado: float) -> float:
    """
    Calcula el error absoluto entre un valor real y una aproximación.
    
    Args:
        valor_real: El valor real (exacto)
        valor_aproximado: El valor aproximado
        
    Returns:
        Error absoluto: |valor_real - valor_aproximado|
    """
    return abs(valor_real - valor_aproximado)


def error_relativo(valor_real: float, valor_aproximado: float) -> float:
    """
    Calcula el error relativo entre un valor real y una aproximación.
    
    Args:
        valor_real: El valor real (exacto)
        valor_aproximado: El valor aproximado
        
    Returns:
        Error relativo: |valor_real - valor_aproximado| / |valor_real|
    """
    if valor_real == 0:
        return float('inf') if valor_aproximado != 0 else 0
    return abs(valor_real - valor_aproximado) / abs(valor_real)


def validar_intervalo(func: Callable[[float], float], a: float, b: float) -> bool:
    """
    Valida que en el intervalo [a,b] la función cambie de signo (teorema de Bolzano).
    
    Args:
        func: Función a evaluar
        a: Extremo inferior del intervalo
        b: Extremo superior del intervalo
        
    Returns:
        True si hay cambio de signo, False en caso contrario
        
    Raises:
        ValueError: Si a >= b
    """
    if a >= b:
        raise ValueError("El extremo inferior 'a' debe ser menor que el extremo superior 'b'")
    
    try:
        fa = func(a)
        fb = func(b)
        return fa * fb < 0  # Cambio de signo
    except (ValueError, ZeroDivisionError):
        raise ValueError("Error al evaluar la función en los extremos del intervalo")


def verificar_convergencia(
    aproximacion_actual: float, 
    aproximacion_anterior: float, 
    tolerancia: float = 1e-6
) -> bool:
    """
    Verifica si se ha alcanzado la convergencia comparando dos aproximaciones consecutivas.
    
    Args:
        aproximacion_actual: Aproximación en la iteración actual
        aproximacion_anterior: Aproximación en la iteración anterior
        tolerancia: Tolerancia para considerar convergencia
        
    Returns:
        True si se alcanzó la convergencia, False en caso contrario
    """
    if aproximacion_anterior == 0:
        return abs(aproximacion_actual) < tolerancia
    
    error_rel = abs(aproximacion_actual - aproximacion_anterior) / abs(aproximacion_anterior)
    return error_rel < tolerancia


def aceleracion_aitken(secuencia: list[float]) -> float:
    """
    Aplica la aceleración de Aitken a una secuencia convergente.
    
    La aceleración de Aitken se basa en la fórmula:
    x* ≈ x_n - (x_{n+1} - x_n)² / (x_{n+2} - 2*x_{n+1} + x_n)
    
    Args:
        secuencia: Lista con al menos 3 elementos de la secuencia
        
    Returns:
        Valor acelerado de la secuencia
        
    Raises:
        ValueError: Si la secuencia tiene menos de 3 elementos
    """
    if len(secuencia) < 3:
        raise ValueError("La secuencia debe tener al menos 3 elementos para aplicar Aitken")
    
    x_n = secuencia[-3]
    x_n1 = secuencia[-2] 
    x_n2 = secuencia[-1]
    
    numerador = (x_n1 - x_n) ** 2
    denominador = x_n2 - 2 * x_n1 + x_n
    
    if abs(denominador) < 1e-15:
        return x_n2  # Evitar división por cero
    
    return x_n2 - numerador / denominador


def aceleracion_steffensen(
    func: Callable[[float], float], 
    punto_inicial: float, 
    max_iteraciones: int = 100,
    tolerancia: float = 1e-6
) -> Tuple[float, int, bool]:
    """
    Implementa la aceleración de Steffensen para métodos de punto fijo.
    
    Args:
        func: Función de iteración g(x) donde x = g(x)
        punto_inicial: Punto inicial para comenzar las iteraciones
        max_iteraciones: Número máximo de iteraciones
        tolerancia: Tolerancia para la convergencia
        
    Returns:
        Tupla con (raiz_aproximada, iteraciones_usadas, convergencia_alcanzada)
    """
    x = punto_inicial
    
    for i in range(max_iteraciones):
        x_anterior = x
        
        # Steffensen: x_{n+1} = x_n - (g(x_n) - x_n)² / (g(g(x_n)) - 2*g(x_n) + x_n)
        gx = func(x)
        ggx = func(gx)
        
        numerador = (gx - x) ** 2
        denominador = ggx - 2 * gx + x
        
        if abs(denominador) < 1e-15:
            return x, i + 1, False  # División por cero
        
        x = x - numerador / denominador
        
        if verificar_convergencia(x, x_anterior, tolerancia):
            return x, i + 1, True
    
    return x, max_iteraciones, False


def calcular_velocidad_convergencia(errores: list[float]) -> Optional[float]:
    """
    Calcula la velocidad de convergencia aproximada basada en los errores.
    
    Args:
        errores: Lista de errores en cada iteración
        
    Returns:
        Velocidad de convergencia aproximada o None si no se puede calcular
    """
    if len(errores) < 3:
        return None
    
    # Usar los últimos 3 errores para calcular la velocidad
    e_n2 = errores[-3]
    e_n1 = errores[-2]
    e_n = errores[-1]
    
    if e_n2 == 0 or e_n1 == 0:
        return None
    
    # Calcular el cociente de errores
    cociente1 = e_n1 / e_n2
    cociente2 = e_n / e_n1
    
    if cociente1 <= 0 or cociente2 <= 0:
        return None
    
    # Velocidad aproximada
    velocidad = math.log(cociente2) / math.log(cociente1)
    
    return velocidad if velocidad > 0 else None
