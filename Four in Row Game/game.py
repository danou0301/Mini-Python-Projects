#############################################################
# FILE : ex12.py
# WRITERS : Dan Boujenah , danou0301 , 341339901
#         : Chalom Zemmour, chalomz, 888311081
# EXERCISE : intro2cs ex9 2017-2018
# DESCRIPTION : Game Class
#############################################################


class Game:
    """In this class, we defined the internal logic of the game without
    displaying anything"""

    PLAYER_ONE = 0
    PLAYER_TWO = 1
    DRAW = 2
    WIDTH = 7
    HEIGHT = 6
    COIN_WIN_NUMBER = 4
    EMPTY = '_'
    VERTICAL_WINNING = 'V'
    HORIZONTAL_WINNING = 'H'
    DIAGONAL_RIGHT = 'DR'
    DIAGONAL_LEFT = 'DL'

    def __init__(self):
        """Initiation function: we define only the board as a dictionary,
        the player turn, the Winner if there is one and the board dimensions"""

        self.__player_one_play = True
        self.__winner = None  # composed by three arguments: winner, position of
                            # min coin that win and the win direction
        self.__board = {(x, y): self.EMPTY for x in range(self.WIDTH)
                      for y in range(self.HEIGHT)}

    def make_move(self, column):
        """Make a move, turn one in two the player and return the position of
        the new coin and which player add it"""

        if not self.__winner:  # if there is no winner continue the game
            new_coin = None
            for y in range(self.HEIGHT-1, -1, -1):
                # check if the position is empty, if not check on the upper
                # line
                if self.__board[(column, y)] == self.EMPTY:
                    if self.__player_one_play:
                        self.__board[(column, y)] = self.PLAYER_ONE
                        new_coin = (column, y), self.PLAYER_ONE
                    else:
                        self.__board[(column, y)] = self.PLAYER_TWO
                        new_coin = (column, y), self.PLAYER_TWO

                    # check if there is a winner
                    self.__winner = self.__winner_status()
                    # change the turn
                    self.__player_one_play = not self.__player_one_play
                    break

                if y == 0:  # in case the column is full
                    raise Exception('Illegal move')
            return new_coin
        # if someone won and the user want to add an other coin return error
        else:
            raise Exception('Illegal move')

    def __winner_status(self):
        """This function return the winner, position of min coin that win and
        the win direction"""
        # str() to avoid the case of 0 return False
        if self.__horizontal_winner():
            return str(self.get_current_player()), min(self.__horizontal_winner()),\
                   self.HORIZONTAL_WINNING
        elif self.__vertical_winner():
            return str(self.get_current_player()), min(self.__vertical_winner()),\
                   self.VERTICAL_WINNING
        elif self.__diagonal_left():
            return str(self.get_current_player()), min(self.__diagonal_left()),\
                   self.DIAGONAL_LEFT
        elif self.__diagonal_right():
            return str(self.get_current_player()), min(self.__diagonal_right()),\
                   self.DIAGONAL_RIGHT

        # in case the board is full and no one win return Tie
        elif self.EMPTY not in self.__board.values():
            return self.DRAW,

    def __horizontal_winner(self):
        """Helper function that checks the present of 4 coins from the same
        player in horizontal direction and return coordinates of the winning
        coins"""
        for y in range(self.HEIGHT):
            winning = []  # reset the list for the next line
            for x in range(self.WIDTH):
                if self.__board[x, y] == self.get_current_player():
                    winning.append((x, y))
                    if len(winning) == self.COIN_WIN_NUMBER:
                        return winning
                else:
                    winning = []

    def __vertical_winner(self):
        """Helper function that checks the present of 4 coins from the same
        player in vertical direction and return coordinates of the winning
        coins"""

        for x in range(self.WIDTH):
            winning = []  # reset the list for the next column
            for y in range(self.HEIGHT):
                if self.__board[x, y] == self.get_current_player():
                    winning.append((x, y))
                    if len(winning) == self.COIN_WIN_NUMBER:
                        return winning
                else:
                    winning = []

    def __diagonal_left(self):
        """Helper function that checks the present of 4 coins from the same
        player in left diagonal direction and return coordinates of the winning
        coins"""

        for column_i in range(self.WIDTH-1):
            sx = max(column_i-2, 0)
            sy = abs(min(column_i-2, 0))

            winning = []
            for line_i in range(self.HEIGHT):
                x = sx + line_i
                y = sy + line_i
                if x < 0 or y < 0 or x >= self.WIDTH or y >= self.HEIGHT:
                    continue
                if self.__board[x, y] == self.get_current_player():
                    winning.append((x, y))
                    if len(winning) == self.COIN_WIN_NUMBER:
                        return winning
                else:
                    winning = []

    def __diagonal_right(self):
        """Helper function that checks the present of 4 coins from the same
        player in right diagonal direction and return coordinates of winning
        coins"""

        for cx in range(self.WIDTH-1):
            sx = self.WIDTH-1-max(cx-2, 0)
            sy = abs(min(cx-2, 0))
            winning = []
            for cy in range(self.HEIGHT):
                x = sx-cy
                y = sy+cy
                if x < 0 or y < 0 or x >= self.WIDTH or y >= self.HEIGHT:
                    continue
                if self.__board[x, y] == self.get_current_player():
                    winning.append((x, y))
                    if len(winning) == self.COIN_WIN_NUMBER:
                        return winning
                else:
                    winning = []

    def get_winner(self):
        """return only the winner identity according to the exercise
        requirement"""
        if self.__winner:
            return self.__winner[0]

    def get_winner_status(self):
        """This function return the winner detail"""
        return self.__winner

    def get_board(self):
        """This function return the board dictionary"""
        return self.__board

    def get_player_at(self, row, col):
        """This function returns the identity of the player (or None) that
        occupy the position (row,col)"""

        if self.__board[(row, col)] != self.EMPTY:
            return self.__board[(row, col)]
        else:
            return None

    def get_current_player(self):
        """This function return who is the current player"""
        if self.__player_one_play:
            return self.PLAYER_ONE
        else:
            return self.PLAYER_TWO
