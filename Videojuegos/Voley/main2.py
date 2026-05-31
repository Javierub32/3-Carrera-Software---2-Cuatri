import pygame
import pymunk
import pymunk.pygame_util
import math
import os
from pymunk import Vec2d

class Tsim:
    # --- CAMBIO: Ventana más pequeña (1150x650) y suelo ajustado ---
    def __init__(self, width=1150, height=650, suelo=550, PX_M=60, gravedad=(0, -9.81), fondo=None):
        self.width = width
        self.height = height
        self.PX_M = PX_M
        self.M_PX = 1.0 / PX_M
        self.suelo = suelo
        
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Simulación Voleibol - Oikawa Jump Serve")
        self.clock = pygame.time.Clock()
        self.asset_dir = os.path.dirname(os.path.abspath(__file__))
        
        if fondo != None:
            self.fondo = self.pone_fondo(fondo)
        else:
            self.fondo = None    
            
        self.space = pymunk.Space()
        self.space.gravity = Vec2d(gravedad[0], -gravedad[1]) * PX_M
        self.space.iterations = 35 
        
        self._eventos_teclado = {}
        self.running = True
        self.font = pygame.font.SysFont("Arial", 22, bold=True) # Fuente un poco más pequeña
        
    def resolver_asset_path(self, ruta):
        if ruta is None: return None
        if os.path.isabs(ruta): return ruta
        return os.path.join(self.asset_dir, ruta)

    def pone_fondo(self, imagen):
        try:
            fondo = pygame.image.load(self.resolver_asset_path(imagen)).convert()
            return pygame.transform.smoothscale(fondo, (self.width, self.height))
        except:
            return None    
        
    def draw(self):
        if self.fondo: self.screen.blit(self.fondo, (0, 0))
        else: self.screen.fill((200, 220, 240))    
        
    def add_evento_tecla(self, tecla, funcion, activo=True):
        self._eventos_teclado[tecla] = {'func': funcion, 'activo': activo}

    def actualizar_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return False
            if event.type == pygame.KEYDOWN:
                if event.key in self._eventos_teclado:
                    evento = self._eventos_teclado[event.key]
                    if evento['activo']:
                        evento['func']()                            
        return True

###############################################################################################
class Tobjeto:
    def __init__(self, sim):
        self.sim = sim

    def _m_a_px(self, pos_m):
        x_px = pos_m[0] * self.sim.PX_M
        y_px = self.sim.suelo - (pos_m[1] * self.sim.PX_M)
        return Vec2d(x_px, y_px)

    def _px_a_m(self, pos_px):
        x_m = pos_px[0] / self.sim.PX_M
        y_m = (self.sim.suelo - pos_px[1]) / self.sim.PX_M
        return Vec2d(x_m, y_m)

    @property
    def posicion(self):
        return self._px_a_m(self.body.position)

    @posicion.setter
    def posicion(self, pos_m):
        self.body.position = self._m_a_px(pos_m)

    @property
    def velocidad(self):
        v = self.body.velocity / self.sim.PX_M
        return Vec2d(v.x, -v.y)

    @velocidad.setter
    def velocidad(self, vel_m):
        vx = vel_m[0] * self.sim.PX_M
        vy = -vel_m[1] * self.sim.PX_M
        self.body.velocity = (vx, vy)
        
    def draw(self): pass
    def update(self): pass

#############################################################################################
class Tsuelo(Tobjeto):
    def __init__(self, sim):
        super().__init__(sim)
        self.body = self.sim.space.static_body
        self.p1 = Vec2d(0, self.sim.suelo)
        self.p2 = Vec2d(self.sim.width, self.sim.suelo)
        self.shape = pymunk.Segment(self.body, self.p1, self.p2, 5)
        self.shape.elasticity = 0.8
        self.shape.friction = 0.6
        self.sim.space.add(self.shape)
        
    def draw(self):
        pygame.draw.rect(self.sim.screen, (220, 140, 80), (0, self.sim.suelo, self.sim.width, self.sim.height - self.sim.suelo))
        pygame.draw.line(self.sim.screen, (255, 255, 255), self.p1, self.p2, 5)
        for x_m in [0, 9, 18]:
            x_px = int(x_m * self.sim.PX_M)
            pygame.draw.line(self.sim.screen, (255, 255, 255), (x_px, self.sim.suelo), (x_px, self.sim.suelo+10), 4)

