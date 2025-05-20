import config
import math

water_depleted_message_sent = False

def calculate_forces_and_torque(rocket):
    global water_depleted_message_sent

    # Gravedad
    gravity_force_y = -rocket.mass * config.GRAVITY_ACCELERATION

    # Empuje
    thrust_magnitude = 0.0
    if config.SIMULATION_RUNNING and rocket.water_mass > 0:
        current_water_volume_m3 = rocket.water_mass / config.WATER_DENSITY if config.WATER_DENSITY > 0 else 0
        current_air_volume = rocket.bottle_volume - current_water_volume_m3
        if current_air_volume < rocket.initial_air_volume: current_air_volume = rocket.initial_air_volume
        if current_air_volume <= 1e-9: current_air_volume = 1e-9

        rocket.current_air_pressure = (rocket.initial_air_pressure * rocket.initial_air_volume) / current_air_volume
        pressure_difference = rocket.current_air_pressure - config.ATMOSPHERIC_PRESSURE

        if pressure_difference > 0:
            thrust_magnitude = 2 * pressure_difference * rocket.nozzle_area
        else:
            thrust_magnitude = 0.0
        water_depleted_message_sent = False
    elif config.SIMULATION_RUNNING and not water_depleted_message_sent:
        print(
            f"Agua agotada. Masa restante: {rocket.mass:.2f} kg. Presión final: {rocket.current_air_pressure / 1000:.1f} kPa")
        water_depleted_message_sent = True
        rocket.current_air_pressure = config.ATMOSPHERIC_PRESSURE

    # Empuje segun el angulo
    thrust_force_x = -thrust_magnitude * math.sin(rocket.angle)
    thrust_force_y =  thrust_magnitude * math.cos(rocket.angle)

    # Resistencia del Aire
    drag_force_x = 0.0
    drag_force_y = 0.0
    speed = math.sqrt(rocket.vx ** 2 + rocket.vy ** 2)

    if speed > 1e-6:
        k_drag = 0.5 * config.AIR_DENSITY * config.DRAG_COEFFICIENT * config.CROSS_SECTIONAL_AREA_METERS
        drag_magnitude = k_drag * speed ** 2
        drag_force_x = -drag_magnitude * (rocket.vx / speed)
        drag_force_y = -drag_magnitude * (rocket.vy / speed)

    # Fuerzas Netas
    net_force_x = thrust_force_x + drag_force_x
    net_force_y = gravity_force_y + thrust_force_y + drag_force_y

    # Torque
    net_torque = 0.0
    if speed > 1e-3:
        rocket_dir_x = -math.sin(rocket.angle)
        rocket_dir_y = math.cos(rocket.angle)
        v_unit_x = rocket.vx / speed
        v_unit_y = rocket.vy / speed
        sin_AoA = rocket_dir_x * v_unit_y - rocket_dir_y * v_unit_x
        torque_ref_magnitude = 0.5 * config.AIR_DENSITY * (speed ** 2) * \
                               config.CROSS_SECTIONAL_AREA_METERS * rocket.length
        net_torque = -config.AERO_TORQUE_COEFFICIENT * torque_ref_magnitude * sin_AoA

    return net_force_x, net_force_y, net_torque


def update_simulation(rocket, dt):
    if not config.SIMULATION_RUNNING and rocket.vy == 0 and rocket.y <= config.ROCKET_INITIAL_Y_METERS and rocket.angular_velocity == 0:
        return

    # Actualización de Masa y Momento de Inercia
    mass_changed = False
    if config.SIMULATION_RUNNING and rocket.water_mass > 0:
        mass_expelled = config.MASS_FLOW_RATE * dt

        if mass_expelled > rocket.water_mass: mass_expelled = rocket.water_mass
        rocket.water_mass -= mass_expelled
        rocket.mass = rocket.dry_mass + rocket.water_mass
        mass_changed = True

    if mass_changed or rocket.moment_of_inertia <= 0:
        rocket.moment_of_inertia = (1 / 12) * rocket.mass * (rocket.length ** 2)
        if rocket.moment_of_inertia <= 1e-6: rocket.moment_of_inertia = 1e-6

    # Calcular fuerzas y torque
    force_x, force_y, torque = calculate_forces_and_torque(rocket)

    # Actualizar movimiento lineal (m/s^2, m/s, m)
    if rocket.mass <= 1e-6:
        accel_x, accel_y = 0.0, 0.0
    else:
        accel_x = force_x / rocket.mass
        accel_y = force_y / rocket.mass
    rocket.vx += accel_x * dt
    rocket.vy += accel_y * dt
    rocket.x += rocket.vx * dt
    rocket.y += rocket.vy * dt

    # Actualizar movimiento angular (rad/s^2, rad/s, rad)
    if rocket.moment_of_inertia > 1e-9: # Evitar division por cero
        rocket.angular_acceleration = torque / rocket.moment_of_inertia
    else:
        rocket.angular_acceleration = 0.0
    rocket.angular_velocity += rocket.angular_acceleration * dt
    rocket.angle += rocket.angular_velocity * dt

    # Colisión con el suelo
    if rocket.y < config.ROCKET_INITIAL_Y_METERS:
        rocket.y = config.ROCKET_INITIAL_Y_METERS
        rocket.vy = 0.0
        rocket.vx = 0.0
        rocket.angular_velocity = 0.0
        global water_depleted_message_sent
        water_depleted_message_sent = False