"""The Strategy board."""
import contextlib
import copy
from random import randrange

from strategy.colour import Colour
from strategy.exceptions import InvalidCoordinateError, InvalidDimensionsError
from strategy.game import EMPTY, LAKE, Empty, Field, Lake, log
from strategy.pieces import PIECES, Piece

SIZE = 12
DASH = "-"


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

    def get(self, key: tuple[int, int] | tuple[str, int] | str, default: Field | None) -> Field:
        """Return the `Field` (i.e. `Piece` or `Empty`), or default when an `InvalidDimensionsError` was raised."""
        try:
            return self[self._get_coordinates(key)]
        except (InvalidDimensionsError, InvalidCoordinateError):
            return default

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
        if not isinstance(s, str):
            raise InvalidCoordinateError
        lower_char = s.lower()
        if lower_char not in self.TOP:
            raise InvalidCoordinateError
        return self.TOP.index(lower_char)

    def _coordinate_to_tuple(self, s: str) -> tuple[int, int]:
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
        if isinstance(key, tuple):
            if isinstance(key[0], int) and 0 <= key[0] <= 9 and isinstance(key[1], int) and 0 <= key[1] <= 9:
                return key
            elif isinstance(key[0], str) and isinstance(key[1], int) and 1 <= key[1] <= 10:
                return self._str_to_int(key[0]), 10 - key[1]
            else:
                raise InvalidCoordinateError
        elif isinstance(key, str):
            return self._coordinate_to_tuple(key)
