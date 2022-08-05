# Author: Kevin Sekuj
# Date: 3/11/21
# Description: Program implementing a board game known as Janggi, popularly known
# as Korean chess. The game is played on a 9x10 board with pieces somewhat analogous
# to Western chess, with original pieces such as the Elephant and Cannon. The player's
# objective is to induce a checkmate scenario where the enemy's general cannot make
# any legal moves. Each general resides in a "fortress" where they may move to and
# from, but not exit. This program includes checkmate functionality but excludes
# certain scenarios such as perpetual check.


class JanggiGame:
    """
    JanggiGame class where the game board, game state, and other game related variables
    and data members are initialized. This class will handle initializing Piece objects
    on the game board, representing the various game pieces, and also take parameters
    allowing Players to make moves on the board.
    """

    def __init__(self):
        """
        Constructor method for initializing the board, game state, player turn, and other
        parameters. The board will be represented as a two dimensional array, and this method will
        also initialize a dictionary that will allow players to pass board positions like
        "b2", which will correspond to the proper array position, for example, board[1][1].
        Access to this dict will be used in the make_move method.
        """
        self._board = [
            # A   B   C   D   E   F   G   H   I
            ['', '', '', '', '', '', '', '', ''],  # 1
            ['', '', '', '', '', '', '', '', ''],  # 2
            ['', '', '', '', '', '', '', '', ''],  # 3
            ['', '', '', '', '', '', '', '', ''],  # 4
            ['', '', '', '', '', '', '', '', ''],  # 5
            ['', '', '', '', '', '', '', '', ''],  # 6
            ['', '', '', '', '', '', '', '', ''],  # 7
            ['', '', '', '', '', '', '', '', ''],  # 8
            ['', '', '', '', '', '', '', '', ''],  # 9
            ['', '', '', '', '', '', '', '', ''], ]  # 10

        # dict with key:value pairs corresponding to array positions
        self._positions = {
            # A
            'a1': (0, 0),
            'a2': (1, 0),
            'a3': (2, 0),
            'a4': (3, 0),
            'a5': (4, 0),
            'a6': (5, 0),
            'a7': (6, 0),
            'a8': (7, 0),
            'a9': (8, 0),
            'a10': (9, 0),
            # B
            'b1': (0, 1),
            'b2': (1, 1),
            'b3': (2, 1),
            'b4': (3, 1),
            'b5': (4, 1),
            'b6': (5, 1),
            'b7': (6, 1),
            'b8': (7, 1),
            'b9': (8, 1),
            'b10': (9, 1),
            # C
            'c1': (0, 2),
            'c2': (1, 2),
            'c3': (2, 2),
            'c4': (3, 2),
            'c5': (4, 2),
            'c6': (5, 2),
            'c7': (6, 2),
            'c8': (7, 2),
            'c9': (8, 2),
            'c10': (9, 2),
            # D
            'd1': (0, 3),
            'd2': (1, 3),
            'd3': (2, 3),
            'd4': (3, 3),
            'd5': (4, 3),
            'd6': (5, 3),
            'd7': (6, 3),
            'd8': (7, 3),
            'd9': (8, 3),
            'd10': (9, 3),
            # E
            'e1': (0, 4),
            'e2': (1, 4),
            'e3': (2, 4),
            'e4': (3, 4),
            'e5': (4, 4),
            'e6': (5, 4),
            'e7': (6, 4),
            'e8': (7, 4),
            'e9': (8, 4),
            'e10': (9, 4),
            # F
            'f1': (0, 5),
            'f2': (1, 5),
            'f3': (2, 5),
            'f4': (3, 5),
            'f5': (4, 5),
            'f6': (5, 5),
            'f7': (6, 5),
            'f8': (7, 5),
            'f9': (8, 5),
            'f10': (9, 5),
            # G
            'g1': (0, 6),
            'g2': (1, 6),
            'g3': (2, 6),
            'g4': (3, 6),
            'g5': (4, 6),
            'g6': (5, 6),
            'g7': (6, 6),
            'g8': (7, 6),
            'g9': (8, 6),
            'g10': (9, 6),
            # H
            'h1': (0, 7),
            'h2': (1, 7),
            'h3': (2, 7),
            'h4': (3, 7),
            'h5': (4, 7),
            'h6': (5, 7),
            'h7': (6, 7),
            'h8': (7, 7),
            'h9': (8, 7),
            'h10': (9, 7),
            # I
            'i1': (0, 8),
            'i2': (1, 8),
            'i3': (2, 8),
            'i4': (3, 8),
            'i5': (4, 8),
            'i6': (5, 8),
            'i7': (6, 8),
            'i8': (7, 8),
            'i9': (8, 8),
            'i10': (9, 8),
        }

        # initializing game's Players, their Pieces, and the board, as well
        # as various data members for program functionality
        self._game_initialized = False
        self._b = Player("blue")
        self._r = Player("red")
        self._players = [self._b, self._r]
        self._blue_pos = {}
        self._red_pos = {}
        self._gen_check = False
        self._blue_palace = ['d8', 'd9', 'd10', 'e8', 'e9', 'e10', 'f8', 'f9', 'f10']
        self._red_palace = ['d1', 'd2', 'd3', 'e1', 'e2', 'e3', 'f1', 'f2', 'f3']
        self._is_in_palace = False

        self._game_state = "UNFINISHED"  # RED_WON // BLUE_WON
        self._player_turn = "BLUE"  # RED
        self.initialize_game_board()

    def initialize_game_board(self):
        """
        Method to initialize the starting game board layout. Piece objects
        will be added to the proper board slots in the 2 dimensional array
        when the JanggiGame instance is made.
        """
        if self._game_initialized is True:
            pass
        for player in self._players:
            if player.get_color() == 'blue':
                self.update_board('e9', player.get_pieces()[0])  # general
                self.update_board('d10', player.get_pieces()[1])  # guard
                self.update_board('f10', player.get_pieces()[2])  # guard
                self.update_board('c10', player.get_pieces()[3])  # horse
                self.update_board('h10', player.get_pieces()[4])  # horse
                self.update_board('b10', player.get_pieces()[5])  # elephant
                self.update_board('g10', player.get_pieces()[6])  # elephant
                self.update_board('a10', player.get_pieces()[7])  # chariot
                self.update_board('i10', player.get_pieces()[8])  # chariot
                self.update_board('b8', player.get_pieces()[9])  # cannon
                self.update_board('h8', player.get_pieces()[10])  # cannon
                self.update_board('a7', player.get_pieces()[11])  # soldier
                self.update_board('c7', player.get_pieces()[12])  # soldier
                self.update_board('e7', player.get_pieces()[13])  # soldier
                self.update_board('g7', player.get_pieces()[14])  # soldier
                self.update_board('i7', player.get_pieces()[15])  # soldier
            elif player.get_color() == 'red':
                self.update_board('e2', player.get_pieces()[0])  # general
                self.update_board('d1', player.get_pieces()[1])  # guard
                self.update_board('f1', player.get_pieces()[2])  # guard
                self.update_board('c1', player.get_pieces()[3])  # horse
                self.update_board('h1', player.get_pieces()[4])  # horse
                self.update_board('b1', player.get_pieces()[5])  # elephant
                self.update_board('g1', player.get_pieces()[6])  # elephant
                self.update_board('a1', player.get_pieces()[7])  # chariot
                self.update_board('i1', player.get_pieces()[8])  # chariot
                self.update_board('b3', player.get_pieces()[9])  # cannon
                self.update_board('h3', player.get_pieces()[10])  # cannon
                self.update_board('a4', player.get_pieces()[11])  # soldier
                self.update_board('c4', player.get_pieces()[12])  # soldier
                self.update_board('e4', player.get_pieces()[13])  # soldier
                self.update_board('g4', player.get_pieces()[14])  # soldier
                self.update_board('i4', player.get_pieces()[15])  # soldier

        self._game_initialized = True

    def get_game_state(self):
        """
        Get method for returning the game's state, which will be initialized to 'UNFINISHED'
        and result in either 'BLUE_WON' or 'RED_WON'.
        """
        return self._game_state

    def make_move(self, pos_from, pos_to):
        """
        Method which takes string parameters corresponding to board position and will
        pass them to the constructor method's dictionary, holding key:value pairs of
        letter combinations (like a1 or f3) that correspond to the proper array position
        on the game board. It will then process the move through a series of checks and
        helper methods, and update the game board if the move is found to be valid for
        that particular piece/player.
        """

        y, x = self._positions[pos_from][0], self._positions[pos_from][1]
        piece = self._board[y][x]

        if self._game_state != 'UNFINISHED':
            return False

        # piece must exist and belong to player whose turn it is
        if not self.check_pos(piece) and self._gen_check is False:
            return False

        # is the move a valid square/not out of bounds
        if pos_to not in self._positions.keys():
            return False

        # passing a turn
        if pos_from == pos_to:
            if self._player_turn == 'BLUE':
                self._player_turn = 'RED'
                return True

            self._player_turn = 'BLUE'
            return True

        # check if move is within palace for certain pieces
        if piece.get_name() == 'Soldier':
            if piece.get_color() == 'blue':
                if pos_from in self._blue_palace:
                    self._is_in_palace = True

            if piece.get_color() == 'red':
                if pos_from in self._red_palace:
                    self._is_in_palace = True

        # is the move valid for that piece
        if self.move_check(pos_from, pos_to) is False:
            return False

        # check if friendly piece isn't in the way
        a, b = self._positions[pos_to][0], self._positions[pos_to][1]
        next_slot = self._board[a][b]
        if next_slot != '':
            if next_slot.get_color() == piece.get_color():
                return False

        # check if general/guard and moving within palace
        if piece.get_name() == 'General' or piece.get_name() == 'Guard':
            if self.in_palace(piece, pos_to) is False:
                return False

        if piece.get_name() == 'Cannon':
            if self.check_screen(pos_from, pos_to) is False:
                return False

        if piece.get_name() == 'Cannon':
            if next_slot != '':
                if next_slot.get_name() == 'Cannon':
                    return False

        # if the player's general is in check, it forces them to pass a move
        # get out of check. if the move is invalid, this helper will return false
        # if there are no valid moves then the player has been checkmated

        if self.is_in_check(self._player_turn):
            if self.next_turn_in_check(pos_from, pos_to):
                return False

        # bool to break make_move early so as not to edit board when checking
        # whether a player is in check
        if self._gen_check is True:
            return True

        # pass piece position to update_board which will update new pos
        y, x = self._positions[pos_from][0], self._positions[pos_from][1]
        self.update_board(pos_to, self._board[y][x])

        # clear old index
        self._board[y][x] = ''

        # update turn
        if self._player_turn == 'BLUE':
            self._player_turn = 'RED'
        else:
            self._player_turn = 'BLUE'

        # setting in palace bool to false if necessary depending on if a piece
        # like a soldier entered an enemy palace
        self._is_in_palace = False

        # updating game board
        self.update_positions()

        # checking if player is in checkmate after being checked
        if self._player_turn == 'RED':
            self.is_in_checkmate('red')
        else:
            self.is_in_checkmate('blue')
        return True

    def next_turn_in_check(self, pos_from, pos_to):
        """
        Method for checking that the player's next turn is also not in check, and thus
        false. This method passes a proposed move to the game board and checks whether
        the player would still be in check, returning a bool depending on the results.
        The move is then reverted to the actual game board state.
        """
        # pass piece position to update_board which will update new pos
        y, x = self._positions[pos_from][0], self._positions[pos_from][1]
        self.update_board(pos_to, self._board[y][x])

        # clear old index
        self._board[y][x] = ''
        y,x = self._positions[pos_to][0], self._positions[pos_to][1]

        if self.is_in_check(self._player_turn):
            # revert move
            self.update_board(pos_from, self._board[y][x])
            self._board[y][x] = ''
            return True

        self.update_board(pos_from, self._board[y][x])
        self._board[y][x] = ''
        return False

    def possible_move(self, pos_from, pos_to):
        """
        Helper method which will validate the user's attempted move, taking the
        starting position and moving position as parameters. If the move
        is validated for that particular piece, the method will return True and return,
        and make_move will initiate the move.

        If the move cannot be validated, such as in the case where the move is illegal,
        or the player's general is in check and must be moved, then the function will return False.
        """
        y, x = self._positions[pos_from][0], self._positions[pos_from][1]
        piece = self._board[y][x]

        # check if move is within palace
        if piece.get_name() == 'General' or piece.get_name() == 'Guard':
            if self.in_palace(piece, pos_to) is False:
                return False

        # is the move valid for that piece
        if self.move_check(pos_from, pos_to) is False:
            return False

        if piece.get_name() == 'Cannon':
            if self.check_screen(pos_from, pos_to) is False:
                return False

        # check if friendly piece isn't in the way
        a, b = self._positions[pos_to][0], self._positions[pos_to][1]
        next_slot = self._board[a][b]

        if next_slot != '':
            if next_slot.get_color() == piece.get_color():
                return False

        if piece.get_name() == 'Cannon':
            if next_slot != '':
                if next_slot.get_name() == 'Cannon':
                    return False

        return True

    def check_pos(self, piece):
        """
        Helper function for make_move checking if a passed position parameter
        actually exists as a piece and is not an empty board slot. Next, it
        checks that the piece belongs to the player whose turn it is.
        """
        # check if piece exists
        if piece == '':
            return False

        # check if piece belongs to player turn
        if piece.get_color().upper() != self._player_turn:
            return False

        return True

    def move_check(self, pos_from, pos_to):
        """
        Helper method which will validate the user's attempted move, taking the
        starting position and moving position as parameters, along with the piece
        that is being moved, and the Player object the piece belongs to.
        """
        y, x = self._positions[pos_from][0], self._positions[pos_from][1]
        y2, x2 = self._positions[pos_to][0], self._positions[pos_to][1]

        piece = self._board[y][x]

        if piece.get_name() == 'Soldier':
            if self._is_in_palace is True:
                if piece.movement(y, x, y2, x2, True) is False:
                    return False

        # if specific piece's movement is invalid
        if piece.movement(y, x, y2, x2) is False:
            return False

        return True

    def in_palace(self, piece, pos_to):
        """
        Helper method for checking whether or not a piece's movement,
         in this case, a general or guard, is in the palace or not. If
         not, it is an invalid move and the helper returns false.
        """

        if piece.get_color().lower() == 'red':
            if pos_to not in self._red_palace:
                return False

        if piece.get_color().lower() == 'blue':
            if pos_to not in self._blue_palace:
                return False

        return True

    def check_screen(self, pos_from, pos_to):
        """
        Helper method used to check for valid screens for the cannon piece. A cannon
        must have an intervening piece between its position and destination slots, and
        the piece cannot be another cannon, nor can it land on a cannon. This function
        checks whether or not a screen exists in the board slots in range from a cannon's
        starting position and presumptive moving position.
        """
        from_y, from_x = self._positions[pos_from][0], self._positions[pos_from][1]
        to_y, to_x = self._positions[pos_to][0], self._positions[pos_to][1]
        counter = 0

        if from_x == to_x:
            if from_y > to_y:
                for element in range(to_y+1, from_y):
                    if self._board[element][from_x] != '' and \
                            self._board[element][from_x].get_name() != 'Cannon':
                        counter += 1
                if counter != 1:
                    return False
                else:
                    return True

            if to_y > from_y:
                for element in range(from_y + 1 , to_y):
                    if self._board[element][from_x] != '' and \
                            self._board[element][from_x].get_name() != 'Cannon':
                        counter += 1
                if counter != 1:
                    return False
                else:
                    return True

        if from_y == to_y:
            if from_x > to_x:
                for element in range(to_x, from_x):
                    if self._board[from_y][element] != '' and \
                            self._board[from_y][element].get_name() != 'Cannon':
                        counter += 1
                if counter != 1:
                    return False
                else:
                    return True

            if to_x > from_x:
                for element in range(from_x + 1, to_x):
                    if self._board[from_y][element] != '' and \
                            self._board[from_y][element].get_name() != 'Cannon':
                        counter += 1
                if counter != 1:
                    return False
                else:
                    return True

        # else no screens were found
        return False

    def is_in_check(self, color):
        """
        Method which takes player color as a parameter, and returns true if the
        player's general is in check. This method iterates through the enemy
        player's pieces and checks whether or not their position has a valid move
        onto the general in question. If so, the general is in check, and must
        be moved.
        """
        # is it a valid move for enemy pieces? then check
        if color.lower() == 'red':
            gen = self.get_general('red')

            for pos in self._blue_pos.values():
                origin = self.get_pos(pos, 'blue')

                if self.possible_move(origin, gen):
                    return True

        if color.lower() == 'blue':
            gen = self.get_general('blue')

            for pos in self._red_pos.values():
                origin = self.get_pos(pos, 'red')

                if self.possible_move(origin, gen):
                    return True

        return False

    def is_in_checkmate(self, color):
        """
        Helper method which checks to see if the enemy general is in checkmate
        at the end of a turn. For a general to be in checkmate, the general must
        first be in check.

        The positions around the general are stored in an array of tuples. Then,
        the method recursively passes these positions to checkmate_helper which
        checks whether  these positions are in range of an enemy piece with a valid move.
         If all positions around the general are in check, then the general has been
        checkmated and the game is over.

        If a particular slot around a general is occupied, it is skipped, as the general
        cannot move to that position anyway.
        """

        positions = [(1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0)]

        if self.is_in_check(color):
            for pos in range(len(positions)):

                y, x = self.get_index('General', color)
                temp_y, temp_x = positions[pos]
                y += temp_y
                x += temp_x
                gen = self.get_pos((y, x), color)
                a, b = self._positions[gen]
                if self._board[a][b] != '':
                    if self._board[a][b].get_name() != 'General':
                        continue

                if self.checkmate_helper(gen, color) is False:
                    return False

            if color == 'red':
                self._game_state = 'BLUE_WON'
            else:
                self._game_state = 'RED_WON'

            # bool to break make_move function early so as not to update the board
            self._gen_check = False
            return True

        return False

    def checkmate_helper(self, gen, color):
        """
        Helper method which recursively checks whether the positions around
        a general are in range of an enemy piece. The pieces in an the opposing
        player's arsenal are iterated through and passed to each board slot around
        the general. If all the slots around the general are threatened by enemy
        pieces, then the game is over.
        """

        if color.lower() == 'red':

            if gen not in self._red_palace:
                return

            for pos in self._blue_pos.values():
                origin = self.get_pos(pos, color)

                if self.possible_move(origin, gen):
                    return True

        else:
            if gen not in self._blue_palace:
                return

            for pos in self._red_pos.values():
                origin = self.get_pos(pos, color)

                if self.possible_move(origin, gen):
                    return True

        return False

    def get_general(self, color):
        """
        Get method for returning the general's position, used in check
        and checkmate logic.
        """
        if color.lower() == 'red':
            for key, value in self._positions.items():
                if value == self.get_index('General', 'red'):
                    return key

        if color.lower() == 'blue':
            for key, value in self._positions.items():
                if value == self.get_index('General', 'blue'):
                    return key

    def get_index(self, value, color):
        """
        Get method for returning the index of a piece by taking its name and color
        as parameters.
        """
        for row, index in enumerate(self._board):
            for element in index:
                if element != '':
                    if element.get_name() == value and element.get_color() == color:
                        return row, index.index(element)

    def get_pos(self, pos, color):
        """
        Get method for returning the algebraic notation position of a piece by taking
        its index and color.
        """
        if color.lower() == 'red':
            for key, value in self._positions.items():
                if value == pos:
                    return key

        if color.lower() == 'blue':
            for key, value in self._positions.items():
                if value == pos:
                    return key

    def update_positions(self):
        """
        Method which updates the game's pieces positions after a successful move.
        The function clears the old positions dictionaries, and then enumerates
        through the 2d array, filling the player positions dictionaries with
        proper positions for each piece still left on the board.
        """
        self._blue_pos = {}
        self._red_pos = {}

        for row, index in enumerate(self._board):
            for element in index:
                if element != '':
                    if element.get_color() == 'blue':
                        self._blue_pos[element] = row, index.index(element)

        for row, index in enumerate(self._board):
            for element in index:
                if element != '':
                    if element.get_color() == 'red':
                        self._red_pos[element] = row, index.index(element)

    def update_board(self, key, piece):
        """
        Method for updating the gameboard when a piece makes a successful move.
        """
        y, x = self._positions[key][0], self._positions[key][1]

        self._board[y][x] = piece
        return True


