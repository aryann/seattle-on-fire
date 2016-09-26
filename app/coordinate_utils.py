import config
import math

from google.appengine.api import datastore_types

R_EARTH_METERS = 6371008.8
SEATTLE_TOP_LEFT = (
    datastore_types.GeoPt(47.742476, -122.450239))
SEATTLE_BOTTOM_RIGHT = (
    datastore_types.GeoPt(47.492421, -122.226049))

def calculate_distance(a, b):
    """Returns the equirectangular approximation between two GPS
    coordinates.

    The results are returned as a tuple of (dx, dy) in meters.
    """
    dx = math.radians(b.lon - a.lon) * math.cos(
        math.radians(b.lat + a.lat) / 2)
    dy = math.radians(b.lat - a.lat)
    return dx * R_EARTH_METERS, dy * R_EARTH_METERS


SEATTLE_WIDTH, SEATTLE_HEIGHT = calculate_distance(
    SEATTLE_TOP_LEFT, SEATTLE_BOTTOM_RIGHT)
CANVAS_WIDTH = 500
CANVAS_HEIGHT = int(abs(CANVAS_WIDTH * SEATTLE_HEIGHT / SEATTLE_WIDTH))


def get_relative_placement(point):
    dx, dy = calculate_distance(SEATTLE_TOP_LEFT, point)
    return (int(dx / SEATTLE_WIDTH * CANVAS_WIDTH),
            int(dy / SEATTLE_HEIGHT * CANVAS_HEIGHT))
