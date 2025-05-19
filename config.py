# Configuración de ventana
import math

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
VIEW_HEIGHT = WINDOW_HEIGHT * 5

WINDOW_TITLE = b"WATER ROCKET"

# Configuración de colores
BACKGROUND_COLOR = (0.1, 0.1, 0.2, 1.0)  # Azul oscuro
ROCKET_BODY_COLOR = (0.8, 0.8, 0.8)      # Gris claro
ROCKET_NOSE_COLOR = (1.0, 0.0, 0.0)      # Rojo
ROCKET_FIN_COLOR = (0.6, 0.6, 0.6)       # Gris medio

# Configuración inicial del cohete
ROCKET_WIDTH = 40
ROCKET_BODY_HEIGHT = 100
ROCKET_NOSE_HEIGHT = 30
ROCKET_FIN_WIDTH = 20   # Aleta
ROCKET_FIN_HEIGHT = 35  # Alto base aleta
ROCKET_INITIAL_X = WINDOW_WIDTH / 2
ROCKET_INITIAL_Y = 50
ROCKET_DRY_MASS = 0.5

# Configuración del agua
INITIAL_WATER_VOLUME = 1.0 # Litros
WATER_DENSITY = 1000 # kg/m^3 (o 1 kg/L simplificado)
INITIAL_WATER_MASS = INITIAL_WATER_VOLUME * 1

ROCKET_INITIAL_MASS = ROCKET_DRY_MASS + INITIAL_WATER_MASS
MASS_FLOW_RATE = 0.5 # Duración del empuje

ATMOSPHERIC_PRESSURE = 101325.0 # Presión atmosférica en Pascals (Pa)
INITIAL_AIR_PRESSURE_GAUGE = 20.0 * ATMOSPHERIC_PRESSURE
INITIAL_AIR_PRESSURE_ABSOLUTE = INITIAL_AIR_PRESSURE_GAUGE + ATMOSPHERIC_PRESSURE

BOTTLE_VOLUME = 0.002 # Volumen total de la botella en m^3 (2 Litros)
NOZZLE_RADIUS = 0.01 # Radio de la boquilla en metros (1 cm)
NOZZLE_AREA = math.pi * (NOZZLE_RADIUS ** 2) # Área de la boquilla en m^2

# Constantes físicas
GRAVITY_ACCELERATION = 9.81 * 30 # m/s^2
#INITIAL_THRUST_FORCE = (ROCKET_INITIAL_MASS * GRAVITY_ACCELERATION) * 1.5 # Empuje inicial
ROCKET_INITIAL_MASS = 1.0


# Temporizador
MILLISECONDS_PER_FRAME = 16 # 60fps (1000 ms / 60fps ~= 16)
TIME_STEP = MILLISECONDS_PER_FRAME / 1000.0 # El paso de tiempo dt en segundos (0.016)
SIMULATION_RUNNING = False