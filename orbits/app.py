import math

import pygame
from pygame import Vector2
from . import physmath

def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True

    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)

    earth_pos = Vector2(
        screen.get_width()/2, # X
        screen.get_height()/2, # Y
    )

    sat_pos = Vector2(
        screen.get_width()/2 - 200, # X
        screen.get_height()/2, # Y
    )   
    sat_vel = Vector2(0, 7.78)

    clock = pygame.time.Clock()

    while running:

        dt = clock.tick(100) / 1000

        screen.fill("black")


        pygame.draw.circle(
            screen, 
            BLUE, 
            earth_pos,
            screen.get_height()/20 # size
        )

        pygame.draw.circle(
            screen, 
            GREEN, 
            sat_pos,
            screen.get_height()/200 # size
        )

        #update sat velocity
        grav_kick = physmath.gravity_kick(
            physmath.EARTH_MASS_KG,
            physmath.EARTH_RADIUS_KM,
            (earth_pos - sat_pos).normalize(),
            earth_pos.distance_to(sat_pos),
            dt
        )

        sat_vel += grav_kick

        # update sat position
        sat_pos += sat_vel
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()