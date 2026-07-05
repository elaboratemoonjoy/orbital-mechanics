from typing import TYPE_CHECKING

from numpy import sqrt
from pygame import Surface, Vector2, draw

if TYPE_CHECKING:
    from planet import GravityBody
    from satellite import Sattelite
from scipy import constants


class Orbit():
    def __init__(self, body: GravityBody, sattelite: Sattelite, screen):
        self.body: GravityBody = body
        self.sattelite: Sattelite = sattelite
        self.screen: Surface = screen
        self.sattelite.altitude = self._vector_to_vector(body.position, sattelite.position).length()

    def _vector_to_vector(self, vector1, vector2):
        return Vector2(
            vector1.x - vector2.x,
            vector1.y - vector2.y,
        )

    def _gravity_vector(self):
        ab = Vector2(
            self.sattelite.position.x - self.body.position.x,
            self.sattelite.position.y - self.body.position.y,
        )
        ab = ab.normalize()
        return ab

    def draw(self):
        draw.line(self.screen, "green", self.body.position, self.sattelite.position)
        draw.line(self.screen, "blue", self.sattelite.position, self.sattelite.position + self.sattelite.velocity)


    def update(self, dt):
        ab = self._gravity_vector()
        gravitational_pull = (float(constants.G * self.body.mass * self.sattelite.mass)/pow(self.sattelite.altitude*1000, 2))
        ab = ab * (gravitational_pull/self.sattelite.mass/1000) * dt

        self.sattelite.velocity = self.sattelite.velocity - ab
        self.sattelite.position = self.sattelite.position + (self.sattelite.velocity * dt)
