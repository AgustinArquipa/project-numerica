"""
Método de Iteración de Punto Fijo para resolución de ecuaciones no lineales.

El método de punto fijo transforma la ecuación f(x) = 0 en la forma x = g(x)
y utiliza iteraciones para encontrar el punto fijo de g(x).
"""

from typing import Callable, Tuple, List, Optional
from utils.helpers import verificar_convergencia, aceleracion_aitken, aceleracion_steffensen


def punto_fijo(
    g: Callable[[float], float],
    x0: float,
    tolerancia: float = 1e-6,
    max_iteraciones: int = 100,
    mostrar_iteraciones: bool = False
) -> Tuple[Optional[float], int, bool, List[dict]]:
    """
    Implementa el método de iteración de punto fijo para encontrar raíces de ecuaciones no lineales.
    
    El método de punto fijo transforma f(x) = 0 en x = g(x) y luego itera:
    x_{n+1} = g(x_n)
    
    Args:
        g: Función de iteración g(x) donde x = g(x)
        x0: Punto inicial para comenzar las iteraciones
        tolerancia: Tolerancia para la convergencia (por defecto 1e-6)
        max_iteraciones: Número máximo de iteraciones (por defecto 100)
        mostrar_iteraciones: Si mostrar detalles de cada iteración
        
    Returns:
        Tupla con:
        - raiz: Aproximación de la raíz (None si no converge)
        - iteraciones: Número de iteraciones realizadas
        - convergencia: True si convergió, False en caso contrario
        - historial: Lista con detalles de cada iteración
    """
    
    historial = []
    x = x0
    x_anterior = None
    
    for i in range(max_iteraciones):
        x_anterior = x
        
        # Aplicar la función de iteración
        x = g(x)
        
        # Calcular error relativo si es posible
        error_rel = None
        if x_anterior != 0:
            error_rel = abs(x - x_anterior) / abs(x_anterior)
        
        # Guardar información de la iteración
        iteracion_info = {
            'iteracion': i + 1,
            'x_anterior': x_anterior,
            'x_actual': x,
            'g(x_anterior)': x,
            'error_relativo': error_rel,
            'diferencia': abs(x - x_anterior)
        }
        historial.append(iteracion_info)
        
        if mostrar_iteraciones:
            print(f"Iteración {i+1}:")
            print(f"  x_{i} = {x_anterior:.8f}")
            print(f"  x_{i+1} = g(x_{i}) = {x:.8f}")
            if error_rel is not None:
                print(f"  Error relativo = {error_rel:.8f}")
            print(f"  |x_{i+1} - x_{i}| = {abs(x - x_anterior):.8f}")
            print()
        
        # Verificar convergencia
        if verificar_convergencia(x, x_anterior, tolerancia):
            if mostrar_iteraciones:
                print(f"Convergencia alcanzada en {i+1} iteraciones")
            return x, i + 1, True, historial
        
        # Verificar si la diferencia es muy pequeña
        if abs(x - x_anterior) < tolerancia:
            if mostrar_iteraciones:
                print(f"Raíz encontrada en {i+1} iteraciones (diferencia < tolerancia)")
            return x, i + 1, True, historial
    
    # Si llegamos aquí, no convergió en el número máximo de iteraciones
    if mostrar_iteraciones:
        print(f"No se alcanzó convergencia en {max_iteraciones} iteraciones")
    
    return None, max_iteraciones, False, historial


