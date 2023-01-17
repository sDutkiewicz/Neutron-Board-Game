import random
import kinterboard

class Players:
    def __init__(self, name: str, color: str, strategy: str):
        self.name = name
        self.color = color
        self.strategy = strategy
        self.board = self.bar()
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

    def bar(self):
        return kinterboard.NeutronBoardd()
    


    def get_valid_moves(self, board, is_valid_move):
        """Return a list of valid moves for the player"""
        valid_moves = []
        for i in range(5):
            for j in range(5):
                if board[i][j] == self.color:
                    for direction in self.directions:
                        if is_valid_move(i, j, direction):
                            valid_moves.append((i, j, direction))
        return valid_moves

    def get_valid_neutron_moves(self, board, is_valid_move):
        """Return a list of valid moves for the neutron"""
        valid_moves = []
        for i in range(5):
            for j in range(5):
                if board[i][j] == "O":
                    for direction in self.directions:
                        if is_valid_move(i, j, direction):
                            valid_moves.append((i, j, direction))
        return valid_moves



    def get_move(self, board, current_player):
        """Get the next move for the player"""
        if current_player == self and self.strategy == "Human":
            return None  # Return None to indicate that the move should be prompted from the player
        elif current_player == self and self.strategy == "Computer":
            valid_moves = self.get_valid_moves(board)
            if valid_moves:
                return random.choice(valid_moves)
            else:
                return None  # Return None to indicate that the player has no valid moves

    def distance_to_wall(self, row, col):
        distances = {}
        for direction, (dr, dc) in self.directions.items():
            r, c = row + dr, col + dc
            distance = 0
            while 0 <= r < 5 and 0 <= c < 5:
                distance += 1
                r, c = r + dr, c + dc
            distances[direction] = distance
        return distances

    def smart_move_piece(self, board, row, col, get_valid_moves):
        '''
        Move the piece at position (row, col) in a direction that brings it closer to a wall 
        '''
        directions = ['up', 'down', 'left', 'right', 'up-right', 'up-left', 'down-right', 'down-left']
        distances = self.distance_to_wall(row, col)
        # Sort the directions by distance to the nearest wall
        directions = sorted(directions, key=lambda x: distances[x])
        valid_moves = get_valid_moves(board)
        for direction in directions:
            i, j = row + self.directions[direction][0], col + self.directions[direction][1]
            if (row, col, direction) in valid_moves:
                board[row][col], board[i][j] = board[i][j], board[row][col]
                return True
        return False

    def smart_move_neutron(self, board, neutron_row, neutron_col):
        """
        Move the neutron to a position that brings it closer to the opponent's pieces
        """
        distances = {}
        # calculate the distance from each of opponent's pieces to the neutron
        for i in range(5):
            for j in range(5):
                if board[i][j] == self.opponent_color:
                    distance = abs(neutron_row - i) + abs(neutron_col - j)
                    distances[(i, j)] = distance
        # sort the pieces by distance to the neutron
        distances = sorted(distances.items(), key=lambda x: x[1])
        # move the neutron towards the closest piece
        for piece, distance in distances:
            row, col = piece
            row_diff = row - neutron_row
            col_diff = col - neutron_col
            if row_diff > 0:
                direction = 'down'
            elif row_diff < 0:
                direction = 'up'
            if col_diff > 0:
                direction = 'right'
            elif col_diff < 0:
                direction = 'left'
            if row_diff > 0 and col_diff > 0:
                direction = 'down-right'
            elif row_diff < 0 and col_diff < 0:
                direction = 'up-left'
            elif row_diff > 0 and col_diff < 0:
                direction = 'down-left'
            elif row_diff < 0 and col_diff > 0:
                direction = 'up-right'
            if self.is_valid_neutron_move(board, neutron_row, neutron_col, direction):
                return neutron_row + self.directions[direction][0], neutron_col + self.directions[direction][1]
        return None
