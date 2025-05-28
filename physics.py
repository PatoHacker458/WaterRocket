# physics.py
import config
import math

# Flag global para controlar el mensaje de "Agua agotada" una vez por vuelo.
water_depleted_message_sent = False


def calculate_forces_and_torque(rocket):
    global water_depleted_message_sent

    # FUERZA DE GRAVEDAD (siempre actúa)
    gravity_force_y = -rocket.mass * config.GRAVITY_ACCELERATION

    # FUERZA DE EMPUJE (THRUST)
    thrust_magnitude = 0.0
    pressure_difference_for_flow = 0.0

    if config.SIMULATION_RUNNING and rocket.water_mass > 0:
        current_water_volume_m3 = rocket.water_mass / config.WATER_DENSITY if config.WATER_DENSITY > 0 else 0
        current_air_volume = rocket.bottle_volume - current_water_volume_m3

        if current_air_volume < rocket.initial_air_volume:
            current_air_volume = rocket.initial_air_volume
        if current_air_volume <= 1e-9:
            current_air_volume = 1e-9

        rocket.current_air_pressure = (rocket.initial_air_pressure * rocket.initial_air_volume) / current_air_volume
        pressure_difference_for_flow = rocket.current_air_pressure - config.ATMOSPHERIC_PRESSURE

        if pressure_difference_for_flow > 0:
            thrust_magnitude = 2 * pressure_difference_for_flow * rocket.nozzle_area
        else:
            thrust_magnitude = 0.0
            pressure_difference_for_flow = 0.0

        water_depleted_message_sent = False

    elif config.SIMULATION_RUNNING and not water_depleted_message_sent and rocket.water_mass <= 0:
        print(
            f"Agua agotada. Masa restante: {rocket.mass:.2f} kg. "
            f"Presión final: {rocket.current_air_pressure / 1000:.1f} kPa"
        )
        water_depleted_message_sent = True
        pressure_difference_for_flow = 0.0  # No hay flujo por presión si no hay agua

    rocket.current_thrust_magnitude = thrust_magnitude

    thrust_force_x = -thrust_magnitude * math.sin(rocket.angle)
    thrust_force_y = thrust_magnitude * math.cos(rocket.angle)

    # FUERZA DE RESISTENCIA DEL AIRE (DRAG)
    drag_force_x = 0.0
    drag_force_y = 0.0
    speed = math.sqrt(rocket.vx ** 2 + rocket.vy ** 2)

    if speed > 1e-6:
        k_drag = 0.5 * config.AIR_DENSITY * config.DRAG_COEFFICIENT * config.CROSS_SECTIONAL_AREA_METERS
        drag_magnitude = k_drag * speed ** 2
        drag_force_x = -drag_magnitude * (rocket.vx / speed)
        drag_force_y = -drag_magnitude * (rocket.vy / speed)

    # FUERZAS NETAS
    net_force_x = thrust_force_x + drag_force_x
    net_force_y = gravity_force_y + thrust_force_y + drag_force_y

    # TORQUE AERODINÁMICO
    net_torque = 0.0
    if speed > 1e-3:
        rocket_dir_x = -math.sin(rocket.angle)
        rocket_dir_y = math.cos(rocket.angle)
        v_unit_x = rocket.vx / speed
        v_unit_y = rocket.vy / speed
        sin_AoA = rocket_dir_x * v_unit_y - rocket_dir_y * v_unit_x
        torque_ref_magnitude = (0.5 * config.AIR_DENSITY * speed ** 2) * \
                               config.CROSS_SECTIONAL_AREA_METERS * rocket.length
        net_torque = -config.AERO_TORQUE_COEFFICIENT * torque_ref_magnitude * sin_AoA

    return net_force_x, net_force_y, net_torque, pressure_difference_for_flow