class Player:
    """
    Player class where Player objects will be represented. Players will contain a data
    structure containing Piece objects belonging to them, which is filled at game
    initialization. Player instances are created within the main JanggiGame class.
    """

    def __init__(self, color):
        """
        Constructor class where the Player object's data members are initialized.
        Each of the two player objects are assigned a color, and have an array
        containing Piece objects in their position.
        """
        self._color = color
        self._pieces = []
        self.initialize_pieces()

    def initialize_pieces(self):
        """
        Method to initialize a Player's starting inventory of game pieces.
        """
        self._pieces.append(General('General', self._color))
        # 2 guards
        self._pieces.append(Guard('Guard', self._color))
        self._pieces.append(Guard('Guard', self._color))
        # 2 horses
        self._pieces.append(Horse('Horse', self._color))
        self._pieces.append(Horse('Horse', self._color))
        # 2 elephants
        self._pieces.append(Elephant('Elephant', self._color))
        self._pieces.append(Elephant('Elephant', self._color))
        # 2 chariots
        self._pieces.append(Chariot('Chariot', self._color))
        self._pieces.append(Chariot('Chariot', self._color))
        # 2 cannons
        self._pieces.append(Cannon('Cannon', self._color))
        self._pieces.append(Cannon('Cannon', self._color))
        # 5 soldiers
        for _ in range(5):
            self._pieces.append((Soldier('Soldier', self._color)))

    def get_color(self):
        """
        Get method for returning the color of a particular player object.
        """
        return self._color

    def get_pieces(self):
        """
        Get method for returning the pieces a player object contains.
        """
        return self._pieces


