import pygame
import pymunk
import pymunk.pygame_util
import math

# Configuración de la ventana
WIDTH, HEIGHT = 1000, 600
FPS = 60
NIVEL_DEL_SUELO = HEIGHT - 60 # PIXELES 

# Escala
PX_M = 5 # 5px por metro (Ancho de pantalla = 200m)
M_PX = 1.0 / PX_M

# Parámetros Base
RADIO_M = 0.02134  # 2.134 cm (Diapositiva 8)
HOYO_M = 181.6     # coordenada X del hoyo en metros

def run():
    # 1. Inicializar Pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    # 2. Cargar y ajustar imagen de fondo
    try:
        bg_image = pygame.image.load("Videojuegos\\Tema 6\\calle_golf.png").convert_alpha()
        bg_width, bg_height = bg_image.get_size()
        bg_width *= 0.7
        bg_height *= 0.6
        aspect_ratio = bg_height / bg_width
        new_height = int(WIDTH * aspect_ratio)
        bg_image = pygame.transform.scale(bg_image, (WIDTH, new_height))
        bg_pos = (0, HEIGHT - new_height)
    except pygame.error:
        print("No se pudo cargar la imagen. Se usará fondo color cielo.")
        bg_image = None

    # 3. Inicializar Pymunk (Espacio físico)
    space = pymunk.Space()
    # Gravedad de la Tierra escalada a nuestros píxeles (9.81 * 5 = 49.05 px/s^2)
    space.gravity = (0, 9.81 * PX_M)  
    # Arrastre aerodinámico (Diapositiva 9) para evitar que vuele fuera de la pantalla
    space.damping = 0.97 
 
    # Suelo (Césped general) - Diapositiva 9: Fricción alta (1.5 - 2) y restitución de 0.25
    static_body = space.static_body
    floor_1 = pymunk.Segment(static_body, (0, NIVEL_DEL_SUELO), (HOYO_M * PX_M - RADIO_M * PX_M * 220, NIVEL_DEL_SUELO), 0)
    floor_1.friction = 1.8
    floor_1.elasticity = 0.05
    space.add(floor_1)
 
    floor2 = pymunk.Segment(static_body, (HOYO_M * PX_M + RADIO_M * PX_M * 220, NIVEL_DEL_SUELO), (WIDTH, NIVEL_DEL_SUELO), 0)
    floor2.friction = 1.8
    floor2.elasticity = 0.05
    space.add(floor2)
 
    # La Bola - Diapositiva 8
    m_b = 0.04593 # 45.93 g
    radio_fisico = RADIO_M * PX_M * 30 # Escalado para que colisione y se vea adecuadamente
    moment = (2 / 5) * m_b * (radio_fisico ** 2)
    
    body = pymunk.Body(m_b, moment)
    y_inicial = NIVEL_DEL_SUELO - radio_fisico - 1
    x_inicial = 50
    body.position = (x_inicial, y_inicial)
    body.velocity = (0, 0) # Inicia quieta
    
    shape = pymunk.Circle(body, radio_fisico)
    shape.friction = 0.7     # Diapositiva 8: friction=0.7
    shape.elasticity = 0.91  # Diapositiva 8: elasticity=0.91 (USGA)
    space.add(body, shape)

    # Valores Promedio para el impacto
    m_c = 0.550 # Masa efectiva de la cabeza del palo (250g) + brazo (300g)
    v_cx = 30   # Velocidad intermedia amateur/pro (m/s)
    e = 0.83    # Coeficiente de restitución real para la fórmula matemática
    loft_deg = 31 # Loft de un Hierro 6 (Diapositiva 7)
    loft_rad = math.radians(loft_deg)

    # 4. Bucle principal de simulación
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            # Detectar pulsación del ESPACIO para golpear la bola
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Fórmula de velocidad post-impacto v'_bp (Diapositiva 6)
                    v_bp = ((1 + e) * m_c / (m_b + m_c)) * v_cx * math.cos(loft_rad)
                    
                    # Descomposición de la velocidad usando el ángulo de loft
                    # Multiplicamos por PX_M para convertir metros/seg a píxeles/seg
                    v_x = v_bp * math.cos(loft_rad) * PX_M
                    v_y = -v_bp * math.sin(loft_rad) * PX_M # Negativo porque el eje Y crece hacia abajo
                    
                    # Asignamos la nueva velocidad
                    body.velocity = (v_x, v_y)

        # Limpiar pantalla
        screen.fill((135, 206, 235))

        # Dibujar fondo si existe
        if bg_image:
            screen.blit(bg_image, bg_pos)

        # Paso de tiempo de la física (fijo para estabilidad)
        dt = 1.0 / FPS
        space.step(dt)

        # Dibujar debug de Pymunk (líneas de físicas)
        space.debug_draw(draw_options)

        # Dibujar de forma manual la bola blanca dinámica que sigue al cuerpo de pymunk
        pos_x, pos_y = int(body.position.x), int(body.position.y)
        pygame.draw.circle(screen, (255, 255, 255), (pos_x, pos_y), int(radio_fisico))
        
        # Dibujar el Hoyo (negro en el suelo para diferenciarlo)
        pygame.draw.circle(screen, (0, 0, 0), (int(HOYO_M * PX_M), int(NIVEL_DEL_SUELO)), int(radio_fisico))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    run()