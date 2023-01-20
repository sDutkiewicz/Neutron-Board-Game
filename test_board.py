from nn_normal import NeutronBoard
import pytest

def test_init():
    board = NeutronBoard()
    assert board.board == [['P', 'P', 'P', 'P', 'P'],
                           [' ', ' ', ' ', ' ', ' '],
                           [' ', ' ', 'O', ' ', ' '],
                           [' ', ' ', ' ', ' ', ' '],
                           ['N', 'N', 'N', 'N', 'N']]
    assert board.directions == {'up': (-1, 0), 'down': (1, 0), 'left': (0, -1), 'right': (0, 1), 'up-right': (-1, 1), 'up-left': (-1, -1), 'down-right': (1, 1), 'down-left': (1, -1)}
    assert board.neutron_moved == False
    assert board.current_piece == None
    assert board.move_count == 0
    assert board.first_move == None

def test_find_neutron():
    board = NeutronBoard()
    assert board.find_neutron() == (2, 2)
    board.board[2][2] = ' '
    assert board.find_neutron() == None

def test_move_piece_up():
    board = NeutronBoard()
    initial_pos = (2, 2)
    direction = 'up'
    assert board.move_piece(*initial_pos, direction) == True
    expected_board = [['P', 'P', 'P', 'P', 'P'],
                      [' ', ' ', 'O', ' ', ' '],
                      [' ', ' ', ' ', ' ', ' '],
                      [' ', ' ', ' ', ' ', ' '],
                      ['N', 'N', 'N', 'N', 'N']]
    assert board.board == expected_board

def test_move_piece_down():
    board = NeutronBoard()
    initial_pos = (2, 2)
    direction = 'down'
    assert board.move_piece(*initial_pos, direction) == True
    expected_board = [['P', 'P', 'P', 'P', 'P'],
                      [' ', ' ', ' ', ' ', ' '],
                      [' ', ' ', ' ', ' ', ' '],
                      [' ', ' ', 'O', ' ', ' '],
                      ['N', 'N', 'N', 'N', 'N']]
    assert board.board == expected_board

def test_move_piece_left():
    board = NeutronBoard()
    initial_pos = (2, 2)
    direction = 'left'
    assert board.move_piece(*initial_pos, direction) == True
    expected_board = [['P', 'P', 'P', 'P', 'P'],
                      [' ', ' ', ' ', ' ', ' '],
                      ['O', ' ', ' ', ' ', ' '],
                      [' ', ' ', ' ', ' ', ' '],
                      ['N', 'N', 'N', 'N', 'N']]
    assert board.board == expected_board

def test_move_piece_right():
    board = NeutronBoard()
    board.board = [   ['P', 'P', 'P', 'P', 'P'],
                      [' ', ' ', ' ', ' ', ' '],
                      ['O', ' ', ' ', ' ', ' '],
                      [' ', ' ', ' ', ' ', ' '],
                      ['N', 'N', 'N', 'N', 'N']]
    initial_pos = (2, 0)
    direction = 'right'
    assert board.move_piece(*initial_pos, direction) == True
    expected_board = [['P', 'P', 'P', 'P', 'P'],
                      [' ', ' ', ' ', ' ', ' '],
                      [' ', ' ', ' ', ' ', 'O'],
                      [' ', ' ', ' ', ' ', ' '],
                      ['N', 'N', 'N', 'N', 'N']]
    assert board.board == expected_board

def test_move_piece_up_right():
    board = NeutronBoard()
    board.board = [   ['P', 'P', 'P', 'P', 'P'],
                      [' ', ' ', ' ', ' ', ' '],
                      ['O', ' ', ' ', ' ', ' '],
                      ['N', ' ', ' ', ' ', ' '],
                      [' ', 'N', 'N', 'N', 'N']]
    initial_pos = (3, 0)
    direction = 'up-right'
    assert board.move_piece(*initial_pos, direction) == True
    expected_board = [['P', 'P', 'P', 'P', 'P'],
                      [' ', ' ', 'N', ' ', ' '],
                      ['O', ' ', ' ', ' ', ' '],
                      [' ', ' ', ' ', ' ', ' '],
                      [' ', 'N', 'N', 'N', 'N']]
    assert board.board == expected_board

