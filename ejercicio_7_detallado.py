"""
Ejercicio 7 - Detalle de Funciones de Iteración g(x) Escogidas

Muestra las fórmulas exactas de las funciones g(x) que se escogieron
para cada ecuación del Ejercicio 7.
"""

def mostrar_funciones_g_escogidas():
    """Muestra las funciones g(x) escogidas para cada ecuación"""
    
    print("=" * 80)
    print("EJERCICIO 7 - FUNCIONES DE ITERACIÓN g(x) ESCOGIDAS")
    print("=" * 80)
    print("Para cada ecuación f(x) = 0, se transformó a x = g(x)")
    print()
    
    ecuaciones = {
        'i': {
            'ecuacion': 'f(x) = x² - sen(x) - 1 = 0',
            'g_escogida': 'g₁',
            'formula': 'x = √(sen(x) + 1)',
            'derivada': "g'(x) = cos(x) / (2√(sen(x) + 1))",
            'condicion_fourier': '✓ CUMPLE (|g\'(x)| < 1)',
            'iteraciones': 6,
            'raiz': 1.409624
        },
        'ii': {
            'ecuacion': 'f(x) = ln(x) - 1 - 1/x = 0',
            'g_escogida': 'g₁',
            'formula': 'x = e^(1 + 1/x)',
            'derivada': "g'(x) = -e^(1 + 1/x) / x²",
            'condicion_fourier': '✗ NO CUMPLE pero converge',
            'iteraciones': 12,
            'raiz': 3.591121
        },
        'iii': {
            'ecuacion': 'f(x) = x + 1/x - e^x = 0',
            'g_escogida': 'g₂',
            'formula': 'x = 1/(e^x - x)',
            'derivada': "g'(x) = -(e^x - 1) / (e^x - x)²",
            'condicion_fourier': '✓ CUMPLE (|g\'(x)| < 1)',
            'iteraciones': 26,
            'raiz': 0.738433
        },
        'iv': {
            'ecuacion': 'f(x) = x² - 5x + 3 = 0',
            'g_escogida': 'g₁',
            'formula': 'x = (x² + 3)/5',
            'derivada': "g'(x) = 2x/5",
            'condicion_fourier': '✓ CUMPLE (|g\'(x)| < 1)',
            'iteraciones': 11,
            'raiz': 0.697225
        },
        'v': {
            'ecuacion': 'f(x) = cos(x) - 3x = 0',
            'g_escogida': 'g₁',
            'formula': 'x = cos(x)/3',
            'derivada': "g'(x) = -sen(x)/3",
            'condicion_fourier': '✓ CUMPLE (|g\'(x)| < 1)',
            'iteraciones': 6,
            'raiz': 0.316751
        },
        'vi': {
            'ecuacion': 'f(x) = x·e^x - 1 = 0',
            'g_escogida': 'g₁',
            'formula': 'x = 1/e^x = e^(-x)',
            'derivada': "g'(x) = -e^(-x)",
            'condicion_fourier': '✗ NO CUMPLE pero converge',
            'iteraciones': 22,
            'raiz': 0.567143
        }
    }
    
    for letra, datos in ecuaciones.items():
        print(f"ECUACIÓN {letra.upper()}: {datos['ecuacion']}")
        print("-" * 60)
        print(f"🎯 Función g(x) escogida: {datos['g_escogida']}")
        print(f"📐 Fórmula: {datos['formula']}")
        print(f"📊 Derivada: {datos['derivada']}")
        print(f"🔍 Condición de Fourier: {datos['condicion_fourier']}")
        print(f"📈 Iteraciones: {datos['iteraciones']}")
        print(f"🎯 Raíz: {datos['raiz']:.6f}")
        print()
    
    print("=" * 80)
    print("PROCESO DE SELECCIÓN DE g(x)")
    print("=" * 80)
    print("Para cada ecuación se probaron 3 opciones:")
    print()
    print("1️⃣ g₁: Primera transformación (aislamiento directo)")
    print("2️⃣ g₂: Segunda transformación (inversión o manipulación)")
    print("3️⃣ g₃: Método de suma (x = x + f(x))")
    print()
    print("Criterios de selección:")
    print("✅ Convergencia (prioridad 1)")
    print("✅ Menor número de iteraciones (prioridad 2)")
    print("✅ Condición de Fourier (prioridad 3)")
    print()
    
    print("=" * 80)
    print("DETALLE DE TRANSFORMACIONES POR ECUACIÓN")
    print("=" * 80)
    
    transformaciones = {
        'i': {
            'f': 'x² - sen(x) - 1 = 0',
            'pasos': [
                'x² = sen(x) + 1',
                'x = √(sen(x) + 1)',
                'g₁(x) = √(sen(x) + 1)'
            ],
            'alternativas': [
                'g₂(x) = arcsen(x² - 1) [NO FUNCIONA: dominio restringido]',
                'g₃(x) = x + (x² - sen(x) - 1) [NO CONVERGE]'
            ]
        },
        'ii': {
            'f': 'ln(x) - 1 - 1/x = 0',
            'pasos': [
                'ln(x) = 1 + 1/x',
                'x = e^(1 + 1/x)',
                'g₁(x) = e^(1 + 1/x)'
            ],
            'alternativas': [
                'g₂(x) = 1/(ln(x) - 1) [NO FUNCIONA: dominio restringido]',
                'g₃(x) = x + (ln(x) - 1 - 1/x) [NO FUNCIONA: dominio restringido]'
            ]
        },
        'iii': {
            'f': 'x + 1/x - e^x = 0',
            'pasos': [
                'x + 1/x = e^x',
                '1/x = e^x - x',
                'x = 1/(e^x - x)',
                'g₂(x) = 1/(e^x - x)'
            ],
            'alternativas': [
                'g₁(x) = e^x - 1/x [NO FUNCIONA: overflow]',
                'g₃(x) = x + (x + 1/x - e^x) [NO CONVERGE]'
            ]
        },
        'iv': {
            'f': 'x² - 5x + 3 = 0',
            'pasos': [
                'x² = 5x - 3',
                'x² + 3 = 5x',
                'x = (x² + 3)/5',
                'g₁(x) = (x² + 3)/5'
            ],
            'alternativas': [
                'g₂(x) = √(5x - 3) [CONVERGE pero más lento]',
                'g₃(x) = x + (x² - 5x + 3) [NO CONVERGE]'
            ]
        },
        'v': {
            'f': 'cos(x) - 3x = 0',
            'pasos': [
                'cos(x) = 3x',
                'x = cos(x)/3',
                'g₁(x) = cos(x)/3'
            ],
            'alternativas': [
                'g₂(x) = arccos(3x) [NO FUNCIONA: dominio restringido]',
                'g₃(x) = x + (cos(x) - 3x) [NO CONVERGE]'
            ]
        },
        'vi': {
            'f': 'x·e^x - 1 = 0',
            'pasos': [
                'x·e^x = 1',
                'x = 1/e^x',
                'x = e^(-x)',
                'g₁(x) = e^(-x)'
            ],
            'alternativas': [
                'g₂(x) = e^(-x) [MISMA que g₁]',
                'g₃(x) = x + (x·e^x - 1) [NO CONVERGE]'
            ]
        }
    }
    
    for letra, datos in transformaciones.items():
        print(f"ECUACIÓN {letra.upper()}: {datos['f']}")
        print("-" * 50)
        print("📐 Pasos de transformación:")
        for i, paso in enumerate(datos['pasos'], 1):
            print(f"   {i}. {paso}")
        print()
        print("🔄 Alternativas probadas:")
        for alt in datos['alternativas']:
            print(f"   • {alt}")
        print()
    
    print("=" * 80)
    print("CÓDIGO PYTHON DE LAS FUNCIONES g(x)")
    print("=" * 80)
    print("Aquí tienes el código exacto de cada función g(x) escogida:")
    print()
    
    codigo_python = {
        'i': "g1 = lambda x: math.sqrt(math.sin(x) + 1)",
        'ii': "g1 = lambda x: math.exp(1 + 1/x)",
        'iii': "g2 = lambda x: 1 / (math.exp(x) - x)",
        'iv': "g1 = lambda x: (x**2 + 3) / 5",
        'v': "g1 = lambda x: math.cos(x) / 3",
        'vi': "g1 = lambda x: math.exp(-x)"
    }
    
    for letra, codigo in codigo_python.items():
        print(f"Ecuación {letra.upper()}: {codigo}")
    
    print()
    print("🎯 RESUMEN:")
    print("• 5/6 ecuaciones usaron g₁ (primera opción)")
    print("• 1/6 ecuaciones usó g₂ (segunda opción)")
    print("• 0/6 ecuaciones usó g₃ (método suma)")
    print("• 4/6 ecuaciones cumplen condición de Fourier")
    print("• 6/6 ecuaciones convergen exitosamente")


if __name__ == "__main__":
    mostrar_funciones_g_escogidas()
