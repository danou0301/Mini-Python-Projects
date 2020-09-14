#############################################################
# FILE : ex5.py
# WRITERS : Dan Boujenah , danou0301 , 341339901
#         : Chalom Zemmour, chalomz, 888311081
# EXERCISE : intro2cs ex5 2017-2018
# DESCRIPTION : Crossword3d
# Find words into a several matrix fictitiously ordered into 3d, and return
# them into an output file using the Linux interface
#############################################################

import crossword
import os
import sys

HORIZONTAL = 'a'
VERTICAL_B = 'b'
VERTICAL_C = 'c'
ALL_2d_DIRECTIONS = 'udlrwxyz'
LIST_DIRECTION = [HORIZONTAL, VERTICAL_B, VERTICAL_C]
MATRIX_SEPARATOR = "***"
EMPTY_STRING = ""
NUMBER_OF_ARGUMENTS = 4
WORD_FILE_ARGUMENT = 1
MAT_FILE_ARGUMENT = 2
OUTPUT_FILE_ARGUMENT = 3
DIRECTION_ARGUMENT = 4
WRITE = 'w'
READ = 'r'

INCREASE = 1
NEW_LINE = '\n'
INVALID_MESSAGE = "ERROR: invalid number of parameters. Please enter word" \
                  "_file matrix_file output_file directions"


def cut_mat_string(mat3d):
    """Convert every group of lines  from mat3d to a list contained in a huge
    list"""
    mat_cut = []
    mat_line = []

    for line3d in mat3d:
        if line3d != MATRIX_SEPARATOR:
            mat_line.append(line3d)
        else:  # if the line is '***' we are already read all the 2d matrix
            mat_cut.append(mat_line)
            mat_line = []
    mat_cut.append(mat_line)
    return mat_cut


def column_b(mat_string_3d):
    """This function arranges the matrices that we obtained from the previous
    function and convert it into columnar reading"""

    cut_mat = []  # final form
    words_list = []

    list_3d = cut_mat_string(mat_string_3d)

    for i in range(len(list_3d[0])):
        # put the first line of a matrix with the first line of a other matrix
        # and the second line...

        for mat in list_3d:
            words_list.append(mat[i])

        cut_mat.append(words_list)
        words_list = []

    return cut_mat


def column_c(mat_string_3d):
    """This function also convert the direction reading of the matrices but in
    an other way and from the mat_3d file directly for more convenience"""

    letter_list = []
    words_list = []
    cut_mat = []
    mat_count = 0
    mat_number = mat_string_3d.count(MATRIX_SEPARATOR)

    for i in range(len(mat_string_3d[0])):
        # length of line, i is index of a letter in a line

        for mat_line in mat_string_3d:

            if mat_line != MATRIX_SEPARATOR:
                letter_list.append(list(mat_line)[i])
            else:
                mat_count += INCREASE
                words_list.append(EMPTY_STRING.join(letter_list))
                letter_list = []  # reset for the new line

            if mat_number > 1:
                # check if we are reversed all the matrix
                if mat_number == mat_count and len(letter_list) == len(words_list[0]):

                    mat_count = 0
                    words_list.append(EMPTY_STRING.join(letter_list))
                    cut_mat.append(words_list)

                    # reset for the next index
                    words_list = []
                    letter_list = []
                    break
            else:
                cut_mat.append(letter_list)
                letter_list = []

    return cut_mat


def run(mat_string_3d, directions, words_list):
    """In this function, we check one one the word_list and check if those are
    present in the mat_string list according to the directions letters ordered
    """

    result_3d = []
    result_lst = []
    index_lst = []

    if not mat_string_3d:
        # if nothing in mat_3d file, we don't want an error, the program will
        # return an empty output file
        return result_3d
    else:

        for index in directions:
            if index not in index_lst:
                # Create a list of index to avoid the possibility to check
                # more than once the direction if the user taped it twice
                # or more

                index_lst.append(index)

                if index == HORIZONTAL:

                    for mat_str in cut_mat_string(mat_string_3d):
                        result_3d.append(crossword.run_mat_string(
                            mat_str, ALL_2d_DIRECTIONS, words_list))

                if index == VERTICAL_B:

                    for mat_str in column_b(mat_string_3d):
                        result_3d.append(crossword.run_mat_string(
                            mat_str, ALL_2d_DIRECTIONS, words_list))

                if index == VERTICAL_C:

                    for mat_str in column_c(mat_string_3d):
                        result_3d.append(crossword.run_mat_string(
                            mat_str, ALL_2d_DIRECTIONS, words_list))

        # order the result
        for item in result_3d:
            result_lst.extend(item)

        return result_lst


if __name__ == "__main__":
    if len(sys.argv) == NUMBER_OF_ARGUMENTS + 1:

        # Print errors corresponding to the necessity using os
        if not os.path.isfile(sys.argv[WORD_FILE_ARGUMENT]):
            print("ERROR: Word file " + sys.argv[WORD_FILE_ARGUMENT]
                  + " does not exist.")

        elif not os.path.isfile(sys.argv[MAT_FILE_ARGUMENT]):
            print("ERROR: Matrix file " + sys.argv[MAT_FILE_ARGUMENT]
                  + " does not exist.")

        elif not crossword.check_directions(sys.argv[DIRECTION_ARGUMENT],
                                            LIST_DIRECTION):
            print("ERROR: invalid directions.")

        else:
            # We will write in the output file, if it not exist it will
            # create it

            # open the word_list file and transfer the words to list
            word_list = []

            with open(sys.argv[OUTPUT_FILE_ARGUMENT], WRITE) as output_file:
                # build or reset the file
                pass

            with open(sys.argv[WORD_FILE_ARGUMENT], READ) as word_file:
                for line in word_file:
                    word_list.append(line.split(NEW_LINE)[0].lower())

            with open(sys.argv[MAT_FILE_ARGUMENT], READ) as mat_file:
                crossword.order_result(run(
                    crossword.mat(mat_file),
                    sys.argv[DIRECTION_ARGUMENT], word_list))

    else:  # If the user not provide 4 arguments
        print(INVALID_MESSAGE)
