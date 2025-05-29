import math

from OpenGL.GLUT import *
import config
import graphics
from rocket import Rocket
import input_handler
import timer
import sys


def get_user_launch_parameters():
    print("\nPARÁMETROS INICIALES")
    print("Presiona Enter para usar el valor por defecto")

    default_pressure_atm_manometric = config.INITIAL_AIR_PRESSURE_GAUGE / config.ATMOSPHERIC_PRESSURE
    default_water_liters = config.INITIAL_WATER_VOLUME
    default_dry_mass_kg = config.ROCKET_DRY_MASS
    default_initial_angle_deg = -45

    try:
        pressure_str = input(
            f"Presión inicial del aire (atmósferas manométricas, ej: {default_pressure_atm_manometric:.1f}): ")
        user_pressure_atm_manometric = float(pressure_str) if pressure_str.strip() else default_pressure_atm_manometric
        if user_pressure_atm_manometric < 0.1:  # Evitar presiones muy bajas o negativas
            print("Presión demasiado baja, usando mínimo de 0.1 atm.")
            user_pressure_atm_manometric = 0.1
    except ValueError:
        print(f"Entrada inválida. Usando presión por defecto: {default_pressure_atm_manometric:.1f} atm")
        user_pressure_atm_manometric = default_pressure_atm_manometric

    try:
        water_str = input(f"Volumen inicial de agua (litros, ej: {default_water_liters:.2f}): ")
        user_water_liters = float(water_str) if water_str.strip() else default_water_liters
        if user_water_liters < 0: user_water_liters = 0.0
        # Validar que el agua no exceda el volumen de la botella (dejando un mínimo de espacio para aire)
        min_air_volume_m3 = 0.0001  # 0.1L de aire mínimo
        max_water_volume_m3 = config.BOTTLE_VOLUME - min_air_volume_m3
        max_water_liters = max_water_volume_m3 * 1000.0
        if user_water_liters > max_water_liters:
            print(f"Volumen de agua excede capacidad ({max_water_liters:.2f} L máx). Ajustando a máximo.")
            user_water_liters = max_water_liters
    except ValueError:
        print(f"Entrada inválida. Usando volumen de agua por defecto: {default_water_liters:.2f} L")
        user_water_liters = default_water_liters

    try:
        mass_str = input(f"Masa seca del cohete (kg, ej: {default_dry_mass_kg:.2f}): ")
        user_dry_mass_kg = float(mass_str) if mass_str.strip() else default_dry_mass_kg
        if user_dry_mass_kg <= 0.01:  # Evitar masa cero o negativa
            print("Masa seca demasiado baja, usando mínimo de 0.01 kg.")
            user_dry_mass_kg = 0.01
    except ValueError:
        print(f"Entrada inválida. Usando masa seca por defecto: {default_dry_mass_kg:.2f} kg")
        user_dry_mass_kg = default_dry_mass_kg

    try:
        angle_str = input(
            f"Ángulo de lanzamiento inicial (grados desde la vertical=: ")
        user_initial_angle_deg = float(angle_str) if angle_str.strip() else default_initial_angle_deg
    except ValueError:
        print(f"Entrada inválida. Usando ángulo por defecto: {default_initial_angle_deg:.1f} grados")
        user_initial_angle_deg = default_initial_angle_deg

    return user_pressure_atm_manometric, user_water_liters, user_dry_mass_kg, user_initial_angle_deg  # Devuelve el ángulo

def main():

    user_pressure_atm, user_water_liters, user_dry_mass_kg, user_initial_angle_deg = get_user_launch_parameters() # Recibe el ángulo

    config.INITIAL_AIR_PRESSURE_GAUGE = user_pressure_atm * config.ATMOSPHERIC_PRESSURE
    config.INITIAL_AIR_PRESSURE_ABSOLUTE = config.INITIAL_AIR_PRESSURE_GAUGE + config.ATMOSPHERIC_PRESSURE
    config.INITIAL_WATER_VOLUME = user_water_liters
    config.INITIAL_WATER_MASS = user_water_liters * 1.0
    config.ROCKET_DRY_MASS = user_dry_mass_kg
    config.ROCKET_INITIAL_MASS = config.ROCKET_DRY_MASS + config.INITIAL_WATER_MASS
    config.CURRENT_LAUNCH_ANGLE_RAD = math.radians(user_initial_angle_deg)
    # ----------------------------------------------------
    print("Iniciando")
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
    glutCreateWindow(config.WINDOW_TITLE)
    graphics.init_opengl()
    graphics.rocket_instance = Rocket() # Crear la instancia del cohete
    graphics.rocket_instance.angle = math.radians(user_initial_angle_deg)
    glutDisplayFunc(graphics.display)
    glutReshapeFunc(graphics.reshape)
    glutKeyboardFunc(input_handler.keyboard_func)

    print("Controles:")
    print("ESPACIO: Lanzar")
    print("R: Reiniciar")

    glutTimerFunc(config.MILLISECONDS_PER_FRAME, timer.update_loop, 0)
    glutMainLoop()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Error")
    finally:
        print("Fin")