from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import config

rocket_instance = None  # Instancia del cohete

def init_opengl():
    glClearColor(*config.BACKGROUND_COLOR)  # Color de fondo
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    # Mantener relacion de aspecto
    window_aspect_ratio = config.WINDOW_WIDTH / config.WINDOW_HEIGHT
    world_visible_width = config.VIEW_HEIGHT * window_aspect_ratio
    gluOrtho2D(0, world_visible_width, 0, config.VIEW_HEIGHT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

# Ventana cambia de tamaño
def reshape(width, height):
    if height == 0: height = 1
    glViewport(0, 0, width, height)  # Usar toda la ventana para renderizar
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    # Mantener relacion de aspecto
    window_aspect_ratio = width / height
    world_visible_width = config.VIEW_HEIGHT * window_aspect_ratio
    gluOrtho2D(0, world_visible_width, 0, config.VIEW_HEIGHT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def display():
    if rocket_instance is None:
        return
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    rocket_instance.draw()  # Dibujar el cohete
    glutSwapBuffers()