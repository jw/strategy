"""The Strategy pieces."""
from dataclasses import dataclass
from functools import total_ordering

from strategy.colour import Colour
from strategy.exceptions import InvalidOperationError

EMPTY = "empty"
LAKE = "lake"

BOMB = "bomb"
MARSHAL = "marshal"
GENERAL = "general"
COLONEL = "colonel"
MAJOR = "major"
CAPTAIN = "captain"
LIEUTENANT = "lieutenant"
SERGEANT = "sergeant"
MINER = "miner"
SCOUT = "scout"
SPY = "spy"
FLAG = "flag"


@dataclass
class Field:
    """The base class of the `Piece`s, the `Empty` field or the `Lake` field in the `Board`."""

    name: str
    x: int
    y: int

    def __str__(self) -> str:
        """Show the Field."""
        return f"{self.name} ({self.x=}, {self.y=})"


class Empty(Field):
    """An empty field."""

    pass


class Lake(Field):
    """A lake field."""

    pass


@total_ordering
class Piece(Field):
    """The Strategy piece."""

    def __init__(
        self,
        name: str,
        power: int,
        colour: Colour | None = None,
        x: int | None = None,
        y: int | None = None,
        seen: bool = False,
    ) -> None:
        """Create a type by power and colour."""
        super().__init__(name, x, y)
        self.power = power
        self.colour = colour
        self.seen = seen

    def __str__(self) -> str:
        """Show the piece."""
        if self.x and self.y:
            coordinates = f" at x:{self.x}|y:{self.y}"
        else:
            coordinates = ""
        return f"{self.colour.name.lower()} {self.name} ({self.power}){coordinates}"

    def attack(self, other: "Piece") -> bool | None:
        """
        Return the attack result.

        Return the `True` when this `Piece` wins the attack against `other`. If the attack is a draw, return `None`.
        Otherwise, return `False`.
        """
        if not self.can_attack():
            raise InvalidOperationError
        if self.name == MINER and other.name == BOMB:
            return True
        if self.name == SPY and other.name == MARSHAL:
            return True
        if self == other:
            return None
        return self > other

    def can_attack(self) -> bool:
        """Return `True` when this piece can attack.  Otherwise, return `False`."""
        return self.name != BOMB and self.name != FLAG

    def __repr__(self) -> str:
        """Show the piece."""
        return self.__str__()

    def __eq__(self, other: "Piece") -> bool:
        """Return `True` when self and other are the same type and have the same name."""
        if isinstance(other, Piece):
            return self.name == other.name
        return False

    def __lt__(self, other: "Piece") -> bool:
        """Return `True` when self's power is higher than other's."""
        if isinstance(other, Piece):
            return self.power < other.power
        raise TypeError


PIECES = [
    Piece(BOMB, 11),
    Piece(BOMB, 11),
    Piece(BOMB, 11),
    Piece(BOMB, 11),
    Piece(BOMB, 11),
    Piece(BOMB, 11),
    Piece(MARSHAL, 10),
    Piece(GENERAL, 9),
    Piece(COLONEL, 8),
    Piece(COLONEL, 8),
    Piece(MAJOR, 7),
    Piece(MAJOR, 7),
    Piece(MAJOR, 7),
    Piece(CAPTAIN, 6),
    Piece(CAPTAIN, 6),
    Piece(CAPTAIN, 6),
    Piece(CAPTAIN, 6),
    Piece(LIEUTENANT, 5),
    Piece(LIEUTENANT, 5),
    Piece(LIEUTENANT, 5),
    Piece(LIEUTENANT, 5),
    Piece(SERGEANT, 4),
    Piece(SERGEANT, 4),
    Piece(SERGEANT, 4),
    Piece(SERGEANT, 4),
    Piece(MINER, 3),
    Piece(MINER, 3),
    Piece(MINER, 3),
    Piece(MINER, 3),
    Piece(MINER, 3),
    Piece(SCOUT, 2),
    Piece(SCOUT, 2),
    Piece(SCOUT, 2),
    Piece(SCOUT, 2),
    Piece(SCOUT, 2),
    Piece(SCOUT, 2),
    Piece(SCOUT, 2),
    Piece(SCOUT, 2),
    Piece(SPY, 1),
    Piece(FLAG, 0),
]