class Piece:
    """
    Piece super class which specific Janggi pieces such as General or Soldier
    will inherit from. This class will contains the basic data members of each
    piece that inherits from it, such as name and color, as well as the palace
    positions for each player, which is used in palace movement for pieces like
    the Soldier.
    """

    def __init__(self, name, color):
        """
        Constructor method for Piece super class. Each piece object will be initialized
        by name and color.
        """
        self._name = name
        self._color = color
        self._blue_palace = ['d8', 'd9', 'd10', 'e8', 'e9', 'e10', 'f8', 'f9', 'f10']
        self._red_palace = ['d1', 'd2', 'd3', 'e1', 'e2', 'e3', 'f1', 'f2', 'f3']

    def __repr__(self):
        """
        Repr method to represent the piece objects as two letter abbreviations
        depending on the first letter in their color and name. Generals and Chariots
        will be represented with their letters reversed in order to differentiate them
        from guards and cannons.
        """
        if self._name == 'General':
            return self._name[0] + self._color[0].upper()

        if self._name == 'Chariot':
            return ('C' + self._color[0]).upper()

        return self._color[0].upper() + self._name[0]

    def get_color(self):
        """
        Get method for returning piece color.
        """
        return self._color

    def get_name(self):
        """
        Get method for returning piece name.
        """
        return self._name

    def palace(self, color):
        """
        Method for returning palace positions for a particular player object,
        by taking their color as a parameter. Used in movement for pieces within
        a palace/fortress.
        """
        if color.lower() == 'red':
            return self._red_palace
        else:
            return self._blue_palace


