"""The Strategy game."""

from enum import Enum, auto
from typing import Any

from pydantic import BaseModel, root_validator


class Player(Enum):
    """The Player can be `RED` or `BLUE`."""

    BLUE = auto()
    RED = auto()


class _Empty:
    """The Empty cell."""

    def __repr__(self) -> str:
        """Return `<empty>`."""
        return "<empty>"

    def __bool__(self) -> bool:  # noqa: CCE001
        """Return `False`."""
        return False

    __nonzero__ = __bool__


Empty = _Empty()


class _Lake:
    """The Lake cell."""

    def __repr__(self) -> str:
        """Return `<lake>`."""
        return "<lake>"

    def __bool__(self) -> bool:  # noqa: CCE001
        """Return `False`."""
        return False

    __nonzero__ = __bool__


Lake = _Lake()


class InvalidDimensionsError(Exception):
    """Invalid dimension."""

    pass


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

    def __repr__(self) -> str:
        """Show the board."""
        return f"<{self.__class__.__name__} ({self._board})>"

    def __len__(self) -> int:
        """Get the lenght of the board."""
        return 10 * 10

    def __getitem__(self, item: list) -> Any:
        """Get a cell from the board."""
        return self._board.get(item, Empty)

    def __setitem__(self, key: tuple[int, int], value: Any) -> None:
        """Put `value` in a cell of the board."""
        if 0 > key[0] > 9:
            raise InvalidDimensionsError()
        if 0 > key[1] > 9:
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


class Action(BaseModel):
    """A player action."""

    source: tuple[int, int]
    destination: tuple[int, int]
    player: Player

    @root_validator
    def check_action(cls, action: "Action") -> "Action":  # noqa: N805
        """Check the action."""
        return action
