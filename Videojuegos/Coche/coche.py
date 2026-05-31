import pygame
import math
import numpy as np
from scipy.interpolate import interp1d
import sys

# =========================================================
# CONFIGURACIÓN DEL SIMULADOR
# =========================================================
ANCHO = 1200
ALTO = 600
FPS = 60

# Colores (Estilo Telemetría Moderna)
NEGRO = (15, 15, 20)
BLANCO = (255, 255, 255)
GRIS = (50, 50, 50)
GRIS_CLARO = (150, 150, 150)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ROJO = (255, 50, 50)
AMARILLO = (255, 200, 0)

# =========================================================
# FÍSICA Y DATOS DEL MOTOR (Ferrari F430)
# =========================================================
RPM_DATOS = np.array([1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5250, 5500, 6000, 6500, 7000, 7500, 8000, 8500])
PAR_DATOS = np.array([320, 345, 370, 400, 415, 430, 445, 455, 465, 465, 460, 455, 450, 440, 430, 415, 390])
interp_par = interp1d(RPM_DATOS, PAR_DATOS, kind='cubic', fill_value="extrapolate")

RELACIONES = {1: 3.29, 2: 2.16, 3: 1.61, 4: 1.26, 5: 1.03, 6: 0.85}
FINAL_DRIVE = 4.30
RADIO_RUEDA = 0.38
MASA = 1450.0

class CocheSimulador:
    def __init__(self):
        self.x = 0.0          # Distancia (m)
        self.v = 0.0          # Velocidad (m/s)
        self.rpm = 1000.0
        self.marcha = 1
        
        self.acelerando = False
        self.frenando = False
        
        # Datos para la telemetría visual
        self.par_motor_actual = 0.0
        self.fuerza_drag = 0.0
        self.aceleracion_actual = 0.0

    def obtener_par(self):
        rpm_seguras = max(1000, min(self.rpm, 8500))
        return float(interp_par(rpm_seguras))

    def actualizar(self, dt):
        # 1. Cálculo de RPM según la velocidad (Cinemática de transmisión)
        if self.v > 0.1:
            omega_rueda = self.v / RADIO_RUEDA
            rpm_calculadas = omega_rueda * RELACIONES[self.marcha] * FINAL_DRIVE * (60 / (2 * math.pi))
            self.rpm = max(1000, rpm_calculadas)
        else:
            self.rpm = 1000 if not self.acelerando else min(4500, self.rpm + 3000 * dt)

        # 2. Fuerzas Motrices
        fuerza_traccion = 0
        self.par_motor_actual = 0
        
        if self.acelerando and self.rpm <= 8500:
            self.par_motor_actual = self.obtener_par()
            par_rueda = self.par_motor_actual * RELACIONES[self.marcha] * FINAL_DRIVE * 0.85 # 85% eficiencia
            fuerza_traccion = par_rueda / RADIO_RUEDA
            
        if self.rpm > 8500:
            self.rpm = 8500 # Corte de inyección (limita RPM pero no frena bruscamente)

        # 3. Fuerzas Resistivas
        self.fuerza_drag = 0.5 * 1.225 * 0.33 * 2.03 * (self.v ** 2) # F_drag = 1/2 * rho * Cd * A * v^2
        fuerza_rodadura = 0.015 * MASA * 9.81
        
        fuerza_freno = 0
        if self.frenando and self.v > 0:
            fuerza_freno = 12000 # Fuerza de frenado en Newtons

        # 4. 2ª Ley de Newton (F = m * a)
        fuerza_neta = fuerza_traccion - self.fuerza_drag - fuerza_rodadura - fuerza_freno
        
        # Evitar que el coche vaya marcha atrás por la rodadura/freno
        if self.v <= 0 and fuerza_neta < 0:
            fuerza_neta = 0
            self.v = 0

        self.aceleracion_actual = fuerza_neta / MASA
        
        # Integración de Euler
        self.v += self.aceleracion_actual * dt
        self.x += self.v * dt

    def cambiar_marcha(self, subir=True):
        if subir and self.marcha < 6:
            self.marcha += 1
            # Caída de RPM al subir marcha
            self.rpm = self.rpm * (RELACIONES[self.marcha] / RELACIONES[self.marcha - 1])
        elif not subir and self.marcha > 1:
            # Proteccion para no pasar de vueltas al reducir
            rpm_estimada = self.rpm * (RELACIONES[self.marcha - 1] / RELACIONES[self.marcha])
            if rpm_estimada < 8500:
                self.marcha -= 1
                self.rpm = rpm_estimada

