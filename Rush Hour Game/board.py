############################################################
# Imports
############################################################
import game_helper as gh
from car import Car, Direction

############################################################
# Constants
############################################################

MSG_SUCCESS = "A car was added successfully!"
MSG_FAIL = "Error! Car not added"
MSG_NOT_AVAILABLE = "location not available"
DEFAULT_SIZE = 6
EMPTY_LOCATION = '_'
EXIT_SYMBOL = 'E'
RED_CAR_SYMBOL = 'R'

############################################################
# Class definition
############################################################


class Board:
    """
    A class representing a rush hour board.
    """

    def __init__(self, cars, exit_board, size=DEFAULT_SIZE):
        """
        Initialize a new Board object.
        :param cars: A list of cars. @can be empty
        :param exit_board: coordinate of the exit
        :param size: Size of board (Default size is 6).
        """

        self.size = size
        self.cars = cars
        self.exit_board = exit_board

    def add_car(self, car):
        """
        Add a single car to the board.
        :param car: A car object
        :return: True if a car was succesfuly added, or False otherwise.
        """

        for location in car.locations_list():

            if not self.is_free(location):
                print("A car was not added")
                return False

        self.cars.append(car)
        print("A car was added successfully!")
        return True

    def is_free(self, location):
        """
        Check if a given location on the board is free.
        :param location: x and y coordinations of location to be check
        :return: True if location is free, False otherwise
        """
        if not 0 <= location[0] < self.size or not 0 <= location[1] < self.size:
            return False
        for car in self.cars:
            if location in car.locations_list():
                return False

        return True
    
    def move(self, car, direction):
        """
        Move a car in the given direction.
        :param car: A Car object to be moved.
        :param direction: A Direction object representing desired direction
            to move car.
        :return: True if movement was possible and car was moved, False otherwise.
        """
        # implement your code here (and then delete the next line - 'pass')
        pass
    
    def __repr__(self):
        """
        :return: Return a string representation of the board.
        """

        board_list = []

        for index in range(self.size + 1):

            if index < self.size:
                line = [str(index)]
                for i in range(self.size):
                    line.append('_')

            else:
                line = ['-']
                for i in range(self.size):
                    line.append(str(i))

            board_list.append(line)

        if self.exit_board[0] == self.size - 1:
            board_list[self.exit_board[0]+1][self.exit_board[1]+1] = EXIT_SYMBOL
        else:
            board_list[self.exit_board[0]][self.exit_board[1]] = EXIT_SYMBOL

        for car in self.cars:
            for location in car.locations_list():
                    board_list[location[0]][location[1] + 1] = car.color

        board_string = ''
        for line in board_list:
            board_string += str(line) + '\n'

        return board_string