def verificar_condicion_fourier(
    g: Callable[[float], float],
    g_derivada: Callable[[float], float],
    x0: float,
    radio: float = 1.0
) -> Tuple[bool, float]:
    """
    Verifica la condición de Fourier para la convergencia del método de punto fijo.
    
    La condición de Fourier establece que |g'(x)| < 1 en una vecindad del punto fijo
    para garantizar convergencia.
    
    Args:
        g: Función de iteración g(x)
        g_derivada: Derivada de g(x)
        x0: Punto donde verificar la condición
        radio: Radio de la vecindad alrededor de x0
        
    Returns:
        Tupla con:
        - cumple_condicion: True si cumple la condición de Fourier
        - max_derivada: Máximo valor absoluto de la derivada en la vecindad
    """
    
    # Evaluar en varios puntos alrededor de x0
    puntos = [x0 - radio, x0 - radio/2, x0, x0 + radio/2, x0 + radio]
    
    derivadas = []
    for punto in puntos:
        try:
            derivada = abs(g_derivada(punto))
            derivadas.append(derivada)
        except (ValueError, ZeroDivisionError):
            continue
    
    if not derivadas:
        return False, float('inf')
    
    max_derivada = max(derivadas)
    cumple_condicion = max_derivada < 1
    
    return cumple_condicion, max_derivada


def punto_fijo_con_aceleracion(
    g: Callable[[float], float],
    x0: float,
    tolerancia: float = 1e-6,
    max_iteraciones: int = 100,
    usar_aitken: bool = True,
    usar_steffensen: bool = False,
    mostrar_iteraciones: bool = False
) -> Tuple[Optional[float], int, bool, List[dict], Optional[float]]:
    """
    Implementa el método de punto fijo con técnicas de aceleración de convergencia.
    
    Args:
        g: Función de iteración g(x) donde x = g(x)
        x0: Punto inicial para comenzar las iteraciones
        tolerancia: Tolerancia para la convergencia
        max_iteraciones: Número máximo de iteraciones
        usar_aitken: Si usar aceleración de Aitken
        usar_steffensen: Si usar aceleración de Steffensen
        mostrar_iteraciones: Si mostrar detalles de cada iteración
        
    Returns:
        Tupla con:
        - raiz: Aproximación de la raíz
        - iteraciones: Número de iteraciones realizadas
        - convergencia: True si convergió
        - historial: Lista con detalles de cada iteración
        - raiz_acelerada: Raíz obtenida con aceleración (si aplicable)
    """
    
    if usar_steffensen:
        # Usar aceleración de Steffensen
        raiz_acelerada, iter_steff, conv_steff = aceleracion_steffensen(
            g, x0, max_iteraciones, tolerancia
        )
        
        if conv_steff:
            return raiz_acelerada, iter_steff, True, [], raiz_acelerada
        else:
            # Si Steffensen falla, usar método tradicional
            raiz, iteraciones, convergencia, historial = punto_fijo(
                g, x0, tolerancia, max_iteraciones, mostrar_iteraciones
            )
            return raiz, iteraciones, convergencia, historial, raiz_acelerada
    
    # Método tradicional con posible aceleración de Aitken
    raiz, iteraciones, convergencia, historial = punto_fijo(
        g, x0, tolerancia, max_iteraciones, mostrar_iteraciones
    )
    
    raiz_acelerada = None
    if usar_aitken and len(historial) >= 3:
        # Aplicar aceleración de Aitken
        secuencia = [h['x_actual'] for h in historial[-3:]]
        raiz_acelerada = aceleracion_aitken(secuencia)
    
    return raiz, iteraciones, convergencia, historial, raiz_acelerada


