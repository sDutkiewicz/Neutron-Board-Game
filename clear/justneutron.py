from nngui import NeutronGameGUI
from clear_player import Player


class NeutronBoard:
    def __init__(self):
        # Initialize the board
        self.board = [['P', 'P', 'P', 'P', 'P'],
                      [' ', ' ', ' ', ' ', ' '],
                      [' ', ' ', 'O', ' ', ' '],
                      [' ', ' ', ' ', ' ', ' '],
                      ['N', 'N', 'N', 'N', 'N']]

        self.human_player = Player("Human", "N", is_computer=False)
        self.computer_player = Player("Computer", "P", is_computer=True)
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

    def display_board(self):
        # Display the board
        for row in self.board:
            print(" ".join(row))

    def on_canvas_click(self, event):
        x, y = event.x, event.y
        row, col = int(y // 60), int(x // 60)
        selected_piece = self.game.get_piece(row, col)
        if selected_piece == self.game.human_player.color:
            self.selected_piece = (row, col)
            print(f"Selected piece: {self.selected_piece}")
        self.possible_directions = [d for d in self.game.directions.keys() if self.game.move_piece(row, col, d, 'O')]
        print(f"Possible directions: {self.possible_directions}")



    def find_neutron(self):
        # Find the position of the neutron
        for i, row in enumerate(self.board):
            for j, piece in enumerate(row):
                if piece == 'O':
                    return i, j

    def move_piece(self, row, col, direction, color):

        try:
            row_offset, col_offset = self.directions[direction]
        except KeyError:
            print("You entered the wrong direction, please try again!")
            return False

        if self.board[row][col] != color:
            if color == 'O':
                print("Wrong Piece Error: You can't move neutron in this turn")
                return False
            print("Wrong Piece Error. You can't move other pieces")
            return False

        new_row = row + row_offset
        new_col = col + col_offset
        if new_row < 0 or new_row > 4 or new_col < 0 or new_col > 4:
            if color == 'N':
                print("Direction Error: You can't move to the wall that is next to you")  # noqa: E501
                return False
            return False
        if self.board[new_row][new_col] != ' ':
            if color == 'N':
                print("Direction Error: You can't move to the piece that is next to you")  # noqa: E501
                return False
            return False
        while new_row >= 0 and new_row <= 4 and new_col >= 0 and new_col <= 4 and self.board[new_row][new_col] == ' ':  # noqa: E501
            self.board[row][col] = ' '
            self.board[new_row][new_col] = color
            row = new_row
            col = new_col
            new_row += row_offset
            new_col += col_offset
        return True

    def check_winner(self):
        i, j = self.find_neutron()
        if i == 0:
            return 'N'
        elif i == 4:
            return 'P'
        elif (self.board[i-1][j] != ' ' and self.board[i+1][j] != ' ' and
              self.board[i][j-1] != ' ' and self.board[i][j+1] != ' '):
            if (self.board[i-1][j] != 'N' and self.board[i+1][j] != 'N' and
                    self.board[i][j-1] != 'N' and self.board[i][j+1] != 'N'):
                return 'P'
            else:
                return 'N'
        return None


if __name__ == "__main__":
    game = NeutronBoard()
    gui = NeutronGameGUI(game)
    gui.start()
