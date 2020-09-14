############################################################
# Imports
############################################################
import game_helper as gh
from car import Car, Direction
from board import Board

############################################################
# Class definition
############################################################
MSG_WELCOME = "Welcome to rush Hour game"
MSG_CHOSEN = "Already chosen color, try again..."
RED_CAR_COLOR = 'R'
RED_CAR_LENGTH = 2



class Game:
    """
    A class representing a rush hour game.
    A game is composed of cars that are located on a square board and a user
    which tries to move them in a way that will allow the red car to get out
    through the exit
    """

    def __init__(self, board):
        """
        Initialize a new Game object.
        :param board: An object of type board
        """
        self.__board = board

    def __single_turn(self):
        """
        Note - this function is here to guide you and it is *not mandatory*
        to implement it. The logic defined by this function must be implemented
        but if you wish to do so in another function (or some other functions)
        it is ok.

        The function runs one round of the game :
            1. Print board to the screen
            2. Get user's input of: what color car to move, and what direction to
                move it.
            2.a. Check the the input is valid. If not, print an error message and
                return to step 2.
            2. Move car according to user's input. If movement failed (trying
                to move out of board etc.), return to step 2. 
            3. Report to the user the result of current round ()
        """

        pass

    def win_game(self, red_car):
        pass

    def __add_red_car(self):
        if self.__board.exit_board[0] == self.__board.size-1:
            location = (0, self.__board.exit_board[1])
            orientation = Direction.VERTICAL
        else:
            location = (self.__board.exit_board[0], self.__board.size - RED_CAR_LENGTH)
            orientation = Direction.HORIZONTAL
        red_car = Car(RED_CAR_COLOR, RED_CAR_LENGTH, location, orientation)
        self.__board.add_car(red_car)

    def play(self):
        """
        The main driver of the Game. Manages the game until completion.
        :return: None
        """
        gh.report(MSG_WELCOME)  # print welcome message
        self.__add_red_car()  # add the red car
        gh.report(self.__board)  # print the empty board
        chosen_color = [RED_CAR_COLOR]
        num_car = gh.get_num_cars()  # ask how much car play with

        for i in range(num_car):
            car_tuple = gh.get_car_input(self.__board.size)
            while car_tuple[0] in chosen_color:
                gh.report(MSG_CHOSEN)
                car_tuple = gh.get_car_input(self.__board.size)

            chosen_color.append(car_tuple[0])
            car = Car(car_tuple[0], car_tuple[1], car_tuple[2], car_tuple[3])
            self.__board.add_car(car)
            print(self.__board)

        while self.win_game(red_car):
            self.__single_turn()
            print(self.__board)

        gh.report_game_over()




############################################################
# An example usage of the game
############################################################
if __name__ == "__main__":

    board = Board([], [3, 0])  # list of cars and the exit
    game = Game(board)
    game.play()
