import numpy as np
import matplotlib.pyplot as plt

def regla_rectangulo_grafica(funcion, a, b, n):
    """
    Calcula la integral numérica usando la regla del rectángulo (Punto Medio)
    y genera una gráfica similar a la diapositiva.
    
    Parámetros:
    funcion: La función matemática a integrar (como lambda o def)
    a: Inicio del intervalo
    b: Fin del intervalo
    n: Número de subintervalos (rectángulos)
    """
    
    # 1. CÁLCULO NUMÉRICO
    # Ancho de cada subintervalo (Delta x)
    dx = (b - a) / n
    
    # Puntos medios de cada rectángulo (para determinar la altura)
    # Se usa el punto medio para reducir el error, tal como parece sugerir el gráfico
    x_mid = np.linspace(a + dx/2, b - dx/2, n)
    
    # Altura de los rectángulos: f(x) evaluada en los puntos medios
    alturas = funcion(x_mid)
    
    # Área total = Suma de (base * altura)
    area_total = np.sum(alturas * dx)
    
    print(f"--- Resultados ---")
    print(f"Intervalo: [{a}, {b}]")
    print(f"Número de rectángulos (n): {n}")
    print(f"Ancho del intervalo (Δx): {dx:.4f}")
    print(f"Área aproximada: {area_total:.6f}")

    # 2. VISUALIZACIÓN (RECREACIÓN DE LA IMAGEN)
    plt.figure(figsize=(10, 6))
    
    # A. Dibujar la función suave (curva azul)
    x_suave = np.linspace(a, b, 200)
    y_suave = funcion(x_suave)
    plt.plot(x_suave, y_suave, 'b-', label='Función f(x)', linewidth=2)
    
    # B. Dibujar los rectángulos (barras naranjas)
    # Usamos alpha=0.4 para que sean semitransparentes como en la imagen
    # width=dx hace que las barras se toquen entre sí
    plt.bar(x_mid, alturas, width=dx, align='center', 
            color='orange', alpha=0.4, edgecolor='chocolate', label='Suma de Riemann')
    
    # C. Detalles estéticos para parecerse a la diapositiva
    plt.title(f'Integración Numérica - Regla del Rectángulo (n={n})')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.axhline(0, color='black', linewidth=1) # Eje X
    plt.axvline(a, color='gray', linestyle='--') # Línea en a
    plt.axvline(b, color='gray', linestyle='--') # Línea en b
    
    # Etiquetas a y b en el eje
    plt.xticks(list(plt.xticks()[0]) + [a, b])
    plt.text(a - 0.1, 0.2, 'a', horizontalalignment='center', color='black')
    plt.text(b + 0.1, 0.2, 'b', horizontalalignment='center', color='black')
    
    # Flecha y etiqueta para Delta x (Δx) - Decorativo
    mid_idx = n // 2
    x_arrow = x_mid[mid_idx]
    y_arrow_pos = 0 # Base del rectángulo
    
    plt.annotate('', xy=(x_arrow - dx/2, y_arrow_pos), xytext=(x_arrow + dx/2, y_arrow_pos),
                 arrowprops=dict(arrowstyle='<->', color='black'))
    plt.text(x_arrow, y_arrow_pos - 1.5, r'$\Delta x$', horizontalalignment='center', fontsize=12)

    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.show()
    

def regla_trapecio_grafica(funcion, a, b, n):
    dx = (b - a) / n
    
    # Puntos medios de cada rectángulo (para determinar la altura)
    # Se usa el punto medio para reducir el error, tal como parece sugerir el gráfico
    x_init = np.linspace(a, b - dx, n)  # Puntos iniciales de cada subintervalo
    x_end = np.linspace(a + dx, b, n)   # Puntos finales
    
    # Altura de los rectángulos: f(x) evaluada en los puntos medios
    alturas_iniciales = funcion(x_init)
    alturas_finales = funcion(x_end)
    
    # Área total = Suma de (base * altura)
    area_total = np.sum(((alturas_iniciales + alturas_finales)/ 2) * dx)
    
    print(f"--- Resultados Trapecio ---")
    print(f"Intervalo: [{a}, {b}]")
    print(f"Número de trapecios (n): {n}")
    print(f"Ancho del intervalo (Δx): {dx:.4f}")
    print(f"Área aproximada: {area_total:.6f}")
    
    # 2. VISUALIZACIÓN (RECREACIÓN DE LA IMAGEN)
    plt.figure(figsize=(10, 6))
    
    # A. Dibujar la función suave (curva azul)
    x_suave = np.linspace(a, b, 200)
    y_suave = funcion(x_suave)
    plt.plot(x_suave, y_suave, 'b-', label='Función f(x)', linewidth=2)
    
    # B. Dibujar los trapecios (barras naranjas)
    for i in range(n):
       x_trapecio = [x_init[i], x_end[i], x_end[i], x_init[i]]
       y_trapecio = [0, 0, alturas_finales[i], alturas_iniciales[i]]
       plt.fill(x_trapecio, y_trapecio, color='orange', alpha=0.4, edgecolor='chocolate')
    
    # C. Detalles estéticos para parecerse a la diapositiva
    plt.title(f'Integración Numérica - Regla del Trapecio (n={n})')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.axhline(0, color='black', linewidth=1) # Eje X
    plt.axvline(a, color='gray', linestyle='--') # Línea en a
    plt.axvline(b, color='gray', linestyle='--') # Línea en b
    
    # Etiquetas a y b en el eje
    plt.xticks(list(plt.xticks()[0]) + [a, b])
    plt.text(a - 0.1, 0.2, 'a', horizontalalignment='center', color='black')
    plt.text(b + 0.1, 0.2, 'b', horizontalalignment='center', color='black')
    
    # Flecha y etiqueta para Delta x (Δx) - Decorativo
    mid_idx = n // 2
    x_arrow = (x_init[mid_idx] + x_end[mid_idx]) / 2
    y_arrow_pos = 0 # Base del trapecio
    
    plt.annotate('', xy=(x_arrow - dx/2, y_arrow_pos), xytext=(x_arrow + dx/2, y_arrow_pos),
        arrowprops=dict(arrowstyle='<->', color='black'))
    plt.text(x_arrow, y_arrow_pos - 1.5, r'$\Delta x$', horizontalalignment='center', fontsize=12)

    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.show()
    

# --- EJECUCIÓN DEL PROGRAMA ---

# Definimos una función de prueba.
# Usaré una parábola invertida similar a la imagen: f(x) = -(x-3)^2 + 10
def mi_funcion(x):
    return -(x - 3)**3 + 20

# Parámetros definidos por el usuario
a = 0   # Inicio
b = 5   # Fin
n = 10000   # Número de rectángulos (prueba cambiando esto a 4, 10, 50)

# Llamamos a la función
regla_rectangulo_grafica(mi_funcion, a, b, n)

regla_trapecio_grafica(mi_funcion, a, b, n)