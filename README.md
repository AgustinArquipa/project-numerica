# Project Numerica - Métodos de Resolución de Ecuaciones No Lineales

## Descripción

Este proyecto implementa métodos numéricos para resolver ecuaciones no lineales de la forma **f(x) = 0**. Fue desarrollado para la materia **Programación Numérica** como parte del **Tema III: Resolución de Ecuaciones No Lineales**.

## Estructura del Proyecto

```
project-numerica/
│── main.py                # Archivo principal para probar métodos
│
├── cerrados/              # Métodos cerrados
│   ├── __init__.py
│   ├── biseccion.py       # Método de Bisección
│   ├── regula_falsi.py    # Método de Regula Falsi
│   └── regula_falsi_modificada.py  # Regula Falsi Modificada
│
├── abiertos/              # Métodos abiertos
│   ├── __init__.py
│   ├── punto_fijo.py      # Iteración de Punto Fijo
│   ├── newton.py          # Método de Newton
│   └── secante.py         # Método de la Secante
│
├── utils/                 # Utilidades comunes
│   ├── __init__.py
│   ├── helpers.py         # Funciones de error, validaciones, etc.
│   └── export.py          # Funciones de exportación a CSV/JSON
│
├── resultados/            # Archivos CSV/JSON generados (se crea automáticamente)
├── ejemplo_exportacion.py # Ejemplo de uso de funcionalidades de exportación
└── README.md              # Esta documentación
```

## Métodos Implementados

### Métodos Cerrados

#### 1. Método de Bisección
- **Descripción**: Divide el intervalo por la mitad en cada iteración
- **Ventajas**: Siempre converge, robusto
- **Desventajas**: Convergencia lenta (lineal)
- **Velocidad**: O(1/2^n)

#### 2. Método de Regula Falsi
- **Descripción**: Utiliza interpolación lineal para aproximar la raíz
- **Ventajas**: Más rápido que bisección en algunos casos
- **Desventajas**: Puede converger lentamente si un extremo se mantiene fijo
- **Velocidad**: Superlineal

#### 3. Método de Regula Falsi Modificada
- **Descripción**: Mejora de Regula Falsi que evita extremos fijos
- **Ventajas**: Mejor convergencia que Regula Falsi tradicional
- **Desventajas**: Parámetro adicional (factor de reducción)
- **Velocidad**: Superlineal mejorada

### Métodos Abiertos

