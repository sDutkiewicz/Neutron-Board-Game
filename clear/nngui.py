import tkinter as tk


class NeutronGameGUI:
    def __init__(self, game):
        self.game = game
        self.root = tk.Tk()
        self.root.title("Neutron Game")
        self.possible_directions = []
        self.selected_piece = None
        
    def start(self):
        self.create_widgets()
        self.root.mainloop()
        
    def create_widgets(self):
        self.moves_list = tk.Listbox(self.root)
        self.moves_list.grid(row=0, column=0, rowspan=5, padx=5, pady=5)
        
        self.board = tk.Canvas(self.root, width=300, height=300)
        self.board.grid(row=0, column=1, padx=5, pady=5)
        self.board.bind("<Button-1>", self.on_canvas_click)
        
        self.directions_list = tk.Listbox(self.root)
        self.directions_list.grid(row=0, column=2, rowspan=5, padx=5)
        
        self.move_button = tk.Button(self.root, text="Move", command=self.move_piece)
        self.move_button.grid(row=5, column=2, pady=5)
        self.move_button.config(state='disable')

        self.exit_button = tk.Button(self.root, text="Exit", command=self.root.destroy)
        self.exit_button.grid(row=5, column=3, pady=5)


    def on_canvas_click(self, event):
        x, y = event.x, event.y
        row, col = int(y // 60), int(x // 60)
        if self.game.board[row][col] in ["N", "P"]:
            self.possible_directions = [d for d in self.game.directions.keys() if self.game.move_piece(row, col, d, self.game.board[row][col])]  # noqa: E501
            self.selected_piece = (row, col)
            self.directions_list.delete(0, tk.END)
            for direction in self.possible_directions:
                self.directions_list.insert(tk.END, direction)


    def move_neutron(self):
        current_player = self.game.human_player if self.game.human_turn else self.game.computer_player  # noqa: E501
        current_player.make_move(self.game)

    def move_piece(self):
        if not self.selected_piece:
            print("Please select a piece to move first.")
            return
        direction = self.directions_list.get(
            self.directions_list.curselection())
        if direction is None:
            print("Please select a direction to move the piece.")
            return
        i, j = self.selected_piece
        current_player = self.game.human_player if self.game.human_turn else self.game.computer_player
        if not self.game.move_piece(i, j, direction, current_player.color):
            print("Invalid move, please try again.")
            return
        current_player.make_move_with_neutron(self.game)
        self.draw_board()
        self.update_directions_list()



    def draw_board(self):
        self.board.delete("all")
        for row in range(len(self.game.board)):
            for col in range(len(self.game.board[row])):
                x1, y1 = col*60, row*60
                x2, y2 = x1+60, y1+60
                color = "white"
                if self.game.board[row][col] == "P":
                    color = "red"
                elif self.game.board[row][col] == "N":
                    color = "blue"
                self.board.create_rectangle(x1, y1, x2, y2, fill=color)

    def find_neutron(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 'O':
                    return i, j

