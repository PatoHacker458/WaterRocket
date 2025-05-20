import math

# Configuración de ventana
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = b"WATER ROCKET"
VIEW_HEIGHT = WINDOW_HEIGHT * 10 # Vista Alejada

PIXELS_PER_METER = 30  # Cuantos píxeles son 1 metro.

# Configuración de colores
BACKGROUND_COLOR = (0.1, 0.1, 0.2, 1.0)
ROCKET_BODY_COLOR = (0.8, 0.8, 0.8)
ROCKET_NOSE_COLOR = (1.0, 0.0, 0.0)
ROCKET_FIN_COLOR = (0.6, 0.6, 0.6)

# Configuración del Cohete - Dimensiones Visuales
ROCKET_WIDTH_PX = 40
ROCKET_BODY_HEIGHT_PX = 100
ROCKET_NOSE_HEIGHT_PX = 30
ROCKET_FIN_WIDTH_PX = 20
ROCKET_FIN_HEIGHT_PX = 35

# Posición inicial - Visual
ROCKET_INITIAL_X_PX = WINDOW_WIDTH / 2
ROCKET_INITIAL_Y_PX = 50 # Píxeles desde el borde inferior de la ventana

ROCKET_INITIAL_Y_METERS = ROCKET_INITIAL_Y_PX / PIXELS_PER_METER # Convertir posición inicial a metros
ROCKET_INITIAL_X_METERS = (WINDOW_WIDTH / 2) / PIXELS_PER_METER

# Dimensiones fisicas
ROCKET_DIAMETER_METERS = 0.1 # 10cm
CROSS_SECTIONAL_AREA_METERS = math.pi * (ROCKET_DIAMETER_METERS / 2)**2 # m^2
ROCKET_LENGTH_METERS = (ROCKET_BODY_HEIGHT_PX + ROCKET_NOSE_HEIGHT_PX) / PIXELS_PER_METER # Longitud del cohete (rotacion)

# Masa
ROCKET_DRY_MASS = 0.5  # kg
INITIAL_WATER_VOLUME = 0.03  # Litros
WATER_DENSITY = 1000 # kg/m^3
INITIAL_WATER_MASS = INITIAL_WATER_VOLUME * 1 # kg
ROCKET_INITIAL_MASS = ROCKET_DRY_MASS + INITIAL_WATER_MASS
MASS_FLOW_RATE = 0.5 # kg/s

# Constantes para Física de Fluidos
ATMOSPHERIC_PRESSURE = 101325.0 # Pa
INITIAL_AIR_PRESSURE_GAUGE = 10.0 * ATMOSPHERIC_PRESSURE # Pa (manométrica)
INITIAL_AIR_PRESSURE_ABSOLUTE = INITIAL_AIR_PRESSURE_GAUGE + ATMOSPHERIC_PRESSURE
BOTTLE_VOLUME = 0.002 # m^3
NOZZLE_RADIUS = 0.01 # m
NOZZLE_AREA = math.pi * (NOZZLE_RADIUS ** 2) # m^2

# Constantes para Resistencia del Aire
AIR_DENSITY = 1.225 # kg/m^3
DRAG_COEFFICIENT = 0.5 # Coeficiente de arrastre

# Constantes para Rotación
# Un valor positivo tiende a estabilizar el cohete (efecto veleta).
# Valores típicos pequeños (ej: 0.1 a 2.0).
AERO_TORQUE_COEFFICIENT = 0.025 # Coeficiente para el torque aerodinámico

# Constantes físicas
GRAVITY_ACCELERATION = 9.81 # m/s^2

# Temporizador y Control de Simulación
MILLISECONDS_PER_FRAME = 16
TIME_STEP = MILLISECONDS_PER_FRAME / 1000.0
SIMULATION_RUNNING = False