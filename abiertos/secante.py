"""
Método de la Secante para resolución de ecuaciones no lineales.

El método de la Secante es una variación del método de Newton que no requiere
el cálculo de la derivada, utilizando en su lugar diferencias finitas.
"""

from typing import Callable, Tuple, List, Optional
from utils.helpers import verificar_convergencia


def secante(
    f: Callable[[float], float],
    x0: float,
    x1: float,
    tolerancia: float = 1e-6,
    max_iteraciones: int = 100,
    mostrar_iteraciones: bool = False
) -> Tuple[Optional[float], int, bool, List[dict]]:
    """
    Implementa el método de la Secante para encontrar raíces de ecuaciones no lineales.
    
    El método de la Secante utiliza la fórmula:
    x_{n+1} = x_n - f(x_n) * (x_n - x_{n-1}) / (f(x_n) - f(x_{n-1}))
    
    Args:
        f: Función f(x) para la cual se busca la raíz
        x0: Primer punto inicial
        x1: Segundo punto inicial
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
    
    # Evaluar función en los puntos iniciales
    fx0 = f(x0)
    fx1 = f(x1)
    
    # Verificar si alguno de los puntos iniciales es raíz
    if abs(fx0) < tolerancia:
        return x0, 0, True, [{'iteracion': 0, 'x': x0, 'f(x)': fx0, 'convergencia': 'punto_inicial'}]
    
    if abs(fx1) < tolerancia:
        return x1, 0, True, [{'iteracion': 0, 'x': x1, 'f(x)': fx1, 'convergencia': 'punto_inicial'}]
    
    x_anterior = x0
    x_actual = x1
    fx_anterior = fx0
    fx_actual = fx1
    
    for i in range(max_iteraciones):
        # Verificar si f(x_n) - f(x_{n-1}) es muy pequeño (división por cero)
        denominador = fx_actual - fx_anterior
        if abs(denominador) < 1e-15:
            if mostrar_iteraciones:
                print(f"Advertencia: Denominador muy pequeño en iteración {i+1}")
            break
        
        # Aplicar fórmula de la secante (según pseudocódigo)
        # x_n+1 = (x_n-1 * f(x_n) - x_n * f(x_n-1)) / (f(x_n) - f(x_n-1))
        x_siguiente = (x_anterior * fx_actual - x_actual * fx_anterior) / denominador
        fx_siguiente = f(x_siguiente)
        
        # Calcular error relativo si es posible
        error_rel = None
        if x_actual != 0:
            error_rel = abs(x_siguiente - x_actual) / abs(x_actual)
        
        # Guardar información de la iteración
        iteracion_info = {
            'iteracion': i + 1,
            'x_anterior': x_anterior,
            'x_actual': x_actual,
            'x_siguiente': x_siguiente,
            'f(x_anterior)': fx_anterior,
            'f(x_actual)': fx_actual,
            'f(x_siguiente)': fx_siguiente,
            'error_relativo': error_rel,
            'diferencia': abs(x_siguiente - x_actual),
            'denominador': denominador
        }
        historial.append(iteracion_info)
        
        if mostrar_iteraciones:
            print(f"Iteración {i+1}:")
            print(f"  x_{i-1} = {x_anterior:.8f}, f(x_{i-1}) = {fx_anterior:.8f}")
            print(f"  x_{i} = {x_actual:.8f}, f(x_{i}) = {fx_actual:.8f}")
            print(f"  x_{i+1} = {x_siguiente:.8f}, f(x_{i+1}) = {fx_siguiente:.8f}")
            if error_rel is not None:
                print(f"  Error relativo = {error_rel:.8f}")
            print(f"  |x_{i+1} - x_{i}| = {abs(x_siguiente - x_actual):.8f}")
            print()
        
        # Verificar convergencia
        if verificar_convergencia(x_siguiente, x_actual, tolerancia):
            if mostrar_iteraciones:
                print(f"Convergencia alcanzada en {i+1} iteraciones")
            return x_siguiente, i + 1, True, historial
        
        # Verificar si la diferencia es muy pequeña
        if abs(x_siguiente - x_actual) < tolerancia:
            if mostrar_iteraciones:
                print(f"Raíz encontrada en {i+1} iteraciones (diferencia < tolerancia)")
            return x_siguiente, i + 1, True, historial
        
        # Verificar si f(x) es suficientemente pequeño
        if abs(fx_siguiente) < tolerancia:
            if mostrar_iteraciones:
                print(f"Raíz encontrada en {i+1} iteraciones (f(x) ≈ 0)")
            return x_siguiente, i + 1, True, historial
        
        # Actualizar para la siguiente iteración
        x_anterior = x_actual
        x_actual = x_siguiente
        fx_anterior = fx_actual
        fx_actual = fx_siguiente
    
    # Si llegamos aquí, no convergió en el número máximo de iteraciones
    if mostrar_iteraciones:
        print(f"No se alcanzó convergencia en {max_iteraciones} iteraciones")
    
    return None, max_iteraciones, False, historial


def secante_modificada(
    f: Callable[[float], float],
    x0: float,
    h: float = 0.01,
    tolerancia: float = 1e-6,
    max_iteraciones: int = 100,
    mostrar_iteraciones: bool = False
) -> Tuple[Optional[float], int, bool, List[dict]]:
    """
    Implementa el método de la Secante Modificada.
    
    En lugar de usar dos puntos anteriores, usa x y x+h para aproximar la derivada:
    x_{n+1} = x_n - f(x_n) * h / (f(x_n + h) - f(x_n))
    
    Args:
        f: Función f(x) para la cual se busca la raíz
        x0: Punto inicial
        h: Paso para la diferencia finita
        tolerancia: Tolerancia para la convergencia
        max_iteraciones: Número máximo de iteraciones
        mostrar_iteraciones: Si mostrar detalles de cada iteración
        
    Returns:
        Tupla con (raiz, iteraciones, convergencia, historial)
    """
    
    historial = []
    x = x0
    
    for i in range(max_iteraciones):
        # Evaluar función en x y x+h
        fx = f(x)
        fxh = f(x + h)
        
        # Verificar si f(x+h) - f(x) es muy pequeño
        denominador = fxh - fx
        if abs(denominador) < 1e-15:
            if mostrar_iteraciones:
                print(f"Advertencia: Denominador muy pequeño en iteración {i+1}")
            break
        
        # Aplicar fórmula de la secante modificada
        x_siguiente = x - fx * h / denominador
        fx_siguiente = f(x_siguiente)
        
        # Calcular error relativo si es posible
        error_rel = None
        if x != 0:
            error_rel = abs(x_siguiente - x) / abs(x)
        
        # Guardar información de la iteración
        iteracion_info = {
            'iteracion': i + 1,
            'x_actual': x,
            'x_siguiente': x_siguiente,
            'f(x)': fx,
            'f(x+h)': fxh,
            'f(x_siguiente)': fx_siguiente,
            'h': h,
            'error_relativo': error_rel,
            'diferencia': abs(x_siguiente - x)
        }
        historial.append(iteracion_info)
        
        if mostrar_iteraciones:
            print(f"Iteración {i+1}:")
            print(f"  x_{i} = {x:.8f}, f(x_{i}) = {fx:.8f}")
            print(f"  x_{i} + h = {x+h:.8f}, f(x_{i} + h) = {fxh:.8f}")
            print(f"  x_{i+1} = {x_siguiente:.8f}, f(x_{i+1}) = {fx_siguiente:.8f}")
            if error_rel is not None:
                print(f"  Error relativo = {error_rel:.8f}")
            print(f"  |x_{i+1} - x_{i}| = {abs(x_siguiente - x):.8f}")
            print()
        
        # Verificar convergencia
        if verificar_convergencia(x_siguiente, x, tolerancia):
            if mostrar_iteraciones:
                print(f"Convergencia alcanzada en {i+1} iteraciones")
            return x_siguiente, i + 1, True, historial
        
        # Verificar si la diferencia es muy pequeña
        if abs(x_siguiente - x) < tolerancia:
            if mostrar_iteraciones:
                print(f"Raíz encontrada en {i+1} iteraciones")
            return x_siguiente, i + 1, True, historial
        
        # Verificar si f(x) es suficientemente pequeño
        if abs(fx_siguiente) < tolerancia:
            if mostrar_iteraciones:
                print(f"Raíz encontrada en {i+1} iteraciones (f(x) ≈ 0)")
            return x_siguiente, i + 1, True, historial
        
        # Actualizar para la siguiente iteración
        x = x_siguiente
    
    # Si llegamos aquí, no convergió
    if mostrar_iteraciones:
        print(f"No se alcanzó convergencia en {max_iteraciones} iteraciones")
    
    return None, max_iteraciones, False, historial


def secante_analisis(
    f: Callable[[float], float],
    x0: float,
    x1: float,
    tolerancia: float = 1e-6,
    max_iteraciones: int = 100
) -> dict:
    """
    Realiza un análisis completo del método de la Secante.
    
    Args:
        f: Función f(x)
        x0: Primer punto inicial
        x1: Segundo punto inicial
        tolerancia: Tolerancia para la convergencia
        max_iteraciones: Número máximo de iteraciones
        
    Returns:
        Diccionario con análisis detallado del método
    """
    
    # Ejecutar método
    raiz, iteraciones, convergencia, historial = secante(
        f, x0, x1, tolerancia, max_iteraciones, mostrar_iteraciones=False
    )
    
    # Análisis de convergencia
    analisis = {
        'raiz_encontrada': raiz,
        'iteraciones_usadas': iteraciones,
        'convergencia_alcanzada': convergencia,
        'tolerancia_utilizada': tolerancia,
        'puntos_iniciales': (x0, x1),
        'historial_iteraciones': historial
    }
    
    if convergencia and historial:
        # Verificar si la función es cero en la raíz
        if raiz is not None:
            analisis['valor_funcion_raiz'] = f(raiz)
        
        # Análisis de la velocidad de convergencia
        errores_relativos = [iter['error_relativo'] for iter in historial if iter['error_relativo'] is not None]
        if len(errores_relativos) > 2:
            # Verificar convergencia superlineal (aproximadamente 1.618 - número áureo)
            cocientes = []
            for i in range(1, len(errores_relativos)):
                if errores_relativos[i-1] != 0:
                    cocientes.append(errores_relativos[i] / errores_relativos[i-1])
            
            if cocientes:
                analisis['velocidad_convergencia_promedio'] = sum(cocientes) / len(cocientes)
                analisis['velocidad_esperada_secante'] = 1.618  # Número áureo
        
        # Análisis de estabilidad
        denominadores = [abs(iter['denominador']) for iter in historial]
        analisis['min_denominador'] = min(denominadores)
        analisis['max_denominador'] = max(denominadores)
        analisis['denominador_promedio'] = sum(denominadores) / len(denominadores)
        
        # Verificar si hay problemas de estabilidad
        if analisis['min_denominador'] < 1e-10:
            analisis['advertencia_denominador_pequeno'] = True
    
    return analisis


def comparar_secante_variantes(
    f: Callable[[float], float],
    x0: float,
    x1: float,
    h: float = 0.01,
    tolerancia: float = 1e-6,
    max_iteraciones: int = 100
) -> dict:
    """
    Compara las variantes del método de la Secante.
    
    Args:
        f: Función f(x)
        x0: Primer punto inicial
        x1: Segundo punto inicial (para secante tradicional)
        h: Paso para secante modificada
        tolerancia: Tolerancia para la convergencia
        max_iteraciones: Número máximo de iteraciones
        
    Returns:
        Diccionario con comparación de los métodos
    """
    
    # Ejecutar ambos métodos
    raiz_s, iter_s, conv_s, hist_s = secante(f, x0, x1, tolerancia, max_iteraciones)
    raiz_sm, iter_sm, conv_sm, hist_sm = secante_modificada(f, x0, h, tolerancia, max_iteraciones)
    
    comparacion = {
        'secante': {
            'raiz': raiz_s,
            'iteraciones': iter_s,
            'convergencia': conv_s,
            'historial': hist_s
        },
        'secante_modificada': {
            'raiz': raiz_sm,
            'iteraciones': iter_sm,
            'convergencia': conv_sm,
            'historial': hist_sm
        }
    }
    
    # Análisis comparativo
    if conv_s and conv_sm:
        comparacion['analisis'] = {
            'diferencia_iteraciones': abs(iter_s - iter_sm),
            'metodo_mas_rapido': 'secante' if iter_s < iter_sm else 'secante_modificada',
            'diferencia_raices': abs(raiz_s - raiz_sm) if raiz_s and raiz_sm else None
        }
    
    return comparacion


# Ejemplo de uso
if __name__ == "__main__":
    # Ejemplo: f(x) = x³ - x - 1
    def f(x):
        return x**3 - x - 1
    
    print("=== Método de la Secante ===")
    print("Función: f(x) = x³ - x - 1")
    print("Puntos iniciales: x₀ = 1, x₁ = 2")
    print()
    
    # Ejecutar método tradicional
    raiz, iteraciones, convergencia, historial = secante(
        f, 1, 2, tolerancia=1e-6, mostrar_iteraciones=True
    )
    
    print(f"Resultado final:")
    print(f"  Raíz aproximada: {raiz}")
    print(f"  Iteraciones: {iteraciones}")
    print(f"  Convergencia: {convergencia}")
    
    if raiz:
        print(f"  f(raíz) = {f(raiz):.2e}")
    
    print("\n=== Comparación con Secante Modificada ===")
    comparacion = comparar_secante_variantes(f, 1, 2)
    print(f"Secante: {comparacion['secante']['iteraciones']} iteraciones")
    print(f"Secante Modificada: {comparacion['secante_modificada']['iteraciones']} iteraciones")