def update_simulation(rocket, dt):
    if not config.SIMULATION_RUNNING and \
            abs(rocket.vy) < 1e-3 and abs(rocket.vx) < 1e-3 and \
            abs(rocket.y - config.ROCKET_INITIAL_Y_METERS) < 1e-3 and \
            abs(rocket.angular_velocity) < 1e-3:
        return

    # CALCULAR FUERZAS, TORQUE Y PRESIÓN PARA FLUJO
    force_x, force_y, torque, pressure_diff_for_flow = calculate_forces_and_torque(rocket)

    # ACTUALIZACIÓN DE MASA (CON FLUJO MÁSICO DINÁMICO) Y MOMENTO DE INERCIA
    mass_changed = False
    if config.SIMULATION_RUNNING and rocket.water_mass > 0 and rocket.current_thrust_magnitude > 0:
        mass_expelled = 0.0
        if pressure_diff_for_flow > 0 and hasattr(rocket, 'nozzle_area') and \
                hasattr(config, 'WATER_DENSITY') and config.WATER_DENSITY > 0:
            mass_flow_rate_actual = rocket.nozzle_area * math.sqrt(
                max(0, 2 * pressure_diff_for_flow * config.WATER_DENSITY))
            mass_expelled = mass_flow_rate_actual * dt

        if mass_expelled > rocket.water_mass:
            mass_expelled = rocket.water_mass  # No expulsar más agua de la que hay

        rocket.water_mass -= mass_expelled
        rocket.mass = rocket.dry_mass + rocket.water_mass
        mass_changed = True

    if mass_changed or rocket.moment_of_inertia <= 1e-9:  # Si la masa cambió o MoI es inválido/cero
        rocket.moment_of_inertia = (1 / 12) * rocket.mass * (rocket.length ** 2)
        if rocket.moment_of_inertia <= 1e-9:
            rocket.moment_of_inertia = 1e-9  # Evitar MoI cero o negativo

    # ACTUALIZAR MOVIMIENTO LINEAL
    if rocket.mass <= 1e-9:
        accel_x, accel_y = 0.0, 0.0
    else:
        accel_x = force_x / rocket.mass
        accel_y = force_y / rocket.mass

    rocket.vx += accel_x * dt
    rocket.vy += accel_y * dt
    rocket.x += rocket.vx * dt
    rocket.y += rocket.vy * dt

    # ACTUALIZAR MOVIMIENTO ANGULAR
    if rocket.moment_of_inertia > 1e-9:
        rocket.angular_acceleration = torque / rocket.moment_of_inertia
    else:
        rocket.angular_acceleration = 0.0

    rocket.angular_velocity += rocket.angular_acceleration * dt
    rocket.angle += rocket.angular_velocity * dt

    # COLISIÓN CON EL SUELO
    if rocket.y < config.ROCKET_INITIAL_Y_METERS:
        final_pos_x_ground = rocket.x

        rocket.y = config.ROCKET_INITIAL_Y_METERS
        rocket.vy = 0.0
        rocket.vx = 0.0
        rocket.angular_velocity = 0.0

        if config.SIMULATION_RUNNING:
            config.SIMULATION_RUNNING = False

            delta_x = final_pos_x_ground - rocket.launch_pos_x
            delta_y = rocket.y - rocket.launch_pos_y

            rocket.flight_horizontal_range = abs(delta_x)
            rocket.flight_total_displacement = math.sqrt(delta_x ** 2 + delta_y ** 2)
            rocket.show_flight_results = True

            print(f"  Posición de lanzamiento: ({rocket.launch_pos_x:.2f}m, {rocket.launch_pos_y:.2f}m)")
            print(f"  Posición de aterrizaje:  ({final_pos_x_ground:.2f}m, {rocket.y:.2f}m)")  # Usar final_pos_x_ground
            print(f"  Distancia horizontal (alcance): {rocket.flight_horizontal_range:.2f} m")

        global water_depleted_message_sent
        water_depleted_message_sent = False