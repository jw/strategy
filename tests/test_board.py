"""Board tests."""
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
    assert "lake" in str(board)
    assert "empty" in str(board)


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


def test_board_exception():
    board = Board()
    with pytest.raises(InvalidDimensionsError):
        board[-1, 9] = Empty
    with pytest.raises(InvalidDimensionsError):
        board[1, 10] = Empty
    board[1, 9] = Empty


def test_board_red_blue():
    board = Board()
    assert len(board.red()) == 0
    assert len(board.blue()) == 0
    board.create_random_pieces(Player.RED)
    assert len(board.red()) == 40
    assert len(board.blue()) == 0
    board.create_random_pieces(Player.BLUE)
    assert len(board.red()) == 40
    assert len(board.blue()) == 40


def test_board_get():
    board = Board()
    with pytest.raises(InvalidDimensionsError):
        assert board[-1, 0]
    with pytest.raises(InvalidDimensionsError):
        assert board[0, -1]
    with pytest.raises(InvalidDimensionsError):
        assert board[11, 5]
    assert board.get((20, -1), "outside") == "outside"
    assert board.get((0, 0), "empty cell") == Empty
    assert board.get((3, 4), "lake") == Lake
