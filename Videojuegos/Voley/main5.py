import pygame
import pymunk
from pymunk import Vec2d
import math
import os

# --- CONFIGURACIÓN PRINCIPAL ---
WIDTH, HEIGHT = 1150, 650
SUELO_Y = 550
PX_M = 60          # 60 píxeles por cada metro
FPS = 60
SUBSTEPS = 10      # Pasos físicos por cada frame
VEL_SIMULACION = 0.9

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Simulación Voleibol - Estilo Apuntes")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 22, bold=True)

    # =================================================================
    # 1. ESPACIO Y FÍSICA
    # =================================================================
    space = pymunk.Space()
    space.gravity = (0, 9.81 * PX_M) # Gravedad hacia ABAJO (Y positivo)

    # --- Suelo ---
    suelo = pymunk.Segment(space.static_body, (0, SUELO_Y), (WIDTH * 2, SUELO_Y), 5)
    suelo.elasticity = 0.8
    suelo.friction = 0.6
    suelo.collision_type = 1
    space.add(suelo)

    # --- Red ---
    x_red = 9.0 * PX_M
    h_red = 2.43 * PX_M
    red = pymunk.Segment(space.static_body, (x_red, SUELO_Y), (x_red, SUELO_Y - h_red), 4)
    red.elasticity = 0.3
    red.friction = 0.5
    space.add(red)

    # --- Balón ---
    radio_m = 0.105
    radio_px = radio_m * PX_M
    masa = 0.270
    moment = pymunk.moment_for_circle(masa, 0, radio_px)
    
    balon = pymunk.Body(masa, moment)
    pos_inicio = (1.5 * PX_M, SUELO_Y - 3.1 * PX_M)
    balon.position = pos_inicio
    
    forma_balon = pymunk.Circle(balon, radio_px)
    forma_balon.elasticity = 0.85
    forma_balon.friction = 0.6
    forma_balon.collision_type = 2
    space.add(balon, forma_balon)

    # =================================================================
    # 2. VARIABLES DE ESTADO Y LÓGICA (AERODINÁMICA Y CHOQUES)
    # =================================================================
    estado = {
        "lanzado": False,
        "magnus_activo": True,
        "ha_tocado_suelo": False,
        "distancia_impacto": None
    }

    # Función personalizada para aplicar Aerodinámica al balón
    def aerodinamica(body, gravity, damping, dt):
        if not estado["lanzado"]:
            body.velocity = (0, 0)
            body.angular_velocity = 0
            return

        # 1. Aplicamos Gravedad Base
        pymunk.Body.update_velocity(body, gravity, damping, dt)
        
        # 2. Extraemos velocidades y convertimos a m/s
        v_px = body.velocity
        v_m = Vec2d(v_px.x, -v_px.y) / PX_M  # Invertimos Y para las mates clásicas
        v_mag = v_m.length

        if v_mag > 0.1:
            rho = 1.225 
            A = math.pi * (radio_m ** 2)
            
            # --- DRAG ---
            Cd = 0.44 
            f_drag_m = -0.5 * rho * Cd * A * v_mag * v_m
            
            # --- MAGNUS ---
            f_magnus_m = Vec2d(0, 0)
            if estado["magnus_activo"]:
                omega = body.angular_velocity
                if omega != 0:
                    S_param = (radio_m * abs(omega)) / v_mag
                    Cm = (0.6 * S_param) / (2.0 + S_param) 
                    
                    # Regla mano derecha: Topspin (w < 0) empuja hacia abajo (-Y_matemática)
                    if omega < 0:
                        dir_magnus = Vec2d(v_m.y, -v_m.x).normalized()
                    else: 
                        dir_magnus = Vec2d(-v_m.y, v_m.x).normalized()
                        
                    f_magnus_m = dir_magnus * (0.5 * rho * Cm * A * (v_mag**2))

            # --- APLICACIÓN ---
            f_total_m = f_drag_m + f_magnus_m
            acc_m = f_total_m / masa
            acc_px = Vec2d(acc_m.x, -acc_m.y) * PX_M # Convertimos aceleración a píxeles
            body.velocity += acc_px * dt

    balon.velocity_func = aerodinamica

    # Handler para el choque perfecto (Estilo billar_taco.py)
    def al_tocar_suelo(arbiter, space, data):
        if estado["lanzado"] and not estado["ha_tocado_suelo"]:
            estado["ha_tocado_suelo"] = True
            estado["distancia_impacto"] = balon.position.x / PX_M
        return True
    
    space.on_collision(1, 2, begin=al_tocar_suelo)

    # =================================================================
    # 3. PREPARACIÓN DE GRÁFICOS
    # =================================================================
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    
    imgs_oikawa = {}
    
    # ATENCIÓN: Si tus imágenes originales eran .jpg, cambia aquí los nombres
    # a "oikawa1.jpg" y "oikawa2.jpg"
    nombres_imagenes = ["oikawa1.png", "oikawa2.png"] 
    
    for nombre in nombres_imagenes:
        ruta_completa = os.path.join(directorio_actual, nombre)
        try:
            img = pygame.image.load(ruta_completa).convert_alpha()
            
            
            img = pygame.transform.flip(img, True, False) # Rotación espejo
            p_height = int(3.0 * PX_M) 
            ratio = img.get_width() / img.get_height()
            imgs_oikawa[nombre] = pygame.transform.smoothscale(img, (int(p_height * ratio), p_height))
        except Exception as e:
            print(f"❌ ERROR AL CARGAR LA IMAGEN '{nombre}': {e}")
            imgs_oikawa[nombre] = None

    # Superficie para el balón aumentado visualmente
    factor_visual = 1.5
    r_vis = int(radio_px * factor_visual)
    diam = r_vis * 2
    img_balon = pygame.Surface((diam, diam), pygame.SRCALPHA)
    pygame.draw.circle(img_balon, (255, 220, 50), (r_vis, r_vis), r_vis)
    pygame.draw.arc(img_balon, (0, 50, 200), (0, 0, diam, diam), 0, math.pi, 3)
    pygame.draw.arc(img_balon, (0, 50, 200), (0, 0, diam, diam), math.pi/2, 3*math.pi/2, 3)

    # =================================================================
    # 4. BUCLE PRINCIPAL
    # =================================================================
    dt_fisica = (1.0 / FPS / SUBSTEPS) * VEL_SIMULACION
    running = True

    while running:
        # --- EVENTOS ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not estado["lanzado"]:
                        v_ms = 20.0
                        ang_rad = math.radians(6.0)
                        # Cálculo de velocidad (eje Y se invierte porque Pygame crece hacia abajo)
                        vx = v_ms * math.cos(ang_rad) * PX_M
                        vy = -v_ms * math.sin(ang_rad) * PX_M
                        
                        balon.velocity = (vx, vy)
                        balon.angular_velocity = -60.0 # Topspin intenso
                        estado["lanzado"] = True
                        
                if event.key == pygame.K_ESCAPE:
                    estado["lanzado"] = False
                    estado["ha_tocado_suelo"] = False
                    estado["distancia_impacto"] = None
                    balon.position = pos_inicio
                    balon.velocity = (0, 0)
                    balon.angular_velocity = 0
                    
                if event.key == pygame.K_m:
                    estado["magnus_activo"] = not estado["magnus_activo"]

        # --- FÍSICA ---
        for _ in range(SUBSTEPS):
            space.step(dt_fisica)

        # --- DIBUJADO ---
        screen.fill((200, 220, 240))
        
        # Pista y marcas
        pygame.draw.rect(screen, (220, 140, 80), (0, SUELO_Y, WIDTH, HEIGHT - SUELO_Y))
        pygame.draw.line(screen, (255, 255, 255), (0, SUELO_Y), (WIDTH, SUELO_Y), 5)
        for x_m in [0, 9, 18]:
            pygame.draw.line(screen, (255, 255, 255), (int(x_m * PX_M), SUELO_Y), (int(x_m * PX_M), SUELO_Y + 10), 4)

        # Poste y red
        pygame.draw.line(screen, (150, 150, 150), (x_red, SUELO_Y), (x_red, SUELO_Y - h_red), 8)
        pygame.draw.line(screen, (255, 255, 255), (x_red, SUELO_Y - h_red + 60), (x_red, SUELO_Y - h_red), 4)

        # Jugador
        clave_img = "oikawa2.png" if estado["lanzado"] else "oikawa1.png"
        if imgs_oikawa[clave_img]:
            x_jug = int(0.7 * PX_M)
            y_jug = int(SUELO_Y - (2 * PX_M))
            if estado["lanzado"]:
                x_jug += int(0.5 * PX_M)
                y_jug += int(0.3 * PX_M)
            rect_jug = imgs_oikawa[clave_img].get_rect(center=(x_jug, y_jug))
            screen.blit(imgs_oikawa[clave_img], rect_jug)
        else:
            pygame.draw.rect(screen, (0, 150, 150), (int(0.7 * PX_M) - 20, int(SUELO_Y - 2 * PX_M), 40, 80))

        # Balón
        angulo_deg = math.degrees(-balon.angle)
        img_rotada = pygame.transform.rotate(img_balon, angulo_deg)
        rect_balon = img_rotada.get_rect(center=(int(balon.position.x), int(balon.position.y)))
        screen.blit(img_rotada, rect_balon)

        # Marca de impacto en el suelo
        if estado["distancia_impacto"] is not None:
            x_px = int(estado["distancia_impacto"] * PX_M)
            pygame.draw.circle(screen, (220, 30, 30), (x_px, SUELO_Y), 6)
            pygame.draw.circle(screen, (255, 255, 255), (x_px, SUELO_Y), 3)

        # --- TEXTOS / UI ---
        vel_kmh = (balon.velocity.length / PX_M) * 3.6
        rpm = abs(balon.angular_velocity * 9.5493)
        
        screen.blit(font.render("ESPACIO: Sacar | ESC: Reset | M: Efecto Magnus", True, (100, 100, 100)), (20, 20))
        screen.blit(font.render(f"Velocidad: {vel_kmh:.1f} km/h", True, (30, 30, 30)), (WIDTH - 250, 20))
        screen.blit(font.render(f"Topspin: {rpm:.0f} RPM", True, (30, 30, 30)), (WIDTH - 250, 50))
        
        color_mag = (0, 150, 0) if estado["magnus_activo"] else (200, 0, 0)
        screen.blit(font.render(f"Magnus: {'SÍ' if estado['magnus_activo'] else 'NO'}", True, color_mag), (WIDTH - 250, 80))
        
        if estado["distancia_impacto"] is not None:
            screen.blit(font.render(f"Cayó a: {estado['distancia_impacto']:.2f} m", True, (200, 50, 50)), (WIDTH - 250, 110))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        pygame.quit()