from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import config

# Variable global para acceder al cohete desde display()
rocket_instance = None

def init_opengl():
    glClearColor(*config.BACKGROUND_COLOR)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, config.WINDOW_WIDTH, 0, config.VIEW_HEIGHT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Debug
    print("OpenGL inicializado")

# Ventana cambia de tamaño
def reshape(width, height):
    if height == 0: height = 1
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, width, 0, config.VIEW_HEIGHT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

# Función principal de dibujo
def display():
    if rocket_instance is None:
        print("Error")
        return

    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    rocket_instance.draw()

    # environment.draw()
    # particles.draw()
    # ui.draw_info()

    glutSwapBuffers()