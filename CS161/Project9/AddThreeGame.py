# Author: Kevin Sekuj
# Date: 11/21/20
# Description: Two player game where each player alternately chooses a number
# from 1-9. They can't choose numbers already selected by the either player.
# The player whose three numbers sum to 15 wins. If neither player wins and
# all numbers are chosen, the game draws.
#
# The program initializes the private data members within the
# AddThreeGame class and has the get method get_current_state for returning
# the game parameters. Player moves are processed by the make_move method
# which takes the player move and their number choice. If it's not their choice,
# or the int is out of range, or has been picked, or the game has been won or
# drawn, it returns False. Otherwise it records the move and updates the game
# state. If the move results in a win or draw, it returns True.

class AddThreeGame:
    """
    Game class initializing the data members for the game which are updated
    as the game progresses.
    """

    def __init__(self):
        """
        Method initializing private game state parameters.

        player1 and player2: keep track of sum total of player picks. Used as
        a checkpoint in the if conditionals to check win condition if either
        player has summed to 15 or over.

        player1_nums/player2_nums: lists containing individual player picks.

        chosen_nums: list of total picks overall.

        game_state: string value holding the game state, initializing at
        UNFINISHED when the game begins with possible values of FIRST_WON
        / SECOND_WON / DRAW.
        """
        self._player1 = 0
        self._player2 = 0
        self._game_state = "UNFINISHED"
        self._player_turn = "first"
        self._chosen_nums = []
        self._player1_nums = []
        self._player2_nums = []

    def get_current_state(self):
        """
        Get method for returning game state parameter.
        """
        return self._game_state

    def make_move(self, player_move, num_choice):
        """
        Takes player move and number choice through series of if conditionals to
        check if their move is valid or not, storing player move if valid move.
        """

        if player_move == "first":
            if num_choice < 1 or num_choice > 9:
                return False
            if num_choice in self._chosen_nums:
                return False
            elif not self._game_state == "UNFINISHED":
                return False
            elif not self._player_turn == "first":
                return False
            else:
                self._player1 += num_choice
                self._chosen_nums.append(num_choice)
                self._player1_nums.append(num_choice)
                self._player_turn = "second"
                self._game_state = "UNFINISHED"

        elif player_move == "second":
            if num_choice < 1 or num_choice > 9:
                return False
            if num_choice in self._chosen_nums:
                return False
            elif not self._game_state == "UNFINISHED":
                return False
            elif not self._player_turn == "second":
                return False
            else:
                self._player2 += num_choice
                self._chosen_nums.append(num_choice)
                self._player2_nums.append(num_choice)
                self._player_turn = "first"
                self._game_state = "UNFINISHED"

        if self._player1 >= 15:
            # triple nested loop indexing through the list of player nums, checking
            # if three integers in their list sum to the winning condition (15).
            # The program uses a player sum of 15 for ANY integers in their list
            # as a checkpoint to enter the loop and check for the actual win condition.
            for index_1 in range(0, len(self._player1_nums) - 2):
                for index_2 in range(index_1 + 1, len(self._player1_nums) - 1):
                    for index_3 in range(index_2 + 1, len(self._player1_nums)):
                        if self._player1_nums[index_1] + self._player1_nums[index_2]\
                                + self._player1_nums[index_3] == 15:
                            self._game_state = "FIRST_WON"
                            return True

        elif self._player2 >= 15:
            for index_1 in range(0, len(self._player2_nums) - 2):
                for index_2 in range(index_1 + 1, len(self._player2_nums) - 1):
                    for index_3 in range(index_2 + 1, len(self._player1_nums)):
                        if self._player1_nums[index_1] + self._player1_nums[index_2]\
                                + self._player1_nums[index_3] == 15:
                            self._game_state = "SECOND_WON"
                            return True

        if len(self._chosen_nums) == 9 and self._game_state == "UNFINISHED":
            self._game_state = "DRAW"  # draws game if 9 ints are chosen and game state is unfinished.
            return True

        return True
