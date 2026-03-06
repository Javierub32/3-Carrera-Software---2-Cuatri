import pymunk
import pygame
import math
import tkinter as tk
from tkinter import messagebox

def run_simulation(angulo_grados=70, gravedad=900, damping=0.3):
    # Iniciamos pygame
    pygame.init()
    pygame.display.set_caption("Simulación de un Péndulo Amortiguado")
    pantalla = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    
	# Creamos el espacio de simulación
    espacio = pymunk.Space()
    espacio.gravity = (0, gravedad)
    
    # Configuramos la esfera y el hilo
    mass = 1.0
    radius = 40
    longitud_hilo = 350
    angulo_inicial = math.radians(angulo_grados)
    posicion_hilo = (400, 100)
    
	# Creamos el cuerpo (física) y la forma (colisión) de la esfera
    moment = pymunk.moment_for_circle(mass, 0, radius)
    body = pymunk.Body(mass, moment)
    body.position = (
        posicion_hilo[0] + longitud_hilo * math.sin(angulo_inicial),
        posicion_hilo[1] + longitud_hilo * math.cos(angulo_inicial)
    )
    shape = pymunk.Circle(body, radius)
    espacio.add(body, shape)

    # Unimos la esfera al soporte con un PinJoint (hilo inextensible)
    joint = pymunk.PinJoint(espacio.static_body, body, posicion_hilo, (0, 0))
    espacio.add(joint)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False

        # Aplicamos amortiguacion (F = -b * v)
        v = body.velocity
        f_amortiguacion = -damping * v
        body.apply_force_at_world_point(f_amortiguacion, body.position)

		# Dibujamos la escena
        pantalla.fill((255, 255, 255))

        # Dibujar Soporte
        pygame.draw.line(pantalla, (0, 0, 0), (350, 100), (450, 100), 5)
        
        # Dibujar Hilo
        pos = (int(body.position.x), int(body.position.y))
        pygame.draw.line(pantalla, (150, 150, 150), posicion_hilo, pos, 2)

        # Dibujar Esfera
        pygame.draw.circle(pantalla, (50, 100, 255), pos, radius) # Esfera rellena
        pygame.draw.circle(pantalla, (0, 0, 0), pos, radius, 2)   # Borde

		# Refrescamos la pantalla para mostrar los cambios
        pygame.display.flip()
        
		# Avanzamos la simulación 1 frame y limitamos a 60FPS
        espacio.step(1.0 / 60.0)
        clock.tick(60)

    pygame.quit()

def crear_formulario():
    """Crea un formulario para configurar los parámetros del péndulo"""
    def iniciar_simulacion():
        try:
            angulo = float(entry_angulo.get())
            gravedad = float(entry_gravedad.get())
            damp = float(entry_damping.get())
            
            # Validaciones
            if angulo <= 0 or angulo >= 180:
                messagebox.showerror("Error", "El ángulo debe estar entre 0 y 180 grados")
                return
            if gravedad < 0:
                messagebox.showerror("Error", "La gravedad no puede ser negativa")
                return
            if damp < 0:
                messagebox.showerror("Error", "El damping no puede ser negativo")
                return
            
            # Cerrar formulario e iniciar simulación
            root.destroy()
            run_simulation(angulo_grados=angulo, gravedad=gravedad, damping=damp)
            
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa valores numéricos válidos")
    
    # Crear ventana
    root = tk.Tk()
    root.title("Configuración del Péndulo")
    root.geometry("400x220")
    root.resizable(False, False)
    
    # Frame principal
    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack(expand=True)
    
    # Campo ángulo inicial
    tk.Label(frame, text="Ángulo inicial (grados):", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=8)
    entry_angulo = tk.Entry(frame, width=20)
    entry_angulo.insert(0, "70")
    entry_angulo.grid(row=0, column=1, pady=8)
    
    # Campo gravedad
    tk.Label(frame, text="Gravedad (px/s²):", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=8)
    entry_gravedad = tk.Entry(frame, width=20)
    entry_gravedad.insert(0, "900")
    entry_gravedad.grid(row=1, column=1, pady=8)
    
    # Campo damping
    tk.Label(frame, text="Damping (amortiguamiento):", font=("Arial", 10)).grid(row=2, column=0, sticky="w", pady=8)
    entry_damping = tk.Entry(frame, width=20)
    entry_damping.insert(0, "0.3")
    entry_damping.grid(row=2, column=1, pady=8)
    
    # Botón iniciar
    btn_iniciar = tk.Button(frame, text="Iniciar Simulación", command=iniciar_simulacion,
                            bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
                            padx=10, pady=5)
    btn_iniciar.grid(row=3, column=0, columnspan=2, pady=20)
    
    root.mainloop()

if __name__ == "__main__":
    crear_formulario()
