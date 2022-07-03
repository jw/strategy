"""The Strategy pieces."""
from functools import total_ordering

from strategy.exceptions import InvalidOperationError
from strategy.player import Player

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


@total_ordering
class Piece:
    """The Strategy piece."""

    def __init__(
        self, name: str, power: int, player: Player = Player.UNKNOWN, x: int | None = None, y: int | None = None
    ) -> None:
        """Create a type by name and power."""
        self.name = name
        self.power = power
        self.player = player
        self.x = x
        self.y = y

    def __str__(self) -> str:
        """Show the piece."""
        return f"{self.player.name.lower()} {self.name} ({self.power})"

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
    Piece(CAPTAIN, 7),
    Piece(CAPTAIN, 7),
    Piece(CAPTAIN, 7),
    Piece(CAPTAIN, 7),
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
