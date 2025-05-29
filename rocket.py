from OpenGL.GL import *
import config
import math

class Rocket:
    def __init__(self):
        self.current_thrust_magnitude = 0.0
        # Estado cinemático m y m/s
        self.x = config.ROCKET_INITIAL_X_METERS
        self.y = config.ROCKET_INITIAL_Y_METERS
        self.vx = 0.0  # m/s
        self.vy = 0.0  # m/s

        self.launch_pos_x = self.x
        self.launch_pos_y = self.y

        # Dimensiones visuales
        self.width_px = config.ROCKET_WIDTH_PX
        self.body_height_px = config.ROCKET_BODY_HEIGHT_PX
        self.nose_height_px = config.ROCKET_NOSE_HEIGHT_PX
        self.fin_width_px = config.ROCKET_FIN_WIDTH_PX
        self.fin_height_px = config.ROCKET_FIN_HEIGHT_PX

        # Estado cinematico angular
        self.angle = math.radians(-30) # rad
        self.angular_velocity = 0.0  # rad/s
        self.angular_acceleration = 0.0  # rad/s^2

        # Estado físico
        self.dry_mass = config.ROCKET_DRY_MASS
        self.water_mass = config.INITIAL_WATER_MASS
        self.mass = self.dry_mass + self.water_mass
        self.bottle_volume = config.BOTTLE_VOLUME
        self.nozzle_area = config.NOZZLE_AREA
        self.initial_air_volume = self.bottle_volume - (self.water_mass / config.WATER_DENSITY)
        self.initial_air_pressure = config.INITIAL_AIR_PRESSURE_ABSOLUTE
        self.current_air_pressure = self.initial_air_pressure

        # Dimensiones físicas
        self.length = config.ROCKET_LENGTH_METERS  # m
        self.moment_of_inertia = (1 / 12) * self.mass * (self.length ** 2)  # Momento de inercia (kg*m^2)

        if self.initial_air_volume <= 1e-9:
            print("Volumen de agua inicial >= volumen de la botella.")
            self.initial_air_volume = 1e-9

        self.show_flight_results = False
        self.flight_horizontal_range = 0.0
        self.flight_total_displacement = 0.0

    def draw(self):
        glPushMatrix()
        pos_x_px = self.x * config.PIXELS_PER_METER
        pos_y_px = self.y * config.PIXELS_PER_METER

        glTranslatef(pos_x_px, pos_y_px, 0.0)
        glRotatef(math.degrees(self.angle), 0.0, 0.0, 1.0) # Convertir ángulo de radianes a grados

        body_bottom = 0
        body_top = self.body_height_px
        half_width = self.width_px / 2

        v1 = (-half_width, body_bottom)
        v2 = (half_width, body_bottom)
        v3 = (half_width, body_top)
        v4 = (-half_width, body_top)

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
        glVertex2f(0, body_top + self.nose_height_px)
        glEnd()

        glColor3f(*config.ROCKET_FIN_COLOR)
        fin_base_y = body_bottom + 10

        glBegin(GL_TRIANGLES)
        glVertex2f(-half_width, fin_base_y)
        glVertex2f(-half_width, fin_base_y + self.fin_height_px)
        glVertex2f(-half_width - self.fin_width_px, fin_base_y)
        glEnd()

        glBegin(GL_TRIANGLES)
        glVertex2f(half_width, fin_base_y)
        glVertex2f(half_width, fin_base_y + self.fin_height_px)
        glVertex2f(half_width + self.fin_width_px, fin_base_y)
        glEnd()
        glPopMatrix()