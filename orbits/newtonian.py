import math
import sys
import matplotlib.pyplot as plt
import numpy as np

import pygame
from pygame import Vector2

from scipy.constants import G


EARTH_MASS_KG = 5.9722e24 
EARTH_RADIUS_M = 6371 * 1000


def gravity_accel(body_mass, radius) -> float:
    """
    a = GM/r²

    Args
        :param float body_mass: The mass of the orbital center in Kg (single point approximation)
        :param float body_radius: Radius from center of body in meters (assuming perfect sphere)
        
    Returns:
        float: gravitational acceleration produced by body as a scalar of m/s²
  
    """

    return (G * body_mass) / math.pow(radius, 2)


def gravity_kick(
        body_mass: float,
        body_pos: Vector2, 
        target_pos: Vector2, 
        delta_time=1.0, 
        scale_factor=1.0
):
    """
    Time based application of :func:`gravity_accel`

    Args
        :param float body_mass: The mass of the orbital center in Kg (single point approximation)
        :param vector2 body_pos: Position of orbital center as vector2
        :param vector2 target_pos: Position of sattelite
        :param float delta_time: Delta time (change of time) since last kick in ms
        :param float scale_factor: How much of the gravity should be applied. For an example for leapfrog you do 0.5
        
    Returns:
        float: gravitational acceleration produced by body as a scalar of m/s², scaled by delta time
  
    """
    gravity_vector = (body_pos - target_pos).normalize()

    radius = body_pos.distance_to(target_pos)

    a = gravity_accel(body_mass, radius)

    return a * gravity_vector * delta_time * scale_factor


def calculate_needed_orbital_velocity(gravity, radius):
    """
    v = sqrt(a*r)

    Args
        :param float gravity: The gravity effect at the given radius (a)
        :param float radius: Radius of body in meters + altitude (assuming perfect sphere) (r)

    Returns:
        float: Required velocity in meters a second, for perfectly circular orbit 
    """

    return math.sqrt(gravity * radius)


class Satellite():
    def __init__(self, start_altitude, start_speed):
        """
        Args
            :param float start_altitude: Height above planet surface in meters
            :param float start_speed: Starting speed in meters a second (m/s)

        Example:
            With a speed of 7672 m/s at 400km altitude you will get a stable (circular) orbit
        """
        self._position = Vector2(0, EARTH_RADIUS_M + start_altitude)
        self._velocity = Vector2(start_speed, 0)

    @property
    def position(self):
        """
        Returns:
            Vector2: Current position of satellite
        """
        return self._position
    
    @property
    def velocity(self):
        """
        Returns:
            Vector2: Velocity represented as a Vector2
        """
        return self._velocity
    
    @property
    def speed(self):
        """
        Returns:
            float: Speed in meters a second (m/s), derived from velocity vector
        """
        return self.velocity.magnitude()
    
    def apply_gravity(self, gravity):
        """
        Args
            :param Vector2 gravity: Planet gravity represented as Vector2
        """
        self._velocity += gravity

    def update_position(self, delta_time):
        """
        Applies velocity to satellite position, scaled by delta_time

        Args
            :param float delta_time: The time passed since last update
        """
        self._position += self._velocity * delta_time


EARTH_PIXEL_RADIUS = 100  # scale for simulation graphics
FPS = 60
BASE_PHYSICS_HZ = 60  # Physics steps per second
TIME_WARP = 10000  # Time speed up
METERS_PER_PIXEL = EARTH_RADIUS_M / EARTH_PIXEL_RADIUS


def main(multiplier: int):
    pygame.init()

    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()

    pixel_center = Vector2(screen.get_width() / 2, screen.get_height() / 2)
    satellite = Satellite(400 * 1000, 8672)

    physics_hz = BASE_PHYSICS_HZ * multiplier
    phys_dt = (1 / physics_hz) * TIME_WARP
    phys_per_frame = range(int(physics_hz / FPS))

    periapsis_angles = []
    prev_distance = pixel_center.distance_to(satellite.position)
    pos_at_periapsis = satellite.position
    is_outbound = False

    running = True
    while running:
        clock.tick(FPS)
        screen.fill("black")

        # physics loop
        for _ in phys_per_frame:
            # kick
            kick = gravity_kick(
                body_mass=EARTH_MASS_KG,
                body_pos=Vector2(0, 0),
                target_pos=satellite.position,
                delta_time=phys_dt,
            )
            satellite.apply_gravity(kick)
          
            # coast
            satellite.update_position(phys_dt)

            current_distance = Vector2(0, 0).distance_to(satellite.position)
            if current_distance > prev_distance and not is_outbound:
                angle_rad = math.atan2(pos_at_periapsis.y - Vector2(0, 0).y, pos_at_periapsis.x - Vector2(0, 0).x)
                periapsis_angles.append(math.degrees(angle_rad))
                is_outbound = True

            if current_distance < prev_distance:
                is_outbound = False
                pos_at_periapsis = satellite.position

            prev_distance = current_distance

        if len(periapsis_angles) == 201:
            periapsis_angles.pop(0)
            running = False

        # Draw objects
        pygame.draw.circle(
            screen, 
            pygame.Color("blue"), 
            pixel_center,
            EARTH_PIXEL_RADIUS,
            width=1
        )
        pygame.draw.circle(
            screen, 
            pygame.Color("green"), 
            Vector2(
                pixel_center.x + (satellite.position.x / METERS_PER_PIXEL),
                pixel_center.y - (satellite.position.y / METERS_PER_PIXEL)
            ),
            screen.get_height() / 200  # size
        )
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
        
    periapsis_angles = np.degrees(np.unwrap(np.radians(periapsis_angles)))

    plt.plot(periapsis_angles, marker='o')
    plt.xlabel("Orbit Number")
    plt.ylabel("Periapsis Angle (Degrees)")
    plt.title("Periapsis Angle per Orbit")
    plt.grid(True)
    plt.savefig(f"data/newt/Periapsis_angles_{multiplier}.png", dpi=300)

    with open(f"data/newt/Periapsis_angles_{multiplier}.txt", "w") as f:
        for index, periapsis in enumerate(periapsis_angles, start=1):
            f.write(f"{index}, {periapsis}\n")

    pygame.quit()


if __name__ == "__main__":
    # Default to 17 (1020 Hz) if no argument is provided
    multiplier = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    main(multiplier)