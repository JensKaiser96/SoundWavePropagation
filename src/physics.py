from typing import NamedTuple

SPEED_OF_SOUND = 343  # m/s


class Point2D(NamedTuple):
    x: int
    y: int


class Space:
    dimensions: Point2D

    def __init__(self, size=8):
        self.dimensions = Point2D(size, size)
