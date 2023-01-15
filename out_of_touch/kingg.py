from kinbb import NeutronBoardd, Player
import tkinter as tk

class Game:
    def __init__(self):
        self.root = tk.Tk()
        self.board = NeutronBoardd()
        self.players = self.board.players
        self.turn = self.board.turn
        self.current_player = self.players[self.turn]
        self.game_over = False
        self.create_buttons()
        self.create_directions_list()
        self.board.display_board()
        self.root.mainloop()

    def create_buttons(self):
        self.buttons = self.board.buttons
        for button in self.buttons:
            button.config(
                command=lambda button=button: self.on_button_clicked(button))

    def create_directions_list(self):
        self.direction_var = tk.StringVar(self.root)
        self.direction_var.set(list(self.board.directions.keys())[0])
        self.direction_list = tk.OptionMenu(
            self.root, self.direction_var, *list(self.board.directions.keys()))
        self.direction_list.grid(row=5, column=0, columnspan=5)
        self.move_button = tk.Button(
            self.root, text='Move', command=self.on_move_clicked)
        self.move_button.grid(row=6, column=0, columnspan=5)

    def on_button_clicked(self, button):
        """Handle button click event"""
        self.board.current_piece = (int(button.grid_info()["row"]), int(
            button.grid_info()["column"]))

    def display_board(self):
        self.board.display_board()
    


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

    def start_game(self):
        self.create_buttons()
        self.create_directions_list()
        self.display_board()
        self.root.mainloop()

game = Game()
game.start_game()
