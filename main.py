import sys
from OpenGL.GLUT import *
import config
import graphics
from rocket import Rocket
import physics
import input_handler
import timer

def main():
    # Debug
    print("Iniciando")

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
    glutInitWindowPosition(100, 100) # Posición inicial
    glutCreateWindow(config.WINDOW_TITLE)

    graphics.init_opengl()
    graphics.rocket_instance = Rocket()

    glutDisplayFunc(graphics.display)
    glutReshapeFunc(graphics.reshape)
    glutKeyboardFunc(input_handler.keyboard_func)

    print("Controles:")
    print("ESPACIO: Lanzar cohete")
    glutTimerFunc(config.MILLISECONDS_PER_FRAME, timer.update_loop, 0)

    glutMainLoop()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print("Error")
    finally:
        print("Finalizando")



#IMPLEMENTAR MODELO MATEMATICO, HACER CALCULOS CON TODAS LAS ENTRADAS Y REGRESE SALIDAS
# Y A PARTIR DE ESO SIMULAR EN EL COHETE
# ENTRADAS: PRESION, ANGULO DE TIRO, PESO DEL COHETE, GRAVEDAD, RESISTENCIA AL VIENTE
# SALIDAS: ALTURA MAXIMA, DISTANCIA MAXIMA DESDE ORIGEN, TIEMPO EN EL AIRE, ACELERACION


#3D USAR BLENDER SI ASI SE NECESITA Q