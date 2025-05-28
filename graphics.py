from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import config
import particle_system

rocket_instance = None  # Instancia del cohete

def draw_text_stroke(x, y, text_string, scale=0.15, r=1.0, g=1.0, b=1.0, line_width=2.0):
    glPushMatrix()
    glTranslatef(x, y, 0)
    glScalef(scale, scale, scale) # Escalar el texto
    glColor3f(r, g, b)
    glLineWidth(line_width)
    for char_code in text_string.encode():
        glutStrokeCharacter(GLUT_STROKE_ROMAN, char_code)
    glPopMatrix()
    glLineWidth(1.0) # Resetear grosor de línea

def draw_text_bitmap(x, y, text_string, font=GLUT_BITMAP_HELVETICA_18, r=1.0, g=1.0, b=1.0):
    glColor3f(r, g, b)
    glRasterPos2f(x, y)
    for char_code in text_string.encode():
        glutBitmapCharacter(font, char_code)

def init_opengl():
    glClearColor(*config.BACKGROUND_COLOR)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    window_aspect_ratio = config.WINDOW_WIDTH / config.WINDOW_HEIGHT
    world_visible_width = config.VIEW_HEIGHT * window_aspect_ratio
    gluOrtho2D(0, world_visible_width, 0, config.VIEW_HEIGHT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def reshape(width, height):
    if height == 0: height = 1
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    window_aspect_ratio = width / height
    world_visible_width = config.VIEW_HEIGHT * window_aspect_ratio
    gluOrtho2D(0, world_visible_width, 0, config.VIEW_HEIGHT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def display():
    if rocket_instance is None:
        print("Error")
        return

    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    rocket_instance.draw() # Dibujar el cohete

    particle_system.draw_particles()  # Dibujar partículas

    if rocket_instance.show_flight_results:
        current_window_width = glutGet(GLUT_WINDOW_WIDTH)
        current_window_height = glutGet(GLUT_WINDOW_HEIGHT)

        # Guardar matrices actuales
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, current_window_width, 0, current_window_height)  # Proyección pixel-perfect

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        text_y_start = current_window_height - 30

        range_text = f"Alcance Horizontal: {rocket_instance.flight_horizontal_range:.2f} m"
        draw_text_bitmap(10, text_y_start, range_text, font=GLUT_BITMAP_9_BY_15, r=0.9, g=0.9, b=0.9)

        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

    glutSwapBuffers()