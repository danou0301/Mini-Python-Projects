#############################################################
# FILE : ex9.py
# WRITERS : Dan Boujenah , danou0301 , 341339901
#         : Chalom Zemmour, chalomz, 888311081
# EXERCISE : intro2cs ex9 2017-2018
# DESCRIPTION : Asteroids Game
#############################################################
from screen import Screen
from ship import Ship
from asteroid import Asteroid
from torpedo import Torpedo
import sys
import math
from random import randint

DEFAULT_ASTEROIDS_NUM = 3
TURN_LEFT = 7
TURN_RIGHT = -7

INITIAL_SCORE = 0
NUM_MAX_TORPEDOS = 15
ASTEROID_DIVIDE = 2

BIG_SIZE = 3
SCORE_BIG_SIZE = 20
MEDIUM_SIZE = 2
SCORE_MEDIUM_SIZE = 50
SMALL_SIZE = 1
SCORE_SMALL_SIZE = 100

ASTEROID_DIVIDE_SIZE = 1
LOSS_LIVE = 1
INCREASE_TIME = 1

SHIP_COLLISION_MESSAGE_TITLE = "Wounded"
SHIP_COLLISION_MESSAGE = "Be careful next time..."
VICTORY_MESSAGE_TITLE = "YOU WIN!"
VICTORY_MESSAGE = "Congratulations, try with more asteroids...!"
LOSS_MESSAGE_TITLE = "GAME OVER"
LOSS_MESSAGE = "Sorry, you loss. Try again..."
EXIT_MESSAGE_TITLE = "EXIT"
EXIT_MESSAGE = 'See you soon !'


