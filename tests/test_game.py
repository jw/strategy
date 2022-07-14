import pytest
from _pytest.fixtures import fixture

from strategy.board import Board, EmptyRangePiece, PieceRange
from strategy.colour import Colour
from strategy.exceptions import InvalidCoordinateError, NoPieceError
from strategy.pieces import BOMB, CAPTAIN, FLAG, MINER, SCOUT, SPY, Piece


@fixture
def board():
    return Board()


def test_board_available_range_no_piece(board):
    with pytest.raises(NoPieceError):
        board.available_range(x=7, y=2)


def test_board_available_range_flag_and_bomb(board):
    board[7, 2] = Piece(FLAG, 0, Colour.RED)
    assert board.available_range(x=7, y=2) == EmptyRangePiece
    board[7, 2] = Piece(BOMB, 11, Colour.RED)
    assert board.available_range(x=7, y=2) == EmptyRangePiece


def test_board_available_range_all_empty(board):
    piece = Piece(CAPTAIN, 5, Colour.RED)
    data = {
        "piece": piece,
        "north": (1, None),
        "east": (1, None),
        "south": (1, None),
        "west": (1, None),
    }
    required = PieceRange(**data)
    board[7, 2] = Piece(CAPTAIN, 5, Colour.RED)
    assert board.available_range(x=7, y=2) == required


def test_board_available_range_empty_lake_north(board):
    piece = Piece(CAPTAIN, 5, Colour.RED)
    data = {
        "piece": piece,
        "north": (0, None),
        "east": (1, None),
        "south": (1, None),
        "west": (1, None),
    }
    required = PieceRange(**data)
    board[3, 6] = piece
    assert board.available_range(x=3, y=6) == required


def test_board_available_range_empty_left_bottom_corner(board):
    piece = Piece(CAPTAIN, 5, Colour.RED)
    data = {
        "piece": piece,
        "north": (1, None),
        "east": (1, None),
        "south": (0, None),
        "west": (0, None),
    }
    required = PieceRange(**data)
    board[0, 9] = piece
    assert board.available_range(x=0, y=9) == required


def test_board_available_range_corners_with_opposition(board):
    piece = Piece(CAPTAIN, 5, Colour.RED, x=0, y=9)
    # left bottom
    data = {
        "piece": piece,
        "north": (0, Piece(MINER, 3, Colour.BLUE, x=0, y=8)),
        "east": (0, Piece(MINER, 3, Colour.BLUE, x=1, y=9)),
        "south": (0, None),
        "west": (0, None),
    }
    required = PieceRange(**data)
    board[0, 8] = Piece(MINER, 3, Colour.BLUE, x=0, y=8)
    board[1, 9] = Piece(MINER, 3, Colour.BLUE, x=1, y=9)
    board[0, 9] = piece
    assert board.available_range(x=0, y=9) == required

    # right bottom
    piece = Piece(CAPTAIN, 5, Colour.RED, x=9, y=9)
    data = {
        "piece": piece,
        "north": (0, Piece(MINER, 3, Colour.BLUE, x=9, y=8)),
        "east": (0, None),
        "south": (0, None),
        "west": (0, Piece(MINER, 3, Colour.BLUE, x=8, y=9)),
    }
    required = PieceRange(**data)
    board[9, 8] = Piece(MINER, 3, Colour.BLUE, x=9, y=8)
    board[8, 9] = Piece(MINER, 3, Colour.BLUE, x=8, y=9)
    board[9, 9] = piece
    assert board.available_range(x=9, y=9) == required

    # left top
    piece = Piece(CAPTAIN, 5, Colour.RED, x=0, y=0)
    data = {
        "piece": piece,
        "north": (0, None),
        "east": (0, Piece(MINER, 3, Colour.BLUE, x=1, y=0)),
        "south": (0, Piece(MINER, 3, Colour.BLUE, x=0, y=1)),
        "west": (0, None),
    }
    required = PieceRange(**data)
    board[1, 0] = Piece(MINER, 3, Colour.BLUE, x=1, y=0)
    board[0, 1] = Piece(MINER, 3, Colour.BLUE, x=0, y=1)
    board[0, 0] = piece
    assert board.available_range(x=0, y=0) == required

    # right top
    piece = Piece(CAPTAIN, 5, Colour.RED, x=9, y=0)
    data = {
        "piece": piece,
        "north": (0, None),
        "east": (0, None),
        "south": (0, Piece(MINER, 3, Colour.BLUE, x=9, y=1)),
        "west": (0, Piece(MINER, 3, Colour.BLUE, x=8, y=0)),
    }
    required = PieceRange(**data)
    board[8, 0] = Piece(MINER, 3, Colour.BLUE, x=8, y=0)
    board[9, 1] = Piece(MINER, 3, Colour.BLUE, x=9, y=1)
    board[9, 0] = piece
    assert board.available_range(x=9, y=0) == required


