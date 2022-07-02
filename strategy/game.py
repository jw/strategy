"""The Strategy game."""
import logging

from pydantic import BaseModel, root_validator

from strategy.player import Player

log = logging.getLogger(__name__)


class _Empty:
    """The Empty cell."""

    def __repr__(self) -> str:
        """Return `<empty>`."""
        return "<empty>"


Empty = _Empty()


class _Lake:
    """The Lake cell."""

    def __repr__(self) -> str:
        """Return `<lake>`."""
        return "<lake>"


Lake = _Lake()


class Action(BaseModel):
    """A player action."""

    source: tuple[int, int]
    destination: tuple[int, int]
    player: Player

    @root_validator
    def check_action(cls, action: "Action") -> "Action":  # noqa: N805
        """Check the action."""
        return action
