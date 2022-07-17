"""Board tests."""
import pytest
from pytest import fixture

from strategy.board import Board, EmptyPieceRange, PieceRange
from strategy.colour import Colour
from strategy.exceptions import InvalidCoordinateError, InvalidDestinationError, InvalidDimensionsError, NoPieceError
from strategy.pieces import BOMB, CAPTAIN, EMPTY, FLAG, LAKE, MINER, SCOUT, Empty, Lake, Piece


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
    with pytest.raises(InvalidDestinationError):
        board[0, 0] = Piece(MINER, 3, Colour.RED, x=0, y=0)
        board.move((0, 0), (9, 9))
    # regular move
    board[6, 7] = Piece(SCOUT, 2, Colour.RED, x=6, y=7)
    board.move((6, 7), (5, 7))
    # scout attacks bomb and loses
    bomb = Piece(BOMB, 11, Colour.BLUE, x=6, y=7)
    board[3, 7] = bomb
    board.move((5, 7), (3, 7))
    assert board[3, 7] == bomb
    assert board[5, 7] == Empty(EMPTY, x=5, y=7)
    # miner attacks bomb and wins
    miner = Piece(MINER, 3, Colour.RED, x=2, y=7)
    board[2, 7] = miner
    board.move((2, 7), (3, 7))
    assert board[3, 7] == miner
    # miner attacks miner and both disappear
    other_miner = Piece(MINER, 3, Colour.BLUE, x=4, y=7)
    board[4, 7] = other_miner
    board.move((3, 7), (4, 7))
    assert board[3, 7] == Empty(EMPTY, x=3, y=7)
    assert board[4, 7] == Empty(EMPTY, x=4, y=7)
    # get the moves
    expected = [
        (Colour.RED, (6, 7), (5, 7)),
        (Colour.RED, (5, 7), (3, 7)),
        (Colour.RED, (2, 7), (3, 7)),
        (Colour.RED, (3, 7), (4, 7)),
    ]
    assert board.moves == expected


def test_board_repr(board):
    assert f"{board!r}".startswith("<Board (")
    assert f"{board!r}".endswith(">")
    assert "lake" in f"{board!r}"


def test_board_flag_by_colour(board):
    flag = Piece(FLAG, 0, Colour.RED, x=0, y=0)
    board[0, 0] = flag
    assert board._flag_by_colour(Colour.RED) is True
    assert board._flag_by_colour(Colour.BLUE) is False


def test_board_winner_no_winner(board):
    red_flag = Piece(FLAG, 0, Colour.RED, x=0, y=0)
    red_movable_piece = Piece(SCOUT, 2, Colour.RED, x=1, y=0)
    blue_flag = Piece(FLAG, 0, Colour.BLUE, x=9, y=9)
    blue_movable_piece = Piece(SCOUT, 2, Colour.BLUE, x=8, y=9)
    board[0, 0] = red_flag
    board[1, 0] = red_movable_piece
    board[9, 9] = blue_flag
    board[8, 9] = blue_movable_piece
    assert board.winner is None


def test_board_winner_red_wins(board):
    red_flag = Piece(FLAG, 0, Colour.RED, x=0, y=0)
    red_movable_piece = Piece(SCOUT, 2, Colour.RED, x=1, y=0)
    board[0, 0] = red_flag
    board[1, 0] = red_movable_piece
    assert board.winner is Colour.RED


def test_board_winner_blue_wins(board):
    blue_flag = Piece(FLAG, 0, Colour.BLUE, x=0, y=0)
    blue_movable_piece = Piece(SCOUT, 2, Colour.BLUE, x=1, y=0)
    board[0, 0] = blue_flag
    board[1, 0] = blue_movable_piece
    assert board.winner is Colour.BLUE


def test_board_format(board):
    red_piece = Piece(MINER, 3, Colour.RED, x=0, y=0)
    assert board._format(red_piece, x=0, y=0) == "[red]   miner    [/red] | "
    blue_piece = Piece(MINER, 3, Colour.BLUE, x=0, y=0)
    assert board._format(blue_piece, x=0, y=0) == "[blue]   miner    [/blue] | "
    lake = Lake(LAKE, x=0, y=0)
    assert board._format(lake, x=0, y=0) == "[green]    lake    [/green] | "
    empty = Empty(EMPTY, x=0, y=0)
    assert board._format(empty, x=0, y=0) == "[bright_black]   empty    [/bright_black] | "


def test_board_has_movable(board):
    captain = Piece(CAPTAIN, 6, Colour.RED, x=0, y=0)
    board[0, 0] = captain
    assert board._has_movable(Colour.RED) is True
    assert board._has_movable(Colour.BLUE) is False


def test_board_piece_range_can_move():
    assert EmptyPieceRange.can_move is False
    miner = Piece(MINER, 6, Colour.RED, x=0, y=0)
    piece_range = PieceRange(miner, (1, None), (1, None), (0, None), (0, None))
    assert piece_range.can_move is True


def test_board_piece_range_can_attack():
    assert EmptyPieceRange.can_attack is False
    miner = Piece(MINER, 3, Colour.RED, x=0, y=0)
    bomb = Piece(BOMB, 11, Colour.BLUE, x=1, y=0)
    piece_range = PieceRange(miner, (1, bomb), (1, None), (0, None), (0, None))
    assert piece_range.can_attack is True


def test_board_piece_range_attackables():
    assert EmptyPieceRange.attackables == {}
    miner = Piece(MINER, 3, Colour.RED, x=0, y=0)
    bomb = Piece(BOMB, 11, Colour.BLUE, x=1, y=0)
    piece_range = PieceRange(miner, (1, bomb), (1, None), (0, None), (0, None))
    assert piece_range.attackables == {"north": bomb}
    piece_range = PieceRange(miner, (1, bomb), (1, bomb), (1, bomb), (1, bomb))
    assert piece_range.attackables == {"north": bomb, "east": bomb, "south": bomb, "west": bomb}
