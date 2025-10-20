from typing import Callable, Tuple, Optional, List
from utils.helpers import verificar_convergencia

def halley(
    f: Callable[[float], float],
    f1: Callable[[float], float],
    f2: Callable[[float], float],
    x0: float,
    tolerancia: float = 1e-6,
    max_iteraciones: int = 100,
    mostrar_iteraciones: bool = False
) -> Tuple[Optional[float], int, bool, List[dict]]:
    """
    Implementa el método de Halley para encontrar raíces de ecuaciones no lineales.
    
    El método de Halley utiliza la fórmula:
    x_{n+1} = x_n - (2 * f(x_n) * f'(x_n)) / (2 * (f'(x_n))^2 - f(x_n) * f''(x_n))
    
    Args:
        f: Función f(x) para la cual se busca la raíz.
        f1: Derivada primera de f(x).
        f2: Derivada segunda de f(x).
        x0: Punto inicial para comenzar las iteraciones.
        tolerancia: Tolerancia para la convergencia (por defecto 1e-6).
        max_iteraciones: Número máximo de iteraciones (por defecto 100).
        mostrar_iteraciones: Si mostrar detalles de cada iteración.
        
    Returns:
        Tupla con:
        - raiz: Aproximación de la raíz (None si no converge).
        - iteraciones: Número de iteraciones realizadas.
        - convergencia: True si convergió, False en caso contrario.
        - historial: Lista con detalles de cada iteración.
    """
    
    historial = []
    x = x0
    
    # Verificar si el punto inicial es ya una raíz
    fx0 = f(x0)
    if abs(fx0) < tolerancia:
        return x0, 0, True, [{'iteracion': 0, 'x_actual': x0, 'f(x)': fx0, 'convergencia': 'punto_inicial'}]
    
    for n in range(max_iteraciones):
        # Evaluar f(x), f'(x) y f''(x)
        f0 = f(x)
        f1_val = f1(x)
        f2_val = f2(x)
        
        # Calcular el denominador
        D = 2 * (f1_val ** 2) - f0 * f2_val
        
        # Verificar si el denominador es muy pequeño
        if abs(D) < 1e-15:
            if mostrar_iteraciones:
                print(f"Advertencia: Denominador muy pequeño en iteración {n+1}")
            break
        
        # Calcular el incremento
        delta_x = (2 * f0 * f1_val) / D
        
        # Actualizar x
        x_siguiente = x - delta_x
        
        # Calcular error relativo si es posible
        error_rel = None
        if x != 0:
            error_rel = abs(x_siguiente - x) / abs(x)
        
        # Guardar información de la iteración
        iteracion_info = {
            'iteracion': n + 1,
            'x_anterior': x,
            'x_actual': x_siguiente,
            'f(x)': f0,
            'f\'(x)': f1_val,
            'f\'\'(x)': f2_val,
            'denominador': D,
            'delta_x': delta_x,
            'error_relativo': error_rel,
            'diferencia': abs(x_siguiente - x)
        }
        historial.append(iteracion_info)
        
        if mostrar_iteraciones:
            print(f"Iteración {n+1}:")
            print(f"  x_{n} = {x:.8f}, f(x) = {f0:.8f}, f'(x) = {f1_val:.8f}, f''(x) = {f2_val:.8f}")
            print(f"  Denominador = {D:.8f}, Δx = {delta_x:.8f}")
            print(f"  x_{n+1} = {x_siguiente:.8f}")
            if error_rel is not None:
                print(f"  Error relativo = {error_rel:.8f}")
            print()
        
        # Verificar convergencia usando la función helper
        if verificar_convergencia(x_siguiente, x, tolerancia):
            if mostrar_iteraciones:
                print(f"Convergencia alcanzada en {n+1} iteraciones")
            return x_siguiente, n + 1, True, historial
        
        # Verificar si f(x) es suficientemente pequeño
        if abs(f0) < tolerancia:
            if mostrar_iteraciones:
                print(f"Raíz encontrada en {n+1} iteraciones (f(x) ≈ 0)")
            return x_siguiente, n + 1, True, historial
        
        # Actualizar x para la siguiente iteración
        x = x_siguiente
    
    # Si no converge en el número máximo de iteraciones
    if mostrar_iteraciones:
        print(f"No se alcanzó convergencia en {max_iteraciones} iteraciones")
    
    return None, max_iteraciones, False, historial