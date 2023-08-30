#Stanislaw Dutkiewicz 329076
import tkinter as tk
import tkinter.simpledialog as simpledialog
from player import Players
import tkinter.messagebox as messagebox
from tkinter import DISABLED

from neutron_board import NeutronBoard


class NeutronBoardGUI(NeutronBoard):
    """
    Class representing a graphical user interface (GUI)
    version of the NeutronBoard game.
    The GUI allows players to interact with the game board
    using a Tkinter interface. # noqa: E731
    """

    def __init__(self):
        """
        Initializes the NeutronBoardGUI class, creating the Tkinter
        root window and setting up the game board and player objects.
        """
        super().__init__()

        self.root = tk.Tk()
        self.root.config(bg='gray')
        self.root.title("Neutron Board Game")
        self.root.geometry("350x400")
        self.root.resizable(False, False)
        autograph_label = tk.Label(self.root, text="Created by Stanislaw Dutkiewicz", bg='gray', fg='white', font=("Helvetica", 10))
        autograph_label.grid(row=11, column=0, columnspan=5, pady=10)
        
        self.setup_menu()

        self.computer_strategy = self.get_computer_strategy()
        self.players = [Players("Human", "N", "Human"), Players(
            "Computer", "P", self.computer_strategy)]
        self.winner_label = tk.Label(
            self.root, text='', font=("Helvetica", 12))
        self.winner_label.grid(row=10, column=0, columnspan=5)
        self.buttons = []
        self.create_buttons()
        self.create_directions_list()
        self.display_board()
        self.winner_label.config(
            text="Welcome! Please start by moving your piece")
        self.root.mainloop()

    def get_computer_strategy(self):
        """
        Prompts the user to enter a strategy for the
        computer player (either 'random' or 'smart')
         Return:
            strategy (str) : the entered strategy or the error box
            if the user typed wrongly
        """
        while True:
            strategy = simpledialog.askstring(
                "Computer Strategy", "Enter the strategy for the computer player (random/smart):")  # noqa: E501
            if strategy == "random" or strategy == "smart":
                return strategy
            else:
                messagebox.showerror(
                    "Error", "Invalid input. Please enter either 'random' or 'smart'.")  # noqa: E501

    def create_directions_list(self):
        """
        Creates the list of directions for the player
        to select from when moving a piece
        """
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
            self.root.grid_columnconfigure(i, weight=1)
            self.root.grid_rowconfigure(i, weight=1, minsize=40)  # Setting a minimum size for the row
            for j in range(5):
                button = tk.Button(self.root, width=5, height=2)  # Using text units for width and height
                button.grid(row=i, column=j, padx=0, pady=0, sticky='nsew')  # Ensuring the button stretches to fill the cell
                button.config(bd=3, relief='solid', bg='black')
                button.config(
                    command=lambda button=button: self.on_button_clicked(button))
                if (i+j) % 2 == 0:
                    button.config(bg='white')
                else:
                    button.config(bg='green')
                # Change font and font color of button text
                button.config(font=("Helvetica", 12), fg='black')
                self.buttons.append(button)

        # Add exit button
        exit_button = tk.Button(self.root, text='Exit',
                                command=self.on_exit_clicked)
        exit_button.grid(row=5, column=5, padx=2, pady=2)
        exit_button.place(x=350, y=280)


    def on_button_clicked(self, button):
        """
        Event handler for when a game board button is clicked.
        """

        # allows user only to click neutron
        # and it has to move neutron
        if self.neutron_moved is True:
            if button["text"] == "O":
                self.current_piece = (
                    button.grid_info()["row"], button.grid_info()["column"])
                self.move_button.config(state='normal')
            else:
                self.current_piece = None
                self.move_button.config(state='disabled')
        else:
            if button["text"] == "N":
                self.current_piece = (
                    button.grid_info()["row"], button.grid_info()["column"])
                self.move_button.config(state='normal')
            else:
                self.current_piece = None
                self.move_button.config(state='disabled')

    def on_move_clicked(self):
        """
        Event handler for when the 'Move' button is clicked.
        """

        # The special loop where the human
        # starts the game with just moving his piece
        if self.first_move is None:
            if self.human_move() is True:
                self.switch_neutron_moved()
            else:
                self.winner_label.config(text="Invalid move, try again")
                return False

            self.computer_move()
            self.first_move = True
            self.winner_label.config(text="Please pick neutron and move")
        else:

            # Moving neutron and then piece
            if self.human_move() is True:
                self.switch_neutron_moved()
            else:
                self.winner_label.config(text="Invalid move, try again")
                return False

            # Ensuring that human will move piece and neutron at his turn
            self.move_count += 1

            if self.move_count == 2:
                self.move_count = 0
                self.computer_move()

        if self.neutron_moved is False:
            self.winner_label.config(text="Please pick oyur piece and move")
        else:
            self.winner_label.config(text="Please pick neutron and move")

        self.display_board()

    def display_board(self):
        """Display the current state of the game board on the GUI"""
        for i in range(5):
            for j in range(5):
                button = self.buttons[i * 5 + j]
                button["text"] = self.board[i][j]
                button.config(width=5, height=2, bd=3, relief='solid')





    def game_over(self, piece):
        """
        Displays game over message and
        winner on the GUI

        Args:
            winner (str): The winner of the game. 'N' for player1,
            'P' for player2, 'T' for tie
        """
        if piece == "N":
            self.display_board()
            self.winner_label.config(
                text="Player " + self.players[0].name + " wins!")
        else:
            self.display_board()
            self.winner_label.config(
                text="Player " + self.players[1].name + " wins!")

        # Disable the move button
        self.move_button.config(state=DISABLED)

        # Disable all buttons on the board
        for button in self.buttons:
            button.config(state=DISABLED)

        play_again = messagebox.askyesno(
            "Game Over", "Do you want to play again?")
        if play_again:
            self.root.destroy()
            NeutronBoardGUI()
        else:
            self.root.destroy()

    def on_exit_clicked(self):
        """
        Handle the event when the Exit button is clicked
        """
        if messagebox.askyesno("Exit", "Are you sure you want to exit the game?"):  # noqa: E501
            self.root.destroy()

    def setup_menu(self):
        """
        Set up the main menu for the game window.
        """
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        # Create "Help" submenu
        help_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Credits", command=self.show_credits)



    def show_credits(self):
        """
        Display a popup window with the game credits.
        """
        credits_window = tk.Toplevel(self.root)
        credits_window.title("Credits")
        tk.Label(credits_window, text="Neutron Board Game", font=("Helvetica", 16)).pack(pady=10)
        tk.Label(credits_window, text="Created by Stanislaw Dutkiewicz - 329076", font=("Helvetica", 12)).pack(pady=10)
        tk.Button(credits_window, text="Close", command=credits_window.destroy).pack(pady=10)

