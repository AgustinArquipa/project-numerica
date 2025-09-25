"""
Método de Newton para resolución de ecuaciones no lineales.

El método de Newton utiliza la derivada de la función para encontrar
aproximaciones sucesivas de la raíz de f(x) = 0.
"""

from typing import Callable, Tuple, List, Optional
from utils.helpers import verificar_convergencia


def newton(
    f: Callable[[float], float],
    f_derivada: Callable[[float], float],
    x0: float,
    tolerancia: float = 1e-6,
    max_iteraciones: int = 100,
    mostrar_iteraciones: bool = False
) -> Tuple[Optional[float], int, bool, List[dict]]:
    """
    Implementa el método de Newton para encontrar raíces de ecuaciones no lineales.
    
    El método de Newton utiliza la fórmula:
    x_{n+1} = x_n - f(x_n) / f'(x_n)
    
    Args:
        f: Función f(x) para la cual se busca la raíz
        f_derivada: Derivada de f(x)
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
        
        # Evaluar función y su derivada
        fx = f(x)
        fpx = f_derivada(x)
        
        # Verificar si la derivada es cero (división por cero)
        if abs(fpx) < 1e-15:
            if mostrar_iteraciones:
                print(f"Advertencia: Derivada muy pequeña en iteración {i+1}")
            break
        
        # Aplicar fórmula de Newton
        x = x - fx / fpx
        
        # Calcular error relativo si es posible
        error_rel = None
        if x_anterior != 0:
            error_rel = abs(x - x_anterior) / abs(x_anterior)
        
        # Calcular error cuadrático (para análisis de convergencia)
        error_cuadratico = None
        if x_anterior is not None:
            error_cuadratico = abs(x - x_anterior) ** 2
        
        # Guardar información de la iteración
        iteracion_info = {
            'iteracion': i + 1,
            'x_anterior': x_anterior,
            'x_actual': x,
            'f(x_anterior)': fx,
            'f\'(x_anterior)': fpx,
            'error_relativo': error_rel,
            'error_cuadratico': error_cuadratico,
            'diferencia': abs(x - x_anterior)
        }
        historial.append(iteracion_info)
        
        if mostrar_iteraciones:
            print(f"Iteración {i+1}:")
            print(f"  x_{i} = {x_anterior:.8f}")
            print(f"  f(x_{i}) = {fx:.8f}")
            print(f"  f'(x_{i}) = {fpx:.8f}")
            print(f"  x_{i+1} = {x:.8f}")
            if error_rel is not None:
                print(f"  Error relativo = {error_rel:.8f}")
            if error_cuadratico is not None:
                print(f"  Error cuadrático = {error_cuadratico:.8f}")
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
        
        # Verificar si f(x) es suficientemente pequeño
        if abs(fx) < tolerancia:
            if mostrar_iteraciones:
                print(f"Raíz encontrada en {i+1} iteraciones (f(x) ≈ 0)")
            return x, i + 1, True, historial
    
    # Si llegamos aquí, no convergió en el número máximo de iteraciones
    if mostrar_iteraciones:
        print(f"No se alcanzó convergencia en {max_iteraciones} iteraciones")
    
    return None, max_iteraciones, False, historial


def newton_raphson(
    f: Callable[[float], float],
    f_derivada: Callable[[float], float],
    f_segunda_derivada: Callable[[float], float],
    x0: float,
    tolerancia: float = 1e-6,
    max_iteraciones: int = 100,
    mostrar_iteraciones: bool = False
) -> Tuple[Optional[float], int, bool, List[dict]]:
    """
    Implementa el método de Newton-Raphson con información de segunda derivada.
    
    Utiliza la fórmula mejorada que incluye información de la segunda derivada:
    x_{n+1} = x_n - f(x_n)/f'(x_n) - (1/2)(f''(x_n)/f'(x_n))(f(x_n)/f'(x_n))²
    
    Args:
        f: Función f(x) para la cual se busca la raíz
        f_derivada: Primera derivada de f(x)
        f_segunda_derivada: Segunda derivada de f(x)
        x0: Punto inicial para comenzar las iteraciones
        tolerancia: Tolerancia para la convergencia
        max_iteraciones: Número máximo de iteraciones
        mostrar_iteraciones: Si mostrar detalles de cada iteración
        
    Returns:
        Tupla con (raiz, iteraciones, convergencia, historial)
    """
    
    historial = []
    x = x0
    x_anterior = None
    
    for i in range(max_iteraciones):
        x_anterior = x
        
        # Evaluar función y sus derivadas
        fx = f(x)
        fpx = f_derivada(x)
        fppx = f_segunda_derivada(x)
        
        # Verificar si la derivada es cero
        if abs(fpx) < 1e-15:
            if mostrar_iteraciones:
                print(f"Advertencia: Derivada muy pequeña en iteración {i+1}")
            break
        
        # Término principal de Newton
        termino_newton = fx / fpx
        
        # Término de corrección con segunda derivada
        termino_correccion = 0.5 * (fppx / fpx) * (termino_newton ** 2)
        
        # Aplicar fórmula mejorada
        x = x - termino_newton - termino_correccion
        
        # Calcular error relativo si es posible
        error_rel = None
        if x_anterior != 0:
            error_rel = abs(x - x_anterior) / abs(x_anterior)
        
        # Guardar información de la iteración
        iteracion_info = {
            'iteracion': i + 1,
            'x_anterior': x_anterior,
            'x_actual': x,
            'f(x_anterior)': fx,
            'f\'(x_anterior)': fpx,
            'f\'\'(x_anterior)': fppx,
            'termino_newton': termino_newton,
            'termino_correccion': termino_correccion,
            'error_relativo': error_rel,
            'diferencia': abs(x - x_anterior)
        }
        historial.append(iteracion_info)
        
        if mostrar_iteraciones:
            print(f"Iteración {i+1}:")
            print(f"  x_{i} = {x_anterior:.8f}")
            print(f"  f(x_{i}) = {fx:.8f}")
            print(f"  f'(x_{i}) = {fpx:.8f}")
            print(f"  f''(x_{i}) = {fppx:.8f}")
            print(f"  Término Newton = {termino_newton:.8f}")
            print(f"  Término corrección = {termino_correccion:.8f}")
            print(f"  x_{i+1} = {x:.8f}")
            if error_rel is not None:
                print(f"  Error relativo = {error_rel:.8f}")
            print()
        
        # Verificar convergencia
        if verificar_convergencia(x, x_anterior, tolerancia):
            if mostrar_iteraciones:
                print(f"Convergencia alcanzada en {i+1} iteraciones")
            return x, i + 1, True, historial
        
        # Verificar si la diferencia es muy pequeña
        if abs(x - x_anterior) < tolerancia:
            if mostrar_iteraciones:
                print(f"Raíz encontrada en {i+1} iteraciones")
            return x, i + 1, True, historial
        
        # Verificar si f(x) es suficientemente pequeño
        if abs(fx) < tolerancia:
            if mostrar_iteraciones:
                print(f"Raíz encontrada en {i+1} iteraciones (f(x) ≈ 0)")
            return x, i + 1, True, historial
    
    # Si llegamos aquí, no convergió
    if mostrar_iteraciones:
        print(f"No se alcanzó convergencia en {max_iteraciones} iteraciones")
    
    return None, max_iteraciones, False, historial


def newton_analisis(
    f: Callable[[float], float],
    f_derivada: Callable[[float], float],
    x0: float,
    tolerancia: float = 1e-6,
    max_iteraciones: int = 100
) -> dict:
    """
    Realiza un análisis completo del método de Newton.
    
    Args:
        f: Función f(x)
        f_derivada: Derivada de f(x)
        x0: Punto inicial
        tolerancia: Tolerancia para la convergencia
        max_iteraciones: Número máximo de iteraciones
        
    Returns:
        Diccionario con análisis detallado del método
    """
    
    # Ejecutar método
    raiz, iteraciones, convergencia, historial = newton(
        f, f_derivada, x0, tolerancia, max_iteraciones, mostrar_iteraciones=False
    )
    
    # Análisis de convergencia
    analisis = {
        'raiz_encontrada': raiz,
        'iteraciones_usadas': iteraciones,
        'convergencia_alcanzada': convergencia,
        'tolerancia_utilizada': tolerancia,
        'punto_inicial': x0,
        'historial_iteraciones': historial
    }
    
    if convergencia and historial:
        # Verificar si la función es cero en la raíz
        if raiz is not None:
            analisis['valor_funcion_raiz'] = f(raiz)
        
        # Análisis de la velocidad de convergencia cuadrática
        errores_relativos = [iter['error_relativo'] for iter in historial if iter['error_relativo'] is not None]
        errores_cuadraticos = [iter['error_cuadratico'] for iter in historial if iter['error_cuadratico'] is not None]
        
        if len(errores_relativos) > 2:
            # Verificar convergencia cuadrática
            cocientes = []
            for i in range(1, len(errores_relativos)):
                if errores_relativos[i-1] != 0:
                    cocientes.append(errores_relativos[i] / (errores_relativos[i-1] ** 2))
            
            if cocientes:
                analisis['velocidad_convergencia_cuadratica'] = sum(cocientes) / len(cocientes)
        
        # Análisis de estabilidad
        derivadas = [abs(iter['f\'(x_anterior)']) for iter in historial]
        analisis['min_derivada'] = min(derivadas)
        analisis['max_derivada'] = max(derivadas)
        analisis['derivada_promedio'] = sum(derivadas) / len(derivadas)
        
        # Verificar si hay problemas de estabilidad
        if analisis['min_derivada'] < 1e-10:
            analisis['advertencia_derivada_pequena'] = True
    
    return analisis


def comparar_newton_variantes(
    f: Callable[[float], float],
    f_derivada: Callable[[float], float],
    f_segunda_derivada: Callable[[float], float],
    x0: float,
    tolerancia: float = 1e-6,
    max_iteraciones: int = 100
) -> dict:
    """
    Compara el método de Newton tradicional con Newton-Raphson.
    
    Args:
        f: Función f(x)
        f_derivada: Primera derivada de f(x)
        f_segunda_derivada: Segunda derivada de f(x)
        x0: Punto inicial
        tolerancia: Tolerancia para la convergencia
        max_iteraciones: Número máximo de iteraciones
        
    Returns:
        Diccionario con comparación de ambos métodos
    """
    
    # Ejecutar ambos métodos
    raiz_n, iter_n, conv_n, hist_n = newton(f, f_derivada, x0, tolerancia, max_iteraciones)
    raiz_nr, iter_nr, conv_nr, hist_nr = newton_raphson(f, f_derivada, f_segunda_derivada, x0, tolerancia, max_iteraciones)
    
    comparacion = {
        'newton': {
            'raiz': raiz_n,
            'iteraciones': iter_n,
            'convergencia': conv_n,
            'historial': hist_n
        },
        'newton_raphson': {
            'raiz': raiz_nr,
            'iteraciones': iter_nr,
            'convergencia': conv_nr,
            'historial': hist_nr
        }
    }
    
    # Análisis comparativo
    if conv_n and conv_nr:
        comparacion['analisis'] = {
            'diferencia_iteraciones': abs(iter_n - iter_nr),
            'metodo_mas_rapido': 'newton' if iter_n < iter_nr else 'newton_raphson',
            'diferencia_raices': abs(raiz_n - raiz_nr) if raiz_n and raiz_nr else None
        }
    
    return comparacion


# Ejemplo de uso
if __name__ == "__main__":
    # Ejemplo: f(x) = x³ - x - 1
    def f(x):
        return x**3 - x - 1
    
    def f_derivada(x):
        return 3 * x**2 - 1
    
    def f_segunda_derivada(x):
        return 6 * x
    
    print("=== Método de Newton ===")
    print("Función: f(x) = x³ - x - 1")
    print("Derivada: f'(x) = 3x² - 1")
    print("Punto inicial: x₀ = 1.5")
    print()
    
    # Ejecutar método tradicional
    raiz, iteraciones, convergencia, historial = newton(
        f, f_derivada, 1.5, tolerancia=1e-6, mostrar_iteraciones=True
    )
    
    print(f"Resultado final:")
    print(f"  Raíz aproximada: {raiz}")
    print(f"  Iteraciones: {iteraciones}")
    print(f"  Convergencia: {convergencia}")
    
    if raiz:
        print(f"  f(raíz) = {f(raiz):.2e}")
    
    print("\n=== Comparación con Newton-Raphson ===")
    comparacion = comparar_newton_variantes(f, f_derivada, f_segunda_derivada, 1.5)
    print(f"Newton: {comparacion['newton']['iteraciones']} iteraciones")
    print(f"Newton-Raphson: {comparacion['newton_raphson']['iteraciones']} iteraciones")
