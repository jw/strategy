"""Strategy main module."""

import logging
import random
import sys

from strategy.board import Board
from strategy.colour import Colour
from strategy.console import console

log = logging.getLogger(__name__)


def turn(board: Board, colour: Colour) -> None:
    """Perform a turn for a given `Colour`."""
    movable_pieces = []
    if colour == Colour.RED:
        pieces = board.red()
    else:
        pieces = board.blue()
    for piece in pieces:
        range = board.available_range(piece.x, piece.y)
        if range.can_move:
            movable_pieces.append(range)
    console.print(
        f"Movable {colour.name} pieces: {', '.join([f'{piece_range.piece}' for piece_range in movable_pieces])}."
    )
    piece_range = random.choice(movable_pieces)
    console.print(f"Will move {piece_range.piece} ({piece_range}):")
    console.print(f"  Movables: {piece_range.movables}.")
    console.print(f"  Attackables: {piece_range.attackables}.")
    all_movables = []
    for coordinates in piece_range.movables.values():
        all_movables.extend(coordinates)
    board.move((piece_range.piece.x, piece_range.piece.y), random.choice(all_movables))
    console.print(f"{board}", soft_wrap=True)
    if winner := board.winner:
        console.print(f"{winner.name.capitalize()} wins the game!")
        sys.exit()


def show_moves(moves: list[tuple[Colour, tuple[int, int], tuple[int, int]]]) -> None:
    """Show the moves."""
    for move in moves:
        console.print(f"{move[0]:>8}: x={move[1][0]}, y={move[1][1]} -> x={move[2][0]}, y={move[2][1]}")


def main() -> None:
    """Create a random board and start a cpu vs cpu game."""
    board = Board()
    board.create_random_pieces(Colour.RED)
    board.create_random_pieces(Colour.BLUE)
    console.print("Created random board.")
    console.print(f"{board}", soft_wrap=True)

    while True:
        turn(board, Colour.RED)
        turn(board, Colour.BLUE)


if __name__ == "__main__":
    main()
