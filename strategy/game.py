"""The Strategy game."""
import logging
from dataclasses import dataclass

from pydantic import BaseModel, root_validator

from strategy.colour import Colour

log = logging.getLogger(__name__)

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


class Action(BaseModel):
    """A player action."""

    source: tuple[int, int]
    destination: tuple[int, int]
    player: Colour

    @root_validator
    def check_action(cls, action: "Action") -> "Action":  # noqa: N805
        """Check the action."""
        return action
