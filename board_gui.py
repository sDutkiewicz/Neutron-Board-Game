import tkinter as tk
import tkinter.simpledialog as simpledialog
from player import Players
import tkinter.messagebox as messagebox
from tkinter import DISABLED
from PIL import Image, ImageTk
import sys
import os

from neutron_board import NeutronBoard

class NeutronBoardGUI(NeutronBoard):
    """
    Class representing a graphical user interface (GUI)
    version of the NeutronBoard game.
    The GUI allows players to interact with the game board
    using a Tkinter interface.
    """

    def __init__(self):
        """
        Initializes the NeutronBoardGUI class, creating the Tkinter
        root window and setting up the game board and player objects.
        """
        super().__init__()
        self.root = tk.Tk()

        self.root.withdraw()  # Hide the main window until strategy is selected

        self.computer_strategy = self.get_computer_strategy()
        
        self.root.deiconify()  # Show the main window after strategy selection

        
        self.root.title("Neutron Board Game")
        self.root.geometry("350x400")
        self.root.resizable(False, False)
        autograph_label = tk.Label(self.root, text="Created by Stanislaw Dutkiewicz", bg='gray', fg='white', font=("Helvetica", 10))
        autograph_label.grid(row=11, column=0, columnspan=5, pady=10)

        # Adding background image
        background_path = os.path.join(os.path.dirname(__file__), "gallery", "background.jpg")
        if os.path.exists(background_path):
            self.background_image = Image.open(background_path)
            self.background_image = self.zoom_out(self.background_image, 0.5)  # Zoom out to 50% of the original size
            self.background_photo = ImageTk.PhotoImage(self.background_image)
            self.background_label = tk.Label(self.root, image=self.background_photo)
            self.background_label.place(relx=0.5, rely=0.5, anchor='center')
        else:
            print(f"Background image file not found: {background_path}")
    
        self.setup_menu()

        
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


    def zoom_out(self, img, scale_factor):
        """
        Zooms out the image by resizing it to a smaller dimension
        based on the provided scale factor.
        """
        width, height = img.size
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        return img.resize((new_width, new_height), Image.ANTIALIAS)

    def get_computer_strategy(self):
        """
        Prompts the user to enter a strategy for the
        computer player (either 'random' or 'smart') using buttons.
        If the user cancels or closes the window, the program will exit.
        Return:
            strategy (str) : the entered strategy
        """
        self.strategy_window = tk.Toplevel(self.root)
        self.strategy_window.title("Computer Strategy")
        self.strategy_window.geometry("300x100")
        self.strategy_window.resizable(False, False)
        
        label = tk.Label(self.strategy_window, text="Choose the strategy for the computer player:", font=("Helvetica", 10))
        label.pack(pady=10)

        def set_strategy(strategy):
            self.computer_strategy = strategy
            self.strategy_window.destroy()

        def on_cancel():
            self.root.destroy()

        random_button = tk.Button(self.strategy_window, text="Random", command=lambda: set_strategy("random"))
        random_button.pack(side=tk.LEFT, padx=20, pady=10)

        smart_button = tk.Button(self.strategy_window, text="Smart", command=lambda: set_strategy("smart"))
        smart_button.pack(side=tk.RIGHT, padx=20, pady=10)

        self.strategy_window.protocol("WM_DELETE_WINDOW", on_cancel)  # Handle window close button

        self.root.wait_window(self.strategy_window)  # Wait for the strategy window to be closed

        if not hasattr(self, 'computer_strategy'):
            on_cancel()  # If the window was closed without setting a strategy, exit the application

        return self.computer_strategy


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
        button_width = 5  # Fixed width for buttons
        button_height = 2  # Fixed height for buttons
        for i in range(5):
            self.root.grid_columnconfigure(i, weight=1)
            self.root.grid_rowconfigure(i, weight=1)
            for j in range(5):
                button = tk.Button(self.root, width=button_width, height=button_height)
                button.grid(row=i, column=j, padx=0, pady=0, sticky='nsew')  # No padding
                button.config(bd=3, relief='solid', bg='black')
                button.config(
                    command=lambda button=button: self.on_button_clicked(button))
                if (i + j) % 2 == 0:
                    button.config(bg='white')
                else:
                    button.config(bg='green')
                # Change font and font color of button text
                button.config(font=("Helvetica", 12), fg='black')
                self.buttons.append(button)

        # Add exit button
        exit_button = tk.Button(self.root, text='Exit',
                                command=self.on_exit_clicked)
        exit_button.place(x=290, y=350)  # Fixed position for the exit button


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

        # Add "License" option
        help_menu.add_command(label="License", command=self.show_license)

    def show_credits(self):
        """
        Display a popup window with the game credits.
        """
        credits_window = tk.Toplevel(self.root)
        credits_window.title("Credits")
        tk.Label(credits_window, text="Neutron Board Game", font=("Helvetica", 16)).pack(pady=10)
        tk.Label(credits_window, text="Created by Stanislaw Dutkiewicz - 329076", font=("Helvetica", 12)).pack(pady=10)
        tk.Button(credits_window, text="Close", command=credits_window.destroy).pack(pady=10)

    def get_license_path(self):
        if getattr(sys, 'frozen', False):
            # If the application is run as a bundle/exe
            return os.path.join(sys._MEIPASS, 'LICENSE')
        else:
            # If the application is run from a script
            return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'LICENSE')

    def show_license(self):
        """
        Display a window with the full license text.
        """
        license_window = tk.Toplevel(self.root)
        license_window.title("License")
        
        # Assuming the license text is stored in a file named LICENSE.txt
        with open(self.get_license_path(), "r") as file:
            license_text = file.read()

        
        # Display the license text in a scrollable Text widget
        text_widget = tk.Text(license_window, wrap=tk.WORD, height=20, width=50)
        text_widget.insert(tk.END, license_text)
        text_widget.pack(padx=10, pady=10)
        
        # Add a close button
        tk.Button(license_window, text="Close", command=license_window.destroy).pack(pady=10)


