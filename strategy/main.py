"""Strategy main module."""

import logging
from random import choice, randrange
from typing import NamedTuple

from strategy.board import Board
from strategy.console import console
from strategy.game import Empty
from strategy.pieces import BOMB, FLAG, SCOUT
from strategy.player import Player

log = logging.getLogger(__name__)


def select_a_cell(player: Player) -> tuple[int, int]:
    """Return a random cell."""
    line_start = 0 if player == Player.RED else 6
    return randrange(line_start, line_start + 4), randrange(10)


class Range(NamedTuple):
    """The range of a Piece in a cell on the board."""

    north: int
    east: int
    south: int
    west: int


EmptyRange = Range(0, 0, 0, 0)


def get_available_range(board: Board, x: int, y: int) -> Range:
    """Return the available `Range` for a piece at `x`, `y` on a board."""
    piece = board[x, y]
    if piece.name == FLAG or piece.name == BOMB:
        return EmptyRange
    if piece.name != SCOUT:
        north = 1 if board.get((x, y - 1), None) == Empty else 0
        east = 1 if board.get((x + 1, y), None) == Empty else 0
        south = 1 if board.get((x, y + 1), None) == Empty else 0
        west = 1 if board.get((x - 1, y), None) == Empty else 0
    else:
        i = 1
        while board.get((x, y - i), None) == Empty:
            i += 1
        north = i - 1
        i = 1
        while board.get((x + i, y), None) == Empty:
            i += 1
        east = i - 1
        i = 1
        while board.get((x, y + i), None) == Empty:
            i += 1
        south = i - 1
        i = 1
        while board.get((x - i, y), None) == Empty:
            i += 1
        west = i - 1
    return Range(north, east, south, west)


if __name__ == "__main__":
    console.print("Strategy started.")
    board = Board()
    board.create_random_pieces(Player.RED)
    board.create_random_pieces(Player.BLUE)
    console.print("Created random board.")
    console.print(f"{board}", soft_wrap=True)
    red_piece = choice(board.red())
    console.print(f"Random {red_piece} at {red_piece.x}|{red_piece.y}.")
    console.print(f"Available range: {get_available_range(board, red_piece.x, red_piece.y)}")
    other_piece = board[0, 6]
    console.print(f"Other {other_piece} at {other_piece.x}|{other_piece.y}.")
    console.print(f"Available range: {get_available_range(board, 0, 6)}")
    console.print("Strategy ended.")
