"""
Método de Regula Falsi Modificada para resolución de ecuaciones no lineales.

El método de Regula Falsi Modificada es una mejora del método de Regula Falsi
que intenta superar el problema de la convergencia lenta cuando uno de los
extremos del intervalo se mantiene fijo.
"""

from typing import Callable, Tuple, List, Optional
from utils.helpers import validar_intervalo, verificar_convergencia


def regula_falsi_modificada(
    func: Callable[[float], float],
    a: float,
    b: float,
    tolerancia: float = 1e-6,
    max_iteraciones: int = 100,
    factor_reduccion: float = 0.5,
    mostrar_iteraciones: bool = False
) -> Tuple[Optional[float], int, bool, List[dict]]:
    """
    Implementa el método de Regula Falsi Modificada para encontrar raíces de ecuaciones no lineales.
    
    Este método mejora la convergencia del Regula Falsi tradicional aplicando una reducción
    artificial del valor de la función en el extremo que no cambia, evitando así que uno
    de los extremos se mantenga fijo durante muchas iteraciones.
    
    Args:
        func: Función f(x) para la cual se busca la raíz
        a: Extremo inferior del intervalo inicial
        b: Extremo superior del intervalo inicial
        tolerancia: Tolerancia para la convergencia (por defecto 1e-6)
        max_iteraciones: Número máximo de iteraciones (por defecto 100)
        factor_reduccion: Factor para reducir f(x) cuando un extremo no cambia (por defecto 0.5)
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
    contador_a = 0  # Contador para extremo a
    contador_b = 0  # Contador para extremo b
    
    for i in range(max_iteraciones):
        fa = func(a)
        fb = func(b)
        
        # Aplicar reducción si un extremo no ha cambiado
        if contador_a > 1:
            fa = fa * factor_reduccion
        if contador_b > 1:
            fb = fb * factor_reduccion
        
        # Verificar si f(b) - f(a) es muy pequeño (división por cero)
        if abs(fb - fa) < 1e-15:
            if mostrar_iteraciones:
                print(f"Advertencia: f(b) - f(a) es muy pequeño en iteración {i+1}")
            break
        
        # Calcular nueva aproximación usando interpolación lineal
        c = (a * fb - b * fa) / (fb - fa)
        fc = func(c)
        
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
            'longitud_intervalo': b - a,
            'contador_a': contador_a,
            'contador_b': contador_b,
            'reduccion_aplicada': contador_a > 1 or contador_b > 1
        }
        historial.append(iteracion_info)
        
        if mostrar_iteraciones:
            print(f"Iteración {i+1}:")
            print(f"  a = {a:.8f}, b = {b:.8f}, c = {c:.8f}")
            print(f"  f(a) = {fa:.8f}, f(b) = {fb:.8f}, f(c) = {fc:.8f}")
            if error_rel is not None:
                print(f"  Error relativo = {error_rel:.8f}")
            print(f"  Longitud del intervalo = {b-a:.8f}")
            print(f"  Contador a = {contador_a}, Contador b = {contador_b}")
            if iteracion_info['reduccion_aplicada']:
                print(f"  ✓ Reducción aplicada")
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
        a_anterior = a
        b_anterior = b
        
        if func(a) * fc < 0:
            b = c  # La raíz está en [a,c]
        else:
            a = c  # La raíz está en [c,b]
        
        # Actualizar contadores
        if a == a_anterior:
            contador_a += 1
        else:
            contador_a = 0
            
        if b == b_anterior:
            contador_b += 1
        else:
            contador_b = 0
        
        c_anterior = c
    
    # Si llegamos aquí, no convergió en el número máximo de iteraciones
    if mostrar_iteraciones:
        print(f"No se alcanzó convergencia en {max_iteraciones} iteraciones")
    
    return None, max_iteraciones, False, historial


def regula_falsi_modificada_analisis(
    func: Callable[[float], float],
    a: float,
    b: float,
    tolerancia: float = 1e-6,
    max_iteraciones: int = 100,
    factor_reduccion: float = 0.5
) -> dict:
    """
    Realiza un análisis completo del método de Regula Falsi Modificada.
    
    Args:
        func: Función f(x) para la cual se busca la raíz
        a: Extremo inferior del intervalo inicial
        b: Extremo superior del intervalo inicial
        tolerancia: Tolerancia para la convergencia
        max_iteraciones: Número máximo de iteraciones
        factor_reduccion: Factor de reducción utilizado
        
    Returns:
        Diccionario con análisis detallado del método
    """
    
    raiz, iteraciones, convergencia, historial = regula_falsi_modificada(
        func, a, b, tolerancia, max_iteraciones, factor_reduccion, mostrar_iteraciones=False
    )
    
    # Análisis de convergencia
    analisis = {
        'raiz_encontrada': raiz,
        'iteraciones_usadas': iteraciones,
        'convergencia_alcanzada': convergencia,
        'tolerancia_utilizada': tolerancia,
        'factor_reduccion': factor_reduccion,
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
        
        # Verificar si la función es cero en la raíz
        if raiz is not None:
            analisis['valor_funcion_raiz'] = func(raiz)
        
        # Análisis de las reducciones aplicadas
        reducciones_aplicadas = sum(1 for iter in historial if iter['reduccion_aplicada'])
        analisis['total_reducciones'] = reducciones_aplicadas
        analisis['porcentaje_reducciones'] = (reducciones_aplicadas / len(historial)) * 100
        
        # Análisis de la velocidad de convergencia
        errores_relativos = [iter['error_relativo'] for iter in historial if iter['error_relativo'] is not None]
        if len(errores_relativos) > 2:
            velocidades = []
            for i in range(1, len(errores_relativos)):
                if errores_relativos[i-1] != 0:
                    velocidades.append(errores_relativos[i] / errores_relativos[i-1])
            
            if velocidades:
                analisis['velocidad_convergencia_promedio'] = sum(velocidades) / len(velocidades)
    
    return analisis


def comparar_regula_falsi_variantes(
    func: Callable[[float], float],
    a: float,
    b: float,
    tolerancia: float = 1e-6,
    max_iteraciones: int = 100
) -> dict:
    """
    Compara las tres variantes del método de Regula Falsi.
    
    Args:
        func: Función f(x) para la cual se busca la raíz
        a: Extremo inferior del intervalo inicial
        b: Extremo superior del intervalo inicial
        tolerancia: Tolerancia para la convergencia
        max_iteraciones: Número máximo de iteraciones
        
    Returns:
        Diccionario con comparación de los tres métodos
    """
    
    # Importar métodos para comparar
    from .regula_falsi import regula_falsi
    
    # Ejecutar los tres métodos
    raiz_rf, iter_rf, conv_rf, hist_rf = regula_falsi(func, a, b, tolerancia, max_iteraciones)
    raiz_rfm, iter_rfm, conv_rfm, hist_rfm = regula_falsi_modificada(
        func, a, b, tolerancia, max_iteraciones, factor_reduccion=0.5
    )
    raiz_rfm2, iter_rfm2, conv_rfm2, hist_rfm2 = regula_falsi_modificada(
        func, a, b, tolerancia, max_iteraciones, factor_reduccion=0.25
    )
    
    comparacion = {
        'regula_falsi': {
            'raiz': raiz_rf,
            'iteraciones': iter_rf,
            'convergencia': conv_rf,
            'historial': hist_rf
        },
        'regula_falsi_modificada_0.5': {
            'raiz': raiz_rfm,
            'iteraciones': iter_rfm,
            'convergencia': conv_rfm,
            'historial': hist_rfm
        },
        'regula_falsi_modificada_0.25': {
            'raiz': raiz_rfm2,
            'iteraciones': iter_rfm2,
            'convergencia': conv_rfm2,
            'historial': hist_rfm2
        }
    }
    
    # Análisis comparativo
    metodos_convergentes = [k for k, v in comparacion.items() if v['convergencia']]
    if len(metodos_convergentes) > 1:
        mejor_metodo = min(metodos_convergentes, key=lambda k: comparacion[k]['iteraciones'])
        comparacion['analisis'] = {
            'metodo_mas_rapido': mejor_metodo,
            'mejora_iteraciones': comparacion['regula_falsi']['iteraciones'] - comparacion[mejor_metodo]['iteraciones']
        }
    
    return comparacion


# Ejemplo de uso
if __name__ == "__main__":
    # Ejemplo: f(x) = x³ - x - 1
    def ejemplo_func(x):
        return x**3 - x - 1
    
    print("=== Método de Regula Falsi Modificada ===")
    print("Función: f(x) = x³ - x - 1")
    print("Intervalo inicial: [1, 2]")
    print("Factor de reducción: 0.5")
    print()
    
    # Ejecutar método
    raiz, iteraciones, convergencia, historial = regula_falsi_modificada(
        ejemplo_func, 1, 2, tolerancia=1e-6, factor_reduccion=0.5, mostrar_iteraciones=True
    )
    
    print(f"Resultado final:")
    print(f"  Raíz aproximada: {raiz}")
    print(f"  Iteraciones: {iteraciones}")
    print(f"  Convergencia: {convergencia}")
    
    if raiz:
        print(f"  f(raíz) = {ejemplo_func(raiz):.2e}")
    
    print("\n=== Comparación de Variantes ===")
    comparacion = comparar_regula_falsi_variantes(ejemplo_func, 1, 2)
    for metodo, datos in comparacion.items():
        if isinstance(datos, dict) and 'iteraciones' in datos:
            print(f"{metodo}: {datos['iteraciones']} iteraciones")
