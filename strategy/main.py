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


def available_range(board: Board, x: int, y: int) -> RangePiece:
    """Get the available `RangePiece` of a `Piece` at a given position on the board."""
    piece = board[x, y]
    if not isinstance(piece, Piece):
        raise NoPieceError
    if piece.name == FLAG or piece.name == BOMB:
        return EmptyRangePiece

    if piece.name == SCOUT:
        return _calculate_scout_range_piece(board, piece, x, y)

    else:
        north_field = board.get((x, y - 1), None)
        north = _create_range(piece, north_field)

        east_field = board.get((x + 1, y), None)
        east = _create_range(piece, east_field)

        south_field = board.get((x, y + 1), None)
        south = _create_range(piece, south_field)

        west_field = board.get((x - 1, y), None)
        west = _create_range(piece, west_field)

        return RangePiece(north, east, south, west)


def _calculate_scout_range_piece(board: Board, piece: Piece, x: int, y: int) -> RangePiece:
    """Return the `RangePiece` for a `SCOUT` in the board."""
    i = 1
    while north_field := board.get((x, y - i), None):
        if not isinstance(north_field, Empty):
            break
        i += 1
    north = _create_scout_range(i, piece, north_field)
    i = 1
    while east_field := board.get((x + i, y), None):
        if not isinstance(east_field, Empty):
            break
        i += 1
    east = _create_scout_range(i, piece, east_field)
    i = 1
    while south_field := board.get((x, y + i), None):
        if not isinstance(south_field, Empty):
            break
        i += 1
    south = _create_scout_range(i, piece, south_field)
    i = 1
    while west_field := board.get((x - i, y), None):
        if not isinstance(west_field, Empty):
            break
        i += 1
    west = _create_scout_range(i, piece, west_field)
    return RangePiece(north, east, south, west)


def _create_range(source: Piece, destination: Piece | Empty | None) -> tuple[int, Piece | None]:
    """Create a range tuple containing the length (0 or 1) and the possible `Piece` that can be attacked."""
    if destination and isinstance(destination, Empty):
        north = 1, None
    elif destination and isinstance(destination, Piece) and destination.colour != source.colour:
        north = 0, destination
    else:
        north = 0, None
    return north


def _create_scout_range(index: int, source: Piece, destination: Piece | None) -> tuple[int, Piece | None]:
    """Create a range tuple containing the length (`index - 1`) and the possible `Piece` that can be attacked."""
    if destination and isinstance(destination, Piece) and destination.colour != source.colour:
        north = index - 1, destination
    else:
        north = index - 1, None
    return north


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
