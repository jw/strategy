"""The Strategy game."""
from dataclasses import dataclass

EMPTY = "empty"
LAKE = "lake"


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
