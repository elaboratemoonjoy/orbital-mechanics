import math

from pygame import Vector2
from scipy.constants import G


def gravity_accel(body_mass, radius) -> float:
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

    a = gravity_accel(body_mass, radius)

    return a * gravity_vector * delta_time * scale_factor


class PhysicsEngine():
    def __init__(self):
        ...

    def physics_loop(self, dt, physics_hz, bodies):
        raise NotImplementedError()


class ExplicitEuler(PhysicsEngine):
    def __init__(self):
        ...

    def physics_loop(self, dt, physics_hz, bodies):
        ticks_per_dt = physics_hz * (dt)
        tick_dt = dt / ticks_per_dt
        for _ in range(int(ticks_per_dt)):
            kicks = {}

            for cur_body in bodies:
                accumulated_kick = Vector2(0, 0)
                for target_body in bodies:
                    if target_body is cur_body:
                        continue
                    
                    kick = gravity_kick(
                        body_mass=target_body.mass,
                        body_pos=target_body.position,
                        target_pos=cur_body.position,
                        delta_time=tick_dt,
                    )
                    accumulated_kick += kick

                kicks[cur_body] = accumulated_kick
            
            for cur_body in bodies:
                cur_body.position += cur_body.velocity * tick_dt
                cur_body.velocity += kicks[cur_body]


class SympleticEuler(PhysicsEngine):
    def __init__(self):
        ...

    def physics_loop(self, dt, physics_hz, bodies):
        ticks_per_dt = physics_hz * (dt)
        tick_dt = dt / ticks_per_dt
        for _ in range(int(ticks_per_dt)):
            for cur_body in bodies:
                for target_body in bodies:
                    if target_body is cur_body:
                        continue
                    
                    kick = gravity_kick(
                        body_mass=target_body.mass,
                        body_pos=target_body.position,
                        target_pos=cur_body.position,
                        delta_time=tick_dt,
                    )
                    cur_body.velocity += kick
                
                cur_body.position += cur_body.velocity * tick_dt


class LeapfrogVerlet(PhysicsEngine):
    def __init__(self):
        ...

    def _apply_half_gravity(self, cur_body, tick_dt, bodies):
        for target_body in bodies:
            if target_body is cur_body:
                continue

            kick = gravity_kick(
                body_mass=target_body.mass,
                body_pos=target_body.position,
                target_pos=cur_body.position,
                delta_time=tick_dt,
                scale_factor=0.5
            )
            cur_body.velocity += kick

    def physics_loop(self, dt, physics_hz, bodies):
        ticks_per_dt = physics_hz * (dt)
        tick_dt = dt / ticks_per_dt
        for _ in range(int(ticks_per_dt)):

            for cur_body in bodies:
                self._apply_half_gravity(cur_body, tick_dt, bodies)
                
                cur_body.position += cur_body.velocity * tick_dt

                self._apply_half_gravity(cur_body, tick_dt, bodies)