# =========================================================
# FUNCIONES VISUALES (SIN IMÁGENES EXTERNAS)
# =========================================================
def dibujar_coche_vectorial(pantalla, x, y):
    """Dibuja un deportivo usando polígonos simples"""
    # Carrocería
    puntos_carroceria = [
        (x, y), (x+80, y), (x+110, y+20), (x+130, y+20), 
        (x+140, y+40), (x+140, y+50), (x, y+50)
    ]
    pygame.draw.polygon(pantalla, ROJO, puntos_carroceria)
    pygame.draw.polygon(pantalla, BLANCO, puntos_carroceria, 2)
    
    # Ruedas
    pygame.draw.circle(pantalla, NEGRO, (x+30, y+50), 16)
    pygame.draw.circle(pantalla, GRIS_CLARO, (x+30, y+50), 16, 3)
    pygame.draw.circle(pantalla, NEGRO, (x+110, y+50), 16)
    pygame.draw.circle(pantalla, GRIS_CLARO, (x+110, y+50), 16, 3)

    # Ventana
    pygame.draw.polygon(pantalla, NEGRO, [(x+50, y+5), (x+80, y+5), (x+100, y+20), (x+50, y+20)])
    pygame.draw.polygon(pantalla, CYAN, [(x+50, y+5), (x+80, y+5), (x+100, y+20), (x+50, y+20)], 1)

def dibujar_telemetria(pantalla, fuente_grande, fuente_peq, coche):
    # PANEL SUPERIOR IZQUIERDO: Velocidad y Marcha
    vel_kmh = coche.v * 3.6
    pantalla.blit(fuente_grande.render(f"{int(vel_kmh)} KM/H", True, BLANCO), (30, 30))
    pantalla.blit(fuente_grande.render(f"MARCHA: {coche.marcha}", True, CYAN), (30, 80))

    # PANEL CENTRAL: Tacómetro (Barra RPM)
    pygame.draw.rect(pantalla, GRIS, (300, 60, 600, 30))
    ancho_rpm = (min(coche.rpm, 8500) / 8500) * 600
    
    color_rpm = VERDE_NEON = (50, 255, 50)
    if coche.rpm > 7000: color_rpm = AMARILLO
    if coche.rpm > 8200: color_rpm = ROJO
    
    pygame.draw.rect(pantalla, color_rpm, (300, 60, ancho_rpm, 30))
    pygame.draw.rect(pantalla, BLANCO, (300, 60, 600, 30), 2)
    
    pantalla.blit(fuente_peq.render(f"RPM: {int(coche.rpm)}", True, BLANCO), (300, 35))

    # PANEL DERECHO: Telemetría Física
    x_tel = 950
    pantalla.blit(fuente_peq.render("DATOS FÍSICOS:", True, CYAN), (x_tel, 30))
    pantalla.blit(fuente_peq.render(f"Par Motor: {coche.par_motor_actual:.1f} Nm", True, BLANCO), (x_tel, 60))
    pantalla.blit(fuente_peq.render(f"F. Arrastre: {coche.fuerza_drag:.1f} N", True, BLANCO), (x_tel, 90))
    pantalla.blit(fuente_peq.render(f"Aceleración: {coche.aceleracion_actual:.2f} m/s²", True, BLANCO), (x_tel, 120))
    pantalla.blit(fuente_peq.render(f"Distancia: {coche.x:.1f} m", True, BLANCO), (x_tel, 150))

# =========================================================
# BUCLE PRINCIPAL
# =========================================================
def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Simulador Físico Dinámico - Ferrari F430")
    reloj = pygame.time.Clock()
    
    fuente_grande = pygame.font.SysFont("courier", 36, bold=True)
    fuente_peq = pygame.font.SysFont("courier", 18, bold=True)

    coche = CocheSimulador()
    offset_fondo = 0

    corriendo = True
    while corriendo:
        dt = reloj.tick(FPS) / 1000.0

        # EVENTOS
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RIGHT:
                    coche.cambiar_marcha(subir=True)
                elif evento.key == pygame.K_LEFT:
                    coche.cambiar_marcha(subir=False)
                elif evento.key == pygame.K_r:
                    coche = CocheSimulador() # Reiniciar simulación

        # CONTROLES CONTÍNUOS
        teclas = pygame.key.get_pressed()
        coche.acelerando = teclas[pygame.K_UP]
        coche.frenando = teclas[pygame.K_DOWN]

        # FÍSICA
        coche.actualizar(dt)

        # RENDERIZADO VISUAL
        pantalla.fill(NEGRO)
        
        # Efecto de movimiento del suelo
        offset_fondo = (offset_fondo + coche.v * 3) % 100
        pygame.draw.rect(pantalla, (25, 25, 30), (0, ALTO - 200, ANCHO, 200))
        pygame.draw.line(pantalla, GRIS_CLARO, (0, ALTO - 200), (ANCHO, ALTO - 200), 4)
        
        for i in range(-100, ANCHO + 100, 100):
            x_linea = i - offset_fondo
            pygame.draw.rect(pantalla, BLANCO, (x_linea, ALTO - 100, 40, 6))

        # Dibujar coche y UI
        dibujar_coche_vectorial(pantalla, 150, ALTO - 170)
        dibujar_telemetria(pantalla, fuente_grande, fuente_peq, coche)

        # Controles
        txt_controles = "[ARRIBA] Acelerar | [ABAJO] Frenar | [DERECHA] Subir Marcha | [IZQUIERDA] Bajar Marcha | [R] Reset"
        pantalla.blit(fuente_peq.render(txt_controles, True, GRIS_CLARO), (30, ALTO - 40))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()