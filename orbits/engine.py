import math
import random
import pygame
from pygame import Vector2

from orbits.body_models import PhysicsObject
from orbits.physics import PhysicsEngine

METERS_PER_PIXEL = (6371 * 1000) / 8
WIDTH, HEIGHT = 1920, 1080
COLOR_BG_DARK = (0, 0, 5)

star_colors = [
    (216, 222, 236),
    (202, 215, 255),
    (255, 191, 0),
]

stars = [
    (
        random.randint(0, WIDTH),  # x coordinate
        random.randint(0, HEIGHT),  # y coordinate
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
            int(base_colour[0] * factor * 0.6),
            int(base_colour[1] * factor * 0.6),
            int(base_colour[2] * factor * 0.6),
        )

        pygame.draw.circle(
            surface=surface, 
            color=sparkle_colour, 
            center=(x, y), 
            radius=sparkle_size
        )


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

        pygame.init()
        self.running = True
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        clock = pygame.time.Clock()
        
        dt = (1 / self.fps) * self.time_warp
        font = pygame.font.Font(None, 16)

        expected_frametime = (1 / self.fps) * 1000

        while self.running:
            frametime = clock.tick_busy_loop(self.fps)

            current_time = pygame.time.get_ticks() / 1000.0
            draw_background(screen, current_time)

            text = f"{clock.get_fps():2.0f} FPS"
            if not frametime <= expected_frametime:
                text += f" sim can't keep up {frametime}ms"
            fps_text = font.render(text, False, (255, 255, 255))

            screen.blit(fps_text, (20, 20))

            self.physics_engine.physics_loop(
                dt=dt, 
                physics_hz=self.physics_hz, 
                bodies=self.sim_bodies
            )

            for body in self.sim_bodies:
                body.draw(
                    screen, 
                    meters_per_pixel=METERS_PER_PIXEL
                )

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False
            
        pygame.quit()