class GameRunner:
    """This class manage the game depending on the amount of asteroids"""

    def __init__(self, asteroids_amount):
        """
        Initiation of the GameRunner class
        :parm asteroids_amount: number of asteroids in the game
        """

        self._screen = Screen()
        # create a ship
        self._ship = Ship(randint(Screen.SCREEN_MIN_X, Screen.SCREEN_MAX_X),
                          randint(Screen.SCREEN_MIN_Y, Screen.SCREEN_MAX_Y),
                          Ship.INITIAL_VELOCITY, Ship.INITIAL_VELOCITY,
                          Ship.INITIAL_HEADING, Ship.MAX_LIVES)

        self.screen_max_x = self._screen.SCREEN_MAX_X
        self.screen_max_y = self._screen.SCREEN_MAX_Y
        self.screen_min_x = self._screen.SCREEN_MIN_X
        self.screen_min_y = self._screen.SCREEN_MIN_Y

        # init the asteroids list depending on the asteroids amount
        self.asteroids = []
        self.create_asteroids(asteroids_amount)

        self.torpedos = []  # init the torpedo list
        self._score = INITIAL_SCORE

    def create_one_asteroid(self):
        """This function create one asteroid for the begging of the game"""

        asteroid = Asteroid(randint(Screen.SCREEN_MIN_X, Screen.SCREEN_MAX_X),
                            randint(Screen.SCREEN_MIN_Y, Screen.SCREEN_MAX_Y),
                            randint(Asteroid.MIN_SPEED, Asteroid.MAX_SPEED),
                            randint(Asteroid.MIN_SPEED, Asteroid.MAX_SPEED),
                            Asteroid.MAX_SIZE)

        return asteroid

    def create_asteroids(self, asteroids_amnt):
        """This function create asteroids for the begging of the game"""
        for i in range(asteroids_amnt):
            asteroid = self.create_one_asteroid()

            # check if the asteroid is on the same position that a ship
            while asteroid.get_position_x() == self._ship.get_position_x() and \
                    asteroid.get_position_y() == self._ship.get_position_y():
                self.create_one_asteroid()
            # add the asteroid to the list
            self._screen.register_asteroid(asteroid, asteroid.get_size())
            self.asteroids.append(asteroid)

    def create_torpedo(self, ship):
        """This function create one torpedo if there are less than
        NUM_MAX_TORPEDOS"""

        if len(self.torpedos) <= NUM_MAX_TORPEDOS:
            velocity_x = ship.get_velocity_x() + \
                         Torpedo.ACCELERATION_FACTOR * math.cos(math.radians(
                                                     ship.get_heading()))
            velocity_y = ship.get_velocity_y() + \
                         Torpedo.ACCELERATION_FACTOR * math.sin(math.radians(
                                                     ship.get_heading()))

            torpedo = Torpedo(ship.get_position_x(), ship.get_position_y(),
                              velocity_x, velocity_y, ship.get_heading(),
                              Torpedo.INITIAL_LIFE_TIME)

            # add the torpedo to the list
            self.torpedos.append(torpedo)
            self._screen.register_torpedo(torpedo)

    def run(self):
        self._do_loop()
        self._screen.start_screen()

    def _do_loop(self):
        # You don't need to change this method!
        self._game_loop()

        # Set the timer to go off again
        self._screen.update()
        self._screen.ontimer(self._do_loop, 5)

    def move(self, my_object):
        """move torpedo, ship and asteroids depending on their location and
        velocity"""

        delta_x = self._screen.SCREEN_MAX_X - self._screen.SCREEN_MIN_X
        delta_y = self._screen.SCREEN_MAX_Y - self._screen.SCREEN_MIN_Y
        new_x = (my_object.get_velocity_x() + my_object.get_position_x() -
                 self._screen.SCREEN_MIN_X) % delta_x + self._screen.SCREEN_MIN_X
        new_y = (my_object.get_velocity_y() + my_object.get_position_y() -
                 self._screen.SCREEN_MIN_Y) % delta_y + self._screen.SCREEN_MIN_Y

        # update the location
        my_object.set_position_x(new_x)
        my_object.set_position_y(new_y)

    def change_angle(self, ship):
        """This function change the angle of the ship"""
        if self._screen.is_left_pressed():
            ship.set_heading(ship.get_heading() + TURN_LEFT)

        if self._screen.is_right_pressed():
            ship.set_heading(ship.get_heading() + TURN_RIGHT)

    def acceleration(self, ship):
        """This function check if the user press up button and in case of yes
        accelerate the ship"""
        if self._screen.is_up_pressed():
            ship.set_velocity_x(ship.get_velocity_x() + math.cos(math.radians(
                ship.get_heading())))
            ship.set_velocity_y(ship.get_velocity_y() + math.sin(math.radians(
                ship.get_heading())))

    def collision_asteroid_ship(self, asteroid):
        """This function check if the ship hit an asteroid and in case of yes
        manage it"""
        if asteroid.has_intersection(self._ship):
            # check if the user have live
            if self._ship.get_lives() > 0:

                # remove live to the screen and to the object
                self._screen.remove_life()
                self._ship.set_lives(self._ship.get_lives() - LOSS_LIVE)

                # remove the asteroids that user hit
                self.asteroids.remove(asteroid)
                self._screen.unregister_asteroid(asteroid)

                # display message to the screen
                self._screen.show_message(SHIP_COLLISION_MESSAGE_TITLE,
                                          SHIP_COLLISION_MESSAGE)

    def asteroid_burst(self, asteroid, torpedo):
        """This function divide an asteroid to smaller asteroids with
        opposite velocity and register them"""

        for i in range(ASTEROID_DIVIDE):
            # if we can divide the asteroid, it's mane the asteroid size larger
            #  than the smaller size
            if asteroid.get_size() > SMALL_SIZE:

                norm = math.sqrt(asteroid.get_velocity_x()**2 +
                                 asteroid.get_velocity_y()**2) * (-1)**i

                new_velocity_x = (torpedo.get_velocity_x() +
                                  asteroid.get_velocity_x()) / norm
                new_velocity_y = (torpedo.get_velocity_y() +
                                  asteroid.get_velocity_y()) / norm
                # the size of the asteroid decrease
                new_size = asteroid.get_size() - ASTEROID_DIVIDE_SIZE

                new_asteroid = Asteroid(asteroid.get_position_x(),
                                        asteroid.get_position_y(),
                                        new_velocity_x, new_velocity_y,
                                        new_size)

                # add the asteroid to the register
                self.asteroids.append(new_asteroid)
                self._screen.register_asteroid(new_asteroid,
                                               new_asteroid.get_size())

    def collision_asteroid_torpedo(self, asteroid):
        """This function check if a torpedo hit an asteroid then remove it and
        build two others smaller and remove the torpedo"""

        for torpedo in self.torpedos:
            if asteroid.has_intersection(torpedo):
                # build two smaller asteroids
                self.asteroid_burst(asteroid, torpedo)
                # remove the original asteroid
                self._screen.unregister_asteroid(asteroid)
                self.asteroids.remove(asteroid)
                # remove the torpedo who hit the asteroid
                self._screen.unregister_torpedo(torpedo)
                self.torpedos.remove(torpedo)

                self.get_point(asteroid)
                return True  # it destroy an asteroid

    def manage_asteroid(self):
        """This function manage the asteroids, move them and check if them hit
        a torpedo or a ship"""

        for asteroid in self.asteroids:

            # move asteroids and draw them
            self.move(asteroid)
            self._screen.draw_asteroid(asteroid, asteroid.get_position_x(),
                                       asteroid.get_position_y())

            self.collision_asteroid_ship(asteroid)
            # if torpedo hit asteroid we have to break the for, because we have
            # delete an asteroid and may not run it after
            if self.collision_asteroid_torpedo(asteroid):
                break

    def manage_torpedo(self):
        """This function manage torpedo:
        - build it when the user press the space
        - remove it when it died"""

        if self._screen.is_space_pressed():
            self.create_torpedo(self._ship)

        for torpedo in self.torpedos:

            self.move(torpedo)
            self._screen.draw_torpedo(torpedo, torpedo.get_position_x(),
                                      torpedo.get_position_y(),
                                      torpedo.get_heading())

            # add one to the time life
            torpedo.set_life_time(torpedo.get_life_time() + INCREASE_TIME)
            if torpedo.get_life_time() == Torpedo.LIFE_TIME:
                # remove it
                self.torpedos.remove(torpedo)
                self._screen.unregister_torpedo(torpedo)

    def get_point(self, asteroid):
        """This function add point to the user when he it an asteroid depending
         on it size"""

        if asteroid.get_size() == BIG_SIZE:
            self._score += SCORE_BIG_SIZE
        elif asteroid.get_size() == MEDIUM_SIZE:
            self._score += SCORE_MEDIUM_SIZE
        elif asteroid.get_size() == SMALL_SIZE:
            self._score += SCORE_SMALL_SIZE
        # update the score
        self._screen.set_score(self._score)

    def game_statut(self):
        """Check when the game have to be completed"""

        # when the user hit all asteroids
        if not self.asteroids:
            self._screen.show_message(VICTORY_MESSAGE_TITLE, VICTORY_MESSAGE)
            self._screen.end_game()
            sys.exit()
        # When the user have no live
        elif self._ship.get_lives() == 0:
            self._screen.show_message(LOSS_MESSAGE_TITLE, LOSS_MESSAGE)
            self._screen.end_game()
            sys.exit()
        # the user quit the game
        elif self._screen.should_end():
            self._screen.show_message(EXIT_MESSAGE_TITLE, EXIT_MESSAGE)
            self._screen.end_game()
            sys.exit()

    def _game_loop(self):
        """This function run the game:
        - checks if the user wants to move the ship
        - moves all the objects
        - checks collisions
        - draws all the objects
        - checks if the game is over."""

        self.change_angle(self._ship)
        self.move(self._ship)
        self.acceleration(self._ship)

        self.manage_torpedo()
        self.manage_asteroid()

        self._screen.draw_ship(self._ship.get_position_x(),
                               self._ship.get_position_y(),
                               self._ship.get_heading())
        self.game_statut()


def main(amnt):
    runner = GameRunner(amnt)
    runner.run()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
