from typing import NamedTuple

SPEED_OF_SOUND = 343  # m/s


class Point2D(NamedTuple):
    y: int
    x: int

    def __mul__(self, other):
        return Point2D(self.y * other, self.x * other)

    def __sub__(self, other):
        return Point2D(self.y - other, self.x - other)

    def __add__(self, other):
        return Point2D(self.y + other, self.x + other)


class Space:
    dimensions: Point2D

    def __init__(self, size=8):
        self.dimensions = Point2D(size, size)
