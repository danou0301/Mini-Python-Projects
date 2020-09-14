#############################################################
# FILE : ex5.py
# WRITERS : Dan Boujenah , danou0301 , 341339901
#         : Chalom Zemmour, chalomz, 888311081
# EXERCISE : intro2cs ex5 2017-2018
# DESCRIPTION : Crossword
# Find words into a matrix and return them into an output file using the Linux
# interface
#############################################################
import sys
import os
import copy

UP = 'u'
DOWN = 'd'
RIGHT = 'r'
LEFT = 'l'
DIAGONAL_W = 'w'
DIAGONAL_X = 'x'
DIAGONAL_Y = 'y'
DIAGONAL_Z = 'z'
LIST_DIRECTION = [UP, DOWN, RIGHT, LEFT, DIAGONAL_W, DIAGONAL_X, DIAGONAL_Y,
                  DIAGONAL_Z]

NUMBER_OF_ARGUMENTS = 4
WORD_FILE_ARGUMENT = 1
MAT_FILE_ARGUMENT = 2
OUTPUT_FILE_ARGUMENT = 3
DIRECTION_ARGUMENT = 4
READ = 'r'
WRITE = 'w'
ADD = 'a'

NEW_LINE = '\n'
EMPTY_STRING = ""
COMMA = ","
INVALID_MESSAGE = "ERROR: invalid number of parameters. Please enter word" \
                  "_file matrix_file output_file directions"


def mat(matrix_file):
    """The function takes the content of mat file and convert it into a list
     of strings"""
    mat_string = []

    for item in matrix_file.readlines():
        mat_line = item.split(NEW_LINE)[0]
        line_str = mat_line.replace(COMMA, EMPTY_STRING).lower()

        mat_string.append(line_str)

    return mat_string


def string_to_matrix(mat_string):
    """This function takes a list of strings and converts into a list of other
     lists, each one of these lists contains each letter of the word: a matrix
     """
    # IMPORTANT: For us, we defined A matrix as a list of lists, those lists
    # contain several strings; in our case these strings are letters

    matrix = []

    for mat_line in mat_string:
        line_lst = []

        for letter in mat_line:

            line_lst.append(letter)
        matrix.append(line_lst)

    return matrix


def matrix_to_string(matrix):
    """This function do the inverse role of string_to_matrix function by
    convert a matrix to a list of string compose by the correspondent letters
    from the matrix"""

    math_string = []
    for item in matrix:

        math_string.append(EMPTY_STRING.join(item))

    return math_string


def reverse(mat_string):
    """This function reverses the order of the strings those are contained in
    lists (contained in one huge list)"""

    reverse_mat = []

    for mat_line in mat_string:
        reverse_mat.append(mat_line[::-1])

    return reverse_mat


def column_down(mat_string):
    """This function converts the reading direction of the matrix from
    horizontal to vertical"""
    # We consider the original matrix with all the string one under the second

    total_column = []
    for i in range(len(mat_string[0])):
        column = []
        for mat_line in mat_string:
            column.append(mat_line[i])
        total_column.append(column)

    return total_column


def diagonal_y(mat_string):
    """This function converts the reading direction of the matrix from
    horizontal to diagonal descend to right side"""
    mat_line = []
    mat_total = []
    matrix = string_to_matrix(mat_string)
    num_column, num_line = len(matrix), len(matrix[0])

    for diagonal in range(num_column + num_line - 1):
        # the number of diagonals is always nb of column + nb of line -1

        for index in range(max(diagonal - num_column + 1, 0),
                           min(diagonal + 1, num_line)):
            # We check one after the second the potential beginning of the
            # diagonal depend on the start of the line or the column

            mat_line.append(matrix[num_column - diagonal + index - 1][index])
            # Display the diagonals according to the order required

        mat_total.append(mat_line)
        mat_line = []

    return mat_total


def diagonal_w(mat_string):
    """This function converts the reading direction of the matrix from
    horizontal to diagonal ascend to right side"""
    mat_line = []
    mat_total = []
    matrix = string_to_matrix(mat_string)
    num_column, num_line = len(matrix), len(matrix[0])

    for diagonal in range(num_column + num_line - 1):

        for index in range(max(diagonal - num_column + 1, 0),
                           min(diagonal + 1, num_line)):

            mat_line.append(matrix[diagonal - index][index])
            # Display the diagonals according to the order required

        mat_total.append(mat_line)
        mat_line = []

    return mat_total


