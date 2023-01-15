import pygame


class NeutronBoard:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((500, 500))
        pygame.display.set_caption("Neutron Game")
        self.color_dict = {
            ' ': (255, 255, 255),
            'P': (255, 0, 0),
            'N': (0, 0, 255),
            'O': (0, 255, 0)
        }
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
        self.current_player = 'P'

    def display_board(self):
        self.screen.fill((0, 0, 0))
        for i in range(5):
            for j in range(5):
                pygame.draw.rect(self.screen, self.color_dict[self.board[i][j]], (i*100, j*100, 100, 100))
        pygame.display.flip()
        
    def find_neutron(self):
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
    def __init__(self, color, board):
        self.color = color
        self.board = board
        
    def make_move(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    row, col = x // 100, y // 100
                    if self.board.board[row][col] == self.color:
                        return (row, col)
            self.board.display_board()
            pygame.display.update()


class Game:
    def __init__(self):
        self.board = NeutronBoard()
        self.players = [Player('N', self.board), Player('P', self.board)]
        self.current_player = 0

    def play(self):
        self.board.display_board()
        while not self.board.check_winner():
            row, col = self.players[self.current_player].make_move()
            direction = input(f'Player {self.players[self.current_player].color} make your move')
            if not self.board.move_piece(row, col, direction, self.players[self.current_player].color):
                continue
            self.board.display_board()
            winner = self.board.check_winner()
            if winner:
                print(f'Player {winner} wins!')
                break
            self.current_player = (self.current_player + 1) % 2


if __name__ == '__main__':
    game = Game()
    game.play()
    pygame.quit()


