import pymunk
import pygame
import pymunk.pygame_util
import tkinter as tk
from tkinter import messagebox

ANCHO = 1000
ALTO = 600

def run_simulation(gravedad, v_inicial, w_inicial, mu_aceite, mu_seco, masa, radio, factor_inercia, crr):
    pygame.init()
    pygame.display.set_caption("Simulación Realista de Bolos (Apartado 3)")
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    clock = pygame.time.Clock()
    
    # Creamos el espacio de simulación
    espacio = pymunk.Space()
    espacio.gravity = (0, gravedad)

    # --- PISTA DE BOLOS  ---
    static_body = espacio.static_body
    y_suelo = ALTO - ALTO * 0.1
    x_transicion = ANCHO / 2
    
    # Tramo 1: Aceite 
    floor_aceite = pymunk.Segment(static_body, (0, y_suelo), (x_transicion, y_suelo), 5)
    floor_aceite.friction = mu_aceite
    floor_aceite.color = (150, 200, 255, 255) # Azul
    
    # Tramo 2: Seco 
    floor_seco = pymunk.Segment(static_body, (x_transicion, y_suelo), (20000, y_suelo), 5)
    floor_seco.friction = mu_seco
    floor_seco.color = (255, 180, 100, 255) # Naranja
    
    espacio.add(floor_aceite, floor_seco)

    # --- LA BOLA ---
    moment = factor_inercia * masa * (radio ** 2)	# Momento de inercia modificado
    body = pymunk.Body(masa, moment)
    body.position = (radio, y_suelo - radio)  			
    body.velocity = (v_inicial, 0)  					
    body.angular_velocity = w_inicial               # Giro inicial
    
    shape = pymunk.Circle(body, radio)
    shape.friction = 1.0 
    espacio.add(body, shape)

    draw_options = pymunk.pygame_util.DrawOptions(pantalla)
    
    tiempo = 0
    dt = 1.0 / 60.0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                running = False

        tiempo += dt
        v_actual = body.velocity.x
        w_actual = body.angular_velocity

        # Calculamos si hay rodadura pura (v = w * r)
        if abs(w_actual) > 0.001:
            similitud = abs(1 - (abs(v_actual) / abs(w_actual * radio)))
        else:
            similitud = 9999

        estado = "Deslizamiento"
        if similitud < 0.05: # Umbral de tolerancia
            estado = "Rodadura pura"

        # Rozamiento por rodadura (Solo si se mueve, opone resistencia)
        if abs(w_actual) > 0.01:
            FN = masa * gravedad
            tau_rod = crr * radio * FN
            tau_stop = (body.moment * abs(w_actual)) / dt
            freno = min(tau_rod, tau_stop)
            # Torca opuesta a la rotación
            body.torque = - (1 if w_actual > 0 else -1) * freno
        else:
            body.angular_velocity = 0
            body.torque = 0

        # Identificar zona visualmente
        zona = "ZONA DE ACEITE (Baja fricción)" if body.position.x < x_transicion else "ZONA SECA (Alta fricción)"

        # Fondos visuales
        pygame.draw.rect(pantalla, (235, 245, 255), (0, 0, x_transicion, ALTO))       # Fondo celeste
        pygame.draw.rect(pantalla, (255, 245, 235), (x_transicion, 0, ANCHO, ALTO))   # Fondo naranja claro
        
        # Línea central divisoria
        pygame.draw.line(pantalla, (150, 150, 150), (x_transicion, 0), (x_transicion, ALTO), 2)
        
        espacio.debug_draw(draw_options)
        
        # Textos
        fuente = pygame.font.SysFont("Arial", 20)

        textos = [
            (f"Tiempo: {tiempo:.2f} s", (0, 0, 0)),
            (f"Velocidad (v): {v_actual:.2f} px/s", (0, 0, 0)),
            (f"Vel Angular (w): {w_actual:.2f} rad/s", (0, 0, 0)),
            (f"v ideal (w*r): {w_actual * radio:.2f} px/s", (0, 0, 0)),
            (f"Estado: {estado}", (255, 0, 0) if estado == "Deslizamiento" else (0, 150, 0)),
            (f"Pista: {zona}", (0, 0, 200) if body.position.x < x_transicion else (200, 100, 0))
        ]

        for i, (texto, color) in enumerate(textos):
            img = fuente.render(texto, True, color)
            pantalla.blit(img, (20, 20 + i * 25))

        pygame.display.flip()
        
        espacio.step(dt)
        clock.tick(60)

    pygame.quit()

def crear_formulario():
    def iniciar_simulacion():
        try:
            run_simulation(
                gravedad=float(entry_gravedad.get()),
                v_inicial=float(entry_velocidad.get()),
                w_inicial=float(entry_w_inicial.get()),
                mu_aceite=float(entry_aceite.get()),
                mu_seco=float(entry_seco.get()),
                masa=float(entry_masa.get()),
                radio=float(entry_radio.get()),
                factor_inercia=float(entry_inercia.get()),
                crr=float(entry_crr.get())
            )
        except ValueError:
            messagebox.showerror("Error", "Ingresa valores numéricos válidos")
    
    root = tk.Tk()
    root.title("Configuración Realista (Mitad y Mitad)")
    root.geometry("480x480")
    
    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack(expand=True)
    
    params = [
        ("Gravedad (px/s²):", "980", entry_gravedad := tk.Entry(frame)),
        ("Velocidad lineal inicial (px/s):", "400", entry_velocidad := tk.Entry(frame)),
        ("Vel. Angular inicial (rad/s) [Spin]:", "-10", entry_w_inicial := tk.Entry(frame)),
        ("Fricción mitad 1 (Aceite):", "0.02", entry_aceite := tk.Entry(frame)),
        ("Fricción mitad 2 (Seco):", "0.2", entry_seco := tk.Entry(frame)),
        ("Masa (kg):", "7", entry_masa := tk.Entry(frame)),
        ("Radio (px):", "20", entry_radio := tk.Entry(frame)),
        ("Factor de Inercia (k*m*r²):", "0.45", entry_inercia := tk.Entry(frame)),
        ("Coef. Rodadura (Crr):", "0.01", entry_crr := tk.Entry(frame))
    ]
    
    for i, (label_text, default_val, entry) in enumerate(params):
        tk.Label(frame, text=label_text, font=("Arial", 10)).grid(row=i, column=0, sticky="w", pady=6)
        entry.insert(0, default_val)
        entry.grid(row=i, column=1, pady=6)
    
    tk.Button(frame, text="Iniciar Simulación Realista", command=iniciar_simulacion,
              bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5).grid(row=len(params), column=0, columnspan=2, pady=18)
    
    root.mainloop()

if __name__ == "__main__":
    crear_formulario()