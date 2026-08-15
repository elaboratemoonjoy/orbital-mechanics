import math
import time

import pygame
from pygame import Vector2
from . import physmath
from array import array
def main():
    debug = True

    angles = array('f')  # 'f' stores raw 32-bit floats

    pygame.init()

    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True

    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)

    pixel_center = Vector2(screen.get_width()/2, screen.get_height()/2)

    earth_pixel_radius = 100
    meters_per_pixel = physmath.EARTH_RADIUS_M / earth_pixel_radius


    earth_pos = Vector2(
        0,
        0
    )

    sat_pos = Vector2(0, physmath.EARTH_RADIUS_M + (400*1000))
    sat_vel = Vector2(7469.361555002398, 0)

    last_time = time.perf_counter()

    while running:
        clock.tick(60)
        now = time.perf_counter()
        dt = (now - last_time) * 6000
        last_time = now
        screen.fill("black")

        pygame.draw.circle(
            screen, 
            BLUE, 
            earth_pos + pixel_center,
            earth_pixel_radius,
            width=1
        )

        pygame.draw.circle(
            screen,
            (255, 255, 255),
            screen.get_rect().center,
            1
        )

        sat = pygame.draw.circle(
            screen, 
            GREEN, 
            sat_pos/meters_per_pixel + pixel_center,
            screen.get_height()/200 # size
        )

        sat_pos += sat_vel * dt


        #update sat velocity
        grav_kick = physmath.gravity_kick(
            physmath.EARTH_MASS_KG,
            (earth_pos - sat_pos).normalize(),
            earth_pos.distance_to(sat_pos),
            dt
        )

        sat_vel += grav_kick

        if debug:
            # Generates periapsis angles for precession analysis
            if not 'ascending' in locals():
                ascending = False
                prev_alt = 0
                alt = 0
                hor_vec = Vector2(screen.get_width(), screen.get_height()/2)

            alt = Vector2(sat_pos).distance_to(earth_pos)

            # Determine periapsis
            if prev_alt < alt and not ascending:
                periapsis_pos = sat_pos.copy()
                angles.append(periapsis_pos.angle_to(hor_vec))
                pygame.draw.circle(screen, (255, 0, 0), periapsis_pos, 5)

            # Draw periapsis
            if 'periapsis_pos' in locals():
                pygame.draw.circle(
                    screen,
                    (255, 255, 0),
                    periapsis_pos/meters_per_pixel+pixel_center,
                    5
                )

            ascending = prev_alt < alt
            prev_alt = alt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                with open("angles.bin", "wb") as f:
                    angles.tofile(f)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()