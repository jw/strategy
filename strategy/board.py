"""The Strategy board."""

from random import randrange
from typing import Any

from strategy.exceptions import InvalidDimensionsError
from strategy.game import Empty, Lake, log
from strategy.pieces import PIECES
from strategy.player import Player


class Board:
    """The strategy board."""

    def __init__(self) -> None:
        """Create an empty board."""
        self._board = {}
        self._add_lakes()

    def __str__(self) -> str:
        """Show the board."""
        grid = [[self[x, y] for x in range(10)] for y in range(10)]
        result = "\n"
        for x, line in enumerate(grid):
            for y, cell in enumerate(line):
                result += f"[{x}|{y}: {cell}] "
            result += "\n"
        return result

    def create_random_pieces(self, player: Player) -> None:
        """Create a random setup for a given `Player`. RED is at the bottom, BLUE is on top."""
        setup_list = [None for _ in range(40)]
        for piece in PIECES:
            index = randrange(39)
            while setup_list[index] is not None:
                index = randrange(40)
            setup_list[index] = piece
        current_line = 6 if player == Player.RED else 0
        for index, piece in enumerate(setup_list):
            if index > 0 and index % 10 == 0:
                current_line += 1
            log.debug(f"Adding {piece} to {index % 10}|{current_line}.")
            self[index % 10, current_line] = piece

    def bottom(self) -> list:
        """Return the bottom four lines of the board as a `list`."""
        return [self[x, y] for x in range(0, 10) for y in range(6, 10)]

    def top(self) -> list:
        """Return the top four lines of the board as a `list`."""
        return [self[x, y] for x in range(0, 10) for y in range(0, 4)]

    def __repr__(self) -> str:
        """Show the board."""
        return f"<{self.__class__.__name__} ({self._board})>"

    def __len__(self) -> int:
        """Get the lenght of the board."""
        return 10 * 10

    def __getitem__(self, item: tuple) -> Any:
        """Get a cell from the board."""
        return self._board.get(item, Empty)

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
