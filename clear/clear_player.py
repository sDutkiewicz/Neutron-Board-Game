import random


class Player:
    def __init__(self, name, color, is_computer=False):
        self.name = name
        self.color = color
        self.is_computer = is_computer

    def make_move(self, game):
        if self.is_computer:
            self.make_computer_move(game)
        else:
            self.make_human_move(game)

    def make_computer_move(self, game):
        # Generate a random move for the computer player
        i, j = game.find_neutron()
        possible_directions = [d for d in game.directions.keys() if game.move_piece(i, j, d, 'O')]  # noqa: E501
        if possible_directions:
            direction = random.choice(possible_directions)
            game.move_piece(i, j, direction, 'O')
            print(f"Computer moved neutron to {direction}")

    def make_human_move(self, game):
        # Get the move from the human player
        i, j = game.find_neutron()
        possible_directions = [d for d in game.directions.keys() if game.move_piece(i, j, d, 'O')]  # noqa: E501
        if possible_directions:
            direction = input("Please enter your move direction (up, down, left, right, up-right, up-left, down-right, down-left): ")  # noqa: E501
            if game.move_piece(i, j, direction, 'O'):
                print(f"You moved neutron to {direction}")
            else:
                print("Invalid move, please try again")

    def make_move_with_neutron(self, game):
        if self.is_computer:
            self.make_computer_move_with_neutron(game)
        else:
            self.make_human_move_with_neutron(game)

    def make_computer_move_with_neutron(self, game):
        i, j = game.find_neutron()
        possible_directions = [d for d in game.directions.keys() if game.move_piece(i, j, d, 'O')]  # noqa: E501
        if possible_directions:
            direction = random.choice(possible_directions)
            game.move_piece(i, j, direction, 'O')
            print(f"Computer moved neutron to {direction}")
            self.make_computer_move(game)

    def make_human_move_with_neutron(self, game):
        i, j = game.find_neutron()
        possible_directions = [d for d in game.directions.keys() if game.move_piece(i, j, d, 'O')]  # noqa: E501
        if possible_directions:
            direction = input("Please enter your move direction for neutron (up, down, left, right, up-right, up-left, down-right, down-left): ")  # noqa: E501
            if game.move_piece(i, j, direction, 'O'):
                print(f"You moved neutron to {direction}")
                self.make_human_move(game)
            else:
                print("Invalid move, please try again")
