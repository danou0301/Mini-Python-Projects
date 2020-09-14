#############################################################
# FILE : ex9.py
# WRITERS : Dan Boujenah , danou0301 , 341339901
#         : Chalom Zemmour, chalomz, 888311081
# EXERCISE : intro2cs ex9 2017-2018
# DESCRIPTION : Asteroid Class
#############################################################
import math


class Asteroid:
    """This class manage asteroids: location, velocity, size"""

    MIN_SIZE = 1
    MAX_SIZE = 3

    MIN_SPEED = 1
    MAX_SPEED = 3
    SIZE_FACTOR = 10
    NORMALIZING_FACTOR = -5

    def __init__(self, position_x, position_y, velocity_x, velocity_y, size):
        """
        Initiation of the Asteroid class
        """

        self._position_x = position_x
        self._position_y = position_y
        self._velocity_x = velocity_x
        self._velocity_y = velocity_y
        self._size = size

    def get_position_x(self):
        """This function returns the position on axis x"""
        return self._position_x

    def set_position_x(self, new_position_x):
        """This function sets a position on axis x"""
        self._position_x = new_position_x

    def get_position_y(self):
        """This function returns the position on axis y"""
        return self._position_y

    def set_position_y(self, new_position_y):
        """This function sets a position on axis y"""
        self._position_y = new_position_y

    def get_velocity_x(self):
        """This function returns the velocity on axis x"""
        return self._velocity_x

    def set_velocity_x(self, new_velocity_x):
        """This function sets a velocity on axis x"""
        self._velocity_x = new_velocity_x

    def get_velocity_y(self):
        """This function returns the velocity on axis y"""
        return self._velocity_y

    def set_velocity_y(self, new_velocity_y):
        """This function sets a velocity on axis y"""
        self._velocity_y = new_velocity_y

    def get_radius(self):
        """This function returns the radius of the asteroid"""
        return (self._size * self.SIZE_FACTOR) + self.NORMALIZING_FACTOR

    def get_size(self):
        """This function returns the size of the asteroid"""
        return self._size

    def set_size(self, new_size):
        """This function sets the size of the asteroid"""
        self._size = new_size

    def has_intersection(self, obj):
        """This function returns True if there is an interaction between
        asteroid and an object(ship or torpedo), if not: False"""
        distance_x = (obj.get_position_x() - self._position_x)**2
        distance_y = (obj.get_position_y() - self._position_y)**2
        distance = math.sqrt(distance_x + distance_y)
        if distance <= self.get_radius() + obj.get_radius():
            return True
        return False
