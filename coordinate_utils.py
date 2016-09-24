import config
import math


def calculate_distance(a, b):
    """Returns the equirectangular approximation between two GPS
    coordinates.

    The inputs a and b should be (lat, lon) tuples in degrees.

    The results are returns as a tuples of (dx, dy) in meters.
    """
    lat_a, lon_a = a
    lat_b, lon_b = b
    dx = math.radians(lon_b - lon_a) * math.cos(
        math.radians(lat_b + lat_a) / 2)
    dy = math.radians(lat_b - lat_a)
    return dx * config.R_EARTH_METERS, dy * config.R_EARTH_METERS
