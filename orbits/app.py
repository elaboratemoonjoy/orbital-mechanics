import math
import time

import pygame
from pygame import Vector2
from . import physmath
from array import array


class Satellite():
    def __init__(self, start_altitude, start_speed):
        """
        Args
            :param float start_altitude: Height above planet surface in meters
            :param float start_speed: Starting speed in meters a second (m/s)

        Example:
            With a speed of 7469.361555002398 m/s at 400km altitude you will get a stable orbit
        """
        self._position = Vector2(0, physmath.EARTH_RADIUS_M + start_altitude)
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
    meters_per_pixel = physmath.EARTH_RADIUS_M / earth_pixel_radius

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

            grav_kick = physmath.gravity_kick(
                body_mass = physmath.EARTH_MASS_KG,
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