class General(Piece):
    """
    General class inheriting data members and methods from Piece.
    """

    def __init__(self, name, color):
        """
        Constructor method for general class inheriting from Piece.
        """
        super().__init__(name, color)

    def movement(self, from_y, from_x, to_y, to_x):
        """
        Method which handles movement for the General class, called within JanggiGame
        to perform a successful move after it is validated.
        """
        if to_y == from_y and (to_x == from_x - 1 or to_x == from_x + 1):
            return True

        if to_x == from_x and (to_y == from_y - 1 or to_y == from_y + 1):
            return True

        if to_y == from_y + 1 and (to_x == from_x - 1 or to_x == from_x + 1):
            return True

        if to_y == from_y - 1 and (to_x == from_x - 1 or to_x == from_x + 1):
            return True

        return False


class Guard(Piece):
    """
    Guard class inheriting data members and methods from Piece.
    """

    def __init__(self, name, color):
        """
        Constructor method for Guard class inheriting from Piece
        """
        super().__init__(name, color)

    def movement(self, from_y, from_x, to_y, to_x):
        """
        Method which handles movement for the Guard class, called within JanggiGame
        to perform a successful move after it is validated.
        """
        if to_y == from_y and (to_x == from_x - 1 or to_x == from_x + 1):
            return True

        if to_x == from_x and (to_y == from_y - 1 or to_y == from_y + 1):
            return True

        if to_y == from_y + 1 and (to_x == from_x - 1 or to_x == from_x + 1):
            return True

        if to_y == from_y - 1 and (to_x == from_x - 1 or to_x == from_x + 1):
            return True

        return False


