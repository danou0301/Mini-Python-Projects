#############################################################
# FILE : ex9.py
# WRITERS : Dan Boujenah , danou0301 , 341339901
#         : Chalom Zemmour, chalomz, 888311081
# EXERCISE : intro2cs ex9 2017-2018
# DESCRIPTION : Torpedo Class
#############################################################


class Torpedo:
    """This class manage torpedo, missile that a ship shoot"""
    ACCELERATION_FACTOR = 2
    TORPEDO_RADIUS = 4
    INITIAL_LIFE_TIME = 0
    LIFE_TIME = 200

    def __init__(self, position_x, position_y, velocity_x, velocity_y, heading,
                 life_time):
        """Initiation of the Class Torpedo"""
        self._position_x = position_x
        self._position_y = position_y
        self._velocity_x = velocity_x
        self._velocity_y = velocity_y
        self._heading = heading
        self._life_time = life_time

    def get_position_x(self):
        """This function returns position on axis x"""
        return self._position_x

    def set_position_x(self, new_position_x):
        """This function sets a position on axis x"""
        self._position_x = new_position_x

    def get_position_y(self):
        """This function returns position on axis y"""
        return self._position_y

    def set_position_y(self, new_position_y):
        """This function sets a position on axis y"""
        self._position_y = new_position_y

    def get_velocity_x(self):
        """This function returns velocity on axis x"""
        return self._velocity_x

    def set_velocity_x(self, new_velocity_x):
        """This function sets a velocity on axis x"""
        self._velocity_x = new_velocity_x

    def get_velocity_y(self):
        """This function returns velocity on axis y"""
        return self._velocity_y

    def set_velocity_y(self, new_velocity_y):
        """This function sets a velocity on axis y"""
        self._velocity_y = new_velocity_y

    def get_heading(self):
        """This function returns angle of the torpedo"""
        return self._heading

    def set_heading(self, new_heading):
        """This function sets an angle to the torpedo"""
        self._heading = new_heading

    def get_radius(self):
        """This function returns the torpedo's radius"""
        return self.TORPEDO_RADIUS

    def get_life_time(self):
        """This function returns the life time of the torpedo"""
        return self._life_time

    def set_life_time(self, life_time):
        """This function sets a life time to the torpedo"""
        self._life_time = life_time