def test_move_piece_up_left():
    board = NeutronBoard()
    board.board = [   ['P', 'P', 'P', 'P', 'P'],
                      [' ', ' ', ' ', ' ', ' '],
                      [' ', ' ', 'O', ' ', ' '],
                      [' ', ' ', 'N', ' ', ' '],
                      [' ', 'N', 'N', 'N', 'N']]
    initial_pos = (3, 2)
    direction = 'up-left'
    assert board.move_piece(*initial_pos, direction) == True
    expected_board = [['P', 'P', 'P', 'P', 'P'],
                      ['N', ' ', ' ', ' ', ' '],
                      [' ', ' ', 'O', ' ', ' '],
                      [' ', ' ', ' ', ' ', ' '],
                      [' ', 'N', 'N', 'N', 'N']]
    assert board.board == expected_board


def test_move_piece_down_left():
    board = NeutronBoard()
    board.board = [   ['P', 'P', 'P', 'P', 'P'],
                      [' ', ' ', ' ', ' ', ' '],
                      ['O', ' ', ' ', ' ', ' '],
                      [' ', ' ', 'N', ' ', ' '],
                      [' ', 'N', 'N', 'N', 'N']]
    initial_pos = (0, 3)
    direction = 'down-left'
    assert board.move_piece(*initial_pos, direction) == True
    expected_board = [  ['P', 'P', 'P', ' ', 'P'],
                        [' ', ' ', ' ', ' ', ' '],
                        ['O', ' ', ' ', ' ', ' '],
                        ['P', ' ', 'N', ' ', ' '],
                        [' ', 'N', 'N', 'N', 'N']]
    assert board.board == expected_board

def test_move_piece_down_right():
    board = NeutronBoard()
    board.board = [   ['P', 'P', 'P', 'P', 'P'],
                      [' ', ' ', ' ', ' ', ' '],
                      [' ', ' ', ' ', ' ', ' '],
                      [' ', ' ', 'O', ' ', ' '],
                      ['N', 'N', 'N', 'N', 'N']]
    initial_pos = (0, 2)
    direction = 'down-right'
    assert board.move_piece(*initial_pos, direction) == True
    expected_board = [  ['P', 'P', ' ', 'P', 'P'],
                        [' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', 'P'],
                        [' ', ' ', 'O', ' ', ' '],
                        ['N', 'N', 'N', 'N', 'N']]
    assert board.board == expected_board

def test_move_piece_invalid():
    board = NeutronBoard()
    board.board = [   ['P', 'P', 'P', 'P', 'P'],
                      [' ', ' ', ' ', ' ', ' '],
                      [' ', ' ', ' ', ' ', ' '],
                      [' ', ' ', 'O', ' ', ' '],
                      ['N', 'N', 'N', 'N', 'N']]
    assert board.move_piece(3, 2, 'down') == False
    
def test_check_winner():
    board = NeutronBoard()
    board.board = [['P', 'P', 'P', 'P', 'P'],
                   [' ', ' ', ' ', ' ', ' '],
                   [' ', ' ', ' ', ' ', ' '],
                   [' ', ' ', ' ', ' ', ' '],
                   ['N', 'N', 'O', 'N', 'N']]
    assert board.check_winner() == 'N'
    board.board = [['P', 'P', 'O', 'P', 'P'],
                   [' ', ' ', ' ', ' ', ' '],
                   [' ', ' ', ' ', ' ', ' '],
                   [' ', ' ', ' ', ' ', ' '],
                   [' ', ' ', ' ', ' ', ' ']]
    assert board.check_winner() == 'P'

def test_check_winner_blocked():
    board = NeutronBoard()
    board.board = [['P', ' ', ' ', ' ', 'P'],
                   [' ', ' ', ' ', ' ', ' '],
                   [' ', ' ', 'P', ' ', ' '],
                   [' ', 'P', 'O', 'P', ' '],
                   ['N', 'N', 'P', 'N', 'N']]
    assert board.check_winner() == 'T'


def test_is_valid_move():
    board = NeutronBoard()
    board.board ==        [['P', 'P', 'P', 'P', 'P'],
                           [' ', ' ', ' ', ' ', ' '],
                           [' ', ' ', 'O', ' ', ' '],
                           [' ', ' ', ' ', ' ', ' '],
                           ['N', 'N', 'N', 'N', 'N']]
    board.current_piece = (2, 2)
    assert board.is_valid_move(2, 2, 'up') == True
    assert board.is_valid_move(0, 4, 'left') == False 