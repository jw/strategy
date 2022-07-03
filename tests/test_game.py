import pytest
from _pytest.fixtures import fixture

from strategy.board import Board
from strategy.exceptions import InvalidDimensionsError
from strategy.main import Range, get_available_range
from strategy.pieces import BOMB, FLAG, MINER, SCOUT, SPY, Piece
from strategy.player import Player


@fixture
def board():
    return Board()


def test_board_get_available_range_open_block(board):
    board[5, 2] = Piece(SPY, 1, Player.RED)
    assert get_available_range(board, x=5, y=2) == Range(1, 1, 1, 1)


def test_board_get_available_range_west_block(board):
    board[0, 6] = Piece(SPY, 1, Player.RED)
    assert get_available_range(board, x=0, y=6) == Range(1, 1, 1, 0)


def test_board_get_available_range_east_block(board):
    board[9, 6] = Piece(SPY, 1, Player.RED)
    assert get_available_range(board, x=9, y=6) == Range(1, 0, 1, 1)


def test_board_get_available_range_south_block(board):
    board[4, 9] = Piece(SPY, 1, Player.RED)
    assert get_available_range(board, x=4, y=9) == Range(1, 1, 0, 1)


def test_board_get_available_range_north_block(board):
    board[4, 0] = Piece(SPY, 1, Player.RED)
    assert get_available_range(board, x=4, y=0) == Range(0, 1, 1, 1)
    board[3, 6] = Piece(MINER, 1, Player.RED)
    assert get_available_range(board, x=3, y=6) == Range(0, 1, 1, 1)


def test_board_get_available_range_north_south_block(board):
    board[3, 6] = Piece(SPY, 1, Player.RED)
    board[3, 7] = Piece(MINER, 1, Player.RED)
    assert get_available_range(board, x=3, y=6) == Range(0, 1, 0, 1)


def test_board_get_available_range_east_west_block(board):
    board[1, 4] = Piece(SPY, 1, Player.RED)
    board[0, 4] = Piece(MINER, 1, Player.RED)
    assert get_available_range(board, x=1, y=4) == Range(1, 0, 1, 0)


def test_board_get_available_range_complete_block(board):
    board[1, 4] = Piece(SPY, 1, Player.RED)
    board[0, 4] = Piece(MINER, 1, Player.RED)  # west
    board[1, 3] = Piece(MINER, 1, Player.RED)  # north
    board[1, 5] = Piece(MINER, 1, Player.RED)  # south
    assert get_available_range(board, x=1, y=4) == Range(0, 0, 0, 0)


def test_board_get_available_range_complete_corners(board):
    board[9, 9] = Piece(SPY, 1, Player.RED)
    assert get_available_range(board, x=9, y=9) == Range(1, 0, 0, 1)
    board[0, 0] = Piece(SPY, 1, Player.RED)
    assert get_available_range(board, x=0, y=0) == Range(0, 1, 1, 0)
    board[9, 0] = Piece(SPY, 1, Player.RED)
    assert get_available_range(board, x=9, y=0) == Range(0, 0, 1, 1)
    board[0, 9] = Piece(SPY, 1, Player.RED)
    assert get_available_range(board, x=0, y=9) == Range(1, 1, 0, 0)


def test_board_get_available_range_bomb_flag(board):
    board[3, 8] = Piece(BOMB, 11, Player.RED)
    assert get_available_range(board, x=3, y=8) == Range(0, 0, 0, 0)
    board[9, 9] = Piece(FLAG, 1, Player.RED)
    assert get_available_range(board, x=9, y=9) == Range(0, 0, 0, 0)


def test_board_get_available_range_raises(board):
    with pytest.raises(InvalidDimensionsError):
        get_available_range(board, x=-3, y=8)


def test_board_get_available_range_scout(board):
    board[4, 4] = Piece(SCOUT, 2, Player.RED)
    assert get_available_range(board, x=4, y=4) == Range(4, 1, 5, 0)
    board[4, 9] = Piece(SCOUT, 2, Player.RED)
    assert get_available_range(board, x=4, y=4) == Range(4, 1, 4, 0)
    assert get_available_range(board, x=4, y=9) == Range(4, 5, 0, 4)
    board[0, 9] = Piece(SCOUT, 2, Player.RED)
    assert get_available_range(board, x=0, y=9) == Range(9, 3, 0, 0)
    board[9, 0] = Piece(SCOUT, 2, Player.RED)
    assert get_available_range(board, x=9, y=0) == Range(0, 0, 9, 9)
