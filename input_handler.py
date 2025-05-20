from OpenGL.GLUT import *
import config
import physics
import graphics

def keyboard_func(key, x, y):
    try:
        key_char = key.decode("utf-8").lower()
    except UnicodeDecodeError:
        key_char = None

    if key == b' ':
        if not config.SIMULATION_RUNNING:
            config.SIMULATION_RUNNING = True

    elif key_char == 'r':
        print("Cohete Reiniciado")
        config.SIMULATION_RUNNING = False
        if graphics.rocket_instance:
            graphics.rocket_instance.x = config.ROCKET_INITIAL_X_METERS
            graphics.rocket_instance.y = config.ROCKET_INITIAL_Y_METERS
            graphics.rocket_instance.vx = 0.0
            graphics.rocket_instance.vy = 0.0
            graphics.rocket_instance.angle = 0.0
            graphics.rocket_instance.angular_velocity = 0.0
            graphics.rocket_instance.angular_acceleration = 0.0
            graphics.rocket_instance.water_mass = config.INITIAL_WATER_MASS
            graphics.rocket_instance.mass = config.ROCKET_DRY_MASS + config.INITIAL_WATER_MASS
            graphics.rocket_instance.current_air_pressure = config.INITIAL_AIR_PRESSURE_ABSOLUTE
            graphics.rocket_instance.moment_of_inertia = (1 / 12) * graphics.rocket_instance.mass * (
                        graphics.rocket_instance.length ** 2)
            if graphics.rocket_instance.moment_of_inertia <= 1e-6: graphics.rocket_instance.moment_of_inertia = 1e-6
            physics.water_depleted_message_sent = False
            glutPostRedisplay()

    elif key == b'\x1b':
        sys.exit(0)