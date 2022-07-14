"""Strategy main module."""

import logging
import random
from random import randrange

from strategy.board import Board
from strategy.colour import Colour
from strategy.console import console

log = logging.getLogger(__name__)


def select_a_cell(player: Colour) -> tuple[int, int]:
    """Return a random cell."""
    line_start = 0 if player == Colour.RED else 6
    return randrange(line_start, line_start + 4), randrange(10)


if __name__ == "__main__":
    console.print("Strategy started.")
    board = Board()
    board.create_random_pieces(Colour.RED)
    board.create_random_pieces(Colour.BLUE)
    console.print("Created random board.")
    console.print(f"{board}", soft_wrap=True)
    for i in range(10):
        piece = board[i, 6]
        range = board.available_range(piece.x, piece.y)
        if range.has_opponent_in_sight[1]:
            attack = f"can attack {range.has_opponent_in_sight[1]}"
        else:
            attack = "cannot attack any opponent piece"
        console.print(f"The {piece} can reach {range}, so {attack}.")

    movable_pieces = []
    for piece in board.red():
        range = board.available_range(piece.x, piece.y)
        if range.can_move[0]:
            movable_pieces.append((piece, range))
    console.print(
        f"Movable pieces: {', '.join([piece.colour.name.lower() + ' ' + piece.name for piece, _ in movable_pieces])}."
    )
    piece, range = random.choice(movable_pieces)
    console.print(f"Will move {piece} ({range}).")
    console.print("Strategy ended.")