def test_board_available_range_empty_left_bottom_corner_north_east_same_team(board):
    # left bottom
    piece = Piece(CAPTAIN, 0, Colour.RED, x=0, y=9)
    data = {
        "piece": piece,
        "north": (0, None),
        "east": (0, None),
        "south": (0, None),
        "west": (0, None),
    }
    required = PieceRange(**data)
    board[0, 8] = Piece(MINER, 3, Colour.RED, x=0, y=8)
    board[1, 9] = Piece(MINER, 3, Colour.RED, x=1, y=9)
    board[0, 9] = piece
    assert board.available_range(x=0, y=9) == required

    # right bottom
    piece = Piece(CAPTAIN, 0, Colour.RED, x=9, y=9)
    data = {
        "piece": piece,
        "north": (0, None),
        "east": (0, None),
        "south": (0, None),
        "west": (0, None),
    }
    required = PieceRange(**data)
    board[9, 8] = Piece(MINER, 3, Colour.RED, x=9, y=8)
    board[8, 9] = Piece(MINER, 3, Colour.RED, x=8, y=9)
    board[9, 9] = piece
    assert board.available_range(x=9, y=9) == required

    # left top
    piece = Piece(CAPTAIN, 0, Colour.RED, x=0, y=0)
    data = {
        "piece": piece,
        "north": (0, None),
        "east": (0, None),
        "south": (0, None),
        "west": (0, None),
    }
    required = PieceRange(**data)
    board[1, 0] = Piece(MINER, 3, Colour.RED, x=1, y=0)
    board[0, 1] = Piece(MINER, 3, Colour.RED, x=0, y=1)
    board[0, 0] = piece
    assert board.available_range(x=0, y=0) == required

    # right top
    piece = Piece(CAPTAIN, 0, Colour.RED, x=9, y=0)
    data = {
        "piece": piece,
        "north": (0, None),
        "east": (0, None),
        "south": (0, None),
        "west": (0, None),
    }
    required = PieceRange(**data)
    board[8, 0] = Piece(MINER, 3, Colour.RED, x=8, y=0)
    board[9, 1] = Piece(MINER, 3, Colour.RED, x=9, y=1)
    board[9, 0] = piece
    assert board.available_range(x=9, y=0) == required


def test_board_available_range_complete_block(board):
    piece = Piece(SPY, 1, Colour.RED, x=1, y=4)
    data = {
        "piece": piece,
        "north": (0, None),
        "east": (0, None),
        "south": (0, None),
        "west": (0, None),
    }
    required = PieceRange(**data)
    board[1, 4] = piece
    board[0, 4] = Piece(MINER, 1, Colour.RED, x=0, y=4)
    board[1, 3] = Piece(MINER, 1, Colour.RED, x=1, y=3)
    board[1, 5] = Piece(MINER, 1, Colour.RED, x=1, y=5)
    assert board.available_range(x=1, y=4) == required


def test_board_available_range_raises(board):
    with pytest.raises(InvalidCoordinateError):
        board.available_range(x=-3, y=8)


