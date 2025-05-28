# timer.py
from OpenGL.GLUT import *
import config
import particle_system # Import correcto
import physics
import graphics

def update_loop(value):
    rocket = graphics.rocket_instance
    if not rocket:
        print("Error: Instancia del cohete no encontrada en timer.py")
        glutTimerFunc(config.MILLISECONDS_PER_FRAME, update_loop, 0)
        return

    physics.update_simulation(rocket, config.TIME_STEP) # Esto actualiza rocket.current_thrust_magnitude

    if config.SIMULATION_RUNNING and rocket.water_mass > 0 and \
       hasattr(rocket, 'current_thrust_magnitude') and rocket.current_thrust_magnitude > 0:
        particle_system.emit_particles(rocket)

    particle_system.update_particles(config.TIME_STEP) # Actualizar todas las partículas siempre

    glutPostRedisplay() # Solicitar redibujo
    glutTimerFunc(config.MILLISECONDS_PER_FRAME, update_loop, value + 1)