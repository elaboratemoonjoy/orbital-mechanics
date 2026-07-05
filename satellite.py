from typing import TYPE_CHECKING

from pygame import Vector2, draw
from scipy import constants

from game_object import GameObject

if TYPE_CHECKING:
    from planet import Planet


class Satellite(GameObject):
    def __init__(
        self, 
        position: Vector2 = Vector2(0,0),
        velocity: Vector2 = Vector2(0,0),
        mass: float = 1.0,
        size = 5
    ):
        self.position = position
        self.velocity = velocity
        self.planet: Planet = None
        self.mass = mass
        self.size = size

    def _radius_from_planet(self):
        return Vector2(
            self.position.x - self.planet.position.x,
            self.position.y - self.planet.position.y,
        ).length()

    def _gravity_vector(self):
        ab = Vector2(
            self.position.x - self.planet.position.x,
            self.position.y - self.planet.position.y,
        )
        ab = ab.normalize()
        return ab

    def update(self, dt):
        ab = self._gravity_vector()
        gravitational_pull = (float(constants.G * self.planet.mass)/pow((self._radius_from_planet()*1000), 2))
        ab = ab * gravitational_pull * dt /1000

        self.velocity = self.velocity - ab
        self.position = self.position + (self.velocity * dt)


    def draw(self, screen):
        draw.circle(screen, "yellow", self.position, self.size)