"""The Strategy board."""
import copy
from random import randrange
from typing import Any

from strategy.exceptions import InvalidDimensionsError
from strategy.game import LAKE, Cell, Empty, Lake, log
from strategy.pieces import PIECES, Piece
from strategy.player import Player

SIZE = 12
DASH = "-"


class Board:
    """
    The strategy board.

    The top left is x=0 and y=0, the bottom right is x=9, y=9.
    The left lake is (2, 4), (3, 4), (2, 5) and (3, 5).
    The right lake is (6, 4), (6, 4), (6, 5) and (7, 5).
    The top half is for the blue player, the bottom half for the red player.
    """

    def __init__(self) -> None:
        """Create an empty board."""
        self._board = {}
        self._add_lakes()

    def __str__(self) -> str:
        """Show the board."""
        grid = [[self[x, y] for x in range(10)] for y in range(10)]
        result = self._first_line()
        for x, line in enumerate(grid):
            result += f"{DASH:-^{SIZE + 2}}|" * 10
            result += f"\n  {x + 1:2} | "
            for y, cell in enumerate(line):
                result += self._format(cell, x, y)
            result += "\n ----|"
        result = self._last_line(result)
        return result

    def create_random_pieces(self, player: Player) -> None:
        """Create a random setup for a given `Player`. RED is at the bottom, BLUE is on top."""
        setup_list = self.random_pieces_list()
        current_line = 6 if player == Player.RED else 0
        for index, piece in enumerate(setup_list):
            if index > 0 and index % 10 == 0:
                current_line += 1
            piece.player = player
            piece.x = index % 10
            piece.y = current_line
            log.debug(f"Adding {piece.player.name.lower()} {piece} to {piece.x}|{piece.y}.")
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

    def bottom(self) -> list[Piece | Cell]:
        """Return the empty cells or pieces in bottom four lines of the board as a `list`."""
        return [self[x, y] for x in range(0, 10) for y in range(6, 10)]

    def top(self) -> list[Piece | Cell]:
        """Return the empty cells or pieces in top four lines of the board as a `list`."""
        return [self[x, y] for x in range(0, 10) for y in range(0, 4)]

    def red(self) -> list[Piece]:
        """Return the red pieces on the board."""
        return self._by_color(Player.RED)

    def blue(self) -> list[Piece]:
        """Return the blue pieces on the board."""
        return self._by_color(Player.BLUE)

    def get(self, key: tuple[int, int], default: Any) -> Any:
        """Return the cell, or default when an `InvalidDimensionsError` was raised."""
        try:
            return self[key]
        except InvalidDimensionsError:
            return default

    def __repr__(self) -> str:
        """Show the board."""
        return f"<{self.__class__.__name__} ({self._board})>"

    def __len__(self) -> int:
        """Get the length of the board."""
        return 10 * 10

    def __getitem__(self, key: tuple) -> Any:
        """Get a cell from the board."""
        if key[0] < 0 or key[0] > 9:
            raise InvalidDimensionsError()
        if key[1] < 0 or key[1] > 9:
            raise InvalidDimensionsError()
        return self._board.get(key, Empty)

    def __setitem__(self, key: tuple[int, int], value: Any) -> None:
        """Put `value` in a cell of the board."""
        if key[0] < 0 or key[0] > 9:
            raise InvalidDimensionsError()
        if key[1] < 0 or key[1] > 9:
            raise InvalidDimensionsError()
        self._board[key] = value

    def _add_lakes(self) -> None:
        """Add the lakes to the board."""
        self._board[2, 4] = Lake
        self._board[3, 4] = Lake
        self._board[2, 5] = Lake
        self._board[3, 5] = Lake
        self._board[6, 4] = Lake
        self._board[7, 4] = Lake
        self._board[6, 5] = Lake
        self._board[7, 5] = Lake

    def _by_color(self, player: Player) -> list[Piece]:
        """Return all the pieces of the given player."""
        pieces = []
        for value in self._board.values():
            if not isinstance(value, Cell) and value.player == player:
                pieces.append(value)
        return pieces

    def _first_line(self) -> str:
        """Create the first line of the board."""
        result = "\n     |"
        result += "|".join([f"{item:^{SIZE + 2}}" for item in range(1, 11)])
        result += "|\n ----|"
        return result

    def _last_line(self, result: str) -> str:
        """Create the last line of the board."""
        result += f"{DASH:-^{SIZE + 2}}|" * 10
        result += "\n"
        return result

    def _format(self, cell: Piece | Cell, x: int, y: int, length: int = SIZE) -> str:
        """Return a formatted cell."""
        if isinstance(cell, Piece):
            color = "red" if cell.player == Player.RED else "blue"
        if isinstance(cell, Cell):
            color = "green" if cell.name == LAKE else "bright_black"
        return f"[{color}]{cell.name:^{length}}[/{color}] | "
