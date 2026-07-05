from typing import TYPE_CHECKING

from pygame import Surface, Vector2, draw

from game_object import GameObject

if TYPE_CHECKING:
    from satellite import Satellite

class Planet(GameObject):
    def __init__(self, mass: float, position: Vector2, radius: float, color = "blue"):
        self.mass = mass
        self.position = position
        self.radius = radius
        self.color = color
        self.satellites = []

    def add_satellite(self, satellite: Satellite):
        self.satellites.append(satellite)
        satellite.planet = self

    def update(self, dt):
        ...


    def draw(self, screen):
        draw.circle(screen, self.color, self.position, self.radius)