class Horse(Piece):
    """
    Horse class inheriting data members and methods from Piece.
    """

    def __init__(self, name, color):
        """
        Constructor method for Horse class inheriting from Piece.
        """
        super().__init__(name, color)

    def movement(self, from_y, from_x, to_y, to_x):
        """
        Method for calculating valid horse moves. Horses will always have the same
        relative movements, and so horse_positions is a list of tuples containing these
        relative values to ensure that the horse is making a valid move.
        """
        horse_positions = [(2, 1), (2, -1), (1, 2), (1, -2),
                           (-1, -2), (-1, 2), (-2, -1), (-2, 1)]

        if ((to_y - from_y), (to_x - from_x)) not in horse_positions:
            return False


class Elephant(Piece):
    """
    Elephant class inheriting data members and methods from Piece.
    """

    def __init__(self, name, color):
        """
        Constructor method for Elephant class inheriting from Piece.
        """
        super().__init__(name, color)

    def movement(self, from_y, from_x, to_y, to_x):
        """
        Method for calculating valid horse moves. Horses will always have the same
        relative movements. horse_positions is a list of tuples containing these
        relative values to ensure that the horse is making a valid move.
        """
        elephant_positions = [(3, 2), (3, -2), (2, 3), (2, -3),
                              (-2, -3), (-2, 3), (-3, -2), (-3, 2)]

        if ((to_y - from_y), (to_x - from_x)) not in elephant_positions:
            return False


