#############################################################
# FILE : four_in_a_row.py
# WRITERS : Dan Boujenah , danou0301 , 341339901
#         : Chalom Zemmour, chalomz, 888311081
# EXERCISE : intro2cs ex9 2017-2018
# DESCRIPTION : Four in row game, GUI Class
#############################################################
from game import Game
import tkinter as tki
from communicator import Communicator
import socket
import time
from ai import AI
import sys

SERVER_TITLE = "Server"
CLIENT_TITLE = "Client"
SERVER_ARGS = 3
CLIENT_ARGS = 4
MAX_PORT = 65535
PLAYER_ARG = 1
PORT_ARG = 2
IP_ARG = 3
HUMAN_ARG = 'human'
AI_ARG = 'ai'


class GUI:
    """We defined this class using the tkinter class, here we defined the
    design of the board: colors, visibility, size, mode of operation..."""
    PICTURE_WIDTH = 800
    PICTURE_HEIGHT = 600
    SHIFT_RIGHT = 134
    SHIFT_LEFT = 134
    SHIFT_BOTTOM = 78
    SHIFT_UP = 75
    COIN_WIDTH = 76
    COIN_LENGTH = 90
    COIN_SHIFT = 173
    PLAYER_ONE_TURN_X = 744
    PLAYER_TWO_TURN_X = 58
    PLAYER_TURN_Y = 139
    LINES_LEN = 5
    COLUMN_NUM = 7
    COIN_WIN_NUMBER = 4
    INVALID_COLUMN = 10
    TIME_SLEEP = 0.001
    MOVE_INDEX = 10
    BOARD_IMAGE = 'img/board.png'
    BLUE_COIN_IMAGE = 'img/BLUE.png'
    RED_COIN_IMAGE = 'img/RED.png'
    BLUE_WIN_COIN_IMAGE = 'img/BLUE_WIN.png'
    RED_WIN_COIN_IMAGE = 'img/RED_WIN.png'
    TIE_IMAGE = 'img/Tie.png'
    PLAYER_ONE_NO_TURN_IMAGE = 'img/player_one_no.png'
    PLAYER_TWO_TURN_IMAGE = 'img/player_two_yes.png'

    BOARD_FROM_BOTTOM = PICTURE_HEIGHT - SHIFT_BOTTOM
    BUTTON_LENGTH = int((PICTURE_WIDTH-SHIFT_LEFT-SHIFT_RIGHT)/COLUMN_NUM)

    def __init__(self, parent, port, my_turn, ip=None, ai=None):
        """
        Initiation function of the GUI Class
        :param parent: original board
        :param port: port for communication between computers
        :param my_turn: True if it's the turn of the relevant player
        :param ip: ip address for communication between computers
        """
        self.__parent = parent
        self.__ai = ai
        self.__my_turn = my_turn
        self.__parent.resizable(width=False, height=False)
        self.__game = Game()
        # limits of the board
        self.__canvas = tki.Canvas(self.__parent, width=self.PICTURE_WIDTH,
                                 height=self.PICTURE_HEIGHT)

        self.__background = tki.PhotoImage(file=self.BOARD_IMAGE)
        self.__canvas.create_image(0, 0, anchor=tki.NW, image=self.__background)
        # Anchor NW will position the text so that the reference point
        # coincides with the northwest
        self.__canvas.grid()
        self.__canvas.bind('<Button-1>', self.__callback)

        self.__communicator = Communicator(parent, port, ip)
        self.__communicator.connect()
        # import message
        self.__communicator.bind_action_to_message(self.__handle_message)

        self.__blue_coin = tki.PhotoImage(file=self.BLUE_COIN_IMAGE)
        self.__red_coin = tki.PhotoImage(file=self.RED_COIN_IMAGE)
        self.__blue_coin_win = tki.PhotoImage(file=self.BLUE_WIN_COIN_IMAGE)
        self.__red_coin_win = tki.PhotoImage(file=self.RED_WIN_COIN_IMAGE)
        self.__tie_image = tki.PhotoImage(file=self.TIE_IMAGE)
        # We change a part of the background to indicate the player turn
        self.__player_one_no = tki.PhotoImage(file=self.PLAYER_ONE_NO_TURN_IMAGE)
        self.__one_no = None
        self.__player_two_yes = tki.PhotoImage(file=self.PLAYER_TWO_TURN_IMAGE)
        self.__two_yes = None

        if ip is None and self.__ai:
            column = self.__ai.find_legal_move(self.__game, self.__add_coin)
            self.__communicator.send_message(column)

    def __handle_message(self, column=None):
        """This function allows to add a coin in the screen of the non turn
        player according to the choice of the turn player and it allows the
        next player to play after that"""
        column = int(column)
        if column < self.__game.WIDTH:
            self.__add_coin(column)
            self.__my_turn = not self.__my_turn
        if self.__ai:
            column = self.__ai.find_legal_move(self.__game, self.__add_coin)
            self.__communicator.send_message(column)
            self.__my_turn = not self.__my_turn

    def __callback(self, event):
        """This function allows the player to add a coin according to a *valid*
        column that he has chosen, the "event" value is given from the user
        click according to the function defined in the __init__ it also sends
        to the second player his column choice that will be process in the
        previous handle_message function, and the turn of the actual player
        will be end"""

        position_x = event.x - self.SHIFT_LEFT
        column = position_x//self.BUTTON_LENGTH
        if position_x < 0:
            column = self.INVALID_COLUMN

        if self.__my_turn and column < self.__game.WIDTH:
            self.__add_coin(column)
            self.__communicator.send_message(str(column))
            self.__my_turn = not self.__my_turn

    def __add_coin(self, column):
        """This function call the make_move function that update the game
        status and change the screen displaying according to coin adding"""

        image_coin = None
        if column < self.__game.WIDTH:  # check that is a valid column
            try:
                tuple_move = self.__game.make_move(column)
                # make_move function returns the coordinates of the new coin
                # and the player turn

                if tuple_move[1] == self.__game.PLAYER_ONE:
                    image_coin = self.__blue_coin
                    # display who have to play
                    self.__one_no = self.__canvas.\
                        create_image(self.PLAYER_ONE_TURN_X, self.PLAYER_TURN_Y,
                                     image=self.__player_one_no)
                    self.__two_yes = self.__canvas.\
                        create_image(self.PLAYER_TWO_TURN_X, self.PLAYER_TURN_Y,
                                     image=self.__player_two_yes)

                elif tuple_move[1] == self.__game.PLAYER_TWO:
                    image_coin = self.__red_coin
                    self.__canvas.delete(self.__one_no)
                    self.__canvas.delete(self.__two_yes)

                coin = self.__canvas.\
                    create_image(self.COIN_SHIFT + column * self.COIN_WIDTH,
                                 self.SHIFT_UP, image=image_coin)
                # make move (animation)
                for i in range(int(tuple_move[0][1] * self.COIN_LENGTH /
                                   self.MOVE_INDEX)):
                    self.__canvas.move(coin, 0, self.MOVE_INDEX)
                    time.sleep(self.TIME_SLEEP)
                    self.__canvas.update()

                self.__print_winner()  # Display winner if there is one
            except :
                pass

    def __print_winner(self):
        """When the 4 coins from the same player are aligned, this function
        allows to show on the screen which player won and what"""

        winner = self.__game.get_winner_status()
        if winner:  # if there is the end of the game
            if winner[0] == self.__game.DRAW:
                self.__canvas.create_image(0, 0, anchor=tki.NW, image=self.__tie_image)
                return
            # if someone won
            win_coo = winner[1]
            if winner[0] == str(self.__game.PLAYER_ONE):
                coin_win = self.__blue_coin_win
            else:
                coin_win = self.__red_coin_win

            if winner[2] == self.__game.HORIZONTAL_WINNING:
                for i in range(self.COIN_WIN_NUMBER):
                    self.__canvas.\
                        create_image(self.COIN_SHIFT+(win_coo[0]+i) * self.COIN_WIDTH,
                                     self.BOARD_FROM_BOTTOM - (self.LINES_LEN - win_coo[1])
                                     * self.COIN_LENGTH, image=coin_win)

            elif winner[2] == self.__game.VERTICAL_WINNING:
                for i in range(self.COIN_WIN_NUMBER):
                    self.__canvas.\
                        create_image(self.COIN_SHIFT+win_coo[0] * self.COIN_WIDTH,
                                     self.BOARD_FROM_BOTTOM - (self.LINES_LEN-win_coo[1] - i)
                                     * self.COIN_LENGTH, image=coin_win)

            elif winner[2] == self.__game.DIAGONAL_RIGHT:
                for i in range(self.COIN_WIN_NUMBER):
                    self.__canvas.\
                        create_image(self.COIN_SHIFT+(win_coo[0]+i) * self.COIN_WIDTH,
                                     self.BOARD_FROM_BOTTOM - (self.LINES_LEN-win_coo[1]+i)
                                     * self.COIN_LENGTH, image=coin_win)

            elif winner[2] == self.__game.DIAGONAL_LEFT:
                for i in range(self.COIN_WIN_NUMBER):
                    self.__canvas.\
                        create_image(self.COIN_SHIFT+(win_coo[0]+i) * self.COIN_WIDTH,
                                     self.BOARD_FROM_BOTTOM - (self.LINES_LEN-win_coo[1]-i)
                                     * self.COIN_LENGTH, image=coin_win)


