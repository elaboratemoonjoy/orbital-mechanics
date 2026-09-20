from pygame import Vector2
import pygame


class PhysicsObject():
    def __init__(self, mass, size, start_pos, start_vel):
        self.mass = mass
        self.size = size
        self.position: Vector2 = start_pos
        self.velocity: Vector2 = start_vel

    def draw(self, screen, meters_per_pixel):
        draw_size = self.size / meters_per_pixel
        if draw_size < 1:
            draw_size = 1

        pixel_center = Vector2(screen.get_width() / 2, screen.get_height() / 2)
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

    def draw(self, screen, meters_per_pixel):
        draw_size = self.size / meters_per_pixel
        if draw_size < 1:
            draw_size = 1

        diameter = int(draw_size * 2)

        image = pygame.transform.smoothscale(
            self.image,
            (diameter, diameter)
        )

        pixel_center = Vector2(screen.get_width() / 2, screen.get_height() / 2)
        screen.blit(
            image,
            image.get_rect(
                center=(
                    pixel_center.x + self.position.x / meters_per_pixel,
                    pixel_center.y - self.position.y / meters_per_pixel
                )
            )
        )
