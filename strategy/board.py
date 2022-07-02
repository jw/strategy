"""The Strategy board."""
import copy
from random import randrange
from typing import Any

from strategy.exceptions import InvalidDimensionsError
from strategy.game import LAKE, Cell, Empty, Lake, log
from strategy.pieces import PIECES, Piece
from strategy.player import Player


class Board:
    """
    The strategy board.

    The top left is x=0 and y=0, the bottom right is x=9, y=9.
    The left lake is (2, 4), (3, 4), (2, 5) and (3, 5).
    The right lake is (6, 4), (6, 4), (6, 5) and (7, 5).
    The top is for the blue player, the bottom for the red player.
    """

    def __init__(self) -> None:
        """Create an empty board."""
        self._board = {}
        self._add_lakes()

    def __str__(self) -> str:
        """Show the board."""
        grid = [[self[x, y] for x in range(10)] for y in range(10)]
        result = "\n |"
        foo = "-"
        for x, line in enumerate(grid):
            result += f"{foo:-^14}|" * 10
            result += "\n | "
            for y, cell in enumerate(line):
                result += self.format(cell, x, y)
            result += "\n |"
        result += f"{foo:-^14}|" * 10
        result += "\n"
        return result

    def format(self, cell: Piece | Cell, x: int, y: int, length: int = 12) -> str:
        """Return a formatted cell."""
        if isinstance(cell, Piece):
            color = "red" if cell.player == Player.RED else "blue"
        if isinstance(cell, Cell):
            color = "green" if cell.name == LAKE else "bright_black"
        return f"[{color}]{cell.name:^{length}}[/{color}] | "

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
        """Get the length of the board."""
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