###############################################################################################
class TRedVoley(Tobjeto):
    def __init__(self, sim, x_red_m=9.0):
        super().__init__(sim)
        self.x_px = int(x_red_m * self.sim.PX_M)
        self.y_base_px = self.sim.suelo
        self.altura_px = int(2.43 * self.sim.PX_M) 
        self.y_top_px = self.sim.suelo - self.altura_px
        
        self.body = self.sim.space.static_body
        self.shape = pymunk.Segment(self.body, (self.x_px, self.y_base_px), (self.x_px, self.y_top_px), 4)
        self.shape.elasticity = 0.3
        self.shape.friction = 0.5
        self.sim.space.add(self.shape)

    def draw(self):
        pygame.draw.line(self.sim.screen, (150, 150, 150), (self.x_px, self.y_base_px), (self.x_px, self.y_top_px), 8)
        y_red_bottom = self.y_top_px + int(1.0 * self.sim.PX_M)
        pygame.draw.line(self.sim.screen, (255, 255, 255), (self.x_px, y_red_bottom), (self.x_px, self.y_top_px), 4)
        pygame.draw.rect(self.sim.screen, (250, 250, 250), (self.x_px-5, self.y_top_px, 10, 8))

###############################################################################################
class TbalonVoley(Tobjeto):
    def __init__(self, sim, pos_m):
        super().__init__(sim)
        self.masa = 0.270      
        self.radio_m = 0.105   
        self.radio_px = self.radio_m * self.sim.PX_M
        
        moment = pymunk.moment_for_circle(self.masa, 0, self.radio_px)
        self.body = pymunk.Body(self.masa, moment)
        self.posicion = pos_m 
        
        self.shape = pymunk.Circle(self.body, self.radio_px)
        self.shape.elasticity = 0.85
        self.shape.friction = 0.6
        self.sim.space.add(self.body, self.shape)
        
        self.body.velocity_func = self.aplicar_aerodinamica
        self.img_base = self._preparar_imagen()

    def aplicar_aerodinamica(self, body, gravity, damping, dt):
        if hasattr(self.sim, 'lanzado') and not self.sim.lanzado:
            body.velocity = (0, 0)
            body.angular_velocity = 0
            return

        pymunk.Body.update_velocity(body, gravity, damping, dt)
        
        v_m = Vec2d(body.velocity.x, -body.velocity.y) / self.sim.PX_M
        v_mag = v_m.length

        if v_mag > 0:
            rho = 1.225 
            A = math.pi * (self.radio_m ** 2)
            
            Cd = 0.44 
            f_drag_m = -0.5 * rho * Cd * A * v_mag * v_m
            
            f_magnus_m = Vec2d(0, 0)
            if self.sim.magnus_activo:
                omega = body.angular_velocity
                if omega != 0:
                    S_param = (self.radio_m * abs(omega)) / v_mag
                    k_volley = 0.6
                    Cm = (k_volley * S_param) / (2.0 + S_param) 
                    
                    if omega < 0:
                        dir_magnus = Vec2d(v_m.y, -v_m.x).normalized()
                    else: 
                        dir_magnus = Vec2d(-v_m.y, v_m.x).normalized()
                        
                    f_magnus_scalar = 0.5 * rho * (v_mag**2) * Cm * A
                    f_magnus_m = dir_magnus * f_magnus_scalar

            f_total_m = f_drag_m + f_magnus_m
            aceleracion_m = f_total_m / self.masa
            
            acc_px = Vec2d(aceleracion_m.x, -aceleracion_m.y) * self.sim.PX_M
            body.velocity += acc_px * dt

    def _preparar_imagen(self):
        diametro = int(self.radio_px * 2)
        surf = pygame.Surface((diametro, diametro), pygame.SRCALPHA)
        pygame.draw.circle(surf, (255, 220, 50), (int(self.radio_px), int(self.radio_px)), int(self.radio_px))
        pygame.draw.arc(surf, (0, 50, 200), (0, 0, diametro, diametro), 0, math.pi, 6)
        pygame.draw.arc(surf, (0, 50, 200), (0, 0, diametro, diametro), math.pi/2, 3*math.pi/2, 6)
        return surf

    def draw(self):
        angulo_deg = math.degrees(-self.body.angle)
        img_rotada = pygame.transform.rotate(self.img_base, angulo_deg)
        pos = self.body.position
        rect = img_rotada.get_rect(center=(int(pos.x), int(pos.y)))
        self.sim.screen.blit(img_rotada, rect)

    def lanzar(self, v_ms, angulo_deg, omega=0):  
        rad = math.radians(angulo_deg)
        vx_m = v_ms * math.cos(rad)
        vy_m = v_ms * math.sin(rad)
        
        self.velocidad = (vx_m, vy_m)
        self.body.angular_velocity = omega

