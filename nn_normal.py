#Stanisław Dutkiewicz 
class NeutronBoard:
    """
    The NeutronBoard class represents the game board for the Neutron game.
    """
    def __init__(self):
        """
        Initialize the game board, the directions for moving pieces, and other
        variables such as neutron_moved, current_piece, and move_count.

        Args:
            board (list): The game board represented as a 2D list, with 'P' representing player pieces,
            'N' representing neutron, 'O' representing obstacle, and ' ' representing empty spaces.
            
            directions (dict): A dictionary containing the possible directions for moving pieces on the board,
            with keys as the direction strings ('up', 'down', 'left', 'right', etc.)
                            
            neutron_moved (bool): A flag that indicates whether the neutron has been moved in the current turn.
            
            current_piece (str): The current piece that the player is trying to move.
            
            move_count (int): The number of moves that have been made in the current game.
            
            first_move (tuple): Used to create initiate the start move from the player.
    """
        self.board =[
                    ['P', 'P', 'P', 'P', 'P'],
                    [' ', ' ', ' ', ' ', ' '],
                    [' ', ' ', 'O', ' ', ' '],
                    [' ', ' ', ' ', ' ', ' '],
                    ['N', 'N', 'N', 'N', 'N']]
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
        self.neutron_moved = False
        self.current_piece = None
        self.move_count = 0
        self.first_move = None
    

    def find_neutron(self):
        """
        Find the current position of the neutron on the game board.
        
        Returns:
            Tuple (int, int): The row and column indexes of the neutron on the board
        """
        for i, row in enumerate(self.board):
            for j, piece in enumerate(row):
                if piece == 'O':
                    return i, j

    def move_piece(self, row, col, direction):
        """
        Move a piece on the current game board to a new position in the specified direction.
        Args:
            row (int): current row of the piece to be moved
            col (int): current column of the piece to be moved
            direction (str): direction in which the piece is to be moved
        Returns:
            bool: True if the move is successful, False otherwise
        """
        # Check if the move is valid
        if not self.valid_move(row, col, direction):
            return False
        
        # Get the row and column offset for the specified direction
        row_offset, col_offset = self.directions[direction]

        # Get the piece at the current position
        piece = self.board[row][col]

        # Calculate the new position of the piece
        new_row = row + row_offset
        new_col = col + col_offset

        # Move the piece to the new position as long as 
        # it is within the board boundaries and the new space is empty
        while (0 <= new_row < 5) and (0 <= new_col < 5) and (self.board[new_row][new_col] == ' '):
            self.board[row][col] = ' '
            self.board[new_row][new_col] = piece
            row = new_row
            col = new_col
            new_row += row_offset
            new_col += col_offset

        return True

    def check_winner(self):
        """
        Check if there is a winner

        Returns:
            str: 'N' if N wins, 'P' if P wins, 
            'T' if it is blocked
        """

        i, j = self.find_neutron()
        if i == 0:
            return 'P'
        elif i == 4:
            return 'N'
        # Check if the neutron is blocked by a piece or wall on all sides
        if (self.board[i-1][j] != ' ' and self.board[i+1][j] != ' ' and
                self.board[i][j-1] != ' ' and self.board[i][j+1] != ' '):
            # Check if the neutron is completely surrounded by pieces
            if (self.board[i-1][j] != 'N' and self.board[i+1][j] != 'N' and
                    self.board[i][j-1] != 'N' and self.board[i][j+1] != 'N'):
                return 'T'
            return 'P' if self.players[0].color == 'N' else 'N'
        return None


    def is_valid_move(self, current_i: int, current_j: int, direction: str):
        """
        Check if a move is valid
        Args:
            current_i (int): current row of the piece to be moved
            current_j (int): current column of the piece to be moved
            direction (str): direction in which the piece is to be moved
        Returns:
            bool: True if move is valid, False otherwise
        """

        # Check if the direction is a valid key in self.directions
        if direction not in self.directions:
            return False

        # Calculate the new row and column after the move
        row, col = current_i + self.directions[direction][0], current_j + self.directions[direction][1]

        # Check if the new row and column are within the board's boundaries
        if row < 0 or row > 4 or col < 0 or col > 4:
            return False
        
        # Check if the new spot on the board is empty
        if self.board[row][col] != " ":
            return False

        return True



    def human_move(self):
        """
        Allow the human player to make a move.

        Args:
            player (Players): the player object representing the human player

        Returns:
            bool: True if the human player has made a valid move, False otherwise
        """

        # Get the current position and desired direction of the selected piece
        direction = self.direction_var.get()
        current_i, current_j = self.current_piece
        
        # Make the move on the board
        if self.move_piece(current_i, current_j, direction) == True:
            pass
        else:
            return False
        
        self.current_piece = None
        # Checks if the human won
        if self.check_winner() is not None:
            # If there is a 'T' as the winner then the player who blocked a neutron wins
            if self.check_winner() == 'T':
                self.check_winner() == str(self.players[0].color)
                self.game_over(self.players[0].color)
            self.game_over(self.players[0].color)
        return True

    
    def computer_move(self):
        """
        This function is used to make a move for the computer player. 
        The move is determined by using the function from PLayers class.

        Returns:
            bool: True if a valid move was made, False otherwise.
        """
        # Moves the neutron
        neutron_move = self.players[1].get_computer_move_neutron(self.board)
        if neutron_move:
            self.move_piece(*neutron_move)
        
        # Moves a piece
        piece_move = self.players[1].get_computer_move(self.board)
        if piece_move:
            self.move_piece(*piece_move)
        
       # Checks if the computer won
        if self.check_winner() is not None:
            # If there is a 'T' as the winner then the player who blocked a neutron wins
            if self.check_winner() == 'T':
                self.check_winner() == str(self.players[1].color)
                self.game_over(self.players[1].color)
            self.game_over(self.players[1].color)
        return True
        

    def switch_neutron_moved(self):
        """
        Switch the value of neutron_moved.
        """
        self.neutron_moved = not self.neutron_moved

    def valid_move(self, row, col, direction):
        """
        Check if the specified move is valid.
        A move is valid if it is within the boundaries of the board and
        the new space is empty.

        Args:
            current_i (int): The current row of the piece to be moved.
            current_j (int): The current column of the piece to be moved.
            direction (str): The direction to move the piece.

        Returns:
            bool: True if the move is valid, False otherwise.
        """
        row_offset, col_offset = self.directions[direction]
        new_row = row + row_offset
        new_col = col + col_offset
        if new_row < 0 or new_row > 4 or new_col < 0 or new_col > 4:
            return False
        elif self.board[new_row][new_col] != ' ':
            return False
        return True

