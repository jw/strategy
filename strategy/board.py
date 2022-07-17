"""The Strategy board."""
import contextlib
import copy
import logging
from dataclasses import dataclass
from random import randrange

from strategy.colour import Colour
from strategy.exceptions import InvalidCoordinateError, InvalidDestinationError, InvalidDimensionsError, NoPieceError
from strategy.pieces import BOMB, EMPTY, FLAG, LAKE, PIECES, SCOUT, Empty, Field, Lake, Piece

log = logging.getLogger(__name__)

SIZE = 12
DASH = "-"


@dataclass
class PieceRange:
    """The range of a Piece in a cell on the board: distance and possible piece that it can reach."""

    piece: Piece

    north: tuple[int, Piece | None] = (0, None)
    east: tuple[int, Piece | None] = (0, None)
    south: tuple[int, Piece | None] = (0, None)
    west: tuple[int, Piece | None] = (0, None)

    @property
    def can_move(self) -> bool:
        """Return `True` when a `piece` can move or attack another `Piece`, `False` otherwise."""
        return self.north[0] > 0 or self.east[0] > 0 or self.south[0] > 0 or self.west[0] > 0

    @property
    def can_attack(self) -> bool:
        """Return `True` when a `piece` can attack another `Piece`, `False` otherwise."""
        return (
            self.north[1] is not None
            or self.east[1] is not None
            or self.south[1] is not None
            or self.west[1] is not None
        )

    @property
    def attackables(self) -> dict[str, Piece]:
        """Return the attackable `Pieces` in a `dict[str, Piece]`."""
        d = {}
        if self.north[1]:
            d["north"] = self.north[1]
        if self.east[1]:
            d["east"] = self.east[1]
        if self.south[1]:
            d["south"] = self.south[1]
        if self.west[1]:
            d["west"] = self.west[1]
        return d

    @property
    def movables(self) -> dict[str, list[tuple[int, int]]]:
        """Return all the coordinates the `Piece` can move to in a `dict[str, list[tuple[int, int]]]`."""
        d = {}
        if self.north[0] > 0:
            d["north"] = [(self.piece.x, self.piece.y - i - 1) for i in range(self.north[0])]
        if self.east[0] > 0:
            d["east"] = [(self.piece.x + i + 1, self.piece.y) for i in range(self.east[0])]
        if self.south[0] > 0:
            d["south"] = [(self.piece.x, self.piece.y + i + 1) for i in range(self.south[0])]
        if self.west[0] > 0:
            d["west"] = [(self.piece.x - i - 1, self.piece.y) for i in range(self.west[0])]
        return d

    def __contains__(self, item: tuple[int, int]) -> bool:
        """Return `True` when `item` is in the `self.movables` dict values; `False` otherwise."""
        all_movables = []
        for coordinates in self.movables.values():
            all_movables.extend(coordinates)
        return item in all_movables


EmptyPieceRange = PieceRange(piece=None)


