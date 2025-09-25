"""
Utilidades comunes para métodos numéricos.

Este módulo contiene funciones auxiliares como:
- Cálculo de errores
- Validaciones
- Funciones de convergencia
- Exportación de resultados
"""

from .helpers import (
    error_relativo,
    error_absoluto,
    validar_intervalo,
    verificar_convergencia,
    aceleracion_aitken,
    aceleracion_steffensen
)

from .export import (
    exportar_iteraciones_csv,
    exportar_resultado_completo,
    exportar_comparacion_csv,
    exportar_a_json,
    crear_tabla_resumen,
    listar_archivos_generados,
    limpiar_archivos_antiguos
)

from .precision import (
    redondear_significativos,
    formato_exponencial_legible,
    aplicar_formato_calculadora,
    configurar_decimal_precision,
    redondear_decimal,
    aplicar_precision_calculadora,
    procesar_iteracion_con_precision,
    procesar_historial_con_precision,
    comparar_precisiones,
    simular_calculadora_cientifica,
    mostrar_precision_analysis
)

__all__ = [
    'error_relativo',
    'error_absoluto', 
    'validar_intervalo',
    'verificar_convergencia',
    'aceleracion_aitken',
    'aceleracion_steffensen',
    'exportar_iteraciones_csv',
    'exportar_resultado_completo',
    'exportar_comparacion_csv',
    'exportar_a_json',
    'crear_tabla_resumen',
    'listar_archivos_generados',
    'limpiar_archivos_antiguos',
    'redondear_significativos',
    'formato_exponencial_legible',
    'aplicar_formato_calculadora',
    'configurar_decimal_precision',
    'redondear_decimal',
    'aplicar_precision_calculadora',
    'procesar_iteracion_con_precision',
    'procesar_historial_con_precision',
    'comparar_precisiones',
    'simular_calculadora_cientifica',
    'mostrar_precision_analysis'
]
