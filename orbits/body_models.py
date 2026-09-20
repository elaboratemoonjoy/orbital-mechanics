from pygame import Vector2


class PhysicsObject():
    def __init__(self, mass, size, start_pos, start_vel):
        self.mass = mass
        self.size = size
        self.position: Vector2 = start_pos
        self.velocity: Vector2 = start_vel