#### 4. Iteración de Punto Fijo
- **Descripción**: Transforma f(x) = 0 en x = g(x) y itera
- **Ventajas**: Simple de implementar
- **Desventajas**: Requiere transformación adecuada y condición de Fourier
- **Velocidad**: Lineal (depende de |g'(x)|)

#### 5. Método de Newton
- **Descripción**: Utiliza la derivada para aproximaciones sucesivas
- **Ventajas**: Convergencia cuadrática muy rápida
- **Desventajas**: Requiere cálculo de derivada, puede divergir
- **Velocidad**: Cuadrática O(e_n²)

#### 6. Método de Newton-Raphson
- **Descripción**: Variante de Newton que incluye segunda derivada
- **Ventajas**: Convergencia aún más rápida
- **Desventajas**: Requiere segunda derivada
- **Velocidad**: Cúbica

#### 7. Método de la Secante
- **Descripción**: Aproximación de Newton sin derivada
- **Ventajas**: No requiere derivada, convergencia superlineal
- **Desventajas**: Puede ser menos estable que Newton
- **Velocidad**: Superlineal (~1.618 - número áureo)

#### 8. Método de la Secante Modificada
- **Descripción**: Usa diferencias finitas con paso fijo
- **Ventajas**: No requiere dos puntos iniciales
- **Desventajas**: Requiere selección adecuada del paso h
- **Velocidad**: Superlineal

## Características Principales

### Funcionalidades Implementadas

1. **Implementación completa** de todos los métodos del programa analítico
2. **Análisis de convergencia** con cálculo de velocidades
3. **Validaciones robustas** (intervalos, condiciones de Fourier, etc.)
4. **Cálculo de errores** (absoluto, relativo, cuadrático)
5. **Técnicas de aceleración** (Aitken, Steffensen)
6. **Comparaciones automáticas** entre métodos
7. **Historial detallado** de iteraciones
8. **Interfaz interactiva** para pruebas
9. **Exportación a CSV/JSON** con metadata completa
10. **Comparaciones exportables** entre métodos

### Utilidades Incluidas

- **Cálculo de errores**: Absoluto y relativo
- **Validación de intervalos**: Teorema de Bolzano
- **Condición de Fourier**: Para métodos de punto fijo
- **Aceleración de Aitken**: Para secuencias convergentes
- **Aceleración de Steffensen**: Para métodos de punto fijo
- **Análisis de velocidad**: Cálculo automático de órdenes de convergencia
- **Exportación CSV**: Historiales de iteraciones con metadata
- **Exportación JSON**: Resultados estructurados para análisis
- **Comparaciones exportables**: Tablas comparativas entre métodos
- **Gestión de archivos**: Listado y limpieza automática

## Uso del Proyecto

### Ejecución Básica

```bash
python main.py
```

### Ejemplos de Uso Programático

```python
from cerrados import biseccion
from abiertos import newton
from utils.helpers import error_absoluto

# Definir función
def f(x):
    return x**3 - x - 1

# Método cerrado
raiz, iteraciones, convergencia, historial = biseccion(f, 1, 2)

# Método abierto (requiere derivada)
def f_derivada(x):
    return 3 * x**2 - 1

raiz, iteraciones, convergencia, historial = newton(f, f_derivada, 1.5)

print(f"Raíz encontrada: {raiz}")
print(f"Iteraciones: {iteraciones}")
```

### Ejemplos Incluidos

El archivo `main.py` incluye tres ejemplos completos:

1. **f(x) = x³ - x - 1 = 0**: Ejemplo clásico con todos los métodos
2. **f(x) = e^x - 3x = 0**: Función exponencial
3. **f(x) = x² - 2 = 0**: Cálculo de √2 con análisis de error

### Exportación de Resultados

El proyecto incluye funcionalidades avanzadas de exportación:

```python
from utils import exportar_iteraciones_csv, exportar_resultado_completo

# Exportar historial simple
exportar_iteraciones_csv(historial, "mis_iteraciones.csv")

# Exportar resultado completo con metadata
exportar_resultado_completo(
    metodo="Bisección",
    funcion="f(x) = x³ - x - 1",
    parametros={"a": 1.0, "b": 2.0, "tolerancia": 1e-6},
    resultado={"raiz": 1.32471796, "iteraciones": 20, "convergencia": True},
    historial=historial
)
```

#### Formatos de Exportación

- **CSV simple**: Solo historial de iteraciones
- **CSV completo**: Con metadata, parámetros y resultados
- **JSON**: Datos estructurados para análisis avanzado
- **Comparaciones**: Tablas comparativas entre métodos

#### Ejecutar Ejemplos de Exportación

```bash
python3 ejemplo_exportacion.py
```

## Requisitos

- **Python 3.7+**
- **Bibliotecas estándar**: math, typing
- **No requiere dependencias externas**

## Teoría Matemática

### Condición de Fourier
Para que el método de punto fijo converja, debe cumplirse:
|g'(x)| < 1 en una vecindad del punto fijo

### Velocidades de Convergencia
- **Lineal**: |e_{n+1}| ≤ C|e_n|
- **Superlineal**: |e_{n+1}| ≤ C|e_n|^p con p > 1
- **Cuadrática**: |e_{n+1}| ≤ C|e_n|²
- **Cúbica**: |e_{n+1}| ≤ C|e_n|³

### Aceleración de Aitken
x* ≈ x_n - (x_{n+1} - x_n)² / (x_{n+2} - 2*x_{n+1} + x_n)

### Aceleración de Steffensen
x_{n+1} = x_n - (g(x_n) - x_n)² / (g(g(x_n)) - 2*g(x_n) + x_n)

## Contenido del Programa Analítico

Este proyecto implementa completamente el **Tema III** del programa analítico:

### Métodos Cerrados
- ✅ Bisección
- ✅ Regula Falsi  
- ✅ Regula Falsi Modificada

### Métodos Abiertos
- ✅ Iteración de Punto Fijo
- ✅ Método de Newton
- ✅ Método de la Secante

### Conceptos Teóricos
- ✅ Algoritmos implementados
- ✅ Condición de Fourier
- ✅ Convergencia
- ✅ Velocidad de Convergencia
- ✅ Aceleración de la Convergencia (Aitken y Steffensen)

## Contribuciones

Este proyecto fue desarrollado como material de estudio para la materia **Programación Numérica**, implementando todos los métodos numéricos del programa analítico con ejemplos prácticos y análisis detallado.

## Licencia

Proyecto educativo desarrollado para fines académicos.
