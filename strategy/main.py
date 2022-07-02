"""Strategy main module."""

import logging
from random import randrange
from typing import NamedTuple

from strategy.board import Board
from strategy.console import console
from strategy.exceptions import InvalidOperationError
from strategy.game import Empty, Lake
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


def get_available_range(board: Board, x: int, y: int) -> Range:
    """Return the available range for a cell in a board."""
    if board[x, y] == Lake:
        raise InvalidOperationError
    if board[x, y] == Empty:
        return Range(0, 0, 0, 0)
    north = 0
    east = 0
    south = 0
    west = 0
    return Range(north, east, south, west)


if __name__ == "__main__":
    console.print("Strategy started.")
    board = Board()
    board.create_random_pieces(Player.RED)
    board.create_random_pieces(Player.BLUE)
    console.print("Created random board.")
    console.print(f"{board}", soft_wrap=True)
    console.print("Strategy ended.")
