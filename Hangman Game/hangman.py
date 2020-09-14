#############################################################
# FILE : ex4.py
# WRITER : Dan Boujenah , danou0301 , 341339901
# EXERCISE : intro2cs ex4 2017-2018
# DESCRIPTION : Hangman Game with hints
#############################################################
import hangman_helper

CHAR_A = 97
EMPTY_STRING = ""
UNIT_PATTERN = "_"
NUMBER_OF_LETTERS = 26
INCREASE = 1
LENGTH_LETTER = 1


def update_word_pattern(word, pattern, user_letter):
    """The function updates the pattern with the new letter"""

    pattern_lst = list(pattern)
    word_lst = list(word)

    for (i, word_letter) in enumerate(word_lst):
        # check if the letter is in the word
        if word_letter == user_letter:
            pattern_lst[i] = user_letter

    # rebuild the word from the list to a string
    pattern_new = EMPTY_STRING.join(pattern_lst)

    return pattern_new


def run_single_game(words_list):
    """ parm: list of words
    The function choose one of them and run a single game of hangman"""

    # choose a word among the words_list
    word = hangman_helper.get_random_word(words_list)
    error_count = 0
    wrong_guess_lst = []
    msg = hangman_helper.DEFAULT_MSG
    ask_play = False
    pattern = UNIT_PATTERN * len(word)

    while pattern != word and error_count < hangman_helper.MAX_ERRORS:

        hangman_helper.display_state(pattern, error_count,
                                     wrong_guess_lst, msg, ask_play)
        choice, letter_player = hangman_helper.get_input()

        if choice == hangman_helper.HINT:
            # player want hint
            words_list_hint = filter_words_list(words_list, pattern,
                                                wrong_guess_lst)
            hint = choose_letter(words_list_hint, pattern)
            msg = hangman_helper.HINT_MSG + hint

        if choice == hangman_helper.LETTER:
            # player enter a letter

            if len(letter_player) != LENGTH_LETTER \
                    or not letter_player.islower():
                # no valid type -> display the message
                msg = hangman_helper.NON_VALID_MSG

            elif letter_player in wrong_guess_lst or letter_player\
                    in pattern:
                # letter already taken -> display the message
                msg = hangman_helper.ALREADY_CHOSEN_MSG + letter_player

            elif letter_player in word:
                # the letter is in the word
                # update the pattern and the message
                pattern = update_word_pattern(word, pattern, letter_player)
                msg = hangman_helper.DEFAULT_MSG

            else:
                # the letter isn't in the word
                # update error_count, wrong_guess_list and the message
                error_count += INCREASE
                wrong_guess_lst.append(letter_player)
                msg = hangman_helper.DEFAULT_MSG

    # check if the player win or loss
    if pattern == word:
        msg = hangman_helper.WIN_MSG
    else:
        msg = hangman_helper.LOSS_MSG + word

    # ask if he want to play and other game
    hangman_helper.display_state(pattern, error_count, wrong_guess_lst,
                                 msg, ask_play=True)


def wrong_letter_check(word, wrong_guess_lst):
    """check if there are a wrong letter in the word"""

    flag = True

    for wrong_letter in wrong_guess_lst:

        if wrong_letter in word:
            # if one of the letter in the wrong guess list is in
            # the word return false
            flag = False

    return flag


def filter_words_list(words_list, pattern, wrong_guess_lst):
    """parm: list of words
    This function filters a list of words in accordance to the pattern."""

    words_hint = []

    for word in words_list:

        # check if the pattern and the word are same length
        if len(pattern) == len(word):

            # check if the word contain a wrong guess letter
            if wrong_letter_check(word, wrong_guess_lst) is True:

                # i created a new pattern and update it with letters who are
                # in a pattern
                my_pattern = UNIT_PATTERN * len(word)

                for item in list(pattern):

                    if item != UNIT_PATTERN:
                        # update the pattern
                        my_pattern = update_word_pattern(word, my_pattern,
                                                         item)

                if pattern == my_pattern:
                    words_hint.append(word)

    return words_hint


def letter_to_index(letter):
    """‫‪Return‬‬ ‫‪the‬‬ ‫‪index‬‬ ‫‪of‬‬ ‫‪the‬‬ ‫‪given‬‬ ‫‪letter‬‬ ‫‪in‬‬
    ‫‪an‬‬ ‫‪alphabet‬‬ ‫‪list"""
    return ord(letter.lower())-CHAR_A


def index_to_letter(index):
    """‫‪Return‬‬ ‫‪the‬‬ ‫‪letter‬‬ ‫‪corresponding‬‬ ‫‪to‬‬
    ‫‪the‬‬ ‫‪given‬‬ ‫‪index.‬‬"""
    return chr(index + CHAR_A)


def choose_letter(words_hint, pattern):
    """define who is the letter (not already find) that is more
    present in a list of words"""

    apparition_lst = [0] * NUMBER_OF_LETTERS
    letter_already_choose = []

    for item in list(pattern):
        if item != UNIT_PATTERN:
            letter_already_choose.append(item)

    for word in words_hint:
        for letter in list(word):
            if letter not in letter_already_choose:
                apparition_lst[letter_to_index(letter)] += INCREASE

    return index_to_letter(apparition_lst.index(max(apparition_lst)))


def main():
    """This function allows to run the program."""

    # load the game
    words_list = hangman_helper.load_words()

    run_single_game(words_list)
    # answer of the user about if he want to play more or not
    user_input = hangman_helper.get_input()

    # rerun a game if he want to play more
    while user_input[0] == hangman_helper.PLAY_AGAIN and user_input[1]:

        words_list = hangman_helper.load_words()
        run_single_game(words_list)
        user_input = hangman_helper.get_input()

# run the game
if __name__ == "__main__":
    hangman_helper.start_gui_and_call_main(main)
    hangman_helper.close_gui()
