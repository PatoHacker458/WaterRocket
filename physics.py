
import config
import graphics

water_depleted_message_sent = False

def calculate_forces(rocket):
    global water_depleted_message_sent

    # Fuerza de Gravedad
    gravity_force_y = -rocket.mass * config.GRAVITY_ACCELERATION

    # Fuerza de Empuje (dependiente de la presión)
    thrust_force_y = 0.0
    if config.SIMULATION_RUNNING and rocket.water_mass > 0:
        # --- Cálculo de Presión y Empuje ---
        # 1. Calcular volumen actual de agua y aire (en m^3)
        current_water_volume_m3 = rocket.water_mass / config.WATER_DENSITY  # Asumiendo 1000 kg/m^3
        current_air_volume = rocket.bottle_volume - current_water_volume_m3

        # Asegurar que el volumen de aire actual sea válido y no menor que el inicial
        if current_air_volume < rocket.initial_air_volume:
            current_air_volume = rocket.initial_air_volume  # Evitar errores si water_mass aumenta por error
        if current_air_volume <= 1e-9:  # Evitar división por cero
            current_air_volume = 1e-9

        # 2. Calcular Presión Actual usando Ley de Boyle (P1V1 = P2V2 -> P2 = P1 * V1 / V2)
        # (Más adelante podríamos usar adiabática: P2 = P1 * (V1/V2)^gamma)
        rocket.current_air_pressure = (rocket.initial_air_pressure * rocket.initial_air_volume) / current_air_volume

        # 3. Calcular Empuje usando la fórmula T = 2 * (P_int - P_atm) * A_nozzle
        pressure_difference = rocket.current_air_pressure - config.ATMOSPHERIC_PRESSURE
        if pressure_difference > 0:  # Solo hay empuje si P_interna > P_atmosférica
            thrust_force_y = 2 * pressure_difference * rocket.nozzle_area
        else:
            thrust_force_y = 0  # No hay empuje si la presión interna no supera la atmosférica

        # ------------------------------------
        water_depleted_message_sent = False  # Resetear flag mientras hay agua

    elif config.SIMULATION_RUNNING and not water_depleted_message_sent:
        print(
            f"Agua agotada. Masa restante: {rocket.mass:.2f} kg (Masa seca). Presión final agua: {rocket.current_air_pressure / 1000:.1f} kPa")
        water_depleted_message_sent = True
        rocket.current_air_pressure = config.ATMOSPHERIC_PRESSURE  # Resetear presión a atmosférica como referencia

    # Fuerzas Horizontales
    net_force_x = 0.0

    # Fuerza Neta Vertical
    net_force_y = gravity_force_y + thrust_force_y

    return net_force_x, net_force_y


def update_simulation(rocket, dt):

    if not config.SIMULATION_RUNNING and rocket.vy == 0 and rocket.y <= config.ROCKET_INITIAL_Y:
        return

    if config.SIMULATION_RUNNING and rocket.water_mass > 0:
        mass_expelled = config.MASS_FLOW_RATE * dt
        if mass_expelled > rocket.water_mass:
            mass_expelled = rocket.water_mass
        rocket.water_mass -= mass_expelled
        rocket.mass = rocket.dry_mass + rocket.water_mass

    # Calculo fuerzas netas
    force_x, force_y = calculate_forces(rocket)

    # Calculo aceleración (a = F / m)
    if rocket.mass <= 0:
        accel_x, accel_y = 0.0, 0.0
    else:
        accel_x = force_x / rocket.mass
        accel_y = force_y / rocket.mass

    # Calculo velocidad (v = v0 + a * dt)
    rocket.vx += accel_x * dt
    rocket.vy += accel_y * dt

    # Calculo posición con euler (p = p0 + v * dt)  v_inicial en el intervalo dt
    rocket.x += (rocket.vx - accel_x * dt) * dt
    rocket.y += (rocket.vy - accel_y * dt) * dt

    # Colisión con suelo
    if rocket.y < config.ROCKET_INITIAL_Y:
        rocket.y = config.ROCKET_INITIAL_Y
        rocket.vy = 0
        rocket.vx = 0