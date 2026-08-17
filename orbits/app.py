import math
import time

import pygame
from pygame import Vector2
from array import array

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
    
    meters_from_center = (radius)

    return (G*body_mass)/math.pow(meters_from_center, 2)


def gravity_kick(body_mass, gravity_vector, radius: Vector2, delta_time = 1):
    """
    Time based application of :func:`gravity_accel`

    Args
        :param float body_mass: The mass of the orbital center in Kg (single point approximation)
        :param float body_radius: Radius of body in meters (assuming perfect sphere)
        :param float altitude: Height above surface in meters (assuming perfect sphere)
        :param int dt: Delta time (change of time) since last kick in ms
        
    Returns:
        float: gravitational acceleration produced by body as a scalar of m/s², scaled by delta time
  
    """
    
    return gravity_accel(body_mass, radius) * gravity_vector * delta_time


def calculate_needed_orbital_velocity(gravity, radius):
    """
    v = sqrt(a*r)

    Args
        :param float gravity: The gravity effect at the given radius (a)
        :param float radius: Radius of body in meters + altitude (assuming perfect sphere) (r)

    Returns:
        float: Required velocity in meters a second, for perfectly circular orbit 
    """

    return math.sqrt(gravity*radius)


class Satellite():
    def __init__(self, start_altitude, start_speed):
        """
        Args
            :param float start_altitude: Height above planet surface in meters
            :param float start_speed: Starting speed in meters a second (m/s)

        Example:
            With a speed of 7469.361555002398 m/s at 400km altitude you will get a stable orbit
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


def main():

    angles = array('f')  # 'f' stores raw 32-bit floats

    pygame.init()

    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True

    pixel_center = Vector2(screen.get_width()/2, screen.get_height()/2)
    earth_pos = Vector2(0, 0)
    satellite = Satellite(413*1000, 7672)

    earth_pixel_radius = 100
    meters_per_pixel = EARTH_RADIUS_M / earth_pixel_radius

    fps = 60
    physics_hz = 1000 # Physics steps per second
    physics_loop_per_frame = int(1/fps*physics_hz)
    time_warp = 1000 * physics_hz # Time sped up

    while running:
        # Start loop
        clock.tick(fps)
        screen.fill("black")


        # Draw objects
        pygame.draw.circle(
            screen, 
            pygame.Color("blue"), 
            earth_pos + pixel_center,
            earth_pixel_radius,
            width=1
        )
        pygame.draw.circle(
            screen, 
            pygame.Color("green"), 
            satellite.position/meters_per_pixel + pixel_center,
            screen.get_height()/200 # size
        )


        # Physics
        start_time = time.perf_counter()
        last_time = start_time
        for _ in range(0, physics_loop_per_frame):
            now = time.perf_counter()
            dt = (now - last_time) * time_warp
            last_time = now

            if now - start_time > 1:
                raise Exception("Can't keep up with physics frequency")

            satellite.update_position(dt)

            gravity_vector = (earth_pos - satellite.position).normalize()

            grav_kick = gravity_kick(
                body_mass = EARTH_MASS_KG,
                gravity_vector = gravity_vector,
                radius = earth_pos.distance_to(satellite.position),
                delta_time = dt
            )

            satellite.apply_gravity(grav_kick)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                with open("angles.bin", "wb") as f:
                    angles.tofile(f)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()