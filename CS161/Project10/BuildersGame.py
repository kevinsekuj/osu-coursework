# Author: Kevin Sekuj
# Date: 11/26/20
# Description: Program of a two player board game played on a 5x5 grid, represented by
# a list of lists. Two players, x and o, place two builders on the board in the initial
# move them around the game by one grid slot orthogonally or diagonally. They must place
# towers in adjacent grid slots on each movement, each build creating a tower of 1 height
# on the 2D array game board. Players can only move one level upwards in height at a time,
# and a tower of height 4 is the maximum height at which a tower can be built with no further
# levels allowed.The game ends when a player places one of their builders on top of a 3 level
# tower, or when a player's two builders are both stuck and unable to place a legal move.

class BuildersGame:
    """
    BuildersGame class, containing the methods and data members which are
    updated as the game progresses.
    """

    def __init__(self):
        """
        Method for initializing the game variables.
        The game board's builder heights are represented as a 2D array of 5
        sub-lists, representing the grid in row-column form. Players add height
        to their towers by mutating values in the sublist from 0-3.
        Their position on the game board is represented by x and y coordinate
        objects for each builder. The builder's y and x coordinates are also
        cast to tuples for use in relations, especially set relations. A
        set is also initialized for use in the make_move method to prevent
        illegal moves.
        The game is initialized at UNFINISHED and the player turn is initialized
        to x. The init_placements_done bool is initialized to False until the
        initial_placement method is completed.
        """

        #           col 0  1  2  3  4
        self._board = [[0, 0, 0, 0, 0],  # row 0 | board[0][1] = upper-left most 0
                       [0, 0, 0, 0, 0],  # row 1 |      (y, x)
                       [0, 0, 0, 0, 0],  # row 2 |      (row)(col)
                       [0, 0, 0, 0, 0],  # row 3
                       [0, 0, 0, 0, 0]]  # row 4

        self._builder_x1_y = 0  # initializing builder coordinates
        self._builder_x1_x = 0
        self._builder_x2_x = 0
        self._builder_x2_y = 0

        self._x_pos_1 = ()  # casting their coordinates to tuples for use
        self._x_pos_2 = ()  # in relations and set relations

        self._builder_o1_y = 0
        self._builder_o1_x = 0
        self._builder_o2_y = 0
        self._builder_o2_x = 0

        self._o_pos_1 = ()
        self._o_pos_2 = ()
        # initializing a set of all builder positions used in set relations
        self._builder_set = set()

        self._game_state = "UNFINISHED"  # X_WON / O_WON / UNFINISHED
        self._player_turn = "x"
        self._init_placements_done = False

    def get_current_state(self):
        """
        Get method which returns current game state.
        """
        return self._game_state

    def initial_placement(self, b1_y, b1_x, b2_y, b2_x, player):
        """
        Initial placement method which takes 5 parameters - the row
        and column of each player's two builders, and the player who
        is placing the builders.
        """

        if self._player_turn == "x" and self._init_placements_done is False:
            if player != "x":
                return False

            if b1_y < 0 or b1_y > 4:  # check that builder row/column are not
                return False
            if b1_x < 0 or b1_x > 4:  # out of range
                return False
            #  check that builder coordinates not out of range, or
            #  equal to the first set of coordinates
            if b2_y < 0 or b2_y > 4 or (b2_y == b1_y and b2_x == b1_x):
                return False
            if (b2_x < 0 or b2_x > 4) or (b2_x == b1_x and b2_y == b1_y):
                return False

            else:
                # casting valid moves to builder y/x coordinates
                self._builder_x1_y = b1_y
                self._builder_x1_x = b1_x
                self._builder_x2_y = b2_y
                self._builder_x2_x = b2_x

                self._x_pos_1 = (b1_y, b1_x)
                self._x_pos_2 = (b2_y, b2_x)

                self._player_turn = "o"

        elif self._player_turn == "o" and self._init_placements_done is False:
            if player != "o":
                return False

            if b1_y < 0 or b1_y > 4:
                return False
            if b1_x < 0 or b1_x > 4:
                return False
            if b2_y < 0 or b2_y > 4 or (b2_y == b1_y and b2_x == b1_x):
                return False
            if (b2_x < 0 or b2_x > 4) or (b2_x == b1_x and b2_y == b1_y):
                return False

            #  checking that builder parameters do not equal those input by 'x'
            if (b1_y, b1_x) == self._x_pos_1 and self._x_pos_2:
                return False
            if (b2_y, b2_x) == self._x_pos_2 and self._x_pos_1:
                return False

            else:
                self._builder_o1_y = b1_y
                self._builder_o1_x = b1_x
                self._builder_o2_y = b2_y
                self._builder_o2_x = b2_x

                self._o_pos_1 = (b1_y, b1_x)
                self._o_pos_2 = (b2_y, b2_x)

                self._player_turn = "x"
                # bool to ensure that make_move only valid when initial placements done
                self._init_placements_done = True
                self._builder_set = {self._x_pos_1, self._x_pos_2, self._o_pos_1, self._o_pos_2}
        else:
            return False

        return True

    def make_move(self, from_row, from_column, to_row, to_column, build_row, build_column):
        """
        Method which takes parameters for the row and column of the piece to move,
        the row and column of the grid slot it's moving to, and the row and column
        of the slot it's building in. Returns false if initial placements are not
        complete, an invalid move is placed, an invalid build is placed, or if the
        game is won/drawn. Otherwise, it records the move and updates game state.
        """
        if self._init_placements_done is True and self._game_state == "UNFINISHED":

            if self._player_turn == "x":
                # ensuring grid coordinates correspond to an x builder
                if (from_row, from_column) != self._x_pos_1 and \
                        (from_row, from_column) != self._x_pos_2:
                    return False

                # invalid moves
                if to_row == from_row and to_column == from_column:
                    return False
                if to_row > from_row + 1:
                    return False
                elif to_row < from_row - 1:
                    return False
                if to_column > from_column + 1:
                    return False
                elif to_column < from_column - 1:
                    return False
                # prevent illegal tower hopping
                if self._board[from_row][from_column] < \
                        self._board[to_row][to_column] - 1:
                    return False

                # invalid builds
                if build_row > to_row + 1:
                    return False
                elif build_row < to_row - 1:
                    return False
                if build_column > to_column + 1:
                    return False
                elif build_column < to_column - 1:
                    return False
                # prevent building >4 level towers
                if self._board[build_row][build_column] >= 4:
                    return False

                # block building on self, or moving onto another builder
                if (to_row, to_column) == (build_row, build_column):
                    return False
                elif (to_row, to_column) in (self._builder_set - {(from_row, from_column)}):
                    return False
                # set relation to block tower builds on spots that builders occupy
                if (build_row, build_column) in (self._builder_set - {(from_row, from_column)}):
                    return False

                else:
                    # updates new grid position by checking if new y, x position
                    # is either higher or lower than than old y, x position,
                    # and adding/subtracting 1 depending  on which case.
                    if (from_row, from_column) == self._x_pos_1:
                        if to_row > self._builder_x1_y:
                            self._builder_x1_y += 1
                        elif to_row < self._builder_x1_y:
                            self._builder_x1_y -= 1
                        if to_column > self._builder_x1_x:
                            self._builder_x1_x += 1
                        elif to_column < self._builder_x1_x:
                            self._builder_x1_x -= 1

                        # adds 1 level to tower in the 2d array, and creates a new
                        # tuple containing the builder's new position (y and x coordinates).
                        self._board[build_row][build_column] += 1
                        self._x_pos_1 = self._builder_x1_y, self._builder_x1_x

                        # creates a new set containing updated builder positions
                        # to be used again in set relations again
                        self._builder_set = {self._x_pos_1, self._x_pos_2,
                                             self._o_pos_1, self._o_pos_2}

                        #  updates game state to won if player places their builder
                        #  on a three height tower. Otherwise, the game continues
                        if self._board[self._builder_x1_y][self._builder_x1_x] == 3:
                            self._game_state = "X_WON"
                            return True

                        else:
                            self._game_state = "UNFINISHED"
                            self._player_turn = "o"

                    elif (from_row, from_column) == self._x_pos_2:
                        if to_row > self._builder_x2_y:
                            self._builder_x2_y += 1

                        elif to_row < self._builder_x2_y:
                            self._builder_x2_y -= 1

                        if to_column > self._builder_x2_x:
                            self._builder_x2_x += 1

                        elif to_column < self._builder_x2_x:
                            self._builder_x2_x -= 1

                        self._board[build_row][build_column] += 1
                        self._x_pos_2 = self._builder_x2_y, self._builder_x2_x
                        self._builder_set = {self._x_pos_1, self._x_pos_2,
                                             self._o_pos_1, self._o_pos_2}

                    if self._board[to_row][to_column] == 3:
                        self._game_state = "X_WON"
                        return True

                    else:
                        self._game_state = "UNFINISHED"
                        self._player_turn = "o"
                return True

            elif self._player_turn == "o":
                if (from_row, from_column) != self._o_pos_1 and \
                        (from_row, from_column) != self._o_pos_2:
                    return False

                # invalid moves
                if to_row == from_row and to_column == from_column:
                    return False
                if to_row > from_row + 1:
                    return False
                elif to_row < from_row - 1:
                    return False
                if to_column > from_column + 1:
                    return False
                elif to_column < from_column - 1:
                    return False

                # prevent illegal tower hopping
                if self._board[from_row][from_column] < \
                        self._board[to_row][to_column] - 1:
                    return False

                # invalid builds
                if build_row > to_row + 1:
                    return False
                elif build_row < to_row - 1:
                    return False
                if build_column > to_column + 1:
                    return False
                elif build_column < to_column - 1:
                    return False
                # block building >4 level towers
                if self._board[build_row][build_column] >= 4:
                    return False

                # prevent build on self or other builder
                if (to_row, to_column) == (build_row, build_column):
                    return False
                elif (to_row, to_column) in (self._builder_set - {(from_row, from_column)}):
                    return False
                if (build_row, build_column) in (self._builder_set - {(from_row, from_column)}):
                    return False

                else:
                    if (from_row, from_column) == self._o_pos_1:
                        if to_row > self._builder_o1_y:
                            self._builder_o1_y += 1

                        elif to_row < self._builder_o1_y:
                            self._builder_o1_y -= 1

                        if to_column > self._builder_o1_x:
                            self._builder_o1_x += 1

                        elif to_column < self._builder_o1_x:
                            self._builder_o1_x -= 1

                        self._board[build_row][build_column] += 1
                        self._o_pos_1 = self._builder_o1_y, self._builder_o1_x
                        self._builder_set = {self._x_pos_1, self._x_pos_2, self._o_pos_1, self._o_pos_2}

                        if self._board[to_row][to_column] == 3:
                            self._game_state = "O_WON"
                            return True

                        else:
                            self._game_state = "UNFINISHED"
                            self._player_turn = "x"

                    elif (from_row, from_column) == self._o_pos_2:
                        if to_row > self._builder_o2_y:
                            self._builder_o2_y += 1

                        elif to_row < self._builder_o2_y:
                            self._builder_o2_y -= 1

                        if to_column > self._builder_o2_x:
                            self._builder_o2_x += 1

                        elif to_column < self._builder_o2_x:
                            self._builder_o2_x -= 1

                        self._board[build_row][build_column] += 1
                        self._o_pos_2 = self._builder_o2_y, self._builder_o2_x
                        self._builder_set = {self._x_pos_1, self._x_pos_2, self._o_pos_1, self._o_pos_2}

                    if self._board[to_row][to_column] == 3:
                        self._game_state = "O_WON"
                        return True

                    else:
                        self._game_state = "UNFINISHED"
                        self._player_turn = "x"
                return True

        else:
            return False
