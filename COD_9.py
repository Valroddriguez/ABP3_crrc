import pygame, random, sys, time

pygame.init()
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
reloj = pygame.time.Clock()
sonido = pygame.mixer.Sound("pop.wav")

COLORES = [(255,200,200), (255,255,150), (200,255,200), (200,200,255), (230,200,255)]
COLOR_BOTON, COLOR_BOTON_HOVER, COLOR_TEXTO = (180,180,180), (220,220,220), (0,0,0)
fuente_botones = pygame.font.SysFont(None, 32)

class Boton:
    def __init__(self, x, y, w, h, texto):
        self.rect = pygame.Rect(x, y, w, h)
        self.texto = texto
    def dibujar(self, surf):
        color = COLOR_BOTON_HOVER if self.rect.collidepoint(pygame.mouse.get_pos()) else COLOR_BOTON
        pygame.draw.rect(surf, color, self.rect)
        txt = fuente_botones.render(self.texto, True, COLOR_TEXTO)
        surf.blit(txt, txt.get_rect(center=self.rect.center))
    def clickeado(self, e): return e.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(e.pos)

class Pelota:
    def __init__(self):
        self.radio = random.randint(20, 40)
        self.x = random.randint(self.radio, ANCHO - self.radio)
        self.y = random.randint(self.radio, ALTO - self.radio)
        self.vx = random.choice([-1,1]) * random.randint(1,4)
        self.vy = random.choice([-1,1]) * random.randint(1,4)
        self.color = random.choice(COLORES)
        self.last_sound_time = 0
    def mover(self):
        self.x += self.vx
        self.y += self.vy
        ahora = time.time()
        rebote = False
        if self.x - self.radio < 0 or self.x + self.radio > ANCHO:
            self.vx *= -1; rebote = True
        if self.y - self.radio < 0 or self.y + self.radio > ALTO:
            self.vy *= -1; rebote = True
        if rebote and ahora - self.last_sound_time > 0.1:
            sonido.play(); self.last_sound_time = ahora
    def dibujar(self):
        sombra = tuple(max(c - 40, 0) for c in self.color)
        pygame.draw.circle(pantalla, sombra, (int(self.x)+3, int(self.y)+3), self.radio)
        pygame.draw.circle(pantalla, self.color, (int(self.x), int(self.y)), self.radio)

pelotas = [Pelota() for _ in range(10)]
last_collision = 0
pausado = False
boton_pausa = Boton(20, 20, 160, 40, "Pausar / Reanudar (P)")
boton_salir = Boton(200, 20, 80, 40, "Salir (ESC)")

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE) or boton_salir.clickeado(e):
            pygame.quit(); sys.exit()
        elif e.type == pygame.KEYDOWN and e.key == pygame.K_p or boton_pausa.clickeado(e):
            pausado = not pausado

    pantalla.fill((0, 0, 0))
    boton_pausa.dibujar(pantalla)
    boton_salir.dibujar(pantalla)

    if not pausado:
        for p in pelotas: p.mover()
    for p in pelotas: p.dibujar()

    if not pausado:
        ahora = time.time()
        for i, p1 in enumerate(pelotas):
            for p2 in pelotas[i+1:]:
                dx, dy = p1.x - p2.x, p1.y - p2.y
                dist = (dx**2 + dy**2)**0.5
                if dist < p1.radio + p2.radio:
                    p1.vx, p2.vx = p2.vx, p1.vx
                    p1.vy, p2.vy = p2.vy, p1.vy
                    if dist:
                        overlap = p1.radio + p2.radio - dist
                        dx /= dist; dy /= dist
                        p1.x += dx * (overlap / 2)
                        p1.y += dy * (overlap / 2)
                        p2.x -= dx * (overlap / 2)
                        p2.y -= dy * (overlap / 2)
                    if ahora - last_collision > 0.1:
                        sonido.play(); last_collision = ahora
    else:
        msg = pygame.font.SysFont(None, 48).render("PAUSA - Presiona P o clic en el botón", True, (255,255,255))
        pantalla.blit(msg, msg.get_rect(center=(ANCHO//2, ALTO//2)))

    pygame.display.flip()
    reloj.tick(60)
