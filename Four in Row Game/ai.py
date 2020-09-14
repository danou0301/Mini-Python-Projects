#############################################################
# FILE : ai.py
# WRITERS : Dan Boujenah , danou0301 , 341339901
#         : Chalom Zemmour, chalomz, 888311081
# EXERCISE : intro2cs ex9 2017-2018
# DESCRIPTION : AI Class
#############################################################
import random


class AI:

    def find_legal_move(self, g, func, timeout=None):

        column_list = list({key[0]: value for key, value in g.get_board().items()
                            if key[1] == 0 and value == g.EMPTY}.keys())
        if len(column_list) == 0:
            raise Exception("‫‪No‬‬ ‫‪possible‬‬ ‫‪AI‬‬ ‫‪moves‬‬")
        else:
            column = random.choice(column_list)
            func(column)

        return column

