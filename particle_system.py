from OpenGL.GL import *
import random
import math
from particles import Particle
import config

particle_list = []


def emit_particles(rocket):
    if not config.SIMULATION_RUNNING or rocket.water_mass <= 0 or rocket.current_thrust_magnitude <= 0:
        return

    num_particles_to_emit = config.PARTICLES_PER_EMISSION
    base_dir_x = math.sin(rocket.angle)
    base_dir_y = -math.cos(rocket.angle)

    nozzle_pos_x = rocket.x  # Coordenadas en METROS
    nozzle_pos_y = rocket.y  # Coordenadas en METROS

    for _ in range(num_particles_to_emit):
        # Variación en la velocidad y dirección
        speed_magnitude = random.uniform(config.PARTICLE_SPEED_MIN, config.PARTICLE_SPEED_MAX)
        angle_spread = math.radians(random.uniform(-config.PARTICLE_SPREAD_ANGLE, config.PARTICLE_SPREAD_ANGLE))

        # Rotar el vector base de dirección por el ángulo de dispersión
        final_dir_x = base_dir_x * math.cos(angle_spread) - base_dir_y * math.sin(angle_spread)
        final_dir_y = base_dir_x * math.sin(angle_spread) + base_dir_y * math.cos(angle_spread)

        particle_vx = final_dir_x * speed_magnitude
        particle_vy = final_dir_y * speed_magnitude

        lifetime = random.uniform(config.PARTICLE_LIFETIME_MIN, config.PARTICLE_LIFETIME_MAX)
        size = random.uniform(config.PARTICLE_SIZE_MIN, config.PARTICLE_SIZE_MAX)

        particle_list.append(
            Particle(nozzle_pos_x, nozzle_pos_y, particle_vx, particle_vy, lifetime, config.PARTICLE_COLOR, size)
        )


def update_particles(dt):
    global particle_list
    for i in range(len(particle_list) - 1, -1, -1):
        particle = particle_list[i]
        particle.update(dt)
        if particle.lifetime <= 0:
            particle_list.pop(i)


def draw_particles():

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    for particle in particle_list:
        particle.draw()
    glDisable(GL_BLEND)