from OpenGL.GLUT import *
import config
import physics
import graphics

def update_loop(value):
    rocket = graphics.rocket_instance
    if not rocket:
        glutTimerFunc(config.MILLISECONDS_PER_FRAME, update_loop, 0)
        return

    # Actualizar física
    physics.update_simulation(rocket, config.TIME_STEP)
    glutPostRedisplay()
    glutTimerFunc(config.MILLISECONDS_PER_FRAME, update_loop, value)