from pygame import Vector2
import pygame


class PhysicsObject():
    def __init__(self, mass, size, start_pos, start_vel):
        self.mass = mass
        self.size = size
        self.position: Vector2 = start_pos
        self.velocity: Vector2 = start_vel

    def draw(self, screen, meters_per_pixel, pixel_center):
        draw_size = self.size / meters_per_pixel
        if draw_size < 1:
            draw_size = 1
        
        pygame.draw.circle(
            screen, 
            pygame.Color("green"), 
            Vector2(
                pixel_center.x + (self.position.x / meters_per_pixel),
                pixel_center.y - (self.position.y / meters_per_pixel)
            ),
            draw_size
        )


class Body(PhysicsObject):
    def __init__(self, mass, size, position, velocity, image):
        super().__init__(mass, size, position, velocity)
        self.image = image

    def draw(self, screen, meters_per_pixel, pixel_center):
        draw_size = self.size / meters_per_pixel
        if draw_size < 1:
            draw_size = 1

        diameter = int(draw_size * 2)

        image = pygame.transform.smoothscale(
            self.image,
            (diameter, diameter)
        )

        screen.blit(
            image,
            image.get_rect(
                center=(
                    pixel_center.x + self.position.x / meters_per_pixel,
                    pixel_center.y - self.position.y / meters_per_pixel
                )
            )
        )


class Satellite(PhysicsObject):
    def __init__(self, mass, size, position, velocity):
        super().__init__(mass, size, position, velocity)
        self.trail = [position.copy()]
        self.trail_length = 50

    def draw(self, screen, meters_per_pixel, pixel_center):
        draw_size = self.size / meters_per_pixel
        if draw_size < 1:
            draw_size = 1

        pygame.draw.circle(
            screen, 
            pygame.Color("green"), 
            Vector2(
                pixel_center.x + (self.position.x / meters_per_pixel),
                pixel_center.y - (self.position.y / meters_per_pixel)
            ),
            draw_size
        )

        start = self.trail[0]
        for element in self.trail[1:]:
            pygame.draw.line(
                surface=screen,
                color=pygame.Color("white"), 
                start_pos=Vector2(
                    pixel_center.x + (start.x / meters_per_pixel),
                    pixel_center.y - (start.y / meters_per_pixel)
                ), 
                end_pos=Vector2(
                    pixel_center.x + (element.x / meters_per_pixel),
                    pixel_center.y - (element.y / meters_per_pixel)
                )
            )
            start = element

        if len(self.trail) >= self.trail_length:
            del self.trail[0]

        self.trail.append(self.position.copy())
