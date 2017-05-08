from enum import Enum


class Direction(str, Enum):
    NORTH = 'N - North'
    EAST = 'E - East'
    SOUTH = 'S - South'
    WEST = 'W - West'

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            order = [Direction.WEST, Direction.NORTH, Direction.EAST, Direction.SOUTH]
            return order.index(self) < order.index(other)
