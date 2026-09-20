import math
import random

import pygame
from pygame import Vector2
from orbits.body_models import PhysicsObject
from orbits.physics import PhysicsEngine

FPS = 60
METERS_PER_PIXEL = (6371 * 1000) / 5
WIDTH, HEIGHT = 1280, 720
COLOR_BG_DARK = (0, 0, 5)

star_colors = [
    (216, 222, 236),  # B-Type (Blue-White)
    (202, 215, 255),  # A-Type (Pure White)
    (255, 191, 0),  # G-Type (Yellow)
]

stars = [
    (
        random.randint(0, WIDTH), 
        random.randint(0, HEIGHT), 
        random.randint(1, 2),  # size
        random.choice(star_colors),
        random.uniform(0.5, 2),  # twinkle speed
        random.uniform(0.0, 2 * math.pi),  # random phase offset
    )
    for _ in range(200)
]


def draw_background(surface, current_time):
    surface.fill(COLOR_BG_DARK)

    for star in stars:
        x, y, size, base_colour, speed, offset = star

        factor = 0.7 + 0.3 * math.sin(current_time * speed + offset)

        sparkle_size = factor * size

        if sparkle_size < 1:
            sparkle_size = 1

        sparkle_colour = (
            min(255, int(base_colour[0] * factor * 0.6)),
            min(255, int(base_colour[1] * factor * 0.6)),
            min(255, int(base_colour[2] * factor * 0.6)),
        )

        pygame.draw.circle(surface, sparkle_colour, (x, y), sparkle_size)


class SimEngine():
    def __init__(
        self, 
        physics_engine: PhysicsEngine,
        sim_bodies: list[PhysicsObject],
        fps: int,
        time_warp: int,
        physics_hz: int,
    ):
        self.physics_engine = physics_engine
        self.sim_bodies = sim_bodies
        self.fps = fps
        self.time_warp = time_warp
        self.physics_hz = physics_hz
        self.running = False

    def start(self):
        self.running = True
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        clock = pygame.time.Clock()
        pixel_center = Vector2(screen.get_width() / 2, screen.get_height() / 2)
        dt = (1 / self.physics_hz) * self.time_warp

        while self.running:
            clock.tick(FPS)

            current_time = pygame.time.get_ticks() / 1000.0
            draw_background(screen, current_time)

            self.physics_engine.physics_loop(
                dt=dt, 
                physics_hz=self.physics_hz, 
                bodies=self.sim_bodies
            )

            for body in self.sim_bodies:
                size = body.size / METERS_PER_PIXEL
                if size < 1:
                    size = 1
                pygame.draw.circle(
                    screen, 
                    pygame.Color("green"), 
                    Vector2(
                        pixel_center.x + (body.position.x / METERS_PER_PIXEL),
                        pixel_center.y - (body.position.y / METERS_PER_PIXEL)
                    ),
                    size
                )

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False
            
        pygame.quit()
