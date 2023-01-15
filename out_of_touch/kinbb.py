import tkinter as tk
import random


class Player:
    def __init__(self, name, color, strategy):
        self.name = name
        self.color = color
        self.strategy = strategy

    def make_move(self, board):
        if self.strategy == 'human':
            # Prompt the player to enter a move
            while True:
                move = input(f'{self.name}: Enter your move (row column direction): ')
                try:
                    row, col, direction = move.split()
                    row, col = int(row), int(col)
                    if board.move_piece(row, col, direction, self.color):
                        return True
                except ValueError:
                    print('Wrong input, try again!')
                    pass
        elif self.strategy == 'random':
            # Choose a random move
            while True:
                row = int(random.randint(0, 4))
                col = int(random.randint(0, 4))
                direction = random.choice(list(board.directions.keys()))
                if board.move_piece(row, col, direction, self.color):
                    return True

class NeutronBoardd:
    def __init__(self):
        self.root = tk.Tk()
        self.root.config(bg='#ffc180')
        self.root.title("Neutron Board Game")
        self.board = [['P', 'P', 'P', 'P', 'P'],
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
        self.current_player = None
        self.game_over = False
        self.current_piece = None
        self.buttons = []
        self.create_buttons()
        self.create_directions_list()
        self.display_board()
        self.players = [Player("Player1", "N", "Human"), Player("Computer", "P", "Computer")]
        self.turn = 0


    def create_buttons(self):
        for i in range(5):
            for j in range(5):
                button = tk.Button(self.root, text='', width=5, height=2)
                button.config(
                    command=lambda button=button: self.on_button_clicked(button))
                button.grid(row=i, column=j)
                self.buttons.append(button)
        exit_button = tk.Button(self.root, text='Exit',
                                command=self.root.destroy)
        exit_button.grid(row=5, column=5)

    def create_directions_list(self):
        self.direction_var = tk.StringVar(self.root)
        self.direction_var.set(list(self.directions.keys())[0])
        self.direction_list = tk.OptionMenu(
            self.root, self.direction_var, *list(self.directions.keys()))
        self.direction_list.grid(row=5, column=0, columnspan=5)
        self.move_button = tk.Button(
            self.root, text='Move', command=self.on_move_clicked)
        self.move_button.grid(row=6, column=0, columnspan=5)

    def on_button_clicked(self, button):
        """Handle button click event"""
        self.current_piece = (int(button.grid_info()["row"]), int(
            button.grid_info()["column"]))

    def on_move_clicked(self):
        if self.game_over:
            return
        if self.current_piece is None:
            return
        direction = self.direction_var.get()
        if not self.move_piece(self.current_piece[0], self.current_piece[1], direction):
            return
        self.turn = (self.turn + 1) % 2
        self.display_board()
        winner = self.check_winner()
        if winner:
            self.game_over = True
            self.show_winner(winner)
        if self.players[self.turn].strategy == "Computer":
            self.computer_move()
        else:
            self.current_player = self.players[self.turn]


    def find_neutron(self):
        for i, row in enumerate(self.board):
            for j, piece in enumerate(row):
                if piece == 'O':
                    return i, j

    def move_piece(self, row, col, direction):
        try:
            row_offset, col_offset = self.directions[direction]
        except KeyError:
            print("Invalid direction. Please try again.")
            return False

        piece = self.board[row][col]
        if piece == ' ':
            print("No piece to move. Please select a valid piece.")
            return False
        elif piece == 'O':
            if self.neutron_moved:
                print(
                    "The neutron has already been moved this turn. Please select a different piece.")
                return False
            self.neutron_moved = True
        elif piece != self.current_player:
            print("You cannot move your opponent's pieces.")
            return False

        new_row = row + row_offset
        new_col = col + col_offset
        while (0 <= new_row < 5) and (0 <= new_col < 5) and (self.board[new_row][new_col] == ' '):
            self.board[row][col] = ' '
            self.board[new_row][new_col] = piece
            row = new_row
            col = new_col
            new_row += row_offset
            new_col += col_offset

        self.display_board()
        return True

    def check_winner(self):
        """Check if there is a winner"""
        i, j = self.find_neutron()
        # Check if the neutron is blocked by the top or bottom wall
        if i == 0 or i == 4:
            return 'P' if i == 4 else 'N'
        # Check if the neutron is blocked by a piece or wall on all sides
        if (self.board[i-1][j] != ' ' and self.board[i+1][j] != ' ' and
                self.board[i][j-1] != ' ' and self.board[i][j+1] != ' '):
            # Check if the neutron is completely surrounded by pieces
            if (self.board[i-1][j] != 'N' and self.board[i+1][j] != 'N' and
                    self.board[i][j-1] != 'N' and self.board[i][j+1] != 'N'):
                return 'T'  # tie
            return 'P' if self.current_player == 'N' else 'N'
        return None

    def display_board(self):

        for i in range(5):
            for j in range(5):
                self.buttons[i * 5 + j].config(text=self.board[i][j])

    def update_player_label(self):
        """Update the current player label"""
        self.player_label.config(text=self.current_player.name)

    def show_winner(self, winner):
        """Show the winner message"""
        if winner == 'T':
            message = "It's a Tie!"
        else:
            message = f"{winner} player wins!"
        self.winner_label.config(text=message)

    def computer_move(self):
        legal_moves = []
        for i in range(5):
            for j in range(5):
                if self.board[i][j] == self.players[self.turn].color:
                    for direction in self.directions:
                        if self.move_piece(i, j, direction):
                            legal_moves.append((i, j, direction))
        if legal_moves:
            move = random.choice(legal_moves)
            self.move_piece(*move)
            self.display_board()
            self.turn = (self.turn + 1) % 2
            winner = self.check_winner()
            if winner:
                self.game_over = True
                self.show_winner(winner)
            if self.players[self.turn].strategy == "Computer":
                self.computer_move()
            else:
                self.current_player = self.players[self.turn]


    def get_legal_moves(self):
        legal_moves = []
        for i in range(5):
            for j in range(5):
                if self.board[i][j] == self.players[self.turn].color:
                    for direction in self.directions.values():
                        if self.is_valid_move(i, j, direction):
                            legal_moves.append((i, j))
        return legal_moves

    def is_valid_move(self, row, col, direction):
        """Check if a move is valid"""
        row += direction[0]
        col += direction[1]
        if row < 0 or row > 4 or col < 0 or col > 4:
            return False
        if self.board[row][col] != " ":
            return False
        return True
