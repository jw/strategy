"""The Strategy game."""
import logging
from dataclasses import dataclass

from pydantic import BaseModel, root_validator

from strategy.player import Player

log = logging.getLogger(__name__)

EMPTY = "empty"
LAKE = "lake"


@dataclass
class Field:
    """The base class of an empty or lake field in the `Board`."""

    name: str

    def __str__(self) -> str:
        """Show the Cell."""
        return self.name


Empty = Field(EMPTY)
Lake = Field(LAKE)


class Action(BaseModel):
    """A player action."""

    source: tuple[int, int]
    destination: tuple[int, int]
    player: Player

    @root_validator
    def check_action(cls, action: "Action") -> "Action":  # noqa: N805
        """Check the action."""
        return action
