import pymunk
import pygame
import pymunk.pygame_util
import tkinter as tk
from tkinter import messagebox

ANCHO = 800
ALTO = 600

def run_simulation(gravedad=900, v_inicial=0, coef_roz=0, masa=1, radio=40):
    # Iniciamos pygame
    pygame.init()
    pygame.display.set_caption("Simulación de Bolos (Apartado 2)")
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    clock = pygame.time.Clock()
    
    # Creamos el espacio de simulación
    espacio = pymunk.Space()
    espacio.gravity = (0, gravedad)


    # --- PISTA DE BOLOS ---
    static_body = espacio.static_body
    p1 = (ANCHO, ALTO - ALTO * 0.1)
    p2 = (0, ALTO - ALTO * 0.1)
    floor = pymunk.Segment(static_body, p1, p2, 5)
    floor.friction = coef_roz
    espacio.add(floor)


    # --- LA BOLA ---
    moment = (2 / 5) * masa * (radio ** 2)				# Momento de inercia para una esfera sólida
    body = pymunk.Body(masa, moment)
    x_inicial = radio  									# Pegada al borde izquierdo
    y_inicial = (ALTO - ALTO * 0.1) - radio  			# Justo apoyada sobre el suelo
    body.position = (x_inicial, y_inicial)  			# Posición inicial de la esfera
    body.velocity = (v_inicial, 0)  					# Velocidad inicial (horizontal)
    shape = pymunk.Circle(body, radio)
    shape.friction = 1.0
    espacio.add(body, shape)

    draw_options = pymunk.pygame_util.DrawOptions(pantalla)
    tiempo = 0
    tiempo_des = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                running = False

        tiempo += 1.0 / 60.0
        
        v_actual = body.velocity.x
        w_actual = body.angular_velocity

        similitud = abs(1 - (v_actual / (w_actual * radio))) if w_actual != 0 else 9999

		# Determinamos el estado de la bola (rodadura pura o deslizamiento) basándonos en la similitud entre v y w*R
        estado = ''
        if similitud < 0.005:
            estado = "Rodadura pura"
        else:
            tiempo_des = tiempo
            estado = "Deslizamiento"


        # Limpiamos la pantalla (fondo blanco)
        pantalla.fill((255, 255, 255))

        # Dibujamos TODO lo que hay en el espacio automáticamente
        espacio.debug_draw(draw_options)
        
        fuente = pygame.font.SysFont("Arial", 20)

        textos = [
            (f"Tiempo total: {tiempo:.2f} s", (0, 0, 0)),
            (f"Velocidad (v): {v_actual:.2f} px/s", (0, 0, 0)),
            (f"Vel Angular (w): {w_actual:.2f} rad/s", (0, 0, 0)),
            (f"Estado: {estado}", (255, 0, 0) if estado == "Deslizamiento" else (0, 150, 0)),
            (f"Tiempo deslizamiento: {tiempo_des:.2f} s", (100, 100, 100))
        ]

        for i, (texto, color) in enumerate(textos):
            img = fuente.render(texto, True, color) 
            pantalla.blit(img, (20, 20 + i * 25))

        pygame.display.flip()
        
        # Avanzamos la simulación
        espacio.step(1.0 / 60.0)
        clock.tick(60)

    pygame.quit()
    

def crear_formulario():
    def iniciar_simulacion():
        try:
            run_simulation(
                gravedad=float(entry_gravedad.get()),
                v_inicial=float(entry_velocidad.get()),
                coef_roz=float(entry_rozamiento.get()),
                masa=float(entry_masa.get()),
                radio=float(entry_radio.get())
            )
        except ValueError:
            messagebox.showerror("Error", "Ingresa valores numéricos válidos")
    
    root = tk.Tk()
    root.title("Configuración Ideal (Apartado 2)")
    root.geometry("400x320")
    
    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack(expand=True)
    
    params = [
        ("Gravedad (px/s²):", "980", entry_gravedad := tk.Entry(frame)),
        ("Velocidad lineal inicial (px/s):", "400", entry_velocidad := tk.Entry(frame)),
        ("Coeficiente de rozamiento:", "0.1", entry_rozamiento := tk.Entry(frame)),
        ("Masa (kg):", "7", entry_masa := tk.Entry(frame)),
        ("Radio (px):", "20", entry_radio := tk.Entry(frame))
    ]
    
    for i, (label_text, default_val, entry) in enumerate(params):
        tk.Label(frame, text=label_text, font=("Arial", 10)).grid(row=i, column=0, sticky="w", pady=6)
        entry.insert(0, default_val)
        entry.grid(row=i, column=1, pady=6)
    
    tk.Button(frame, text="Iniciar Simulación Ideal", command=iniciar_simulacion,
              bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5).grid(row=len(params), column=0, columnspan=2, pady=18)
    
    root.mainloop()

if __name__ == "__main__":
    crear_formulario()