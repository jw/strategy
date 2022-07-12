"""Strategy main module."""

import logging
from dataclasses import dataclass
from random import randrange

from strategy.board import Board
from strategy.colour import Colour
from strategy.console import console
from strategy.exceptions import NoPieceError
from strategy.game import Empty
from strategy.pieces import BOMB, FLAG, SCOUT, Piece

log = logging.getLogger(__name__)


def select_a_cell(player: Colour) -> tuple[int, int]:
    """Return a random cell."""
    line_start = 0 if player == Colour.RED else 6
    return randrange(line_start, line_start + 4), randrange(10)


@dataclass
class RangePiece:
    """The range of a Piece in a cell on the board: distance and possible piece."""

    north: tuple[int, Piece | Empty | None] = (0, None)
    east: tuple[int, Piece | Empty | None] = (0, None)
    south: tuple[int, Piece | Empty | None] = (0, None)
    west: tuple[int, Piece | Empty | None] = (0, None)

    @property
    def has_opponent_in_sight(self) -> tuple[bool, Piece | None]:
        """Return `(True, Piece)` when a `Piece` can be attached, `(False, None)` otherwise."""
        if self.north[1] is not None:
            return True, self.north[1]
        if self.east[1] is not None:
            return True, self.east[1]
        if self.south[1] is not None:
            return True, self.south[1]
        if self.west[1] is not None:
            return True, self.west[1]
        return False, None


EmptyRangePiece = RangePiece()


def available_range(board: Board, x: int, y: int) -> RangePiece:  # noqa: C901
    """Get the available `RangePiece` of a `Piece` at a given position on the board."""
    piece = board[x, y]
    if not isinstance(piece, Piece):
        raise NoPieceError
    if piece.name == FLAG or piece.name == BOMB:
        return EmptyRangePiece

    if piece.name == SCOUT:

        i = 1
        while north_field := board.get((x, y - i), None):
            if not isinstance(north_field, Empty):
                break
            i += 1
        if north_field and isinstance(north_field, Piece) and north_field.colour != piece.colour:
            north = i - 1, north_field
        else:
            north = i - 1, None

        i = 1
        while east_field := board.get((x + i, y), None):
            if not isinstance(east_field, Empty):
                break
            i += 1
        if east_field and isinstance(east_field, Piece) and east_field.colour != piece.colour:
            east = i - 1, east_field
        else:
            east = i - 1, None

        i = 1
        while south_field := board.get((x, y + i), None):
            if not isinstance(south_field, Empty):
                break
            i += 1
        if south_field and isinstance(south_field, Piece) and south_field.colour != piece.colour:
            south = i - 1, south_field
        else:
            south = i - 1, None

        i = 1
        while west_field := board.get((x - i, y), None):
            if not isinstance(west_field, Empty):
                break
            i += 1
        if west_field and isinstance(west_field, Piece) and west_field.colour != piece.colour:
            west = i - 1, west_field
        else:
            west = i - 1, None

    else:

        north_field = board.get((x, y - 1), None)
        if north_field and isinstance(north_field, Empty):
            north = 1, None
        elif north_field and isinstance(north_field, Piece) and north_field.colour != piece.colour:
            north = 1, north_field
        else:
            north = 0, None

        east_field = board.get((x + 1, y), None)
        if east_field and isinstance(east_field, Empty):
            east = 1, None
        elif east_field and isinstance(east_field, Piece) and east_field.colour != piece.colour:
            east = 1, east_field
        else:
            east = 0, None

        south_field = board.get((x, y + 1), None)
        if south_field and isinstance(south_field, Empty):
            south = 1, None
        elif south_field and isinstance(south_field, Piece) and south_field.colour != piece.colour:
            south = 1, south_field
        else:
            south = 0, None

        west_field = board.get((x - 1, y), None)
        if west_field and isinstance(west_field, Empty):
            west = 1, None
        elif west_field and isinstance(west_field, Piece) and west_field.colour != piece.colour:
            west = 1, west_field
        else:
            west = 0, None

    return RangePiece(north, east, south, west)


if __name__ == "__main__":
    console.print("Strategy started.")
    board = Board()
    board.create_random_pieces(Colour.RED)
    board.create_random_pieces(Colour.BLUE)
    console.print("Created random board.")
    console.print(f"{board}", soft_wrap=True)
    for i in range(10):
        piece = board[i, 6]
        range = available_range(board, piece.x, piece.y)
        if range.has_opponent_in_sight[1]:
            attack = f"can attack {range.has_opponent_in_sight[1]}"
        else:
            attack = "cannot attack any opponent piece"
        console.print(f"The {piece} can reach {range}, so {attack}.")
    console.print("Strategy ended.")
