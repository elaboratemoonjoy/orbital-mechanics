from pygame import Vector2
from scipy.constants import G
import math


EARTH_MASS_KG = 5.9722e24 
EARTH_RADIUS_KM = 6371


def gravity_accel(body_mass, radius) -> float:
    """
    a = GM/r²

    Args
        :param float body_mass: The mass of the orbital center in Kg (single point approximation)
        :param float body_radius: Radius from center of body in Km (assuming perfect sphere)
        
    Returns:
        float: gravitational acceleration produced by body as a scalar of m/s²
  
    """
    
    meters_from_center = (radius) * 1000

    return (G*body_mass)/math.pow(meters_from_center, 2)


def gravity_kick(body_mass, body_radius, body_vector: Vector2, altitude, dt = 1):
    """
    Time based application of :func:`gravity_accel`

    Args
        :param float body_mass: The mass of the orbital center in Kg (single point approximation)
        :param float body_radius: Radius of body in Km (assuming perfect sphere)
        :param float altitude: Height above surface in Km (assuming perfect sphere)
        :param int dt: Delta time (change of time) since last kick in ms
        
    Returns:
        float: gravitational acceleration produced by body as a scalar of m/s², scaled by delta time
  
    """
    
    if not body_vector.is_normalized():
        raise ValueError("'body_vector' must be a normalized 2d vector")

    return gravity_accel(body_mass, body_radius + altitude) * body_vector * dt