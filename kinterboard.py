import tkinter as tk
import random


class Players:
    def __init__(self, name: str, color: str, strategy: str):
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
        self.players = [Players("Player1", "N", "Human"), Players("Computer", "P", "Computer")]
        self.turn = 0
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
        self.winner_label = tk.Label(self.root, text='', font=("Helvetica", 16))
        self.winner_label.grid(row=10, column=0, columnspan=5)
        self.neutron_moved = False
        self.game_over = False
        self.current_piece = None
        self.buttons = []
        self.create_buttons()
        self.create_directions_list()
        self.display_board()
        self.current_button = None
        self.current_player = self.players[0]
        self.root.mainloop()
        

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
        if self.game_over:
            return
        if self.turn == 0 and button["text"] == "O":
            self.current_piece = (button.grid_info()["row"], button.grid_info()["column"])
            self.move_button.config(state='normal')
        elif self.players[self.turn].strategy == "Human" and button["text"] == self.players[self.turn].color:
            self.current_piece = (button.grid_info()["row"], button.grid_info()["column"])
            self.move_button.config(state='normal')
        else:
            self.current_piece = None
            self.move_button.config(state='disabled')






    def on_move_clicked(self):
        if not self.current_piece:
            return
        direction = self.direction_var.get()
        current_i, current_j = self.current_piece
        if self.is_valid_move(current_i, current_j, direction):
            self.move_piece(current_i, current_j, direction)
            self.switch_players()
            self.display_board()
            self.current_piece = None
            if self.check_game_over():
                self.game_over = True
                self.winner_label.config(text=f"{self.players[self.turn].name} wins!")
                self.move_button.config(state='disabled')
            if self.current_player.strategy == "Computer":
                    self.computer_move()
        






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
        # elif piece != self.players[self.turn]:
        #     print("You cannot move your opponent's pieces.")
        #     return False

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
        self.player_label.config(text=self.players[self.turn].name)

    def show_winner(self, winner):
        """Show the winner message"""
        if winner == 'T':
            message = "It's a Tie!"
        else:
            message = f"{winner} player wins!"
        self.winner_label.config(text=message)

    def computer_move(self):
        # get valid moves for computer's piece
        valid_piece_moves = self.players[1].get_valid_moves(self.board, self.is_valid_move)
        if valid_piece_moves:
            move = random.choice(valid_piece_moves)
            self.move_piece(*move)
        # get valid moves for computer's neutron
        valid_neutron_moves = self.players[1].get_valid_neutron_moves(self.board, self.is_valid_move)
        if valid_neutron_moves:
            move = random.choice(valid_neutron_moves)
            self.move_piece(*move)
            self.switch_players()



    def get_legal_moves(self):
        legal_moves = []
        for i in range(5):
            for j in range(5):
                if self.board[i][j] == self.players[self.turn].color:
                    for direction in self.directions.values():
                        if self.is_valid_move(i, j, direction):
                            legal_moves.append((i, j))
        return legal_moves

    def is_valid_move(self, current_i: int, current_j: int, direction: str):
        """Check if a move is valid"""
        if direction not in self.directions:
            return False
        row, col = current_i + self.directions[direction][0], current_j + self.directions[direction][1]
        if row < 0 or row > 4 or col < 0 or col > 4:
            return False
        if self.board[row][col] != " ":
            return False
        return True

    def check_game_over(self):
        """Check if the game is over"""
        if self.neutron_moved:
            self.game_over = all(['N' not in row for row in self.board])
            if self.game_over:
                self.winner_label.config(text="Player " + self.current_player.name + " wins!")
        else:
            self.game_over = all(['P' not in row for row in self.board])
            if self.game_over:
                self.winner_label.config(text="Player " + self.players[(self.turn + 1) % 2].name + " wins!")

    def switch_players(self):
        """Switch the current player to the next player in the players list"""
        current_index = self.players.index(self.current_player)
        next_index = (current_index + 1) % len(self.players)
        self.current_player = self.players[next_index]