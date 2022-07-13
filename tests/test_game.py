import pytest
from _pytest.fixtures import fixture

from strategy.board import Board
from strategy.colour import Colour
from strategy.exceptions import InvalidDimensionsError, NoPieceError
from strategy.main import EmptyRangePiece, RangePiece, available_range
from strategy.pieces import BOMB, CAPTAIN, FLAG, MINER, SCOUT, SPY, Piece


@fixture
def board():
    return Board()


def test_board_available_range_no_piece(board):
    with pytest.raises(NoPieceError):
        available_range(board, x=7, y=2)


def test_board_available_range_flag_and_bomb(board):
    board[7, 2] = Piece(FLAG, 0, Colour.RED)
    assert available_range(board, x=7, y=2) == EmptyRangePiece
    board[7, 2] = Piece(BOMB, 11, Colour.RED)
    assert available_range(board, x=7, y=2) == EmptyRangePiece


def test_board_available_range_all_empty(board):
    data = {
        "north": (1, None),
        "east": (1, None),
        "south": (1, None),
        "west": (1, None),
    }
    required = RangePiece(**data)
    board[7, 2] = Piece(CAPTAIN, 0, Colour.RED)
    assert available_range(board, x=7, y=2) == required


def test_board_available_range_empty_lake_north(board):
    data = {
        "north": (0, None),
        "east": (1, None),
        "south": (1, None),
        "west": (1, None),
    }
    required = RangePiece(**data)
    board[3, 6] = Piece(CAPTAIN, 0, Colour.RED)
    assert available_range(board, x=3, y=6) == required


def test_board_available_range_empty_left_bottom_corner(board):
    data = {
        "north": (1, None),
        "east": (1, None),
        "south": (0, None),
        "west": (0, None),
    }
    required = RangePiece(**data)
    board[0, 9] = Piece(CAPTAIN, 0, Colour.RED)
    assert available_range(board, x=0, y=9) == required


def test_board_available_range_corners_with_opposition(board):
    # left bottom
    data = {
        "north": (0, Piece(MINER, 3, Colour.BLUE, x=0, y=8)),
        "east": (0, Piece(MINER, 3, Colour.BLUE, x=1, y=9)),
        "south": (0, None),
        "west": (0, None),
    }
    required = RangePiece(**data)
    board[0, 8] = Piece(MINER, 3, Colour.BLUE, x=0, y=8)
    board[1, 9] = Piece(MINER, 3, Colour.BLUE, x=1, y=9)
    board[0, 9] = Piece(CAPTAIN, 0, Colour.RED)
    assert available_range(board, x=0, y=9) == required

    # right bottom
    data = {
        "north": (0, Piece(MINER, 3, Colour.BLUE, x=9, y=8)),
        "east": (0, None),
        "south": (0, None),
        "west": (0, Piece(MINER, 3, Colour.BLUE, x=8, y=9)),
    }
    required = RangePiece(**data)
    board[9, 8] = Piece(MINER, 3, Colour.BLUE, x=9, y=8)
    board[8, 9] = Piece(MINER, 3, Colour.BLUE, x=8, y=9)
    board[9, 9] = Piece(CAPTAIN, 0, Colour.RED)
    assert available_range(board, x=9, y=9) == required

    # left top
    data = {
        "north": (0, None),
        "east": (0, Piece(MINER, 3, Colour.BLUE, x=1, y=0)),
        "south": (0, Piece(MINER, 3, Colour.BLUE, x=0, y=1)),
        "west": (0, None),
    }
    required = RangePiece(**data)
    board[1, 0] = Piece(MINER, 3, Colour.BLUE, x=1, y=0)
    board[0, 1] = Piece(MINER, 3, Colour.BLUE, x=0, y=1)
    board[0, 0] = Piece(CAPTAIN, 0, Colour.RED)
    assert available_range(board, x=0, y=0) == required

    # right top
    data = {
        "north": (0, None),
        "east": (0, None),
        "south": (0, Piece(MINER, 3, Colour.BLUE, x=9, y=1)),
        "west": (0, Piece(MINER, 3, Colour.BLUE, x=8, y=0)),
    }
    required = RangePiece(**data)
    board[8, 0] = Piece(MINER, 3, Colour.BLUE, x=8, y=0)
    board[9, 1] = Piece(MINER, 3, Colour.BLUE, x=9, y=1)
    board[9, 0] = Piece(CAPTAIN, 0, Colour.RED)
    assert available_range(board, x=9, y=0) == required


def test_board_available_range_empty_left_bottom_corner_north_east_same_team(board):
    # left bottom
    data = {
        "north": (0, None),
        "east": (0, None),
        "south": (0, None),
        "west": (0, None),
    }
    required = RangePiece(**data)
    board[0, 8] = Piece(MINER, 3, Colour.RED, x=0, y=8)
    board[1, 9] = Piece(MINER, 3, Colour.RED, x=1, y=9)
    board[0, 9] = Piece(CAPTAIN, 0, Colour.RED)
    assert available_range(board, x=0, y=9) == required

    # right bottom
    data = {
        "north": (0, None),
        "east": (0, None),
        "south": (0, None),
        "west": (0, None),
    }
    required = RangePiece(**data)
    board[9, 8] = Piece(MINER, 3, Colour.RED, x=9, y=8)
    board[8, 9] = Piece(MINER, 3, Colour.RED, x=8, y=9)
    board[9, 9] = Piece(CAPTAIN, 0, Colour.RED)
    assert available_range(board, x=9, y=9) == required

    # left top
    data = {
        "north": (0, None),
        "east": (0, None),
        "south": (0, None),
        "west": (0, None),
    }
    required = RangePiece(**data)
    board[1, 0] = Piece(MINER, 3, Colour.RED, x=1, y=0)
    board[0, 1] = Piece(MINER, 3, Colour.RED, x=0, y=1)
    board[0, 0] = Piece(CAPTAIN, 0, Colour.RED)
    assert available_range(board, x=0, y=0) == required

    # right top
    data = {
        "north": (0, None),
        "east": (0, None),
        "south": (0, None),
        "west": (0, None),
    }
    required = RangePiece(**data)
    board[8, 0] = Piece(MINER, 3, Colour.RED, x=8, y=0)
    board[9, 1] = Piece(MINER, 3, Colour.RED, x=9, y=1)
    board[9, 0] = Piece(CAPTAIN, 0, Colour.RED)
    assert available_range(board, x=9, y=0) == required


