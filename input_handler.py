from OpenGL.GLUT import *
import sys
import config
import graphics
import physics


def keyboard_func(key, x, y):
    global rocket_instance

    try:
        key_char = key.decode("utf-8").lower()
    except UnicodeDecodeError:
        key_char = None

    if key == b' ': # Espacio
        if not config.SIMULATION_RUNNING:
            print("Lanzamiento")
            config.SIMULATION_RUNNING = True
        else:
            print("Lanzado")

    # Resetear estado cinemático
    elif key_char == 'r':  # R
        print("--- REINICIANDO ---")
        config.SIMULATION_RUNNING = False
        if graphics.rocket_instance:
            graphics.rocket_instance.x = config.ROCKET_INITIAL_X
            graphics.rocket_instance.y = config.ROCKET_INITIAL_Y
            graphics.rocket_instance.vx = 0.0
            graphics.rocket_instance.vy = 0.0
            graphics.rocket_instance.angle = 0.0
            graphics.rocket_instance.water_mass = config.INITIAL_WATER_MASS
            graphics.rocket_instance.mass = config.ROCKET_DRY_MASS + config.INITIAL_WATER_MASS
            physics.water_depleted_message_sent = False
            print(f"Cohete reiniciado. Masa restaurada a {graphics.rocket_instance.mass:.2f} kg")
            glutPostRedisplay()
        else:
            print("Error")

    # ESC
    elif key == b'\x1b': # Esc
        print("Finalizando")
        sys.exit(0)