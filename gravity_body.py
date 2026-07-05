from pygame import Surface, Vector2, draw


class GravityBody():
    def __init__(self, mass: float, position: Vector2, radius: float, screen: Surface, color = "blue"):
        self.mass = mass
        self.position = position
        self.radius = radius
        self.screen = screen
        self.color = color

    def render(self):
        draw.circle(self.screen, self.color, self.position, self.radius)