def test_board_available_range_complete_block(board):
    data = {
        "north": (0, None),
        "east": (0, None),
        "south": (0, None),
        "west": (0, None),
    }
    required = RangePiece(**data)
    board[1, 4] = Piece(SPY, 1, Colour.RED, x=1, y=4)
    board[0, 4] = Piece(MINER, 1, Colour.RED, x=0, y=4)
    board[1, 3] = Piece(MINER, 1, Colour.RED, x=1, y=3)
    board[1, 5] = Piece(MINER, 1, Colour.RED, x=1, y=5)
    assert available_range(board, x=1, y=4) == required


def test_board_available_range_raises(board):
    with pytest.raises(InvalidDimensionsError):
        available_range(board, x=-3, y=8)


def test_board_available_range_scout(board):
    board[4, 4] = Piece(SCOUT, 2, Colour.RED)
    data = {
        "north": (4, None),
        "east": (1, None),
        "south": (5, None),
        "west": (0, None),
    }
    assert available_range(board, x=4, y=4) == RangePiece(**data)
    board[4, 9] = Piece(SCOUT, 2, Colour.RED)
    data = {
        "north": (4, None),
        "east": (1, None),
        "south": (4, None),
        "west": (0, None),
    }
    assert available_range(board, x=4, y=4) == RangePiece(**data)
    data = {
        "north": (4, None),
        "east": (5, None),
        "south": (0, None),
        "west": (4, None),
    }
    assert available_range(board, x=4, y=9) == RangePiece(**data)
    board[0, 9] = Piece(SCOUT, 2, Colour.RED, x=0, y=9)
    data = {
        "north": (9, None),
        "east": (3, None),
        "south": (0, None),
        "west": (0, None),
    }
    assert available_range(board, x=0, y=9) == RangePiece(**data)
    board[9, 0] = Piece(SCOUT, 2, Colour.RED, x=9, y=0)
    data = {
        "north": (0, None),
        "east": (0, None),
        "south": (9, None),
        "west": (9, None),
    }
    assert available_range(board, x=9, y=0) == RangePiece(**data)


def test_board_available_range_scout_oppostion_and_same_team(board):
    board[0, 0] = Piece(MINER, 2, Colour.BLUE, x=0, y=0)  # opposite
    board[0, 4] = Piece(SCOUT, 2, Colour.RED, x=0, y=4)  # central piece
    data = {
        "north": (3, Piece(MINER, 2, Colour.BLUE, x=0, y=0)),
        "east": (1, None),
        "south": (5, None),
        "west": (0, None),
    }
    assert available_range(board, x=0, y=4) == RangePiece(**data)

    board[1, 4] = Piece(MINER, 2, Colour.RED, x=1, y=4)  # opposite
    data = {
        "north": (3, Piece(MINER, 2, Colour.BLUE, x=0, y=0)),
        "east": (0, None),
        "south": (5, None),
        "west": (0, None),
    }
    assert available_range(board, x=0, y=4) == RangePiece(**data)

    board[0, 5] = Piece(MINER, 2, Colour.RED, x=0, y=5)  # same team
    data = {
        "north": (3, Piece(MINER, 2, Colour.BLUE, x=0, y=0)),
        "east": (0, None),
        "south": (0, None),
        "west": (0, None),
    }
    assert available_range(board, x=0, y=4) == RangePiece(**data)


def test_board_available_range_scout_opposition_at_four_sides(board):
    board[4, 6] = Piece(SCOUT, 2, Colour.RED, x=4, y=6)  # central piece
    board[4, 0] = Piece(MINER, 2, Colour.BLUE, x=4, y=0)  # north
    board[9, 6] = Piece(MINER, 2, Colour.BLUE, x=9, y=6)  # east
    board[4, 9] = Piece(MINER, 2, Colour.BLUE, x=4, y=9)  # south
    board[0, 6] = Piece(MINER, 2, Colour.BLUE, x=0, y=6)  # west

    data = {
        "north": (5, Piece(MINER, 2, Colour.BLUE, x=4, y=0)),
        "east": (4, Piece(MINER, 2, Colour.BLUE, x=9, y=6)),
        "south": (2, Piece(MINER, 2, Colour.BLUE, x=4, y=9)),
        "west": (3, Piece(MINER, 2, Colour.BLUE, x=0, y=6)),
    }
    assert available_range(board, x=4, y=6) == RangePiece(**data)


def test_board_available_range_opposition_north(board):
    board[4, 4] = Piece(MINER, 2, Colour.RED, x=4, y=6)  # central piece
    board[4, 3] = Piece(MINER, 2, Colour.BLUE, x=4, y=3)  # opposition
    data = {
        "north": (0, Piece(MINER, 2, Colour.BLUE, x=4, y=3)),
        "east": (1, None),
        "south": (1, None),
        "west": (0, None),
    }
    assert available_range(board, x=4, y=4) == RangePiece(**data)
