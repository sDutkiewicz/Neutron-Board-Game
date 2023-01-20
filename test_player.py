#Stanislaw Dutkiewicz 329076
from player import Players
import random


def test_get_computer_move(monkeypatch):
    monkeypatch.setattr(random, 'choice', lambda x: 'down')
    player = Players("player", "P", "random")
    board = [['P', ' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' ', ' '],
             [' ', ' ', 'O', ' ', ' '],
             [' ', ' ', ' ', ' ', ' '],
             ['N', 'N', 'N', 'N', 'N']]
    assert player.get_computer_move(board) == 'down'


def test_get_computer_move_neutron(monkeypatch):
    monkeypatch.setattr(random, 'choice', lambda x: 'down')
    player = Players("player", "P", "random")
    board = [['P', 'P', 'O', 'P', ' '],
             [' ', 'P', ' ', 'P', ' '],
             [' ', ' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' ', ' '],
             ['N', 'N', 'N', 'N', 'N']]
    assert player.get_computer_move_neutron(board) == 'down'


def test_get_valid_moves():
    player = Players("player", "P", "random")
    board = [['P', ' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' ', ' '],
             [' ', ' ', 'O', ' ', ' '],
             [' ', ' ', ' ', ' ', ' '],
             ['N', 'N', 'N', 'N', 'N']]
    assert player.get_valid_moves(board, player.is_valid_move) == [
        (0, 0, 'down'), (0, 0, 'right'), (0, 0, 'down-right')]


def test_is_valid_move():
    player = Players("player", "P", "random")
    board = [['P', ' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' ', ' '],
             [' ', ' ', 'O', ' ', ' '],
             [' ', ' ', ' ', ' ', ' '],
             ['N', 'N', 'N', 'N', 'N']]
    assert player.is_valid_move(board, 0, 0, 'down') is True
    assert player.is_valid_move(board, 0, 0, 'up') is False
    assert player.is_valid_move(board, 2, 2, 'left') is True


def test_smart_move_piece():
    player = Players("player", "P", "smart")
    board = [['P', ' ', ' ', ' ', ' '],
             [' ', ' ', 'P', ' ', 'P'],
             [' ', ' ', ' ', ' ', ' '],
             ['O', ' ', ' ', 'P', ' '],
             ['N', 'N', 'N', 'N', 'N']]
    assert player.smart_move_piece(
        board, 2, 2, player.get_valid_moves) == (1, 2, 'up')


def test_find_neutron():
    player = Players("player", "P", "smart")
    board = [['P', ' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' ', ' '],
             [' ', ' ', 'O', ' ', ' '],
             [' ', ' ', ' ', ' ', ' '],
             ['N', 'N', 'N', 'N', 'N']]
    assert player.find_neutron(board) == (2, 2)
    board = [[' ', ' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' ', ' '],
             ['N', 'N', 'N', 'N', 'N']]
    assert player.find_neutron(board) is None


def test_smart_move_neutron():
    player = Players("player", "P", "smart")
    board = [['P', ' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' ', ' '],
             [' ', ' ', 'O', ' ', ' '],
             [' ', ' ', ' ', ' ', ' '],
             ['N', 'N', 'N', 'N', 'N']]
    assert player.smart_move_neutron(board, 2, 2) == (2, 2, 'down')
