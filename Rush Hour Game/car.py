############################################################
# Helper class
############################################################


class Direction:
    """
    Class representing a direction in 2D world.
    but all other implementations are for you to carry out.
    """
    UP = 1
    DOWN = 2
    RIGHT = 3
    LEFT = 4

    NOT_MOVING = 0

    VERTICAL = 0
    HORIZONTAL = 1

    ALL_DIRECTIONS = (UP, DOWN, LEFT, RIGHT)

############################################################
# Class definition
############################################################


class Car:
    """
    A class representing a car in rush hour game.
    A car is 1-dimensional object that could be laid in either horizontal or
    vertical alignment.
    A car drives on its vertical\horizontal axis back and
    forth until reaching the board's boarders. A car can only drive to an empty
    slot (it can't override another car).
    """

    def __init__(self, color, length, location, orientation):
        # car : ('o', 2, (2, 3), 0)
        """
        A constructor for a Car object
        :param color: A string representing the car's color
        :param length: An int in the range of (2,4) representing the car's length.
        :param location: A list representing the car's head (x, y) location
        :param orientation: An int representing the car's orientation
        """
        self.color = color
        self.length = length
        self.location = location
        self.orientation = orientation

    def locations_list(self):
        """function that return all coordinate that take a car
        return: list of coordinate"""

        locations_list = []
        if self.orientation == Direction.HORIZONTAL:
            for i in range(self.length):
                locations_list.append((self.location[0], self.location[1] + i))

        if self.orientation == Direction.VERTICAL:
            for k in range(self.length):
                locations_list.append((self.location[0] + k, self.location[1]))

        return locations_list



