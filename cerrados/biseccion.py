"""
Método de Bisección para resolución de ecuaciones no lineales.

El método de bisección es un método cerrado que encuentra la raíz de una
ecuación f(x) = 0 en un intervalo [a,b] donde la función cambia de signo.
"""

from typing import Callable, Tuple, List, Optional
from utils.helpers import validar_intervalo, verificar_convergencia, error_absoluto


def biseccion(
    func: Callable[[float], float],
    a: float,
    b: float,
    tolerancia: float = 1e-6,
    max_iteraciones: int = 100,
    mostrar_iteraciones: bool = False
) -> Tuple[Optional[float], int, bool, List[dict]]:
    """
    Implementa el método de bisección para encontrar raíces de ecuaciones no lineales.
    
    El método de bisección divide repetidamente el intervalo [a,b] por la mitad
    y selecciona el subintervalo que contiene la raíz basándose en el cambio de signo.
    
    Args:
        func: Función f(x) para la cual se busca la raíz
        a: Extremo inferior del intervalo inicial
        b: Extremo superior del intervalo inicial
        tolerancia: Tolerancia para la convergencia (por defecto 1e-6)
        max_iteraciones: Número máximo de iteraciones (por defecto 100)
        mostrar_iteraciones: Si mostrar detalles de cada iteración
        
    Returns:
        Tupla con:
        - raiz: Aproximación de la raíz (None si no converge)
        - iteraciones: Número de iteraciones realizadas
        - convergencia: True si convergió, False en caso contrario
        - historial: Lista con detalles de cada iteración
        
    Raises:
        ValueError: Si el intervalo no es válido o no hay cambio de signo
    """
    
    # Validar el intervalo
    if a >= b:
        raise ValueError("El extremo inferior 'a' debe ser menor que el extremo superior 'b'")
    
    if not validar_intervalo(func, a, b):
        raise ValueError("No hay cambio de signo en el intervalo [a,b]. No se puede garantizar una raíz.")
    
    historial = []
    c_anterior = None
    
    for i in range(max_iteraciones):
        # Calcular punto medio
        c = (a + b) / 2
        fc = func(c)
        fa = func(a)
        fb = func(b)
        
        # Calcular error relativo si es posible
        error_rel = None
        if c_anterior is not None:
            if c_anterior != 0:
                error_rel = abs(c - c_anterior) / abs(c_anterior)
        
        # Guardar información de la iteración
        iteracion_info = {
            'iteracion': i + 1,
            'a': a,
            'b': b,
            'c': c,
            'f(a)': fa,
            'f(b)': fb,
            'f(c)': fc,
            'error_relativo': error_rel,
            'longitud_intervalo': b - a
        }
        historial.append(iteracion_info)
        
        if mostrar_iteraciones:
            print(f"Iteración {i+1}:")
            print(f"  a = {a:.8f}, b = {b:.8f}, c = {c:.8f}")
            print(f"  f(a) = {fa:.8f}, f(b) = {fb:.8f}, f(c) = {fc:.8f}")
            if error_rel is not None:
                print(f"  Error relativo = {error_rel:.8f}")
            print(f"  Longitud del intervalo = {b-a:.8f}")
            print()
        
        # Verificar convergencia
        if c_anterior is not None and verificar_convergencia(c, c_anterior, tolerancia):
            if mostrar_iteraciones:
                print(f"Convergencia alcanzada en {i+1} iteraciones")
            return c, i + 1, True, historial
        
        # Verificar si f(c) es suficientemente pequeño
        if abs(fc) < tolerancia:
            if mostrar_iteraciones:
                print(f"Raíz encontrada en {i+1} iteraciones (f(c) ≈ 0)")
            return c, i + 1, True, historial
        
        # Actualizar intervalo según el signo de f(c)
        if fa * fc < 0:
            b = c  # La raíz está en [a,c]
        else:
            a = c  # La raíz está en [c,b]
        
        c_anterior = c
    
    # Si llegamos aquí, no convergió en el número máximo de iteraciones
    if mostrar_iteraciones:
        print(f"No se alcanzó convergencia en {max_iteraciones} iteraciones")
    
    return None, max_iteraciones, False, historial


def biseccion_analisis(
    func: Callable[[float], float],
    a: float,
    b: float,
    tolerancia: float = 1e-6,
    max_iteraciones: int = 100
) -> dict:
    """
    Realiza un análisis completo del método de bisección.
    
    Args:
        func: Función f(x) para la cual se busca la raíz
        a: Extremo inferior del intervalo inicial
        b: Extremo superior del intervalo inicial
        tolerancia: Tolerancia para la convergencia
        max_iteraciones: Número máximo de iteraciones
        
    Returns:
        Diccionario con análisis detallado del método
    """
    
    raiz, iteraciones, convergencia, historial = biseccion(
        func, a, b, tolerancia, max_iteraciones, mostrar_iteraciones=False
    )
    
    # Análisis de convergencia
    analisis = {
        'raiz_encontrada': raiz,
        'iteraciones_usadas': iteraciones,
        'convergencia_alcanzada': convergencia,
        'tolerancia_utilizada': tolerancia,
        'longitud_intervalo_inicial': b - a,
        'historial_iteraciones': historial
    }
    
    if convergencia and historial:
        # Calcular la longitud final del intervalo
        ultima_iteracion = historial[-1]
        analisis['longitud_intervalo_final'] = ultima_iteracion['longitud_intervalo']
        
        # Calcular reducción del intervalo
        reduccion = (analisis['longitud_intervalo_inicial'] - 
                    analisis['longitud_intervalo_final']) / analisis['longitud_intervalo_inicial']
        analisis['reduccion_intervalo'] = reduccion
        
        # Estimación del error máximo
        analisis['error_maximo_estimado'] = analisis['longitud_intervalo_final'] / 2
        
        # Verificar si la función es cero en la raíz
        if raiz is not None:
            analisis['valor_funcion_raiz'] = func(raiz)
    
    return analisis


# Ejemplo de uso
if __name__ == "__main__":
    # Ejemplo: f(x) = x³ - x - 1
    def ejemplo_func(x):
        return x**3 - x - 1
    
    print("=== Método de Bisección ===")
    print("Función: f(x) = x³ - x - 1")
    print("Intervalo inicial: [1, 2]")
    print()
    
    # Ejecutar método
    raiz, iteraciones, convergencia, historial = biseccion(
        ejemplo_func, 1, 2, tolerancia=1e-6, mostrar_iteraciones=True
    )
    
    print(f"Resultado final:")
    print(f"  Raíz aproximada: {raiz}")
    print(f"  Iteraciones: {iteraciones}")
    print(f"  Convergencia: {convergencia}")
    
    if raiz:
        print(f"  f(raíz) = {ejemplo_func(raiz):.2e}")