class Chariot(Piece):
    """
    Chariot class inheriting data members and methods from Piece.
    """

    def __init__(self, name, color):
        """
        Constructor method for Chariot class inheriting from Piece.
        """
        super().__init__(name, color)

    def movement(self, from_y, from_x, to_y, to_x):
        """
        Method detailing movement for the Chariot object, which is analogous
        to a rook in Western chess.
        """
        if from_y == to_y or from_x == to_x:
            return True
        return False


class Cannon(Piece):
    """
    Cannon class inheriting data members and methods from Piece.
    """

    def __init__(self, name, color):
        """
        Constructor method for Cannon class inheriting from Piece.
        """
        super().__init__(name, color)

    def movement(self, from_y, from_x, to_y, to_x):
        """
        Movement method containing the possible positions for a Cannon piece.
        When this method is called, the cannon's move has been validated in the
        main JanggiGame class in terms of having a valid screen, not jumping over
        another cannon, and not capturing a cannon on a valid move.
        """
        if from_y == to_y:
            return True

        if from_x == to_x:
            return True
        return False


class Soldier(Piece):
    """
    Soldier class inheriting data members and methods from Piece.
    """

    def __init__(self, name, color):
        """
        Constructor method for Soldier class inheriting from Piece.
        """
        super().__init__(name, color)

    def movement(self, from_y, from_x, to_y, to_x, in_palace=None):
        """
        Method for handling movement in the Soldier class. Besides basic
        movement functionality, soldiers may also move diagonally within a palace.
        When a soldier reaches the end of a board, it may only move side to side
        and does not promote.
        """
        if not in_palace:
            if self.get_color() == 'red':
                if to_y == from_y and (to_x == from_x + 1 or to_x == from_x - 1):
                    return True

                if to_x == from_x and to_y == from_y + 1:
                    return True

            if self.get_color() == 'blue':
                if to_y == from_y and (to_x == from_x + 1 or to_x == from_x - 1):
                    return True

                if to_x == from_x and to_y == from_y - 1:
                    return True

        if self.get_color() == 'red':

            if to_y == from_y and (to_x == from_x - 1 or to_x == from_x + 1):
                return True

            if to_x == from_x and to_y == from_y + 1:
                return True

            if to_y == from_y + 1 and (to_x == from_x - 1 or to_x == from_x + 1):
                return True

        if self.get_color() == 'blue':

            if to_y == from_y and (to_x == from_x - 1 or to_x == from_x + 1):
                return True

            if to_x == from_x and to_y == from_y - 1:
                return True

            if to_y == from_y - 1 and (to_x == from_x - 1 or to_x == from_x + 1):
                return True

        return False