##############################################################################
class TjugadorVoley(Tobjeto):
    def __init__(self, sim):
        super().__init__(sim)
        self.player_imgs = {}
        
        # --- CAMBIO: Carga de imágenes de Oikawa con transparencia ---
        nombres = ["oikawa1.png", "oikawa2.png"]
        
        for name in nombres:
            try:
                img = pygame.image.load(self.sim.resolver_asset_path(name)).convert_alpha()
                
                img = pygame.transform.flip(img, True, False)
                
                # Ajustamos la altura de Oikawa para que concuerde con la escala
                p_height = int(3.0 * self.sim.PX_M) 
                ratio = img.get_width() / img.get_height()
                self.player_imgs[name] = pygame.transform.smoothscale(img, (int(p_height * ratio), p_height))
            except Exception as e:
                print(f"No se pudo cargar la imagen {name}. Asegúrate de que esté en la misma carpeta.")
                self.player_imgs[name] = None
                
    def draw(self):
        # Elegir la imagen dependiendo de si ya se ha golpeado el balón
        img_key = "oikawa2.png" if self.sim.lanzado else "oikawa1.png"
        
        # Posición base en pantalla para que la mano cuadre con el inicio del balón (1.5, 3.2)
        x_px = int(0.7 * self.sim.PX_M) 
        y_px = int(self.sim.suelo - (2 * self.sim.PX_M))
        
        # Cuando saca, movemos ligeramente el dibujo hacia adelante para dar efecto de golpeo
        if self.sim.lanzado:
            x_px += int(0.5 * self.sim.PX_M)
            y_px += int(0.3 * self.sim.PX_M)
        
        if self.player_imgs[img_key]:
            rect = self.player_imgs[img_key].get_rect(center=(x_px, y_px))
            self.sim.screen.blit(self.player_imgs[img_key], rect)
        else:
            pygame.draw.rect(self.sim.screen, (0,150,150), (x_px-20, y_px, 40, 80))

##############################################################################
class TVoley(Tsim):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pos_inicio_balon = (1.5, 3.1) # Posición en la mano de Oikawa
        self.lanzado = False 
        self.magnus_activo = True
        
        # Parámetros del Jump Serve de Oikawa
        self.v_lanzamiento = 10.0    # m/s (~90 km/h)
        self.ang_lanzamiento = 6.0   
        self.w_lanzamiento = -55.0   # Topspin fuerte
        
        self.objetos = []
        
        self.objetos.append(Tsuelo(self))
        self.objetos.append(TRedVoley(self, x_red_m=9.0))
        
        self.jugador = TjugadorVoley(self)
        self.objetos.append(self.jugador)
        
        self.balon = TbalonVoley(self, self.pos_inicio_balon)
        self.objetos.append(self.balon)
        
        self.add_evento_tecla(pygame.K_SPACE, self.ejecutar_saque)
        self.add_evento_tecla(pygame.K_ESCAPE, self.resetear)
        self.add_evento_tecla(pygame.K_m, self.toggle_magnus)

    def ejecutar_saque(self):
        if not self.lanzado:
            self.balon.lanzar(self.v_lanzamiento, self.ang_lanzamiento, self.w_lanzamiento)
            self.lanzado = True

    def toggle_magnus(self):
        self.magnus_activo = not self.magnus_activo

    def resetear(self):
        self.lanzado = False
        self.balon.posicion = self.pos_inicio_balon
        self.balon.body.velocity = (0, 0)
        self.balon.body.angular_velocity = 0

    def draw(self):
        super().draw() 
        for obj in self.objetos:
            obj.draw()
            
        vel_m = self.balon.velocidad.length
        rpm = abs(self.balon.body.angular_velocity * 9.5493)
        
        txt_vel = self.font.render(f"Velocidad: {vel_m*3.6:.1f} km/h", True, (30, 30, 30))
        txt_rpm = self.font.render(f"Topspin: {rpm:.0f} RPM", True, (30, 30, 30))
        
        color_mag = (0, 150, 0) if self.magnus_activo else (200, 0, 0)
        txt_mag = self.font.render(f"Efecto Magnus (M): {'SÍ' if self.magnus_activo else 'NO'}", True, color_mag)
        txt_info = self.font.render("ESPACIO = Remate | ESC = Reiniciar | M = Quitar Magnus", True, (100, 100, 100))

        # Reubicado para adaptarse a la pantalla más pequeña
        self.screen.blit(txt_vel, (self.width - 250, 20))
        self.screen.blit(txt_rpm, (self.width - 250, 50))
        self.screen.blit(txt_mag, (self.width - 250, 80))
        self.screen.blit(txt_info, (20, 20))
            
    def update(self):
        for obj in self.objetos:
            if hasattr(obj, 'update'):
                obj.update()

###############################################################################################
if __name__ == "__main__":
    # --- CAMBIO: Iniciamos con la ventana reducida (1150x650) ---
    sim_voley = TVoley() 

    FPS = 60
    substeps = 10
    dt = 1.0 / FPS / substeps

    while sim_voley.actualizar_eventos():
        sim_voley.update()
        for _ in range(substeps):
            sim_voley.space.step(dt)
            
        sim_voley.draw()
        pygame.display.flip()
        sim_voley.clock.tick(FPS)

    pygame.quit()