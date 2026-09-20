import math
import random
import pygame
from pygame import Vector2
import sys

from orbits.body_models import Body, PhysicsObject
from orbits.engine import SimEngine
from orbits.physics import LeapfrogVerlet, SympleticEuler

WHITE = (255, 255, 255)
LIGHT = (150, 150, 250)
DARK = (100, 100, 200)
COLOR_BG_DARK = (5, 2, 18)
WIDTH, HEIGHT = 1280, 720

star_colors = [
    (216, 222, 236),
    (202, 215, 255),
    (255, 191, 0),
]

stars = [
    (
        random.randint(0, WIDTH),  # x coordinate
        random.randint(0, HEIGHT),  # y coordinate
        random.randint(1, 5),  # size
        random.choice(star_colors),
        random.uniform(0.1, 0.5),  # twinkle speed
        random.uniform(0.0, 2 * math.pi),  # random phase offset
    )
    for _ in range(200)
]


def init_sim(physics_engine):
    earth_png = pygame.image.load('orbits/assets/sprites/earth.png')
    moon_png = pygame.image.load('orbits/assets/sprites/moon.png')
    bodies = [
        Body(5.9722e24, 6371 * 1000, Vector2(0, 0), Vector2(0, 0), earth_png),
        PhysicsObject(1000, 10, Vector2(0, (400 + 6371) * 1000), Vector2(8672, 0)),
        Body(7.342e22, 4000 * 1000, Vector2(0, (400000 + 6371) * 1000), Vector2(1000, 0), moon_png),
    ]

    engine = SimEngine(
        physics_engine=physics_engine,
        sim_bodies=bodies,
        fps=120,
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
            int(base_colour[0] * factor),
            int(base_colour[1] * factor),
            int(base_colour[2] * factor),
        )

        pygame.draw.circle(
            surface=surface, 
            color=sparkle_colour, 
            center=(x, y), 
            radius=sparkle_size
        )


def start_menu():
    pygame.init()
    pygame.display.set_caption("Orbital simulator")

    font = pygame.font.Font("orbits/assets/fonts/OCRA.ttf", 32)
    icon = pygame.image.load("orbits/assets/icon.png")
    pygame.display.set_icon(icon)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
        
    buttons_width = 400
    buttons_height = 55
    buttons_left = WIDTH / 2 - buttons_width / 2 

    sympletic_button = pygame.Rect(buttons_left, 220, buttons_width, buttons_height)
    leapfrog_button = pygame.Rect(buttons_left, 290, buttons_width, buttons_height)
    quit_button = pygame.Rect(buttons_left, 360, buttons_width, buttons_height)

    while True:
        current_time = pygame.time.get_ticks() / 1000.0
        
        draw_background(screen, current_time)

        mouse = pygame.mouse.get_pos()

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
            source=sympletic_text, 
            dest=sympletic_text.get_rect(center=sympletic_button.center)
        )
        screen.blit(
            source=leapfrog_text, 
            dest=leapfrog_text.get_rect(center=leapfrog_button.center)
        )
        screen.blit(
            source=quit_text, 
            dest=quit_text.get_rect(center=quit_button.center)
        )

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