def test_board_available_range_scout(board):
    piece = Piece(SCOUT, 2, Colour.RED, x=4, y=4)
    board[4, 4] = piece
    data = {
        "piece": piece,
        "north": (4, None),
        "east": (1, None),
        "south": (5, None),
        "west": (0, None),
    }
    assert board.available_range(x=4, y=4) == PieceRange(**data)
    piece = Piece(SCOUT, 2, Colour.RED, x=4, y=9)
    board[4, 9] = piece
    data = {
        "piece": piece,
        "north": (4, None),
        "east": (1, None),
        "south": (4, None),
        "west": (0, None),
    }
    assert board.available_range(x=4, y=4) == PieceRange(**data)
    data = {
        "piece": piece,
        "north": (4, None),
        "east": (5, None),
        "south": (0, None),
        "west": (4, None),
    }
    assert board.available_range(x=4, y=9) == PieceRange(**data)
    piece = Piece(SCOUT, 2, Colour.RED, x=0, y=9)
    board[0, 9] = piece
    data = {
        "piece": piece,
        "north": (9, None),
        "east": (3, None),
        "south": (0, None),
        "west": (0, None),
    }
    assert board.available_range(x=0, y=9) == PieceRange(**data)
    piece = Piece(SCOUT, 2, Colour.RED, x=9, y=0)
    board[9, 0] = piece
    data = {
        "piece": piece,
        "north": (0, None),
        "east": (0, None),
        "south": (9, None),
        "west": (9, None),
    }
    assert board.available_range(x=9, y=0) == PieceRange(**data)


def test_board_available_range_scout_oppostion_and_same_team(board):
    board[0, 0] = Piece(MINER, 2, Colour.BLUE, x=0, y=0)  # opposite
    piece = Piece(SCOUT, 2, Colour.RED, x=0, y=4)  # central piece
    board[0, 4] = piece
    data = {
        "piece": piece,
        "north": (3, Piece(MINER, 2, Colour.BLUE, x=0, y=0)),
        "east": (1, None),
        "south": (5, None),
        "west": (0, None),
    }
    assert board.available_range(x=0, y=4) == PieceRange(**data)

    board[1, 4] = Piece(MINER, 2, Colour.RED, x=1, y=4)  # opposite
    data = {
        "piece": piece,
        "north": (3, Piece(MINER, 2, Colour.BLUE, x=0, y=0)),
        "east": (0, None),
        "south": (5, None),
        "west": (0, None),
    }
    assert board.available_range(x=0, y=4) == PieceRange(**data)

    board[0, 5] = Piece(MINER, 2, Colour.RED, x=0, y=5)  # same team
    data = {
        "piece": piece,
        "north": (3, Piece(MINER, 2, Colour.BLUE, x=0, y=0)),
        "east": (0, None),
        "south": (0, None),
        "west": (0, None),
    }
    assert board.available_range(x=0, y=4) == PieceRange(**data)


def test_board_available_range_scout_opposition_at_four_sides(board):
    piece = Piece(SCOUT, 2, Colour.RED, x=4, y=6)  # central piece
    board[4, 6] = piece
    board[4, 0] = Piece(MINER, 2, Colour.BLUE, x=4, y=0)  # north
    board[9, 6] = Piece(MINER, 2, Colour.BLUE, x=9, y=6)  # east
    board[4, 9] = Piece(MINER, 2, Colour.BLUE, x=4, y=9)  # south
    board[0, 6] = Piece(MINER, 2, Colour.BLUE, x=0, y=6)  # west

    data = {
        "piece": piece,
        "north": (5, Piece(MINER, 2, Colour.BLUE, x=4, y=0)),
        "east": (4, Piece(MINER, 2, Colour.BLUE, x=9, y=6)),
        "south": (2, Piece(MINER, 2, Colour.BLUE, x=4, y=9)),
        "west": (3, Piece(MINER, 2, Colour.BLUE, x=0, y=6)),
    }
    assert board.available_range(x=4, y=6) == PieceRange(**data)


def test_board_available_range_opposition_north(board):
    piece = Piece(MINER, 2, Colour.RED, x=4, y=6)  # central piece
    board[4, 4] = piece
    board[4, 3] = Piece(MINER, 2, Colour.BLUE, x=4, y=3)  # opposition
    data = {
        "piece": piece,
        "north": (0, Piece(MINER, 2, Colour.BLUE, x=4, y=3)),
        "east": (1, None),
        "south": (1, None),
        "west": (0, None),
    }
    assert board.available_range(x=4, y=4) == PieceRange(**data)