def run_game(arg):
    """According to the console arguments this function run the four in row
    game """

    root = tki.Tk()
    if check_arguments(arg):
        port = int(arg[PORT_ARG])

        if arg[PLAYER_ARG] == HUMAN_ARG:
            if len(arg) == SERVER_ARGS:
                GUI(root, port, True)
                root.title(SERVER_TITLE)
            elif len(arg) == CLIENT_ARGS:
                GUI(root, port, False, arg[IP_ARG])
                root.title(CLIENT_TITLE)

        elif arg[1] == AI_ARG:
            if len(arg) == SERVER_ARGS:
                GUI(root, port, True, ai=AI())
                root.title(SERVER_TITLE)
            elif len(arg) == CLIENT_ARGS:
                GUI(root, port, False, ip=arg[IP_ARG], ai=AI())
                root.title(CLIENT_TITLE)
        root.mainloop()


def check_arguments(args_list):
    """This function check the console arguments"""

    if len(args_list) != SERVER_ARGS and len(args_list) != CLIENT_ARGS or \
            (int(args_list[PORT_ARG]) >= MAX_PORT) or \
            (args_list[PLAYER_ARG] != HUMAN_ARG and args_list[PLAYER_ARG] != AI_ARG):

        print('Illegal program arguments')
        return False

    return True

if __name__ == '__main__':

    run_game(sys.argv)

