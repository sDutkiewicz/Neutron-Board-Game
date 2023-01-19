import tkinter as tk
import random
import tkinter.simpledialog as simpledialog
from kinterplayer import Players
import tkinter.messagebox as messagebox
from tkinter import DISABLED

class NeutronBoard:
    def __init__(self):
        self.board =[
                    ['P', 'P', 'P', 'P', 'P'],
                    [' ', ' ', ' ', ' ', ' '],
                    [' ', ' ', 'O', ' ', ' '],
                    [' ', ' ', ' ', ' ', ' '],
                    ['N', 'N', 'N', 'N', 'N']]
        self.computer_strategy = self.get_computer_strategy()
        self.players = [Players("Player1", "N", "Human"), Players("Computer", "P", self.computer_strategy)]
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
    
    def get_computer_strategy(self):
        while True:
            strategy = simpledialog.askstring("Computer Strategy", "Enter the strategy for the computer player (random/smart):")
            if strategy == "random" or strategy == "smart":
                return strategy
            else:
                messagebox.showerror("Error", "Invalid input. Please enter either 'random' or 'smart'.")
    def create_buttons(self):
        for i in range(5):
            for j in range(5):
                button = tk.Button(self.root, text='', width=5, height=2)
                button.config(command=lambda button=button: self.on_button_clicked(button))
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



    def find_neutron(self):
        for i, row in enumerate(self.board):
            for j, piece in enumerate(row):
                if piece == 'O':
                    return i, j

    def move_piece(self, row, col, direction):
        row_offset, col_offset = self.directions[direction]

        piece = self.board[row][col]

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

    def human_move(self):
        if not self.current_piece:
            self.winner_label.config(text="Choose a piece to move")
            return
        direction = self.direction_var.get()
        current_i, current_j = self.current_piece
        self.move_piece(current_i, current_j, direction)
        self.display_board()
        self.switch_neutron_moved()
        self.current_piece = None
        if self.check_winner() is not None:
            if self.check_winner() == 'T':
                self.check_winner() == str(self.players[0].color)
                self.game_over(self.players[0].color)
            self.game_over(self.players[0].color)

    
    def game_over(self, piece):
        """Check if the game is over"""
        if piece == "N":
            self.display_board()
            self.winner_label.config(text="Player " + self.players[0].name + " wins!")
        else:
            self.display_board()
            self.winner_label.config(text="Player " + self.players[1].name + " wins!")

        # Disable the move button
        self.move_button.config(state=DISABLED)

        # Unbind the <Button-1> event from the board
        self.board_canvas.unbind("<Button-1>")




    def computter_move(self):
        piece_move = self.players[1].get_computer_move(self.board)
        if piece_move:
            self.move_piece(*piece_move)
        neutron_move = self.players[1].get_computer_move_neutron(self.board)
        if neutron_move:
            self.move_piece(*neutron_move)

    def switch_neutron_moved(self):
        self.neutron_moved = not self.neutron_moved
