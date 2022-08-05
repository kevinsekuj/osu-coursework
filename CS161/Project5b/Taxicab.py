# Author: Kevin Sekuj
# Date: 10/27/20
# Description: Program which includes a class named Taxicab and 3 private data
# members holding x and y coordinates, and odometer distance reading "driven"
# by the taxicab.

class Taxicab:
    """Taxicab class with 3 private data members for x and y coordinates
    and odometer reading"""
    def __init__(self, x, y):
        """initializes x and y coordinates, and odometer"""
        self._x_coordinate = x
        self._y_coordinate = y
        self._odometer = 0

    def get_x_coord(self):
        """returns x coord"""
        return self._x_coordinate

    def get_y_coord(self):
        """returns y coord"""
        return self._y_coordinate

    def get_odometer(self):
        """returns odometer reading"""
        return self._odometer

    def move_x(self, distance):
        """adds absolute distance to odometer for x"""
        self._x_coordinate += distance
        self._odometer += abs(distance)

    def move_y(self, distance):
        """adds absolute distance to odometer for y"""
        self._y_coordinate += distance
        self._odometer += abs(distance)