def check_words(mat_string, words_list):
    """This function researches in a list of strings the number of occurrence
    of words contained in a list """

    check_list = []

    for word in words_list:

        for mat_line in mat_string:

            line_check = mat_line
            while word in line_check:

                index = line_check.index(word)
                line_check = line_check[index + 1:]
                # To include checking "pop" in "popop" word
                check_list.append(word)

    return check_list
    # return as a list of words


def run_mat_string(mat_string, directions_string, words_list):
    """In this function, we check one one the word_list and check if those are
    present in the mat_string list according to the directions letters ordered
    """

    result = []
    directions = list(directions_string)
    if not mat_string:
        # if nothing in mat.txt file, we don't want an error, the program will
        # return an empty output file
        return result
    else:
        index_list = []
        for index in directions:
            if index not in index_list:
                # Create a list of index to avoid the possibility to check
                # more than once the direction if the user taped it twice
                # or more
                index_list.append(index)

                # In all the following, we used the function that we have
                # already use in order to obtain a right result according to
                # the directions requested
                if index == RIGHT:
                    result.append(check_words(mat_string, words_list))
                if index == LEFT:
                    result.append(check_words(reverse(mat_string), words_list))
                if index == DOWN:
                    result.append(check_words(matrix_to_string(
                        column_down(mat_string)), words_list))
                if index == UP:
                    result.append(check_words(reverse(matrix_to_string(
                        column_down(mat_string))), words_list))
                if index == DIAGONAL_Y:
                    result.append(check_words(matrix_to_string(
                        diagonal_y(mat_string)), words_list))
                if index == DIAGONAL_X:
                    result.append(check_words(reverse(matrix_to_string(
                        diagonal_y(mat_string))), words_list))
                if index == DIAGONAL_W:
                    result.append(check_words(matrix_to_string(
                        diagonal_w(mat_string)), words_list))
                if index == DIAGONAL_Z:
                    result.append(check_words(reverse(matrix_to_string(
                        diagonal_w(mat_string))), words_list))

    result_list = []
    # from list of lists of words to list of words
    for lst in result:
        result_list.extend(lst)

    return result_list


def order_result(result_list):
    """In this function, we will count the number of word and display it in
    the output file as request"""

    final_lst = []
    final_word = []

    # no iteration
    for word in result_list:

        if word not in final_word:
            count = result_list.count(word)
            final_word.append(word)
            final_lst.append((word, count))

    # write in the file
    first_line = True
    for tuple_result in sorted(final_lst):  # Alphabetical

        display_word = tuple_result[0]
        display_count = str(tuple_result[1])

        # use True/False to skip a line orderly, no skip line at the end
        if first_line:
            with open(sys.argv[OUTPUT_FILE_ARGUMENT], WRITE) as output_file:
                output_file.write(display_word + COMMA + display_count)
                first_line = False

        else:
            with open(sys.argv[OUTPUT_FILE_ARGUMENT], ADD) as output_file:
                output_file.write(NEW_LINE + display_word + COMMA +
                                  display_count)


def check_directions(string_direction, list_direction):
    """In this we check if there are letters directions inputted"""

    for letter in string_direction:

        if letter not in list_direction:
            return False
    return True


if __name__ == "__main__":

    if len(sys.argv) == NUMBER_OF_ARGUMENTS + 1:

        # Print errors corresponding to the necessity using os
        if not os.path.isfile(sys.argv[WORD_FILE_ARGUMENT]):
            print("ERROR: Word file " + sys.argv[WORD_FILE_ARGUMENT] +
                  " does not exist.")

        elif not os.path.isfile(sys.argv[MAT_FILE_ARGUMENT]):
            print("ERROR: Matrix file " + sys.argv[MAT_FILE_ARGUMENT] +
                  " does not exist.")

        elif not check_directions(sys.argv[DIRECTION_ARGUMENT], LIST_DIRECTION):
            print("ERROR: invalid directions.")

        else:
            # We will write in the output file, if it not exist it will
            # create it
            word_list = []

            with open(sys.argv[OUTPUT_FILE_ARGUMENT], WRITE) as output_file:
                # build or reset the file
                pass

            with open(sys.argv[WORD_FILE_ARGUMENT], READ) as word_file:
                for line in word_file:
                    # open the word_list file and transfer the words to list
                    word_list.append(line.split(NEW_LINE)[0].lower())

            with open(sys.argv[MAT_FILE_ARGUMENT], READ) as mat_file:

                order_result(run_mat_string(
                    mat(mat_file), sys.argv[DIRECTION_ARGUMENT], word_list))

    else:  # If the user not provide 4 arguments
        print(INVALID_MESSAGE)
