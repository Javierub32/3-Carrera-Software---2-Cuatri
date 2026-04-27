import pygame
import pymunk

PX_M = 5 # 5px por metro (PX/M)
M_PX = 1.0 / PX_M

def crearCirculo(space, masa=0.5, radio=5, friction=-99, elasticity=-99, posX=1, posY=1, velX=0, velY=0):
    """Crea un círculo dinámico en Pymunk."""
    radioF = radio * PX_M
    momento = pymunk.moment_for_circle(masa, 0, radioF)

    body = pymunk.Body(masa, momento)
    body.position = (posX, posY)
    body.velocity = (velX, velY)

    shape = pymunk.Circle(body, radioF)
    if friction != -99: shape.friction = friction
    if elasticity != -99: shape.elasticity = elasticity
    
    space.add(body, shape)
    return body, shape

def crearCaja(space, masa=1.0, ancho=10, alto=10, friction=-99, elasticity=-99, posX=0, posY=0):
    """Crea un rectángulo/caja dinámico en Pymunk."""
    ancho_px, alto_px = ancho * PX_M, alto * PX_M
    momento = pymunk.moment_for_box(masa, (ancho_px, alto_px))
    
    body = pymunk.Body(masa, momento)
    body.position = (posX, posY)
    
    shape = pymunk.Poly.create_box(body, (ancho_px, alto_px))
    if friction != -99: shape.friction = friction
    if elasticity != -99: shape.elasticity = elasticity
    
    space.add(body, shape)
    return body, shape

def crearSuelo(space, p1, p2, grosor=5, friction=-99, elasticity=-99):
    """Crea un segmento estático (Suelo o pared)."""
    suelo = pymunk.Segment(space.static_body, p1, p2, grosor)
    if friction != -99: suelo.friction = friction
    if elasticity != -99: suelo.elasticity = elasticity
    space.add(suelo)
    return suelo

def dibujarTextos(pantalla, textos):
    """
    Muestra por pantalla un array de datos.
    Ejemplo de cómo se deben ingresar los datos:
    
    textos = [
        (f"Tiempo total: {tiempo:.2f} s", (0, 0, 0)),
        (f"Velocidad (v): {v_actual:.2f} px/s", (0, 0, 0)),
        (f"Vel Angular (w): {w_actual:.2f} rad/s", (0, 0, 0)),
        (f"Estado: {estado}", (255, 0, 0) if estado == "Deslizamiento" else (0, 150, 0)),
        (f"Tiempo deslizamiento: {tiempo_des:.2f} s", (100, 100, 100))
    ]
    """
    fuente = pygame.font.SysFont("Arial", 20)

    for i, (texto, color) in enumerate(textos):
        img = fuente.render(texto, True, color) 
        pantalla.blit(img, (20, 20 + i * 25))