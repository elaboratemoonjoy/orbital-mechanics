import math
import random

import pygame
from pygame import Vector2
import sys

from orbits.body_models import PhysicsObject
from orbits.engine import SimEngine
from orbits.physics import LeapfrogVerlet, SympleticEuler

WHITE = (255, 255, 255)
LIGHT = (150, 150, 250)
DARK = (100, 100, 200)
BG = (60, 25, 60)
COLOR_BG_DARK = (5, 2, 18)
WIDTH, HEIGHT = 1280, 720

star_colors = [
    (216, 222, 236),  # B-Type (Blue-White)
    (202, 215, 255),  # A-Type (Pure White)
    (255, 191, 0),  # G-Type (Yellow)
]


stars = [
    (
        random.randint(0, WIDTH), 
        random.randint(0, HEIGHT), 
        random.randint(1, 5),  # size
        random.choice(star_colors),
        random.uniform(0.1, 0.5),  # twinkle speed
        random.uniform(0.0, 2 * math.pi),  # random phase offset
    )
    for _ in range(200)
]


def init_sim(physics_engine):
    bodies = [
        PhysicsObject(5.9722e24, 6371 * 1000, Vector2(0, 0), Vector2(0, 0)),
        PhysicsObject(1000, 10, Vector2(0, (400 + 6371) * 1000), Vector2(8672, 0)),
        PhysicsObject(7.342e22, 6371 * 1000, Vector2(0, (400000 + 6371) * 1000), Vector2(1000, 0)),
    ]

    engine = SimEngine(
        physics_engine=physics_engine,
        sim_bodies=bodies,
        fps=60,
        time_warp=1000,
        physics_hz=60
    )

    engine.start()


def draw_background(surface, current_time):
    surface.fill(COLOR_BG_DARK)

    for star in stars:
        x, y, size, base_colour, speed, offset = star

        factor = 0.7 + 0.3 * math.sin(current_time * speed + offset)

        sparkle_size = factor * size

        if sparkle_size < 1:
            sparkle_size = 1

        sparkle_colour = (
            min(255, int(base_colour[0] * factor)),
            min(255, int(base_colour[1] * factor)),
            min(255, int(base_colour[2] * factor)),
        )

        pygame.draw.circle(surface, sparkle_colour, (x, y), sparkle_size)


def start_menu():
    pygame.init()
    font = pygame.font.Font("orbits/fonts/OCRA.ttf", 32)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Orbital simulator")

    while True:

        screen.fill(BG)
        mouse = pygame.mouse.get_pos()

        current_time = pygame.time.get_ticks() / 1000.0
        draw_background(screen, current_time)

        buttons_width = 400
        buttons_height = 55
        buttons_left = WIDTH / 2 - buttons_width / 2 

        sympletic_button = pygame.Rect(buttons_left, 220, buttons_width, buttons_height)
        leapfrog_button = pygame.Rect(buttons_left, 290, buttons_width, buttons_height)
        quit_button = pygame.Rect(buttons_left, 360, buttons_width, buttons_height)

        pygame.draw.rect(
            surface=screen, 
            color=LIGHT if sympletic_button.collidepoint(mouse) else DARK, 
            rect=sympletic_button, 
            border_radius=10
        )
        pygame.draw.rect(
            surface=screen, 
            color=LIGHT if leapfrog_button.collidepoint(mouse) else DARK, 
            rect=leapfrog_button, 
            border_radius=10
        )
        pygame.draw.rect(
            surface=screen, 
            color=LIGHT if quit_button.collidepoint(mouse) else DARK, 
            rect=quit_button, 
            border_radius=10
        )

        sympletic_text = font.render("Symplectic Euler", True, WHITE)
        leapfrog_text = font.render("Leapfrog Verlet", True, WHITE)
        quit_text = font.render("Quit", True, WHITE)

        screen.blit(
            sympletic_text, sympletic_text.get_rect(center=sympletic_button.center)
        )
        screen.blit(leapfrog_text, leapfrog_text.get_rect(center=leapfrog_button.center))
        screen.blit(quit_text, quit_text.get_rect(center=quit_button.center))

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                if sympletic_button.collidepoint(mouse):
                    pygame.quit()
                    init_sim(SympleticEuler())
                    sys.exit()

                if leapfrog_button.collidepoint(mouse):
                    pygame.quit()
                    init_sim(LeapfrogVerlet())
                    sys.exit()

                if quit_button.collidepoint(mouse):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


start_menu()
