import PySimpleGUI as sg

class NeutronBoard:
    def __init__(self):
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
        self.color_dict = {'P':'blue', 'N':'red', 'O':'white', ' ':'gray'}
        self.layout = self.create_board_layout()
        self.window = sg.Window('Neutron Board').Layout(self.layout)
        self.update_board_colors()
        self.game_over = False
        while not self.game_over:
            event, values = self.window.Read()
            if event in self.directions:
                if self.move_piece(self.find_neutron()[0], self.find_neutron()[1], event, 'O'):
                    self.update_board_colors()
                    winner = self.check_winner()
                    if winner:
                        sg.Popup('Player {} wins!'.format(winner))
                        self.game_over = True
            elif event in [(i, j) for i in range(5) for j in range(5)]:
                if self.move_piece(event[0], event[1], values[event], self.board[event[0]][event[1]]):
                    self.update_board_colors()
        
    def create_board_layout(self):
        layout = [[sg.Text('  ')] + [sg.Text(i) for i in range(5)]]
        for i, row in enumerate(self.board):
            layout.append([sg.Text(str(i))] + [sg.Button(row[j], key=(i, j)) for j in range(5)])
        for direction in self.directions:
            layout.append([sg.Button(direction, key=direction)])
        return layout

    def update_board_colors(self):
        for i in range(5):
            for j in range(5):
                button = self.window.FindElement((i, j))
                button.Update(button_color=(self.color_dict[self.board[i][j]]))

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
                print("Direction Error: You can't move to the wall that is next to you")
                return False
            return False
        if self.board[new_row][new_col] != ' ':
            if color == 'N':
                print("Direction Error: You can't move to the piece that is next to you")
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
            return 'P' if self.board[i-1][j] == 'N' or self.board[i+1][j] == 'N' or self.board[i][j-1] == 'N' or self.board[i][j+1] == 'N' else 'N'


        

    def move_neutron(self, direction, color):
        try:
            row_offset, col_offset = self.directions[direction]
        except KeyError:
            print("You entered the wrong direction, please try again!")
            return False
        row, col = self.find_neutron()
        new_row = row + row_offset
        new_col = col + col_offset
        if new_row < 0 or new_row > 4 or new_col < 0 or new_col > 4:
            if color == 'N':
                print("Direction Error: You can't move to the wall that is next to you")
                return False

            return False
        if self.board[new_row][new_col] != ' ':
            if color == 'N':
                print("Direction Error: You can't move to the piece that is next to you")
                return False
            return False

        while new_row >= 0 and new_row <= 4 and new_col >= 0 and new_col <= 4 and self.board[new_row][new_col] == ' ':  # noqa: E501
            self.board[row][col] = ' '
            self.board[new_row][new_col] = 'O'
            row = new_row
            col = new_col
            new_row += row_offset
            new_col += col_offset
        return True



class Player:
    def __init__(self, color):
        self.color = color

    def make_move(self, board, direction):
        neutron_pos = board.find_neutron()
        if not board.move_piece(neutron_pos[0], neutron_pos[1], direction, 'O'):
            return False
        return True


class Game:
    def __init__(self):
        self.board = NeutronBoard()
        self.players = [Player('N'), Player('P')]
        self.current_player = 0

    def play(self):
        self.board.update_board_colors()
        while not self.board.check_winner():
            direction = sg.PopupGetText('Player {} make your move'.format(self.players[self.current_player].color))
            if not self.players[self.current_player].make_move(self.board, direction):
                continue
            self.board.update_board_colors()
            winner = self.board.check_winner()
            if winner:
                sg.Popup('Player {} wins!'.format(winner))
                break
            self.current_player = (self.current_player + 1) % 2


if __name__ == '__main__':
    game = Game()
    game.play()
