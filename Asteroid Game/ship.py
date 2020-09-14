#############################################################
# FILE : ex9.py
# WRITERS : Dan Boujenah , danou0301 , 341339901
#         : Chalom Zemmour, chalomz, 888311081
# EXERCISE : intro2cs ex9 2017-2018
# DESCRIPTION : Ship Class
#############################################################


class Ship:
    """This class manage the ship: location, heading, velocity, lives"""
    MAX_LIVES = 3
    SHIP_RADIUS = 1
    INITIAL_VELOCITY = 0.0
    INITIAL_HEADING = 0.0

    def __init__(self, position_x, position_y, velocity_x, velocity_y, heading,
                 lives):
        """Initiation of the Class Ship"""
        self._position_x = position_x
        self._position_y = position_y
        self._velocity_x = velocity_x
        self._velocity_y = velocity_y
        self._heading = heading
        self._lives = lives

    def get_position_x(self):
        """This function returns the position on axis x"""
        return self._position_x

    def set_position_x(self, new_position_x):
        """This function sets position on axis x"""
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

    def get_heading(self):
        """This function returns the angle of the ship"""
        return self._heading

    def set_heading(self, new_heading):
        """This function sets an angle value for the ship"""
        self._heading = new_heading

    def get_radius(self):
        """This function returns the ship's radius"""
        return self.SHIP_RADIUS

    def get_lives(self):
        """This function returns the number of lives"""
        return self._lives

    def set_lives(self, number_of_lives):
        """This function sets a number of lives"""
        self._lives = number_of_lives
