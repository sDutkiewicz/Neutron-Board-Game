import tkinter as tk
import tkinter.simpledialog as simpledialog
from kinterplayer import Players
import tkinter.messagebox as messagebox
from tkinter import DISABLED

from nn_normal import NeutronBoard

class NeutronBoardGUI(NeutronBoard):
    def __init__(self):
        super().__init__()
        self.root = tk.Tk()
        self.root.config(bg='gray')
        self.root.title("Neutron Board Game")
        self.computer_strategy = self.get_computer_strategy()
        self.players = [Players("Player1", "N", "Human"), Players("Computer", "P", self.computer_strategy)]
        self.winner_label = tk.Label(self.root, text='', font=("Helvetica", 16))
        self.winner_label.grid(row=10, column=0, columnspan=5)
        self.buttons = []
        self.create_buttons()
        self.create_directions_list()
        self.display_board()
        self.root.mainloop()


    
    def get_computer_strategy(self):
        while True:
            strategy = simpledialog.askstring("Computer Strategy", "Enter the strategy for the computer player (random/smart):")
            if strategy == "random" or strategy == "smart":
                return strategy
            else:
                messagebox.showerror("Error", "Invalid input. Please enter either 'random' or 'smart'.")

    def create_directions_list(self):
        self.direction_var = tk.StringVar(self.root)
        self.direction_var.set(list(self.directions.keys())[0])
        self.direction_list = tk.OptionMenu(
            self.root, self.direction_var, *list(self.directions.keys()))
        self.direction_list.grid(row=5, column=0, columnspan=5)
        self.move_button = tk.Button(
            self.root, text='Move', command=self.on_move_clicked)
        self.move_button.grid(row=6, column=0, columnspan=5)
    
    def create_buttons(self):
        for i in range(5):
            self.root.grid_columnconfigure(i, weight=1, pad=15)
            self.root.grid_rowconfigure(i, weight=1, pad=15)
            for j in range(5):
                button = tk.Button(self.root, width=5, height=2)
                button.grid(row=i, column=j, padx=2, pady=2)

                # Set button background color
                button.config(bg='gray')

                button.config(command=lambda button=button: self.on_button_clicked(button))
                
                if (i+j) % 2 == 0:
                    button.config(bg='white')
                else:
                    button.config(bg='green')
                
                # Change font and font color of button text
                button.config(font=("Helvetica", 12), fg='black')
                self.buttons.append(button)
        # Add exit button
        exit_button = tk.Button(self.root, text='Exit', command=self.root.destroy)
        exit_button.grid(row=5, column=5, padx=2, pady=2)
        exit_button.place(x=425, y=356)

    def on_button_clicked(self, button):
        if self.neutron_moved == True:
            if button["text"] == "O":
                self.current_piece = (button.grid_info()["row"], button.grid_info()["column"])
                self.move_button.config(state='normal')
            else:
                self.current_piece = None
                self.move_button.config(state='disabled')
        else:
            if button["text"] == "N":
                self.current_piece = (button.grid_info()["row"], button.grid_info()["column"])
                self.move_button.config(state='normal')
            else:
                self.current_piece = None
                self.move_button.config(state='disabled')

    def on_move_clicked(self):
        if not self.current_piece:
            return
            
        if self.first_move is None:
            self.human_move()
            self.neutron_moved == True
            self.computter_move()
            self.first_move = True
        else:
            self.human_move()
            self.display_board()
            self.move_count += 1
            if self.move_count == 2:
                self.move_count = 0
                self.computter_move()

    def display_board(self):
        for i in range(5):
            for j in range(5):
                if self.board[i][j] == 'P':
                    self.buttons[i * 5 + j]
                elif self.board[i][j] == 'N':
                    self.buttons[i * 5 + j]
                elif self.board[i][j] == 'O':
                    self.buttons[i * 5 + j]
                else:
                    self.buttons[i * 5 + j]
                self.buttons[i * 5 + j].config(text=self.board[i][j])


    
if __name__ == "__main__":
    board = NeutronBoardGUI()