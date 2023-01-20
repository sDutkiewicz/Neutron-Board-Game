import random


class Players:
    """
    The Players class represents a player in the Neutron game.
    It contains methods and properties for determining a
    player's moves and strategies.
    """

    def __init__(self, name: str, color: str, strategy: str):
        """
        Initialize a new player object.

        Args:
            name (str): The name of the player.
            color (str): The color of the player's pieces.
            strategy (str): The player's strategy for making moves.
                Can be 'random' or 'smart'.
        """

        self.name = name
        self.color = color
        self.strategy = strategy
        self.directions = {
            'up': (-1, 0),
            'down': (1, 0),
            'left': (0, -1),
            'right': (0, 1),
            'up-right': (-1, 1),
            'up-left': (-1, -1),
            'down-right': (1, 1),
            'down-left': (1, -1)
        }

    def get_computer_move(self, board):
        """
        Determine the best move for the computer player based
        on the current strategy.

        Args:
            board (list): 2D list representing the current
            state of the game board

        Returns:
            tuple: A tuple containing the row, column and direction of
            the best move for the computer player or None
        """
        if self.strategy == "random":

            valid_moves = self.get_valid_moves(board, self.is_valid_move)
            # If there are valid moves, choose one at random
            if valid_moves:
                return random.choice(valid_moves)
            else:
                return None

        elif self.strategy == "smart":

            # Finds the location of the neutron on the board
            neutron_row, neutron_col = self.find_neutron(board)

            # Uses the smart_move_piece and smart_move_neutron
            # functions to determine the best move
            move = self.smart_move_piece(
                board, neutron_row, neutron_col, self.get_valid_moves)
            if move:
                return move
            else:
                return None

    def get_computer_move_neutron(self, board):
        """
        Get the computer's move for the neutron.
        This function is used when the computer
        is moving the neutron.It determines the
        best move for the neutron based on the computer's strategy.

        Args:
            board (list): 2D list representing the current state
            of the game board

        Returns:
            tuple: A tuple containing the row, column and direction of the
            best move for the computer player
            to move neutron or None
        """
        if self.strategy == "random":
            neutron_moves = self.get_valid_neutron_moves(
                board, self.is_valid_neutron_move)

            # If there are valid moves, choose one at random
            if neutron_moves:
                return random.choice(neutron_moves)
            else:
                return None
        elif self.strategy == "smart":

            neutron_row, neutron_col = self.find_neutron(board)
            # Uses the smart_move_piece and smart_move_neutron
            # functions to determine the best move
            move = self.smart_move_neutron(board, neutron_row, neutron_col)
            if move:
                return move

    def is_valid_move(self, board, current_i, current_j, direction):  # noqa: E501
        """
        Checks if a move is valid
        Args:
            board (list): 2D list representing the current state
            of the game board
            current_i (int): current row of the piece to be moved
            current_j (int): current column of the piece to be moved
            direction (str): direction in which the piece is to be moved
        Returns:
            bool: True if move is valid, False otherwise
        """
        if direction not in self.directions:
            return False
        row, col = current_i + \
            self.directions[direction][0], current_j + \
            self.directions[direction][1]
        if row < 0 or row > 4 or col < 0 or col > 4:
            return False
        if board[row][col] != " ":
            return False
        return True

    def get_valid_moves(self, board, is_valid_move):
        """
        Returns a list of valid moves for the player
        Args:
            board (list): 2D list representing the current
            state of the game board
            is_valid_move (function): Function that checks if a move is valid
        Returns:
            list: List of valid moves in the format of
            (current_i, current_j, direction)
        """
        valid_moves = []
        for i in range(5):
            for j in range(5):
                if board[i][j] == self.color:
                    for direction in self.directions:
                        if is_valid_move(board, i, j, direction):
                            valid_moves.append((i, j, direction))
        return valid_moves

    def get_valid_neutron_moves(self, board, is_valid_move):
        """
        Return a list of valid moves for the neutron
        Args:
            board (list): 2D list representing the current state of the board
            is_valid_move (function): Function that checks
            if a move is valid
        Returns:
            list: List of valid moves in the format of
            (current_i, current_j, direction)
        """
        valid_moves = []
        for i in range(5):
            for j in range(5):
                if board[i][j] == "O":
                    for direction in self.directions:
                        if is_valid_move(board, i, j, direction):
                            valid_moves.append((i, j, direction))
        return valid_moves

    def distance_to_wall(self, row, col):
        """
        Calculate the distance of a piece to the closest wall.

        Args:
            row (int): The row of the piece.
            col (int): The column of the piece.

        Returns:
            int: The distance of the piece to the closest wall.
        """
        distances = {}
        for direction, (dr, dc) in self.directions.items():
            r, c = row + dr, col + dc
            distance = 0
            while 0 <= r < 5 and 0 <= c < 5:
                distance += 1
                r, c = r + dr, c + dc
            distances[direction] = distance
        return distances

    def smart_move_piece(self, board, neutron_row, neutron_col, get_valid_moves):  # noqa: E501
        """

        This method uses the strategy 'smart' which is to move
        the piece that is closest to the neutron in the direction
        that has the shortest distance to a wall.

        Args:
            board (list): 2D list representing the current
            state of the game board
            neutron_row (int): the row of the neutron on the board
            neutron_col (int): the column of the neutron
            on the board
            get_valid_moves (function): a function returns
            a list of valid moves.

        Returns:
            tuple: A tuple containing the row, column and direction
            of the best move for the player or False if no
            move is possible.
        """
        # Find the coordinates of all the player's pieces
        piece_coords = []
        for i in range(5):
            for j in range(5):
                if board[i][j] == self.color:
                    piece_coords.append((i, j))

        # Calculate the distance from each piece to the neutron
        distances = [(abs(row - neutron_row) + abs(col - neutron_col))
                     for row, col in piece_coords]

        # Find the index of the piece that is closest to the neutron
        min_index = distances.index(min(distances))

        # Get the position of the closest piece to the neutron
        row, col = piece_coords[min_index]

        # Get the valid moves for the closest piece
        valid_moves = get_valid_moves(board, self.is_valid_move)

        # Calculate the distance from the chosen piece to the
        # nearest wall in each direction
        distances = {
            'up': row,
            'down': 4 - row,
            'left': col,
            'right': 4 - col,
            'up-right': min(row, 4 - col),
            'up-left': min(row, col),
            'down-right': min(4 - row, 4 - col),
            'down-left': min(4 - row, col)
        }

        # Sort the directions by the distance to the nearest wall
        sorted_distances = sorted(distances.items(), key=lambda x: x[1])

        # Try to move the piece in the direction with
        # the smallest distance to a wall
        for direction, distance in sorted_distances:
            if (row, col, direction) in valid_moves:
                return row, col, direction
        return False

    def smart_move_neutron(self, board, row, col):
        """
        Determines the best move for the neutron based
        on the computer's strategy.

        Args:
            board (list): 2D list representing the current state
            of the game board
            row (int): row of the neutron
            col (int): column of the neutron

        Returns:
            tuple: A tuple containing the row, column and
            direction of the best move for the computer
            player to move neutron or or False if no
            move is possible.
        """
        directions = self.directions.keys()
        distances = self.distance_to_opponent(board, row, col)

        # Sort the directions by distance to the nearest opponent piece
        directions = sorted(directions, key=lambda x: distances[x])

        valid_moves = self.get_valid_neutron_moves(
            board, self.is_valid_neutron_move)
        for direction in directions:
            if (row, col, direction) in valid_moves:
                return row, col, direction
        return False

    def is_valid_neutron_move(self, board, row, col, direction):
        """
        Check if a move is valid for the neutron.
        A move is valid for the neutron if the space
        in the given direction is empty.

        Args:
            board (List[List[str]]): The current game board
            current_i (int): The current row of the neutron
            current_j (int): The current column of the neutron
            direction (str): The direction of the move

        Returns:
            bool: True if the move is valid, False otherwise
        """
        i, j = row + self.directions[direction][0], col + \
            self.directions[direction][1]
        if i < 0 or i > 4 or j < 0 or j > 4:
            return False
        if board[i][j] != " ":
            return False
        return True

    def distance_to_opponent(self, board, neutron_row, neutron_col):
        """
        Calculate the minimum distance from a given position to
        the closest piece of the opponent.This function is used
        to determine the best move for a piece when the smart
        strategy is used.
        Arguments:
            board (list): 2D list representing the current
            state of the game board
            row (int) : The row of the piece for which the distance
            to the opponent is calculated
            col (int) : The column of the piece for which the distance
            to the opponent is calculated
            opponent_color (str) : The color of the opponent's pieces
        Returns:
            int: The minimum distance to the closest opponent piece
        """
        directions = self.directions.keys()
        distances = {}
        for direction in directions:
            row, col = neutron_row, neutron_col
            distance = 0
            while (0 <= row < 5) and (0 <= col < 5):
                if board[row][col] == "N":
                    distances[direction] = distance
                    break
                row += self.directions[direction][0]
                col += self.directions[direction][1]
                distance += 1
            if direction not in distances:
                distances[direction] = float('inf')
        return distances

    def find_neutron(self, board):
        """
        Find the current position of the neutron on the game board.

        Args:
            board : 2D list representing the current state of the game board

        Returns:
            Tuple (int) : The row and column indexes
            of the neutron on the board
        """
        for i, row in enumerate(board):
            for j, piece in enumerate(row):
                if piece == 'O':
                    return i, j