def punto_fijo_analisis(
    g: Callable[[float], float],
    g_derivada: Callable[[float], float],
    x0: float,
    tolerancia: float = 1e-6,
    max_iteraciones: int = 100
) -> dict:
    """
    Realiza un análisis completo del método de punto fijo.
    
    Args:
        g: Función de iteración g(x)
        g_derivada: Derivada de g(x)
        x0: Punto inicial
        tolerancia: Tolerancia para la convergencia
        max_iteraciones: Número máximo de iteraciones
        
    Returns:
        Diccionario con análisis detallado del método
    """
    
    # Verificar condición de Fourier
    cumple_fourier, max_derivada = verificar_condicion_fourier(g, g_derivada, x0)
    
    # Ejecutar método
    raiz, iteraciones, convergencia, historial = punto_fijo(
        g, x0, tolerancia, max_iteraciones, mostrar_iteraciones=False
    )
    
    # Análisis de convergencia
    analisis = {
        'raiz_encontrada': raiz,
        'iteraciones_usadas': iteraciones,
        'convergencia_alcanzada': convergencia,
        'tolerancia_utilizada': tolerancia,
        'punto_inicial': x0,
        'cumple_condicion_fourier': cumple_fourier,
        'max_derivada': max_derivada,
        'historial_iteraciones': historial
    }
    
    if convergencia and historial:
        # Verificar si la función es cero en la raíz
        if raiz is not None:
            analisis['valor_funcion_raiz'] = g(raiz) - raiz  # f(raíz) = g(raíz) - raíz
        
        # Análisis de la velocidad de convergencia
        errores_relativos = [iter['error_relativo'] for iter in historial if iter['error_relativo'] is not None]
        if len(errores_relativos) > 2:
            velocidades = []
            for i in range(1, len(errores_relativos)):
                if errores_relativos[i-1] != 0:
                    velocidades.append(errores_relativos[i] / errores_relativos[i-1])
            
            if velocidades:
                analisis['velocidad_convergencia_promedio'] = sum(velocidades) / len(velocidades)
        
        # Aplicar aceleración de Aitken si es posible
        if len(historial) >= 3:
            secuencia = [h['x_actual'] for h in historial[-3:]]
            analisis['raiz_aitken'] = aceleracion_aitken(secuencia)
    
    return analisis


def transformar_ecuacion_a_punto_fijo(
    f: Callable[[float], float],
    metodo: str = "suma"
) -> Callable[[float], float]:
    """
    Transforma una ecuación f(x) = 0 en la forma x = g(x) para el método de punto fijo.
    
    Args:
        f: Función f(x) = 0
        metodo: Método de transformación ("suma", "producto", "division")
        
    Returns:
        Función g(x) tal que x = g(x) es equivalente a f(x) = 0
    """
    
    if metodo == "suma":
        # x = x + f(x)
        return lambda x: x + f(x)
    elif metodo == "producto":
        # x = x * (1 + f(x)) (cuidado con f(x) = -1)
        return lambda x: x * (1 + f(x))
    elif metodo == "division":
        # x = x / (1 - f(x)) (cuidado con f(x) = 1)
        return lambda x: x / (1 - f(x)) if abs(1 - f(x)) > 1e-10 else x
    else:
        raise ValueError("Método debe ser 'suma', 'producto' o 'division'")


# Ejemplo de uso
if __name__ == "__main__":
    # Ejemplo: f(x) = x³ - x - 1 = 0
    # Transformamos a x = g(x) donde g(x) = x³ - 1
    def g(x):
        return x**3 - 1
    
    def g_derivada(x):
        return 3 * x**2
    
    print("=== Método de Punto Fijo ===")
    print("Ecuación: f(x) = x³ - x - 1 = 0")
    print("Transformación: x = g(x) donde g(x) = x³ - 1")
    print("Punto inicial: x₀ = 1.5")
    print()
    
    # Verificar condición de Fourier
    cumple_fourier, max_derivada = verificar_condicion_fourier(g, g_derivada, 1.5)
    print(f"Condición de Fourier: {'✓' if cumple_fourier else '✗'}")
    print(f"Máxima derivada en vecindad: {max_derivada:.4f}")
    print()
    
    # Ejecutar método
    raiz, iteraciones, convergencia, historial = punto_fijo(
        g, 1.5, tolerancia=1e-6, mostrar_iteraciones=True
    )
    
    print(f"Resultado final:")
    print(f"  Raíz aproximada: {raiz}")
    print(f"  Iteraciones: {iteraciones}")
    print(f"  Convergencia: {convergencia}")
    
    if raiz:
        print(f"  g(raíz) - raíz = {g(raiz) - raiz:.2e}")
        
        # Aplicar aceleración de Aitken
        if len(historial) >= 3:
            secuencia = [h['x_actual'] for h in historial[-3:]]
            raiz_aitken = aceleracion_aitken(secuencia)
            print(f"  Raíz con Aitken: {raiz_aitken}")
            print(f"  Mejora: {abs(raiz - raiz_aitken):.2e}")
