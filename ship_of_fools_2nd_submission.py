"""
Ship of fools !

Ship of fools is a simple dice game. It is played with five standard 6-faced
dice by two or more players. The game goal is to gather a 6, a 5 and a 4
(Ship, Captain and Crew) in the mentioned order. The sum of the two remaining
dice (cargo) is preferred as high as possible. The player with the highest
cargo score wins the round.

In our customized version of this game, we let players play until one of the
players scores 21 or more in total.
"""

import random

__author__ = 'Ripan Kumar Dhar'
__email__ = 'ripankumardhar@gmail.com'
__PersonsNumber__ = '880727-8398'


class Die(object):
    """
    A single die
    """

    def __init__(self):
        self._value = 0

    def get_value(self) -> int:
        """
        Get current rolled number
        """
        return self._value

    def roll(self):
        """
        Roles the die. Sets the value of _value to the rolled number.
        """
        rolled_value = random.randint(1, 6)
        self._value = rolled_value

    def reset_die(self):
        self._value = 0


class DiceCup(object):
    """
    Dice cup containing 5 dices
    """

    def __init__(self):
        self._dice = [Die() for _ in range(5)]
        self._banked_dice = [False for _ in range(5)]

    def value(self) -> int:
        """
        Returns sum of all dices
        """
        dice_sum = 0

        for dice in self._dice:
            dice_sum += dice.get_value()

        return dice_sum

    def bank(self, index: int):
        """
        Banks a dice
        :param index: Index of the dice
        """
        self._banked_dice[index] = True

    def is_banked(self, index: int) -> bool:
        """
        Checks if a dice is banked
        :param index: Index of the dice
        """
        return self._banked_dice[index]

    def all_banked(self):
        count = 0

        for index in self._banked_dice:
            if index:
                count += 1

        return count == 5

    def release(self, index: int):
        die = self._dice[index]
        die.reset_die()

    def release_all(self):
        for index, _ in enumerate(self._dice):
            self.release(index)

    def find_dice(self, value: int) -> int:
        """
        Search if we have a specific value in the rolled dices
        :param value: Searching value
        :return: Returns index if the dice if found, else returns -1
        """
        dice_index = -1

        for index, dice in enumerate(self._dice):
            if not self._banked_dice[index] and dice.get_value() == value:
                dice_index = index
                break

        return dice_index

    def roll(self):
        """
        Roles all un-banked dices
        """
        for index, dice in enumerate(self._dice):
            if not self._banked_dice[index]:
                dice.roll()

    def dices(self) -> list:
        return self._dice

    def reset(self):
        self.release_all()
        self._banked_dice = [False for _ in range(5)]


class ShipOfFoolsGame(object):
    """
    Class which initiates the game
    """

    def __init__(self, winning_score: int):
        self._cup = DiceCup()
        self._winning_score = winning_score
        self._round = None

    def round(self) -> int:
        return self._round

    def set_round(self):
        self._round = 1 if not self._round else self._round + 1

    def cup(self) -> DiceCup:
        return self._cup

    def winning_score(self) -> int:
        return self._winning_score


class Player(object):
    """
    A single player
    """

    def __init__(self, name: str, score=0):
        self._name = name
        self._score = score

    def name(self) -> str:
        return self._name

    def set_name(self, name: str):
        self._name = name

    def current_score(self) -> int:
        return self._score

    def reset_score(self):
        self._score = 0

    def play_round(self, game: ShipOfFoolsGame):
        has_ship = False
        has_captain = False
        has_crew = False

        cup = game.cup()
        dices = cup.dices()

        for turn in range(3):
            if cup.all_banked():
                break

            print('Turn {}'.format(turn + 1))

            # Rolling un-banked dices
            cup.roll()

            # Printing dice roles
            for index, dice in enumerate(dices):
                if cup.is_banked(index):
                    print(dice.get_value(), end=' ')
                else:
                    print(dice.get_value(), end=' ')

            print('\n')

            # Checking if has ship
            if not has_ship:
                ship_index = cup.find_dice(6)

                if ship_index >= 0:
                    has_ship = True
                    cup.bank(ship_index)

            # Checking if has captain
            if has_ship and not has_captain:
                captain_index = cup.find_dice(5)

                if captain_index >= 0:
                    has_captain = True
                    cup.bank(captain_index)

            # Checking if has crew
            if has_ship and has_captain and not has_crew:
                crew_index = cup.find_dice(4)

                if crew_index >= 0:
                    has_crew = True
                    cup.bank(crew_index)

            if not (has_ship and has_ship and has_crew):
                continue

            # Banking remaining dices
            if has_ship and has_captain and has_crew and turn < 2:
                print('Press y/Y to bank dices. Press any other key to roll again.')
                answer = input().strip()

                if answer == 'y' or answer == 'Y':
                    not_done = True

                    while not_done:
                        print('Enter indexes of dices to bank : ')
                        indexes = list(map(int, input().strip().split()))

                        for index in indexes:
                            if cup.is_banked(index):
                                print('This dice is already banked. Try again.')
                                break
                            else:
                                cup.bank(index)
                                not_done = False
                else:
                    continue

        # Calculating score
        if has_ship and has_captain and has_crew:
            score = cup.value() - 15
        else:
            score = 0

        self._score += score

        print('\n{} scored {} in this round. {}\'s total score {}\n'.format(self.name(), score, self.name(),
                                                                            self.current_score()))

        # Resetting dice cup for the next player
        cup.reset()

        # Give player chance to look up their result
        print('\nPress any key to continue.')
        input()


class PlayRoom(object):
    """
    Room which holds all the player and where the game takes place
    """

    def __init__(self):
        self._game = None
        self._players = []
        self._is_game_finished = False
        self._winner = None

    def set_game(self, game: ShipOfFoolsGame):
        """
        Assigns a new game
        :param game: A new game
        """
        self._game = game

    def add_player(self, player: Player):
        self._players.append(player)

    def reset_scores(self):
        for player in self._players:
            player.reset_score()

    def play_round(self):
        game = self._game

        game.set_round()
        print('\nStarting round {} !'.format(game.round()))

        for player in self._players:

            print('\nPlayer {} starting their round'.format(player.name()))
            player.play_round(self._game)

            # If player's score reaches the predefined winning limit , declaring winner
            if player.current_score() >= game.winning_score():
                self._is_game_finished = True
                self._winner = player
                break

    def game_finished(self) -> bool:
        return self._is_game_finished

    def print_scores(self):
        print('***************************************')
        for player in self._players:
            print('{} : {}'.format(player.name(), player.current_score()))
        print('***************************************')

    def print_winner(self):
        print(self._winner.name())


# Winning score
current_winning_score = 21

# Main script, where program starts execution
if __name__ == '__main__':
    print('############ Ship of fools ! ############')

    # Creating new room and assigning new instance of the game
    room = PlayRoom()
    room.set_game(ShipOfFoolsGame(current_winning_score))

    # Adding players
    player_1 = 'John Snow'
    player_2 = 'Khalessi'

    room.add_player(Player(player_1))
    print('{} added to the game'.format(player_1))

    room.add_player(Player(player_2))
    print('{} added to the game'.format(player_2))

    # Resetting previous scores
    room.reset_scores()

    # Starting round
    while not room.game_finished():
        room.play_round()
        room.print_scores()

    # Declaring winner !
    room.print_winner()
