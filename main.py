from OpenGL.GLUT import *
import config
import graphics
from rocket import Rocket
import input_handler
import timer
import sys


def main():
    print("Iniciando")
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
    glutCreateWindow(config.WINDOW_TITLE)
    graphics.init_opengl()
    graphics.rocket_instance = Rocket() # Crear la instancia del cohete
    glutDisplayFunc(graphics.display)
    glutReshapeFunc(graphics.reshape)
    glutKeyboardFunc(input_handler.keyboard_func)

    print("Controles:")
    print("  ESPACIO: Lanzar")
    print("  R: Reiniciar")

    glutTimerFunc(config.MILLISECONDS_PER_FRAME, timer.update_loop, 0)
    glutMainLoop()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Error")
    finally:
        print("Fin")