class Board:
    """
    The strategy board.

    The top left is x=0 and y=0, the bottom right is x=9, y=9.

    The left lake is (2, 4), (3, 4), (2, 5) and (3, 5).
    The right lake is (6, 4), (7, 4), (6, 5) and (7, 5).
    The top half is for the blue player, the bottom half for the red player.

    Each field of the board can be visited via board[int, int], like board[0, 0] or
    board[5, 6].  It is also possible to use chess based coordinates, like board["a10"]
    or board["A", 10] (both are the same as board[0, 0]).
    """

    LEFT_LAKE = [(2, 4), (3, 4), (2, 5), (3, 5)]
    RIGHT_LAKE = [(6, 4), (7, 4), (6, 5), (7, 5)]
    LAKES = LEFT_LAKE + RIGHT_LAKE

    TOP = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]

    def __init__(self) -> None:
        """Create an empty board."""
        self._board = {}
        self._add_lakes()
        self._moves: list[tuple[Colour, tuple[int, int], tuple[int, int]]] = []

    def __str__(self) -> str:
        """Show the board."""
        grid = [[self.get((x, y), Lake) for x in range(10)] for y in range(10)]
        result = self._first_line()
        for x, line in enumerate(grid):
            result += f"{DASH:-^{SIZE + 2}}|" * 10
            result += f"\n  {10 - x:2} | "
            for y, cell in enumerate(line):
                result += self._format(cell, x, y)
            result += "\n ----|"
        result = self._last_line(result)
        return result

    @property
    def winner(self) -> Colour | None:
        """Return the winning Colour; if no winner could be found, return `None`."""
        if self._flag_by_colour(Colour.RED) and self._has_movable(Colour.RED):
            if self._flag_by_colour(Colour.BLUE) and self._has_movable(Colour.BLUE):
                return None
            else:
                return Colour.RED
        else:
            return Colour.BLUE

    @property
    def moves(self) -> list[tuple[Colour, tuple[int, int], tuple[int, int]]]:
        """Return the moves."""
        return self._moves

    def create_random_pieces(self, colour: Colour) -> None:
        """Create a random setup for a given `Player`. RED is at the bottom, BLUE is on top."""
        setup_list = self.random_pieces_list()
        current_line = 6 if colour == Colour.RED else 0
        for index, piece in enumerate(setup_list):
            if index > 0 and index % 10 == 0:
                current_line += 1
            piece.colour = colour
            piece.x = index % 10
            piece.y = current_line
            log.debug(f"Adding {piece.colour.name.lower()} {piece} to {piece.x}|{piece.y}.")
            self[piece.x, piece.y] = piece

    def random_pieces_list(self) -> list[Piece]:
        """Return a random list of the 40 pieces."""
        setup_list = [None for _ in range(40)]
        for piece in copy.deepcopy(PIECES):
            index = randrange(40)
            while setup_list[index] is not None:
                index = randrange(40)
            setup_list[index] = piece
        return setup_list

    def bottom(self) -> list[Piece | Field]:
        """Return the empty cells or pieces in bottom four lines of the board as a `list`."""
        return [self[x, y] for x in range(0, 10) for y in range(6, 10)]

    def top(self) -> list[Piece | Field]:
        """Return the empty cells or pieces in top four lines of the board as a `list`."""
        return [self[x, y] for x in range(0, 10) for y in range(0, 4)]

    def red(self) -> list[Piece]:
        """Return the red pieces on the board."""
        return self._by_colour(Colour.RED)

    def blue(self) -> list[Piece]:
        """Return the blue pieces on the board."""
        return self._by_colour(Colour.BLUE)

    def get(self, key: tuple[int, int] | tuple[str, int] | str, default: Field | None) -> Field | None:
        """Return the `Field` (i.e. `Piece` or `Empty`), or default when an `InvalidDimensionsError` was raised."""
        try:
            return self[self._get_coordinates(key)]
        except (InvalidDimensionsError, InvalidCoordinateError):
            return default

    def move(self, source: tuple[int, int], dest: tuple[int, int]) -> None:
        """
        Move `Piece` at `source` to `destination`, and return the result of the move.

        This might entail an attack.
        """
        piece = self[source]
        if piece == Empty(EMPTY, source[0], source[1]):
            raise NoPieceError
        if not self._is_possible_destination(piece, dest):
            raise InvalidDestinationError
        if self[dest] == Empty(EMPTY, dest[0], dest[1]):
            self[dest] = self[source]
            self[dest].x = dest[0]
            self[dest].y = dest[1]
            self[source] = Empty(EMPTY, source[0], source[1])
        else:
            if piece.attack(self[dest]) is True:
                self[dest] = self[source]
                self[dest].x = dest[0]
                self[dest].y = dest[1]
                self[source] = Empty(EMPTY, source[0], source[1])
            elif piece.attack(self[dest]) is None:
                self[dest] = Empty(EMPTY, dest[0], dest[1])
                self[source] = Empty(EMPTY, source[0], source[1])
            else:
                self[source] = Empty(EMPTY, source[0], source[1])
        self._moves.append((piece.colour, (source[0], source[1]), (dest[0], dest[1])))

    def available_range(self, x: int, y: int) -> PieceRange:
        """
        Return the available `PieceRange` of a `Piece` at a given position on the board.

        The tuples in the `PieceRange` consist of a walkable distance (an int) and a possible `Piece`.
        If at the end of the distance there is an opponent Piece, it is added to the tuple; otherwise,
        the second slot will be None.
        """
        piece = self[x, y]
        if not isinstance(piece, Piece):
            raise NoPieceError
        if piece.name == FLAG or piece.name == BOMB:
            return EmptyPieceRange

        if piece.name == SCOUT:
            return self._calculate_scout_range_piece(piece, x, y)

        else:
            north_field = self.get((x, y - 1), None)
            north = self._create_regular_range(piece, north_field)

            east_field = self.get((x + 1, y), None)
            east = self._create_regular_range(piece, east_field)

            south_field = self.get((x, y + 1), None)
            south = self._create_regular_range(piece, south_field)

            west_field = self.get((x - 1, y), None)
            west = self._create_regular_range(piece, west_field)

            return PieceRange(piece, north, east, south, west)

    def __repr__(self) -> str:
        """Show the board."""
        return f"<{self.__class__.__name__} ({self._board})>"

    def __len__(self) -> int:
        """Get the length of the board."""
        return 10 * 10

    def __getitem__(self, key: tuple[int, int] | tuple[str, int] | str) -> Piece | Lake | Empty:
        """Get a cell from the board."""
        coordinates = self._get_coordinates(key)
        self._raise_when_outside_dimensions(coordinates)
        return self._board.get(coordinates, Empty(EMPTY, x=coordinates[0], y=coordinates[1]))

    def __setitem__(self, key: tuple[int, int], value: Piece | Lake | Empty) -> None:
        """Put `value` in a cell of the board."""
        self._raise_when_outside_dimensions(key)
        self._board[key] = value

    def _add_lakes(self) -> None:
        """Add the lakes to the board."""
        for lake in self.LAKES:
            self._board[lake] = Lake(LAKE, x=lake[0], y=lake[1])

    def _by_colour(self, colour: Colour) -> list[Piece]:
        """Return all the pieces of the given player."""
        pieces = []
        for piece in self._board.values():
            if isinstance(piece, Piece) and piece.colour == colour:
                pieces.append(piece)
        return pieces

    def _first_line(self) -> str:
        """Create the first line of the board."""
        result = "\n     |"
        result += "|".join([f"{item.upper():^{SIZE + 2}}" for item in self.TOP])
        result += "|\n ----|"
        return result

    def _last_line(self, result: str) -> str:
        """Create the last line of the board."""
        result += f"{DASH:-^{SIZE + 2}}|" * 10
        result += "\n"
        return result

    def _format(self, cell: Piece | Field, x: int, y: int, length: int = SIZE) -> str:
        """Return a formatted cell."""
        if isinstance(cell, Piece):
            colour = "red" if cell.colour == Colour.RED else "blue"
        elif isinstance(cell, Lake):
            colour = "green"
        else:
            colour = "bright_black"
        return f"[{colour}]{cell.name:^{length}}[/{colour}] | "

    def _raise_when_outside_dimensions(self, key: tuple[int, int]) -> None:
        """Raise when outside the board dimensions."""
        if key[0] < 0 or key[0] > 9:
            raise InvalidDimensionsError()
        if key[1] < 0 or key[1] > 9:
            raise InvalidDimensionsError()

    def _str_to_int(self, s: str) -> int:
        """Return s in `self.TOP` as an int. `a` is 0,... `j` is 9. This method is case-insensitive."""
        if not isinstance(s, str):
            raise InvalidCoordinateError
        lower_char = s.lower()
        if lower_char not in self.TOP:
            raise InvalidCoordinateError
        return self.TOP.index(lower_char)

    def _coordinate_to_tuple(self, s: str) -> tuple[int, int]:
        """
        Return a chess coordinate to a tuple[int, int].

        "A10" becomes (0, 0), "j1" becomes (9, 9). This method is case-insensitive.
        """
        try:
            x = s[0].lower()  # first should be a character
            y = s[1:]  # second should be a positive int
            if x in self.TOP:
                with contextlib.suppress(ValueError):
                    y_int = int(y)
                    if 1 <= y_int <= 10:
                        return self._str_to_int(x), 10 - y_int
            raise InvalidCoordinateError
        except (IndexError, TypeError):
            raise InvalidCoordinateError

    def _get_coordinates(self, key: tuple[int, int] | tuple[str, int] | str) -> tuple[int, int]:
        """
        Return tuple[int, int] coordinates based on the type.

        :param key:
        :return:
        """
        if isinstance(key, tuple):
            if isinstance(key[0], int) and 0 <= key[0] <= 9 and isinstance(key[1], int) and 0 <= key[1] <= 9:
                return key
            elif isinstance(key[0], str) and isinstance(key[1], int) and 1 <= key[1] <= 10:
                return self._str_to_int(key[0]), 10 - key[1]
            else:
                raise InvalidCoordinateError
        elif isinstance(key, str):
            return self._coordinate_to_tuple(key)

    def _calculate_scout_range_piece(self, piece: Piece, x: int, y: int) -> PieceRange:
        """Return the `RangePiece` for a `SCOUT` in the board."""
        i = 1
        while north_field := self.get((x, y - i), None):
            if not isinstance(north_field, Empty):
                break
            i += 1
        north = self._create_scout_range(i, piece, north_field)
        i = 1
        while east_field := self.get((x + i, y), None):
            if not isinstance(east_field, Empty):
                break
            i += 1
        east = self._create_scout_range(i, piece, east_field)
        i = 1
        while south_field := self.get((x, y + i), None):
            if not isinstance(south_field, Empty):
                break
            i += 1
        south = self._create_scout_range(i, piece, south_field)
        i = 1
        while west_field := self.get((x - i, y), None):
            if not isinstance(west_field, Empty):
                break
            i += 1
        west = self._create_scout_range(i, piece, west_field)
        return PieceRange(piece, north, east, south, west)

    def _create_regular_range(self, source: Piece, destination: Piece | Empty | None) -> tuple[int, Piece | None]:
        """Create a range tuple containing the length (0 or 1) and the possible `Piece` that can be attacked."""
        if destination and isinstance(destination, Empty):
            north = 1, None
        elif destination and isinstance(destination, Piece) and destination.colour != source.colour:
            north = 1, destination
        else:
            north = 0, None
        return north

    def _create_scout_range(self, index: int, source: Piece, destination: Piece | None) -> tuple[int, Piece | None]:
        """Create a range tuple containing the distance and the possible `Piece` that can be attacked."""
        if destination and isinstance(destination, Piece) and destination.colour != source.colour:
            north = index, destination
        else:
            north = index - 1, None
        return north

    def _is_possible_destination(self, piece: Piece, dest: tuple[int, int]) -> bool:
        piece_range = self.available_range(piece.x, piece.y)
        return dest in piece_range

    def _flag_by_colour(self, colour: Colour) -> bool:
        if colour == Colour.RED:
            pieces = self.red()
        else:
            pieces = self.blue()
        return any(piece.name == FLAG for piece in pieces)

    def _has_movable(self, colour: Colour) -> bool:
        if colour == Colour.RED:
            pieces = self.red()
        else:
            pieces = self.blue()
        for piece in pieces:
            piece_range = self.available_range(piece.x, piece.y)
            all_movables = []
            for coordinates in piece_range.movables.values():
                all_movables.extend(coordinates)
            if all_movables:
                return True
        return False
