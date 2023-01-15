from nngui import NeutronGameGUI
from justneutron import NeutronBoard


class Game:
    def __init__(self):
        self.board = NeutronBoard()
        self.gui = NeutronGameGUI(self.board)
        self.human_turn = True

    def start(self):
        self.gui.start()
        self.game_loop()

    def game_loop(self):
        while not self.is_game_over():
            current_player = self.board.human_player if self.human_turn else self.board.computer_player  # noqa: E501
            current_player.make_move(self.board)
            self.human_turn = not self.human_turn
            self.update_gui()

    def is_game_over(self):
        i, j = self.board.find_neutron()
        return i == 0

    def update_gui(self):
        self.gui.update_board_display()
        self.gui.update_moves_list()
