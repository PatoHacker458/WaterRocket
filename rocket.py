from OpenGL.GL import *
import config
import math

class Rocket:
    def __init__(self, x=config.ROCKET_INITIAL_X, y=config.ROCKET_INITIAL_Y):

        # Estado cinemático
        self.x = x
        self.y = y
        self.vx = 0.0  # Velocidad en X
        self.vy = 0.0  # Velocidad en Y
        self.angle = 0.0  # Ángulo (0 grados = vertical hacia arriba)

        # Dimensiones
        self.width = config.ROCKET_WIDTH
        self.body_height = config.ROCKET_BODY_HEIGHT
        self.nose_height = config.ROCKET_NOSE_HEIGHT
        self.fin_width = config.ROCKET_FIN_WIDTH
        self.fin_height = config.ROCKET_FIN_HEIGHT

        # Estado físico
        self.dry_mass = config.ROCKET_DRY_MASS # Masa estructural
        self.water_mass = config.INITIAL_WATER_MASS # Masa de agua actual
        self.mass = self.dry_mass + self.water_mass  # Masa total actual

        # Presion y empuje
        self.bottle_volume = config.BOTTLE_VOLUME  # m^3
        self.nozzle_area = config.NOZZLE_AREA  # m^2

        initial_water_volume_m3 = self.water_mass / config.WATER_DENSITY
        self.initial_air_volume = self.bottle_volume - initial_water_volume_m3  # m^3

        # Estado inicial y actual de la presión del aire
        self.initial_air_pressure = config.INITIAL_AIR_PRESSURE_ABSOLUTE  # Pa (Absoluta)
        self.current_air_pressure = self.initial_air_pressure  # Pa (Absoluta)

        if self.initial_air_volume <= 0:
            print("¡Advertencia! El volumen de agua inicial excede o iguala el volumen de la botella.")
            self.initial_air_volume = 1e-9  # Poner un valor muy pequeño para evitar división por cero

        print(f"Cohete creado en ({self.x:.1f}, {self.y:.1f})")
        print(f"Masa inicial: {self.mass:.2f} kg (Seca: {self.dry_mass:.2f} kg, Agua: {self.water_mass:.2f} kg)")
        print(f"Volumen Botella: {self.bottle_volume * 1000:.1f} L, Agua Inicial: {initial_water_volume_m3 * 1000:.1f} L")
        print(f"Volumen Aire Inicial: {self.initial_air_volume * 1000:.2f} L")
        print(f"Presión Aire Inicial: {self.current_air_pressure / 1000:.1f} kPa (Absoluta)")

        # Debug
        print(f"Cohete creado en ({self.x:.1f}, {self.y:.1f})")
        print(f"  Masa inicial: {self.mass:.2f} kg (Seca: {self.dry_mass:.2f} kg, Agua: {self.water_mass:.2f} kg)")

    def draw(self):

        # Matriz de transformacion
        glPushMatrix()

        # Transformaciones: Translación y rotación
        glTranslatef(self.x, self.y, 0.0)  # Origen a (x,y) de cohete
        glRotatef(self.angle, 0.0, 0.0, 1.0)  # Rotacion eje Z

        # Cohete
        body_bottom = 0
        body_top = self.body_height
        half_width = self.width / 2

        v1 = (-half_width, body_bottom)  # II
        v2 = (half_width, body_bottom)  # ID
        v3 = (half_width, body_top)  # SD
        v4 = (-half_width, body_top)  # SI

        glColor3f(*config.ROCKET_BODY_COLOR)
        glBegin(GL_TRIANGLES)
        glVertex2f(*v1)
        glVertex2f(*v2)
        glVertex2f(*v3)
        glVertex2f(*v1)
        glVertex2f(*v3)
        glVertex2f(*v4)
        glEnd()

        glColor3f(*config.ROCKET_NOSE_COLOR)
        glBegin(GL_TRIANGLES)
        glVertex2f(-half_width, body_top)
        glVertex2f(half_width, body_top)
        glVertex2f(0, body_top + self.nose_height)
        glEnd()

        glColor3f(*config.ROCKET_FIN_COLOR)
        fin_base_y = body_bottom + 10
        glBegin(GL_TRIANGLES)
        glVertex2f(-half_width, fin_base_y)
        glVertex2f(-half_width, fin_base_y + self.fin_height)
        glVertex2f(-half_width - self.fin_width, fin_base_y)
        glEnd()

        glBegin(GL_TRIANGLES)
        glVertex2f(half_width, fin_base_y)
        glVertex2f(half_width, fin_base_y + self.fin_height)
        glVertex2f(half_width + self.fin_width, fin_base_y)
        glEnd()

        glPopMatrix()

    # --- Métodos futuros ---
    # def update_physics(self, dt):
    #    pass