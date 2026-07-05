# Example file showing a circle moving on screen
import pygame
from pygame import Vector2
from scipy import constants

from game_object import GameObject
from object_manager import ObjectManager
from planet import Planet
from orbit import Orbit
from satellite import Satellite

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

# Define objects
planet = Planet(
    mass = 5.972e24,
    position = Vector2(screen.width/2, screen.height/2),
    radius = 10,
    )

satellite = Satellite(
    Vector2(screen.width/2-100, screen.height/2),
    Vector2(0, 60),
)
satellite2 = Satellite(
    Vector2(screen.width/2+200, screen.height/2),
    Vector2(0, 10),
)
object_manager = ObjectManager(
    screen,
    [
        planet,
        satellite,
        satellite2
    ]
)

# Add relations
planet.add_satellite(
    satellite,
)
planet.add_satellite(
    satellite2,
)

clock = pygame.time.Clock()
dt = 0
sim_speed = 2

while running:
    dt = clock.tick(60) / 1000.0 * sim_speed
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    object_manager.update(dt)
    object_manager.draw(screen)

    # flip() the display to put your work on screen
    pygame.display.flip()

pygame.quit()