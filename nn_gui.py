import tkinter as tk
import random
import tkinter.simpledialog as simpledialog
from kinterplayer import Players
import tkinter.messagebox as messagebox
from tkinter import DISABLED

from nn_normal import NeutronBoard

class NeutronBoardGUI(NeutronBoard):
    def __init__(self):
        super().__init__()
        self.root = tk.Tk()
        self.root.config(bg='#ffc180')
        self.root.title("Neutron Board Game")
        self.winner_label = tk.Label(self.root, text='', font=("Helvetica", 16))
        self.winner_label.grid(row=10, column=0, columnspan=5)
        self.root.mainloop()
    

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

    
if __name__ == "__main__":
    board = NeutronBoardGUI()