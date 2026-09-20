import math
import sys
import pygame
from pygame import Vector2

from scipy.constants import G


class PhysicsObject():
    def __init__(self, mass, size, start_pos, start_vel):
        self.mass = mass
        self.size = size
        self.position: Vector2 = start_pos
        self.velocity: Vector2 = start_vel


class PhysicsEngine():

    def __init__(self, phys_objects: list[PhysicsObject]):
        self._phys_objects = phys_objects

    def physics_loop(self, dt, phys_hz):
        raise NotImplementedError()


class SympleticEuler(PhysicsEngine):

    def gravity_accel(self, body_mass, radius) -> float:
        """
        a = GM/r²

        Args
            :param float body_mass: The mass of the orbital center in Kg (single point approximation)
            :param float body_radius: Radius from center of body in meters (assuming perfect sphere)
            
        Returns:
            float: gravitational acceleration produced by body as a scalar of m/s²
    
        """

        return (G * body_mass) / math.pow(radius, 2)
    
    def gravity_kick(
            self,
            body_mass: float,
            body_pos: Vector2, 
            target_pos: Vector2, 
            delta_time=1.0, 
            scale_factor=1.0
    ):
        """
        Time based application of :func:`gravity_accel`

        Args
            :param float body_mass: The mass of the orbital center in Kg (single point approximation)
            :param vector2 body_pos: Position of orbital center as vector2
            :param vector2 target_pos: Position of sattelite
            :param float delta_time: Delta time (change of time) since last kick in ms
            :param float scale_factor: How much of the gravity should be applied. For an example for leapfrog you do 0.5
            
        Returns:
            float: gravitational acceleration produced by body as a scalar of m/s², scaled by delta time
    
        """
        gravity_vector = (body_pos - target_pos).normalize()

        radius = body_pos.distance_to(target_pos)

        a = self.gravity_accel(body_mass, radius)

        return a * gravity_vector * delta_time * scale_factor

    def physics_loop(self, dt, phys_hz):
        phys_frames_for_dt = phys_hz * (dt)
        phys_dt = dt / phys_frames_for_dt
        for _ in range(int(phys_frames_for_dt)):

            for cur_obj in self._phys_objects:

                for target in self._phys_objects:
                    if target is cur_obj:
                        continue
                    
                    kick = self.gravity_kick(
                        body_mass=target.mass,
                        body_pos=target.position,
                        target_pos=cur_obj.position,
                        delta_time=phys_dt,
                    )
                    cur_obj.velocity += kick
                
                cur_obj.position += cur_obj.velocity * phys_dt


class LeapfrogVerlet(PhysicsEngine):

    def gravity_accel(self, body_mass, radius) -> float:
        """
        a = GM/r²

        Args
            :param float body_mass: The mass of the orbital center in Kg (single point approximation)
            :param float body_radius: Radius from center of body in meters (assuming perfect sphere)
            
        Returns:
            float: gravitational acceleration produced by body as a scalar of m/s²
    
        """

        return (G * body_mass) / math.pow(radius, 2)
    
    def gravity_kick(
            self,
            body_mass: float,
            body_pos: Vector2, 
            target_pos: Vector2, 
            delta_time=1.0, 
            scale_factor=1.0
    ):
        """
        Time based application of :func:`gravity_accel`

        Args
            :param float body_mass: The mass of the orbital center in Kg (single point approximation)
            :param vector2 body_pos: Position of orbital center as vector2
            :param vector2 target_pos: Position of sattelite
            :param float delta_time: Delta time (change of time) since last kick in ms
            :param float scale_factor: How much of the gravity should be applied. For an example for leapfrog you do 0.5
            
        Returns:
            float: gravitational acceleration produced by body as a scalar of m/s², scaled by delta time
    
        """
        gravity_vector = (body_pos - target_pos).normalize()

        radius = body_pos.distance_to(target_pos)

        a = self.gravity_accel(body_mass, radius)

        return a * gravity_vector * delta_time * scale_factor

    def _apply_half_gravity(self, cur_obj, phys_dt):
        for target in self._phys_objects:
            if target is cur_obj:
                continue
            
            kick = self.gravity_kick(
                body_mass=target.mass,
                body_pos=target.position,
                target_pos=cur_obj.position,
                delta_time=phys_dt,
                scale_factor=0.5
            )
            cur_obj.velocity += kick

    def physics_loop(self, dt, phys_hz):
        phys_frames_for_dt = phys_hz * (dt)
        phys_dt = dt / phys_frames_for_dt
        for _ in range(int(phys_frames_for_dt)):

            for cur_obj in self._phys_objects:
                self._apply_half_gravity(cur_obj, phys_dt)
                
                cur_obj.position += cur_obj.velocity * phys_dt

                self._apply_half_gravity(cur_obj, phys_dt)


FPS = 60
METERS_PER_PIXEL = (6371 * 1000) / 5


def main():
    pygame.init()

    phys_objs = [
        PhysicsObject(5.9722e24, 6371 * 1000, Vector2(0, 0), Vector2(0, 0)),
        PhysicsObject(1000, 10, Vector2(0, (400 + 6371) * 1000), Vector2(8672, 0)),
        PhysicsObject(7.342e22, 6371 * 1000, Vector2(0, (400000 + 6371) * 1000), Vector2(1000, 0)),
    ]

    physics_engine = SympleticEuler(phys_objs)
    physics_engine = LeapfrogVerlet(phys_objs)

    physics_hz = 60
    time_warp = 12000
    dt = (1 / physics_hz) * time_warp

    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    pixel_center = Vector2(screen.get_width() / 2, screen.get_height() / 2)

    running = True
    while running:
        clock.tick(FPS)
        screen.fill("black")

        physics_engine.physics_loop(dt, physics_hz)

        for obj in physics_engine._phys_objects:
            size = obj.size / METERS_PER_PIXEL
            if size < 1:
                size = 1
            pygame.draw.circle(
                screen, 
                pygame.Color("green"), 
                Vector2(
                    pixel_center.x + (obj.position.x / METERS_PER_PIXEL),
                    pixel_center.y - (obj.position.y / METERS_PER_PIXEL)
                ),
                size
            )
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
        
    pygame.quit()


if __name__ == "__main__":
    main()
