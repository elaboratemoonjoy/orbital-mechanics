from pygame import Vector2, draw

from trail import Trail


class Sattelite():
    def __init__(self, position: Vector2, velocity: Vector2, screen):
        self.trail = Trail()
        self.position = position
        self.mass = 1
        self.velocity = velocity
        self.radius = 5
        self.altitude = 5
        self.screen = screen

    def render(self):
        self.trail.points.append(self.position)
        draw.circle(self.screen, "yellow", self.position, self.radius)
        
        trail = self.trail.create_segments()
        for segment in trail:
            draw.line(self.screen, "grey", segment[0], segment[1])