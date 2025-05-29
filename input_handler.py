# input_handler.py
from OpenGL.GLUT import *
import sys
import math
import config
import physics
import graphics


def keyboard_func(key, x, y):
    try:
        key_char = key.decode("utf-8").lower()
    except UnicodeDecodeError:
        key_char = None

    rocket = graphics.rocket_instance
    if not rocket and key not in [b'\x1b']:
        print("Error")
        return

    if key == b' ':  # Espacio
        if not config.SIMULATION_RUNNING:
            if abs(rocket.y - config.ROCKET_INITIAL_Y_METERS) < 1e-3:
                rocket.x = config.ROCKET_INITIAL_X_METERS
                rocket.y = config.ROCKET_INITIAL_Y_METERS
                rocket.vx = 0.0
                rocket.vy = 0.0
                rocket.angle = config.CURRENT_LAUNCH_ANGLE_RAD
                rocket.angular_velocity = 0.0
                rocket.angular_acceleration = 0.0

                # Resetear estado físico
                rocket.dry_mass = config.ROCKET_DRY_MASS
                rocket.water_mass = config.INITIAL_WATER_MASS
                rocket.mass = rocket.dry_mass + rocket.water_mass
                rocket.current_air_pressure = config.INITIAL_AIR_PRESSURE_ABSOLUTE
                rocket.current_thrust_magnitude = 0.0  # Resetear empuje

                # Recalcular MoI y volumen de aire inicial
                initial_water_volume_m3_reset = rocket.water_mass / config.WATER_DENSITY if config.WATER_DENSITY > 0 else 0
                rocket.initial_air_volume = rocket.bottle_volume - initial_water_volume_m3_reset
                if rocket.initial_air_volume <= 1e-9: rocket.initial_air_volume = 1e-9

                rocket.moment_of_inertia = (1 / 12) * rocket.mass * (rocket.length ** 2)
                if rocket.moment_of_inertia <= 1e-6: rocket.moment_of_inertia = 1e-6

            # Guardar la posición de lanzamiento
            rocket.launch_pos_x = rocket.x
            rocket.launch_pos_y = rocket.y

            config.SIMULATION_RUNNING = True
            physics.water_depleted_message_sent = False
            glutPostRedisplay()
        else:
            print("Simulación ya en curso")

    elif key_char == 'r':
        print("COHETE REINICIADO")
        config.SIMULATION_RUNNING = False  # Detener simulación
        if rocket:
            rocket.x = config.ROCKET_INITIAL_X_METERS
            rocket.y = config.ROCKET_INITIAL_Y_METERS
            rocket.vx = 0.0
            rocket.vy = 0.0
            rocket.angle = config.CURRENT_LAUNCH_ANGLE_RAD
            rocket.angular_velocity = 0.0
            rocket.angular_acceleration = 0.0

            rocket.dry_mass = config.ROCKET_DRY_MASS
            rocket.water_mass = config.INITIAL_WATER_MASS
            rocket.mass = rocket.dry_mass + rocket.water_mass
            rocket.current_air_pressure = config.INITIAL_AIR_PRESSURE_ABSOLUTE
            rocket.current_thrust_magnitude = 0.0

            initial_water_volume_m3_reset = rocket.water_mass / config.WATER_DENSITY if config.WATER_DENSITY > 0 else 0
            rocket.initial_air_volume = rocket.bottle_volume - initial_water_volume_m3_reset
            if rocket.initial_air_volume <= 1e-9: rocket.initial_air_volume = 1e-9

            rocket.moment_of_inertia = (1 / 12) * rocket.mass * (rocket.length ** 2)
            if rocket.moment_of_inertia <= 1e-6: rocket.moment_of_inertia = 1e-6

            # Actualizar la posición
            rocket.launch_pos_x = rocket.x
            rocket.launch_pos_y = rocket.y

            physics.water_depleted_message_sent = False
            glutPostRedisplay()

    elif key == b'\x1b':  # ESC
        print("FINALIZANDO")
        sys.exit(0)