from OpenGL.GL import *
import random
import math
import config

class Particle:
    def __init__(self, x, y, vx, vy, lifetime, color, size):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.lifetime = lifetime
        self.initial_lifetime = lifetime # Para calcular el alfa (opcional)
        self.color = color
        self.size = size
        self.gravity = config.GRAVITY_ACCELERATION * config.PARTICLE_GRAVITY_FACTOR # Gravedad sobre partículas

    def update(self, dt):
        self.vy -= self.gravity * dt # Aplicar gravedad a las partículas
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.lifetime -= dt

    def draw(self):
        if self.lifetime > 0:
            # Calcular alfa para desvanecimiento (opcional)
            alpha = max(0.0, min(1.0, self.lifetime / (self.initial_lifetime * 0.5))) # Desvanecer en la segunda mitad de vida

            glColor4f(self.color[0], self.color[1], self.color[2], alpha) # Usar glColor4f para alfa
            glPointSize(self.size)
            glBegin(GL_POINTS)
            glVertex2f(self.x * config.PIXELS_PER_METER, self.y * config.PIXELS_PER_METER)
            glEnd()
            glPointSize(1.0) # Resetear tamaño del punto