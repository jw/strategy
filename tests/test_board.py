"""First test."""
import pytest

from strategy.board import Board
from strategy.exceptions import InvalidDimensionsError
from strategy.game import Empty, Lake
from strategy.player import Player


def test_board():
    board = Board()
    assert len(board) == 10 * 10
    assert board[1, 2] == Empty
    assert board[2, 4] == Lake
    assert board[4, 2] == Empty


def test_board_str():
    board = Board()
    assert "[4|2: <lake>]" in str(board)
    assert "[6|6: <empty>]" in str(board)


def test_board_top_bottom():
    board = Board()
    assert all([cell == Empty for cell in board.top()])
    assert all([cell == Empty for cell in board.bottom()])


def test_board_create_random_board():
    board = Board()
    board.create_random_pieces(Player.RED)
    assert all([cell == Empty for cell in board.top()])
    assert all([cell != Empty for cell in board.bottom()])
    board.create_random_pieces(Player.BLUE)
    assert all([cell != Empty for cell in board.top()])
    assert all([cell != Empty for cell in board.bottom()])


def test_exception():
    board = Board()
    with pytest.raises(InvalidDimensionsError):
        board[-1, 9] = Empty
    with pytest.raises(InvalidDimensionsError):
        board[1, 10] = Empty
    board[1, 9] = Empty
