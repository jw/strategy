"""Board tests."""
import pytest
from pytest import fixture

from strategy.board import Board
from strategy.colour import Colour
from strategy.exceptions import InvalidCoordinateError, InvalidDimensionsError, NoPieceError
from strategy.game import EMPTY, LAKE, Empty, Lake
from strategy.pieces import SCOUT, Piece


@fixture
def board():
    return Board()


def test_board(board):
    assert len(board) == 10 * 10
    assert board[1, 2] == Empty(EMPTY, x=1, y=2)
    assert board[4, 2] == Empty(EMPTY, x=4, y=2)
    assert board[2, 4] == Lake(LAKE, x=2, y=4)
    assert board[7, 4] == Lake(LAKE, x=7, y=4)


def test_board_str(board):
    assert "lake" in str(board)
    assert "empty" in str(board)


def test_board_top_bottom(board):
    assert all([isinstance(cell, Empty) for cell in board.top()])
    assert all([isinstance(cell, Empty) for cell in board.bottom()])


def test_board_create_random_board(board):
    board.create_random_pieces(Colour.RED)
    assert all([isinstance(cell, Empty) for cell in board.top()])
    assert all([isinstance(cell, Piece) for cell in board.bottom()])
    board.create_random_pieces(Colour.BLUE)
    assert all([isinstance(cell, Piece) for cell in board.top()])
    assert all([isinstance(cell, Piece) for cell in board.bottom()])


def test_board_exception(board):
    with pytest.raises(InvalidDimensionsError):
        board[-1, 9] = Empty
    with pytest.raises(InvalidDimensionsError):
        board[1, 10] = Empty
    board[1, 9] = Empty


def test_board_red_blue(board):
    assert len(board.red()) == 0
    assert len(board.blue()) == 0
    board.create_random_pieces(Colour.RED)
    assert len(board.red()) == 40
    assert len(board.blue()) == 0
    board.create_random_pieces(Colour.BLUE)
    assert len(board.red()) == 40
    assert len(board.blue()) == 40


def test_board_get(board):
    with pytest.raises(InvalidCoordinateError):
        assert board[-1, 0]
    with pytest.raises(InvalidCoordinateError):
        assert board[0, -1]
    with pytest.raises(InvalidCoordinateError):
        assert board[11, 5]
    assert board[2, 4] == Lake(LAKE, x=2, y=4)  # left lake
    assert board[6, 5] == Lake(LAKE, x=6, y=5)  # right lake
    assert board.get((20, -1), "outside") == "outside"
    assert board.get((0, 0), "empty cell") == Empty(EMPTY, x=0, y=0)
    assert board.get((3, 4), Lake) == Lake(LAKE, x=3, y=4)


def test_board_str_to_int(board):
    assert board._str_to_int("a") == 0
    assert board._str_to_int("A") == 0
    assert board._str_to_int("j") == 9
    with pytest.raises(InvalidCoordinateError):
        board._str_to_int("z")
    with pytest.raises(InvalidCoordinateError):
        board._str_to_int(None)
    with pytest.raises(InvalidCoordinateError):
        board._str_to_int("")
    with pytest.raises(InvalidCoordinateError):
        board._str_to_int("ab")


def test_board_coordinate_to_tuple(board):
    assert board._coordinate_to_tuple("a1") == (0, 9)
    assert board._coordinate_to_tuple("a10") == (0, 0)
    assert board._coordinate_to_tuple("b2") == (1, 8)
    assert board._coordinate_to_tuple("h6") == (7, 4)
    assert board._coordinate_to_tuple("j1") == (9, 9)
    with pytest.raises(InvalidCoordinateError):
        board._coordinate_to_tuple("z2")
    with pytest.raises(InvalidCoordinateError):
        board._coordinate_to_tuple("a20")
    with pytest.raises(InvalidCoordinateError):
        board._coordinate_to_tuple("a-2")
    with pytest.raises(InvalidCoordinateError):
        board._coordinate_to_tuple(None)
    with pytest.raises(InvalidCoordinateError):
        board._coordinate_to_tuple("")
    with pytest.raises(InvalidCoordinateError):
        board._coordinate_to_tuple("ab")


def test_board_get_coordinates(board):
    assert board._get_coordinates((0, 0)) == (0, 0)
    assert board._get_coordinates((0, 1)) == (0, 1)
    assert board._get_coordinates((9, 9)) == (9, 9)
    with pytest.raises(InvalidCoordinateError):
        board._get_coordinates((-1, 1))
    with pytest.raises(InvalidCoordinateError):
        board._get_coordinates((-1, "some string"))

    assert board._get_coordinates(("a", 1)) == (0, 9)
    assert board._get_coordinates(("f", 6)) == (5, 4)
    assert board._get_coordinates(("j", 10)) == (9, 0)
    with pytest.raises(InvalidCoordinateError):
        board._get_coordinates(("abc", 10))
    with pytest.raises(InvalidCoordinateError):
        board._get_coordinates(("a", 11))
    with pytest.raises(InvalidCoordinateError):
        board._get_coordinates(("a", -1))
    with pytest.raises(InvalidCoordinateError):
        board._get_coordinates((None, 5))
    with pytest.raises(InvalidCoordinateError):
        board._get_coordinates(("a", None))

    assert board._get_coordinates("a1") == (0, 9)
    assert board._get_coordinates("a10") == (0, 0)
    assert board._get_coordinates("j10") == (9, 0)
    assert board._get_coordinates("f6") == (5, 4)
    assert board._get_coordinates("F6") == (5, 4)
    with pytest.raises(InvalidCoordinateError):
        board._get_coordinates("z4")
    with pytest.raises(InvalidCoordinateError):
        board._get_coordinates("z-4")
    with pytest.raises(InvalidCoordinateError):
        board._get_coordinates("aaa4")


def test_board_move(board):
    with pytest.raises(NoPieceError):
        board.move((0, 0), (0, 1))
    board[6, 7] = Piece(SCOUT, Colour.RED, x=6, y=7)
    board.move((6, 7), (5, 7))
