import random

class Players:
    def __init__(self, name: str, color: str, strategy: str):
        self.name = name
        self.color = color
        self.strategy = strategy
        # self.board = self.bar()
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
        if self.strategy == "random":
            valid_moves = self.get_valid_moves(board, self.is_valid_move)
            neutron_moves = self.get_valid_neutron_moves(board, self.is_valid_neutron_move)
            if valid_moves:
                return random.choice(valid_moves)
            elif neutron_moves:
                return random.choice(neutron_moves)
            else:
                return None
        elif self.strategy == "smart":
            # find the location of the neutron on the board
            for i in range(5):
                for j in range(5):
                    if board[i][j] == "O":
                        neutron_row, neutron_col = i, j
                        break
            # use the smart_move_piece and smart_move_neutron functions to determine the best move
            move = self.smart_move_piece(board, neutron_row, neutron_col, self.get_valid_moves)
            if move:
                return move
            else:
                move = self.smart_move_neutron(board, neutron_row, neutron_col, self.get_valid_moves)
                return move


    def is_valid_move(self, board, current_i: int, current_j: int, direction: str):
        """Check if a move is valid"""
        if direction not in self.directions:
            return False
        row, col = current_i + self.directions[direction][0], current_j + self.directions[direction][1]
        if row < 0 or row > 4 or col < 0 or col > 4:
            return False
        if board[row][col] != " ":
            return False
        return True

    


    def get_valid_moves(self, board, is_valid_move):
        """Return a list of valid moves for the player"""
        valid_moves = []
        for i in range(5):
            for j in range(5):
                if board[i][j] == self.color:
                    for direction in self.directions:
                        if is_valid_move(board,i, j, direction):
                            valid_moves.append((i, j, direction))
        return valid_moves

    def get_valid_neutron_moves(self, board, is_valid_move):
        """Return a list of valid moves for the neutron"""
        valid_moves = []
        for i in range(5):
            for j in range(5):
                if board[i][j] == "O":
                    for direction in self.directions:
                        if is_valid_move(board, i, j, direction):
                            valid_moves.append((i, j, direction))
        return valid_moves


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
        valid_moves = get_valid_moves(board, self.is_valid_move)
        for direction in directions:
            i, j = row + self.directions[direction][0], col + self.directions[direction][1]
            if (row, col, direction) in valid_moves:
                return row, col, direction
        return None

    def smart_move_neutron(self, board, row, col, get_valid_moves):
        '''
        Move the neutron at position (row, col) to a position that brings it closer to the opponent's pieces
        '''
        directions = ['up', 'down', 'left', 'right', 'up-right', 'up-left', 'down-right', 'down-left']
        distances = self.distance_to_opponent(board, row, col)
        # Sort the directions by distance to the nearest opponent piece
        directions = sorted(directions, key=lambda x: distances[x])
        valid_moves = get_valid_moves(board, self.is_valid_neutron_move)
        for direction in directions:
            i, j = row + self.directions[direction][0], col + self.directions[direction][1]
            if (row, col, direction) in valid_moves:
                board[row][col], board[i][j] = board[i][j], board[row][col]
                return row, col, direction
        return None


    def is_valid_neutron_move(self, board, row, col, direction):
        i, j = row + self.directions[direction][0], col + self.directions[direction][1]
        if i < 0 or i > 4 or j < 0 or j > 4:
            return False
        if board[i][j] != " ":
            return False
        return True

    def distance_to_opponent(self, board, neutron_row, neutron_col):
        directions = ['up', 'down', 'left', 'right', 'up-right', 'up-left', 'down-right', 'down-left']
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


