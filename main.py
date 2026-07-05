# Example file showing a circle moving on screen
import pygame
from pygame import Vector2
from scipy import constants

from gravity_body import GravityBody
from orbit import Orbit
from sattelite import Sattelite

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

def create_segments(points: list[Vector2]):
    segments = []

    from_point = points[0]
    for point in points[1:]:
        segments.append((from_point, point))
        from_point = point

    return segments

G = constants.gravitational_constant 

planet = GravityBody(
    mass = 5.972e24,
    position = Vector2(screen.width/2, screen.height/2),
    radius = 10,
    screen = screen
    )

sattelite = Sattelite(
    Vector2(screen.width/2-200, screen.height/2),
    Vector2(0, 20),
    screen=screen
    )

orbit = Orbit(planet, sattelite, screen)


clock = pygame.time.Clock()
dt = 0
sim_speed = 2
while running:
    dt = clock.tick(120) / 1000.0 * sim_speed
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    orbit.update(dt)
    orbit.visualize()

    planet.render()
    sattelite.render()

    # flip() the display to put your work on screen
    pygame.display.flip()

pygame.quit()